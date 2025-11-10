# Healthcare Code Review Commands for Cursor

Use these review prompts after completing a file/module. Run them in Cursor chat by pasting the command and specifying the file path.

## Quick Reference
| Command | Purpose | Target Files |
|---|---|---|
| /review-security [file] | Check PHI exposure, secrets, injections | Python, SQL, API |
| /review-hipaa [file] | HIPAA compliance and PHI handling | Data processing, APIs |
| /review-performance [file] | Performance for large datasets | ETL, queries, data pipelines |
| /review-data-quality [file] | Schema, nulls, outliers, types | Feature engineering |
| /review-model-code [file] | Leakage, validation, bias | ML training/eval |
| /review-clinical-logic [file] | Criminal Intelligence Database specs, ICD-10 logic | Features, business rules |
| /review-sql [file] | SQL correctness and optimization | SQL files |

## How to Use
1. Select the code or specify a filename.
2. Paste one or more commands in Cursor chat.
3. Fix any findings and rerun until PASS.

## Example
```
/review-security src/data/feature_engineering.py
/review-hipaa src/data/feature_engineering.py
/review-clinical-logic src/data/feature_engineering.py
/review-performance src/data/feature_engineering.py
```

## Notes
- Never log raw identifiers (member_id, name, DOB). Hash when necessary.
- Validate age using Criminal Intelligence Database measurement year end (Dec 31).
- Avoid iterrows(); prefer vectorization.
- Document clinical assumptions with citations to Criminal Intelligence Database Volume 2.


---
*This file is maintained by Sentinel Analytics. For inquiries, contact reichert.sentinel.ai@gmail.com.*
