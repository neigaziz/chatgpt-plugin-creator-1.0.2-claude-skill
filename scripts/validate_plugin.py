#!/usr/bin/env python3
"""Offline, bounded checks for creator-generated portable ChatGPT plugins.
No extraction, network access, dependency installation or execution of package code.
This is a conservative creator profile, NOT an OpenAI acceptance simulator.
"""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    sys.stderr.write('Missing dependencies. With user approval run: python3 -m pip install -r requirements.txt\n')
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
MAX_ZIP = 100_000_000
MAX_FILE = 100 * 1024**2
MAX_TOTAL = 512 * 1024**2
MAX_ENTRIES = 5000
MAX_TEXT = 5 * 1024**2  # conservative local inspection cap, not an OpenAI text limit
CATEGORIES = {'Productivity','Creativity','Developer Tools','Business & Operations','Data & Analytics','Communication','Education & Research','Security','Finance','Healthcare','Travel','Entertainment','Other'}
SEMVER = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$')
NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
TEXT_SUFFIXES = {'.md','.json','.yaml','.yml','.txt','.py','.js','.mjs','.ts','.tsx','.html','.css','.svg','.toml','.ini','.cfg','.sh','.csv'}

class Rejected(Exception): pass

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out: raise ValueError('duplicate mapping key')
        out[key] = value
    return out

class SafeYaml(yaml.SafeLoader): pass

def yaml_mapping(loader, node):
    if any(k.value == '<<' for k, _ in node.value): raise ValueError('YAML merge keys not supported in creator metadata')
    return unique_pairs([(loader.construct_object(k, deep=True), loader.construct_object(v, deep=True)) for k,v in node.value])
SafeYaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, yaml_mapping)

def load_yaml(text):
    # Metadata needs neither aliases nor custom tags. Reject them before constructing graphs.
    if len(text) > 65536: raise ValueError('metadata exceeds local 64 KiB safety cap')
    for token in yaml.scan(text):
        if isinstance(token, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken, yaml.tokens.TagToken)):
            raise ValueError('YAML aliases, anchors and tags are not supported')
    return yaml.load(text, Loader=SafeYaml)

def safe_name(name):
    parts = name.rstrip('/').split('/')
    return bool(name and name == name.strip() and '\\' not in name and '\x00' not in name
                and not name.startswith('/') and not re.match(r'^[A-Za-z]:',name)
                and all(p and p not in ('.','..') and not any(ord(c)<32 for c in p) for p in parts)
                and len(parts)<=20 and len(name.encode('utf-8'))<=1024)

def normalize(name): return unicodedata.normalize('NFC', name.rstrip('/')).casefold()

def endpoint(value):
    if not isinstance(value,str) or len(value)>2048 or any(c.isspace() for c in value): return False
    try:
        p = urlsplit(value)
        host = p.hostname or ''
        if p.scheme!='https' or not host or p.username or p.password or p.fragment: return False
        if p.port not in (None,443): return False  # conservative creator policy
        if '.' not in host or host.endswith(('.localhost','.local','.internal','.test','.invalid')) or host=='localhost': return False
        if re.search(r'(^|[.-])(example|your-server|your-domain|placeholder)([.-]|$)',host): return False
        try:
            if not ipaddress.ip_address(host).is_global: return False
        except ValueError: pass
        if p.query: return False  # keep tokens, signed links and query auth out of packages
        return True
    except ValueError: return False

