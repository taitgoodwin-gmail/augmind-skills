#!/bin/bash
# a minimal spec for Levarum that names AugMind once, uses the former name Signal once and carries a price once
cat > leaky_spec.json <<'S'
{"identity": {"offering_name": "Levarum test, formerly Signal", "tagline": "Modeled on the AugMind deck, from $79 per month"},
 "legend": [["Platform rule","platform","x"],["Official guidance","official","x"],["Levarum's design","own","x"],["Open","open","x"]],
 "start": {"views": ["The offering","Roles"], "matrix": {}, "roles": {}},
 "phases": [], "all_phases": [], "sources": []}
S
