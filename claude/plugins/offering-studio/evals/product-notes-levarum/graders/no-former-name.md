---
type: regex
pattern: '\b(Signal|MindLeverX)\b'
match: not_contains
target: { source: file, path: decisions.json }
---