class Bundle:
    def __init__(self, target, add):
        self.target = Path(target)
        self.z = None
        self.records = {}
        self.prefix = ''
        entries = []
        if self.target.is_symlink(): raise Rejected('FILE_TYPE: source must not be a symlink')
        if self.target.is_dir():
            for base, dirs, files in os.walk(self.target, followlinks=False):
                for name in dirs+files:
                    p = Path(base)/name
                    rel = p.relative_to(self.target).as_posix()
                    mode = p.lstat().st_mode
                    entries.append((rel, p, mode, p.stat().st_size if stat.S_ISREG(mode) else 0, stat.S_ISDIR(mode)))
                    if len(entries)>MAX_ENTRIES: raise Rejected('LIMIT: too many entries')
        else:
            if not self.target.is_file(): raise Rejected('INPUT: source does not exist')
            if self.target.stat().st_size > MAX_ZIP: raise Rejected('LIMIT: compressed ZIP exceeds 100 MB')
            self.z = zipfile.ZipFile(self.target)
            infos = self.z.infolist()
            if len(infos)>MAX_ENTRIES: raise Rejected('LIMIT: too many entries')
            for i in infos:
                mode = i.external_attr >> 16
                is_dir = i.is_dir()
                if i.flag_bits & 1 or i.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
                    raise Rejected('ZIP: encrypted or unsupported compression')
                entries.append((i.filename,i,mode,i.file_size,is_dir))
        seen = {}
        total = 0
        for name, item, mode, size, is_dir in entries:
            if not safe_name(name): raise Rejected('PATH: unsafe or overly deep/long member path')
            key = normalize(name)
            if key in seen: raise Rejected('PATH_COLLISION: duplicate/case/Unicode path collision')
            seen[key] = is_dir
            kind = stat.S_IFMT(mode)
            if kind not in (0,stat.S_IFDIR if is_dir else stat.S_IFREG): raise Rejected('FILE_TYPE: only regular files and directories allowed')
            if size>MAX_FILE: raise Rejected('LIMIT: file exceeds 100 MiB')
            total += size
            if total>MAX_TOTAL: raise Rejected('LIMIT: uncompressed content exceeds 512 MiB')
            if not is_dir: self.records[name] = (item,size)
        for key in seen:
            parts = key.split('/')
            if any(seen.get('/'.join(parts[:n])) is False for n in range(1,len(parts))):
                raise Rejected('TYPE_CONFLICT: file also acts as directory')
        if self.z:
            roots = [n[:-len('plugin.json')] for n in self.records if PurePosixPath(n).name=='plugin.json' and len(PurePosixPath(n).parts)<=2]
            if len(roots)!=1: raise Rejected('ROOT: exactly one portable plugin root required')
            self.prefix = roots[0]
            if self.prefix and any(not n.startswith(self.prefix) for n in self.records): raise Rejected('ROOT: wrapper directory has siblings')
        self.names = {n[len(self.prefix):]:n for n in self.records}
        if not self.names: raise Rejected('SURFACE: empty package')

    def read(self,name,limit=MAX_TEXT):
        original = self.names[name]
        item,size = self.records[original]
        if size>limit: raise Rejected('LIMIT: inspection file exceeds local size cap')
        with (self.z.open(item) if self.z else item.open('rb')) as f:
            data = f.read(limit+1)
        if len(data)>limit: raise Rejected('LIMIT: read exceeds local safety cap')
        return data

    def close(self):
        if self.z: self.z.close()

