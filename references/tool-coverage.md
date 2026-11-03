# Tool coverage and status vocabulary

## Commands
```
python3 scripts/validate_plugin.py /path/to/plugin --profile workspace
python3 scripts/validate_plugin.py /path/to/plugin.zip --profile workspace
python3 scripts/package_plugin.py /path/to/plugin /path/to/new-upload.zip --profile workspace
```
Use `--profile public` explicitly for public preparation. JSON is written to stdout; redirect it to a report OUTSIDE plugin source. Exit 0 = checks passed with possible warnings; 1 = validation/build failed; 2 = argument/dependency failure. Scripts have no network access and never run package code. `jsonschema` and PyYAML must be installed; do not install without authorization. Source directory is explicit; output never overwrites an existing path. ZIP output names need not be the plugin identity.

## Actually implemented
| Area | Executable coverage |
|---|---|
| Format | Captured official Draft 2020-12 plugin/MCP schemas, duplicate JSON keys, nonfinite values, object structure |
| YAML | Safe parser, mapping, required strings/body, duplicate mapping keys, no aliases/anchors/custom tags, bounds |
| Identity | Kebab-case creator policy, explicit SemVer, summary <=1024, unique skills, combined identity <=64 |
| Components | Immediate skills, missing skill manifests, included onboarding, portable-only distinction |
| References | Markdown inline local links in SKILL.md within own skill, referenced root interface assets |
| Listings | Selected text limits/types, category, capabilities, starters, safe URL syntax |
| MCP | Streamable-http web profile, URL literal safety/placeholder checks, nonempty headers rejected, schema unknown keys rejected |
| Archive | 100 MB compressed, 100 MiB member, 512 MiB total, 5000 members, 20 levels, local 1024-byte path cap, duplicate/case/NFC collisions, traversal, symlinks/nonregular members, encrypted/unsupported compression, file-directory conflicts, root/wrapper rules, streaming readability/CRC |
| Secrets/junk | Selected key/token/private-key regex heuristics; .env/key/dependency/VCS/cache/OS-junk paths |
| Packaging | Validate source, stable ordering/timestamps, compare content hashes, root-level ZIP, revalidate before final write, no overwrite |
| Public subset | Listing fields, author name/logo, one connected remote MCP, no app refs/hooks, initial 5/3 review cases and real-form demo URL, four MCP listing URLs |

## Not implemented / manual or external checks
- All OpenAI extension/agents/openai.yaml fields; authentication mappings not in base schema; country/translation completeness and exact portal sanitization.
- Markdown reference-style links, plain prose paths or code references, all script imports/resources/dependency licenses.
- Image dimensions, visual quality, SVG active content, EXIF, brand contrast, MIME byte validation and screenshot fidelity.
- MCP liveness, protocol/tool schemas, actual OAuth, DNS resolution/private routing/rebinding, API rate-limit behavior or tool safety.
- Semantic prompt-injection resistance, exact workflow usefulness, scientific accuracy, behavioral activation or successful model evaluations.
- Account permissions, domain verification, official security scans, complete public policies, upload acceptance or directory approval.
- Exhaustive secret/malware detection, nested archive inspection or concurrency-hardening against a malicious process mutating the source tree. Use a private sandbox and do not package concurrently modified sources.

## Status words
**Authored** = files written. **Locally validated** = named executed checks passed. **Archive validated** = exact final ZIP passed offline checks. **Behaviorally tested** = actual prompts and outputs reviewed. **Accepted by ChatGPT** = actual upload accepted. **Live integration tested** = actual protocol/auth/tool execution checked. **Published** = explicit successful external publication. Never substitute one for another.

The validator intentionally rejects some technically possible formats/transports to keep its web-portable profile bounded. A rejection outside that profile is not proof OpenAI rejects the same package. Warnings must remain visible in delivery reports.
