---
type: regex
pattern: 'AugMind'
flags: i
match: not_contains
target: { source: file, path: decisions.json }
---