def validate(target, profile='workspace'):
    report = {'status':'fail','profile':profile,'scope':'offline portable creator profile; not OpenAI acceptance','errors':[],'warnings':[],'files':[], 'checks':[], 'not_checked':['ChatGPT upload and permission checks','OpenAI security scans and review','MCP protocol, authorization and endpoint liveness','model activation and task quality','all possible OpenAI extension fields and UI rendering']}
    def add(code,message,file=None,warning=False):
        item={'code':code,'message':message}
        if file: item['file']=file
        report['warnings' if warning else 'errors'].append(item)
    def obj(value,code,file):
        if not isinstance(value,dict): add(code,'Expected object',file); return {}
        return value
    def json_read(name):
        try:
            return json.loads(bundle.read(name).decode('utf-8'),object_pairs_hook=unique_pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite number')))
        except (ValueError,UnicodeError,Rejected) as e:
            add('JSON',type(e).__name__+': invalid JSON or duplicate keys',name); return {}
    def schema_check(value,schema_name,file):
        schema=json.loads((ROOT/'schemas'/schema_name).read_text())
        Draft202012Validator.check_schema(schema)
        for e in Draft202012Validator(schema).iter_errors(value):
            # Only locations, never values that could expose a secret.
            add('SCHEMA','Schema constraint failed at /'+'/'.join(map(str,e.absolute_path))+' ('+str(e.validator)+')',file)
        report['checks'].append('JSON Schema: '+file)
    bundle=None
    try:
        bundle=Bundle(target,add)
        names=bundle.names
        # Inspect all text for obvious credentials and all data for checksums, bounded per member.
        for name in sorted(names):
            if any(x in {'.DS_Store','__MACOSX','.git','node_modules','__pycache__','.env','.venv','venv'} or x.endswith(('.pem','.key','.pyc')) or x.startswith('.env.') for x in name.split('/')):
                add('UNWANTED','Remove environment, VCS, dependencies, caches, private keys or OS junk',name)
            # Hash by bounded chunks so opaque assets need not fit text cap.
            item,size=bundle.records[names[name]]
            h=hashlib.sha256()
            with (bundle.z.open(item) if bundle.z else item.open('rb')) as f:
                consumed=0
                while True:
                    chunk=f.read(65536)
                    if not chunk: break
                    consumed+=len(chunk)
                    if consumed>MAX_FILE: raise Rejected('LIMIT: stream exceeded file bound')
                    h.update(chunk)
            if consumed!=size: raise Rejected('ZIP: declared size mismatch')
            report['files'].append({'path':name,'bytes':size,'sha256':h.hexdigest()})
            if PurePosixPath(name).suffix.lower() in TEXT_SUFFIXES:
                try: text=bundle.read(name).decode('utf-8')
                except UnicodeError: add('UTF8','Text file must be UTF-8',name); continue
                patterns=[r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'\bAKIA[A-Z0-9]{16}\b',r'\bsk-[A-Za-z0-9_-]{20,}',r'(?i)\b(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)\s*[\"\x27]?\s*[:=]\s*[\"\x27][^\"\x27\s]{8,}[\"\x27]']
                if any(re.search(p,text) for p in patterns): add('SECRET','Possible secret; remove or review without exposing its value',name)
                if re.search(r'(?i)\b(test_credentials|reviewer_instructions|clientSecret)\s*[\"\x27]?\s*:',text): add('SECRET','Credential or unsupported reviewer field detected',name)
        if 'plugin.json' not in names:
            add('MANIFEST','Root plugin.json required; Codex/legacy-only packages are outside this tool profile')
            return report
        manifest=obj(json_read('plugin.json'),'MANIFEST','plugin.json')
        schema_check(manifest,'plugin.schema.json','plugin.json')
        pname=manifest.get('name','')
        if not isinstance(pname,str) or not NAME.fullmatch(pname): add('NAME','Creator uses lowercase kebab-case identifiers','plugin.json')
        ver=manifest.get('version')
        if not isinstance(ver,str) or len(ver)>64 or not SEMVER.fullmatch(ver): add('VERSION','Creator requires explicit semantic version','plugin.json')
        desc=manifest.get('description')
        if not isinstance(desc,str) or not desc.strip() or len(desc)>1024: add('DESCRIPTION','Creator requires a summary of 1–1024 characters','plugin.json')
        extension=obj(manifest.get('extensions',{}),'EXTENSION','plugin.json')
        openai=obj(extension.get('com.openai',{}),'EXTENSION','plugin.json')
        interface=obj(openai.get('interface',{}),'INTERFACE','plugin.json')
        public=profile=='public'
        limits={'displayName':30 if public else 80,'shortDescription':30 if public else 240,'longDescription':4000,'developerName':80 if public else 120}
        for field,limit in limits.items():
            v=interface.get(field)
            if public and v is None: add('PUBLIC_METADATA','Public profile requires '+field,'plugin.json')
            if v is not None and (not isinstance(v,str) or not v.strip() or len(v)>limit or any(ord(c)<32 and c!='\n' for c in v) or (field!='longDescription' and '\n' in v)):
                add('INTERFACE','Invalid text or length: '+field,'plugin.json')
        if 'category' in interface and interface['category'] not in CATEGORIES: add('INTERFACE','Unsupported category','plugin.json')
        if public and 'category' not in interface: add('PUBLIC_METADATA','Category is required','plugin.json')
        prompts=interface.get('defaultPrompt',[])
        if isinstance(prompts,str): prompts=[prompts]
        if not isinstance(prompts,list) or len(prompts)>3: add('INTERFACE','At most three starter prompts','plugin.json')
        else:
            normalized=[]
            for p in prompts:
                if not isinstance(p,str) or not p.strip() or len(p)>(128 if public else 512) or '\n' in p or re.search(r'@\w',p): add('INTERFACE','Invalid starter prompt','plugin.json')
                else: normalized.append(' '.join(unicodedata.normalize('NFKC',p).casefold().split()))
            if len(normalized)!=len(set(normalized)): add('INTERFACE','Duplicate starter prompts','plugin.json')
        caps=interface.get('capabilities',[])
        if not isinstance(caps,list) or len(caps)>20 or any(not isinstance(x,str) or not x.strip() or len(x)>120 for x in caps): add('INTERFACE','Invalid capabilities','plugin.json')
        for field in ('websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL'):
            if field in interface and (not endpoint(interface[field]) or len(interface[field])>(1024 if public else 2048)): add('URL','Expected safe HTTPS '+field,'plugin.json')
        author=obj(manifest.get('author',{}),'AUTHOR','plugin.json')
        if public and not author.get('name'): add('PUBLIC_METADATA','Provide an actual publisher author.name','plugin.json')
        for key,limit in [('name',120),('email',320),('url',2048)]:
            if key in author and (not isinstance(author[key],str) or not author[key].strip() or len(author[key])>limit): add('AUTHOR','Invalid author '+key,'plugin.json')
        for field,value in [('homepage',manifest.get('homepage')),('author.url',author.get('url'))]:
            if value is not None and not endpoint(value): add('URL','Expected safe HTTPS '+field,'plugin.json')
        for field in ('composerIcon','composerIconDark','logo','logoDark','screenshots'):
            refs=interface.get(field,[])
            if isinstance(refs,str): refs=[refs]
            if not isinstance(refs,list): add('ASSET','Asset reference must be string or list','plugin.json'); continue
            for ref in refs:
                if not isinstance(ref,str) or not ref.startswith('./') or not safe_name(ref[2:]) or ref[2:] not in names:
                    add('ASSET','Asset must be included at a safe ./ path','plugin.json'); continue
                n=ref[2:]
                if bundle.records[names[n]][1]>5*1024**2: add('ASSET','Branding asset exceeds 5 MiB',n)
                if PurePosixPath(n).suffix.lower() not in {'.png','.jpg','.jpeg','.webp','.svg'}: add('ASSET','Unsupported image type',n)
                add('IMAGE_REVIEW','Check image dimensions, square icons, SVG safety and visual quality manually',n,True)
        if public and not interface.get('logo'): add('PUBLIC_METADATA','Include primary logo for submission','plugin.json')
        skill_names=set(); skills=[]
        for name in names:
            if name.startswith('skills/') and name.endswith('/SKILL.md'):
                parts=name.split('/')
                if len(parts)!=3 or parts[1].startswith('.'): add('SKILL','Skill must be immediate nonhidden child of skills/',name); continue
                try:
                    text=bundle.read(name).decode('utf-8')
                    match=re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)(.*)',text,re.S)
                    if not match: raise ValueError('missing or unclosed YAML frontmatter')
                    fm=load_yaml(match.group(1)); body=match.group(2)
                    if not isinstance(fm,dict) or not body.strip(): raise ValueError('mapping and nonempty body required')
                    sn=fm.get('name'); sd=fm.get('description')
                    if not isinstance(sn,str) or not NAME.fullmatch(sn): raise ValueError('creator requires kebab-case skill name')
                    if not isinstance(sd,str) or not sd.strip() or len(sd)>1024: raise ValueError('description must contain 1–1024 characters')
                    if sn in skill_names: add('SKILL_NAME','Duplicate skill name',name)
                    if isinstance(pname,str) and len(pname+':'+sn)>64: add('SKILL_IDENTITY','Combined plugin:skill identity exceeds 64 characters',name)
                    skill_names.add(sn); skills.append(name)
                    # Markdown relative links are resolved within the skill, never against the host filesystem.
                    for raw in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',body):
                        link=unquote(raw.split('#')[0])
                        if not link or urlsplit(link).scheme: continue
                        base=PurePosixPath(name).parent
                        joined=os.path.normpath(str(base/link)).replace(os.sep,'/')
                        if not joined.startswith(str(base)+'/') or joined not in names: add('LINK','Missing or out-of-skill reference',name)
                except (ValueError,TypeError,UnicodeError,yaml.YAMLError,Rejected): add('SKILL','Invalid frontmatter, types, UTF-8 or empty instructions',name)
        # Directories with resources but without their own SKILL.md are likely packaging mistakes.
        for n in names:
            parts=n.split('/')
            if len(parts)>=3 and parts[0]=='skills' and f'skills/{parts[1]}/SKILL.md' not in names: add('SKILL','Skill directory missing SKILL.md',n)
        onboard=openai.get('onboardingSkill')
        if onboard is not None and (not isinstance(onboard,str) or not onboard.startswith('./') or onboard[2:] not in skills): add('ONBOARDING','onboardingSkill must reference an included skill','plugin.json')
        servers={}
        if 'mcp.json' in names:
            mcp=obj(json_read('mcp.json'),'MCP','mcp.json'); schema_check(mcp,'mcp.schema.json','mcp.json')
            servers=obj(mcp.get('mcpServers'),'MCP','mcp.json')
            if not servers: add('MCP','Empty mcpServers is not useful','mcp.json')
            for key,server in servers.items():
                if not key.strip(): add('MCP','Empty server name','mcp.json')
                if not isinstance(server,dict): continue
                if server.get('type')!='streamable-http': add('TRANSPORT','Creator targets web streamable-http only; desktop/legacy requires separate verified profile','mcp.json')
                if not endpoint(server.get('url')): add('ENDPOINT','Use a real public HTTPS endpoint, no credentials, query tokens, private addresses or placeholders','mcp.json')
                if server.get('headers'): add('HEADERS','Creator forbids nonempty headers; use supported connection authentication','mcp.json')
            add('MCP_UNTESTED','Static configuration only; verify tools/list, tools/call, auth and permissions in ChatGPT',warning=True)
        if not skills and not servers: add('SURFACE','At least one valid skill or eligible remote MCP connection required')
        if public:
            if not skills: add('SURFACE','Public web submission profile requires at least one skill')
            if any(n=='.app.json' or n.startswith('hooks/') for n in names) or 'hooks' in openai: add('PUBLIC_COMPONENT','Public ZIP cannot contain app references or hooks')
            if len(servers)>1: add('PUBLIC_MCP','Public profile supports one connected MCP server')
            if servers:
                for field in ('websiteURL','supportURL','privacyPolicyURL','termsOfServiceURL'):
                    if field not in interface: add('PUBLIC_METADATA','Remote MCP review needs '+field,'plugin.json')
                review=obj(openai.get('review'),'PUBLIC_REVIEW','plugin.json')
                cases=obj(review.get('test_cases'),'PUBLIC_REVIEW','plugin.json')
                for kind,count in [('positive',5),('negative',3)]:
                    values=cases.get(kind)
                    if not isinstance(values,list) or len(values)!=count: add('PUBLIC_REVIEW',f'Initial MCP review requires exactly {count} {kind} cases','plugin.json'); continue
                    for case in values:
                        required=('description','prompt','tools_triggered','expected_behavior') if kind=='positive' else ('description','prompt')
                        if not isinstance(case,dict) or any(not isinstance(case.get(x),str) or not case[x].strip() for x in required): add('PUBLIC_REVIEW','Incomplete '+kind+' case','plugin.json')
                if not endpoint(review.get('demo_recording_url')): add('PUBLIC_REVIEW','Provide real accessible HTTPS demo recording URL','plugin.json')
            add('PORTAL_PENDING','Identity verification, account permissions, domains, scans, policies and review remain external gates',warning=True)
        # Deliberately reject compatibility overlays rather than silently merge ambiguous semantics.
        if '.mcp.json' in names or '.codex-plugin/plugin.json' in names or '.app.json' in names:
            add('PROFILE','Mixed/Codex/app-reference layouts are outside this portable-only creator profile')
        report['checks'] += ['bounded archive/path/type/size inspection','SHA-256 file inventory','credential heuristics','YAML metadata and relative Markdown links','portable manifest and component checks','public preparation subset' if public else 'workspace preparation subset']
    except (Rejected,zipfile.BadZipFile,OSError,RuntimeError,KeyError,ValueError,TypeError) as e:
        message=str(e) if isinstance(e,Rejected) else 'Input could not be safely processed ('+type(e).__name__+')'
        code=message.split(':',1)[0] if isinstance(e,Rejected) else 'INPUT'
        add(code,message)
    finally:
        if bundle: bundle.close()
    report['status']='fail' if report['errors'] else 'pass'
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('target',help='Portable plugin directory or ZIP (never extracted)')
    p.add_argument('--profile',choices=['workspace','public'],default='workspace')
    args=p.parse_args()
    report=validate(args.target,args.profile)
    print(json.dumps(report,indent=2,ensure_ascii=False))
    return 0 if report['status']=='pass' else 1

if __name__=='__main__': sys.exit(main())
