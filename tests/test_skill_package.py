import hashlib
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit
import yaml

ROOT = Path(__file__).resolve().parents[1]

class SkillPackage(unittest.TestCase):
    def test_core_frontmatter_and_size(self):
        data=(ROOT/'SKILL.md').read_bytes()
        self.assertLessEqual(len(data),12000)
        fm=yaml.safe_load(data.decode().split('---',2)[1])
        self.assertEqual(fm['name'],'chatgpt-plugin-creator')
        self.assertTrue(fm['description'].startswith('Use when'))
        self.assertLessEqual(len(fm['description']),1024)
    def test_all_seven_sources_preserved(self):
        index=json.loads((ROOT/'references/source-index.json').read_text())
        entries=[e for e in index['entries'] if e.get('kind')=='user-supplied']
        self.assertEqual(len(entries),7)
        for e in entries:
            data=(ROOT/e['path']).read_bytes()
            self.assertEqual(len(data),e['bytes'])
            self.assertEqual(hashlib.sha256(data).hexdigest(),e['sha256'])
    def test_successful_live_sources_preserved(self):
        index=json.loads((ROOT/'references/source-index.json').read_text())
        entries=[e for e in index['entries'] if e.get('kind')=='official-live']
        self.assertEqual(len(entries),7)
        for e in entries:
            self.assertEqual(hashlib.sha256((ROOT/e['path']).read_bytes()).hexdigest(),e['sha256'])
    def test_failed_fetches_disclosed(self):
        index=json.loads((ROOT/'references/source-index.json').read_text())
        failures=[e for e in index['entries'] if e.get('status')=='blocked']
        self.assertEqual(len(failures),2)
        self.assertTrue(all('404' in e['error'] for e in failures))
    def test_authored_markdown_links_exist(self):
        for p in ROOT.rglob('*.md'):
            if 'sources' in p.parts: continue  # verbatim captures retain original external-site paths
            for raw in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',p.read_text()):
                link=unquote(raw.split('#')[0])
                if link and not urlsplit(link).scheme:
                    self.assertTrue((p.parent/link).exists(),str(p)+': '+link)
    def test_model_tests_not_misreported(self):
        cases=json.loads((ROOT/'tests/evaluation-cases.json').read_text())
        self.assertEqual(cases['status'],'not_run_model_scenarios')
        self.assertGreaterEqual(len(cases['cases']),12)
    def test_examples_and_requirements_exist(self):
        for name in ['README.md','CHANGELOG.md','requirements.txt','examples/document-summary/plugin.json','examples/document-summary/assets/icon.svg','docs/validation-report.md']:
            self.assertTrue((ROOT/name).is_file(),name)
    def test_schemas_official_ids(self):
        for name in ['plugin','mcp']:
            schema=json.loads((ROOT/f'schemas/{name}.schema.json').read_text())
            self.assertEqual(schema['$id'],f'https://agent-plugins.org/schemas/1.0.0/{name}.schema.json')

if __name__=='__main__': unittest.main()
