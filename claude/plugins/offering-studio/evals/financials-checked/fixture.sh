#!/bin/bash
# one cost line with its range reversed and no source, one price tagged as if a vendor set it
cat > financials.json <<'J'
{"brand": "levarum", "offering": "Test", "currency": "USD", "as_of": "2026-10-30", "lines": [
 {"id": "C1", "group": "cost", "name": "API calls", "low": 3, "base": 2, "high": 1, "unit": "USD per customer per week", "tag": "platform"},
 {"id": "P1", "group": "price", "name": "Monthly price", "low": 50, "base": 80, "high": 120, "unit": "USD per customer per month",
  "tag": "official", "source": "x", "url": "https://example.com", "opened": "2026-10-30", "basis": "x"}]}
J
