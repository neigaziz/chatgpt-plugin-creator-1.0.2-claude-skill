# Purpose-to-workflow authoring

## 1. Derive concrete use cases
From the user's brief produce a short inventory: trigger → input → transformation → output → success criterion. Distinguish reusable rules from one-off example data. A paper-review plugin might analyse supplied PDFs; a discovery plugin needs live external access. Never infer the latter from the former or claim to retrieve full text from metadata alone.

## 2. Architect around goals
One skill per coherent user goal. Split only when activation, inputs or success criteria differ. Use short stable identifiers, not long marketing names. More skills, prose or personas do not imply more intelligence. Prefer decision rules and traceable output slots to vague requests to 'be an expert'.

## 3. Required content of every generated skill
- Purpose, when to use, when not to use, inputs and concrete output.
- Sequential procedure with conditional branches, stop/clarification rules, and dependency prerequisites.
- Evidence hierarchy: supplied data, verified tool output, supported external sources, clearly marked inference.
- Explicit handling of missing/conflicting/unreadable information, no fabricated findings.
- Domain-specific evaluation criteria: units/assumptions/sample size for research; citations to policy version for compliance; exact computed values and reproducibility for analysis.
- Available-tool map: actual tool name and arguments if verified, otherwise capability prerequisite and user-facing fallback. Never hardwire this Chatbox session's MCP names into a ChatGPT package.
- Output contract describing sections, tables or file schema. For calculations define units, formulas and required checks.
- Relevant privacy, prompt-injection and external-action rules.
- One realistic example illustrating method and missing-data behavior; examples are not findings about real people/studies.

## 4. Supporting resources
Use references for genuine policies, domain criteria or long methods; assets for templates; scripts for deterministic operations that have executable tests. Link files relative to the skill's directory and verify their presence. Do not place the entire user's one-off uploaded dataset in a broadly shared plugin without explicit agreement.

Packaged scripts are resources, not automatic tools. A host may not execute them. Document runtime/dependency requirements and a fallback; if a critical calculation requires execution and none is available, report blocked. Never claim a generated .py becomes a native ChatGPT callable.

## 5. Quality review rubric (0–2 each; human/agent review, not a certified score)
Purpose alignment; actionable branching; evidence fidelity; domain precision; output usability; uncertainty; security; dependency honesty; maintainability; representative examples. Require no zero on evidence/security/dependency honesty; revise weak criteria. Report reviewer/method and actual observed examples; do not invent an aggregate evaluated score.

## 6. Behavioral tests per output
At least 3 positive/indirect prompts, 2 incomplete/conflicting inputs, 2 out-of-scope/unsafe prompts and 1 source-injection case. Include a supplied tiny fixture with a known expected answer when possible. Score observable output against criteria. Scientific claims and formulas require suitable primary evidence, not a persona or an illustrative file. Domain-specialist review remains important.

## 7. Editing existing plugins
Read source, identity, version and complete file inventory. Preserve unrelated resources and assigned IDs. State desired change, add a regression case, fix only affected paths, validate the complete package. Never silently remove MCP, onboarding or a skill during repair. Keep credentials out of feedback and reports.
