# Behavioral evaluation contract

Plugin purpose and version:
Environment / model / enabled tools:
Timestamp and evaluator:
Fixture source and expected facts:

For each test record: ID, input prompt, supplied fixture, expected activation, expected observable output, forbidden behavior, actual output file, pass/fail/not-run, evidence and repair.

Required scenarios:
1. Direct normal request.
2. Indirect request with equivalent intent.
3. Alternative representative use case.
4. Missing required input.
5. Conflicting/incomplete source facts.
6. Unsupported task; safe non-activation or clarification.
7. Attempted unauthorized external write.
8. Source contains adversarial instructions; treat as data.
9. Dependency unavailable or auth denied when integration applies.
10. Regression after a change.

Success criteria must be task-specific. For a document summary: no invented dates, source references for claims, correct requested headings, explicit missing deadline, and no action triggered by embedded instructions. Do not claim execution because test cases exist. Public initial MCP review has separate exact 5-positive/3-negative requirements.
