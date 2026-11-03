import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'validate_plugin.py'
PACK = ROOT / 'scripts' / 'package_plugin.py'
MANIFEST = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', 'name': 'document-summary', 'version': '1.0.0', 'description': 'Summarize supplied documents.'}
SKILL = '---\nname: summarize\ndescription: Use when a user asks to summarize a supplied document.\n---\n\n# Summarize\nUse only supplied evidence. Mark missing information.\n'

class Tools(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.p = self.base / 'plugin'
        self.p.mkdir()
        self.write('plugin.json', json.dumps(MANIFEST))
        self.write('skills/summarize/SKILL.md', SKILL)

    def write(self, name, value):
        p = self.p / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(value, encoding='utf-8')

    def run_check(self, target=None, profile='workspace'):
        cp = subprocess.run([sys.executable, str(SCRIPT), str(target or self.p), '--profile', profile], capture_output=True, text=True)
        self.assertIn(cp.returncode, (0, 1), cp.stderr)
        return json.loads(cp.stdout)

    def fails(self, code, **kwargs):
        r = self.run_check(**kwargs)
        self.assertEqual(r['status'], 'fail', r)
        self.assertIn(code, [x['code'] for x in r['errors']], r)

    def archive(self, entries):
        z = self.base / 'input.zip'
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(z, 'w') as f:
                for name, data in entries:
                    f.writestr(name, data)
        return z

    def test_00_cli_exists(self): self.assertTrue(SCRIPT.is_file(), 'validator not implemented yet')
    def test_minimal_portable_passes(self): self.assertEqual(self.run_check()['status'], 'pass')
    def test_missing_manifest(self):
        (self.p/'plugin.json').unlink(); self.fails('MANIFEST')
    def test_schema_disallows_codex_fields(self):
        self.write('plugin.json', json.dumps({**MANIFEST, 'skills': './skills/'})); self.fails('SCHEMA')
    def test_duplicate_json_keys(self):
        self.write('plugin.json', '{"name":"a","name":"b"}'); self.fails('JSON')
    def test_invalid_semver(self):
        self.write('plugin.json', json.dumps({**MANIFEST,'version':'latest'})); self.fails('VERSION')
    def test_wrong_extension_type(self):
        self.write('plugin.json', json.dumps({**MANIFEST,'extensions':{'com.openai':{'interface':[]}}})); self.fails('INTERFACE')
    def test_missing_skill(self):
        (self.p/'skills/summarize/SKILL.md').unlink(); self.fails('SURFACE')
    def test_invalid_yaml(self):
        self.write('skills/summarize/SKILL.md','---\nname: [\n---\nBody'); self.fails('SKILL')
    def test_duplicate_yaml(self):
        self.write('skills/summarize/SKILL.md','---\nname: x\nname: y\ndescription: d\n---\nBody'); self.fails('SKILL')
    def test_empty_skill_body(self):
        self.write('skills/summarize/SKILL.md','---\nname: summarize\ndescription: description\n---\n'); self.fails('SKILL')
    def test_duplicate_skill(self):
        self.write('skills/other/SKILL.md',SKILL); self.fails('SKILL_NAME')
    def test_long_combined_identity(self):
        self.write('plugin.json', json.dumps({**MANIFEST,'name':'a'*60})); self.fails('SKILL_IDENTITY')
    def test_missing_link(self):
        self.write('skills/summarize/SKILL.md',SKILL+'\nRead [policy](references/missing.md).'); self.fails('LINK')
    def test_link_outside_skill(self):
        self.write('skills/summarize/SKILL.md',SKILL+'\nRead [secret](../../../secret).'); self.fails('LINK')
    def test_missing_asset(self):
        self.write('plugin.json', json.dumps({**MANIFEST,'extensions':{'com.openai':{'interface':{'logo':'./assets/no.svg'}}}})); self.fails('ASSET')
    def test_hidden_junk(self):
        self.write('.DS_Store','junk'); self.fails('UNWANTED')
    def test_secret(self):
        self.write('config.txt','-----BEGIN PRIVATE KEY-----'); self.fails('SECRET')
    def test_symlink(self):
        (self.p/'link').symlink_to(self.p/'plugin.json'); self.fails('FILE_TYPE')
    def mcp(self, url='https://mcp.openai.com/mcp', **extra):
        self.write('mcp.json',json.dumps({'$schema':'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json','mcpServers':{'tools':{'type':'streamable-http','url':url,**extra}}}))
    def test_remote_mcp_static_only(self):
        self.mcp(); r=self.run_check(); self.assertEqual(r['status'],'pass'); self.assertTrue(any(x['code']=='MCP_UNTESTED' for x in r['warnings']))
    def test_localhost(self): self.mcp('https://localhost/mcp'); self.fails('ENDPOINT')
    def test_placeholder(self): self.mcp('https://your-server.example.com/mcp'); self.fails('ENDPOINT')
    def test_private_ip(self): self.mcp('https://192.168.1.1/mcp'); self.fails('ENDPOINT')
    def test_headers(self): self.mcp(headers={'Authorization':'Bearer private'}); self.fails('HEADERS')
    def test_unknown_auth_schema(self): self.mcp(auth={'type':'oauth'}); self.fails('SCHEMA')
    def test_public_requires_listing(self): self.fails('PUBLIC_METADATA',profile='public')
    def test_zip_roundtrip(self):
        z=self.archive([('plugin.json',json.dumps(MANIFEST)),('skills/summarize/SKILL.md',SKILL)])
        self.assertEqual(self.run_check(z)['status'],'pass')
    def test_one_wrapper(self):
        z=self.archive([('wrap/plugin.json',json.dumps(MANIFEST)),('wrap/skills/summarize/SKILL.md',SKILL)])
        self.assertEqual(self.run_check(z)['status'],'pass')
    def test_wrapper_sibling(self):
        z=self.archive([('wrap/plugin.json',json.dumps(MANIFEST)),('sibling.txt','x')]); self.fails('ROOT',target=z)
    def test_zip_duplicate(self):
        z=self.archive([('plugin.json','{}'),('plugin.json','{}')]); self.fails('PATH_COLLISION',target=z)
    def test_zip_case_collision(self):
        z=self.archive([('plugin.json','{}'),('PLUGIN.json','{}')]); self.fails('PATH_COLLISION',target=z)
    def test_zip_traversal(self):
        z=self.archive([('../plugin.json','{}')]); self.fails('PATH',target=z)
    def test_zip_backslash(self):
        z=self.archive([('dir\\file','{}')]); self.fails('PATH',target=z)
    def test_zip_type_conflict(self):
        z=self.archive([('file','x'),('file/sub','x')]); self.fails('TYPE_CONFLICT',target=z)
    def test_zip_symlink(self):
        z=self.base/'input.zip'
        with zipfile.ZipFile(z,'w') as f:
            i=zipfile.ZipInfo('link'); i.create_system=3; i.external_attr=(0o120777<<16); f.writestr(i,'/etc/passwd')
        self.fails('FILE_TYPE',target=z)
    def test_pack_and_no_overwrite(self):
        out=self.base/'out.zip'
        cmd=[sys.executable,str(PACK),str(self.p),str(out)]
        cp=subprocess.run(cmd,capture_output=True,text=True); self.assertEqual(cp.returncode,0,cp.stdout+cp.stderr)
        self.assertEqual(self.run_check(out)['status'],'pass')
        cp=subprocess.run(cmd,capture_output=True,text=True); self.assertNotEqual(cp.returncode,0)
    def test_pack_blocks_invalid(self):
        self.write('.env','PASSWORD=do-not-package')
        out=self.base/'out.zip'
        cp=subprocess.run([sys.executable,str(PACK),str(self.p),str(out)],capture_output=True,text=True)
        self.assertNotEqual(cp.returncode,0); self.assertFalse(out.exists())

if __name__ == '__main__': unittest.main()
