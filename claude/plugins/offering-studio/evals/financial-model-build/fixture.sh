#!/bin/bash
mkdir -p home-page
cat > decisions.json <<'J'
{"brand": "levarum", "frame": "product",
 "rules": {"A1": {"answer": true, "basis": "Every week Levarum runs the questions against an AI engine on its own API key"},
           "A2": {"answer": true, "basis": "runs the questions against an AI engine on its own API key"},
           "A3": {"answer": true, "basis": "Data is held in Levarum's own database on AWS."},
           "A4": {"answer": true, "basis": "Data is held in Levarum's own database on AWS."},
           "P1": {"answer": true, "basis": "Agencies sign up and pay by card, enter a client brand"},
           "P2": {"answer": true, "basis": "No one at Levarum does the work for the agency; the app does."}},
 "outputs": {"architecture": "full", "home_page": true, "prototype": "full"}}
J
cat > spec.json <<'J'
{"identity": {"offering_name": "Visibility Tracker", "tagline": "Weekly measurement of how AI answers mention a brand"},
 "legend": [["Platform rule","platform","x"],["Official guidance","official","x"],["Levarum's design","own","x"],["Open","open","x"]],
 "phases": [
  {"number": 1, "name": "Set up", "steps": [{"number": "1.1", "name": "Account and questions", "tasks": [
    {"number": "1.1.1", "name": "Agency signs up and pays by card", "tag": "platform", "sources": ["Stripe: Checkout"]},
    {"number": "1.1.2", "name": "Agency enters brand and competitors", "tag": "own"},
    {"number": "1.1.3", "name": "Agency approves the question set", "tag": "own"}]}]},
  {"number": 2, "name": "Measure", "steps": [{"number": "2.1", "name": "Weekly run", "tasks": [
    {"number": "2.1.1", "name": "App runs the questions on an AI engine API each week", "tag": "platform", "sources": ["Anthropic: Messages API"]},
    {"number": "2.1.2", "name": "Every raw answer is stored on AWS", "tag": "platform", "sources": ["AWS: Amazon S3"]},
    {"number": "2.1.3", "name": "Mentions and citations counted with confidence intervals", "tag": "own"},
    {"number": "2.1.4", "name": "Weekly report emailed with links to stored answers", "tag": "own"}]}]},
  {"number": 3, "name": "Act", "steps": [{"number": "3.1", "name": "Re-measure", "tasks": [
    {"number": "3.1.1", "name": "App re-runs the questions after site changes", "tag": "own"},
    {"number": "3.1.2", "name": "Analyst support hours per customer", "tag": "open"}]}]}],
 "all_phases": [],
 "sources": [{"name": "Stripe: Checkout", "url": "https://docs.stripe.com/payments/checkout"},
             {"name": "Anthropic: Messages API", "url": "https://docs.claude.com/en/api/messages"},
             {"name": "AWS: Amazon S3", "url": "https://aws.amazon.com/s3/"}]}
J
cat > source_notes.json <<'J'
{"sources": [
 {"name": "Stripe: Checkout", "url": "https://docs.stripe.com/payments/checkout", "opened": "2026-10-28", "notes": "Stripe Checkout takes card payments on a hosted page (1.1.1)."},
 {"name": "Anthropic: Messages API", "url": "https://docs.claude.com/en/api/messages", "opened": "2026-10-28", "notes": "The Messages API answers a prompt over HTTPS with an API key (2.1.1)."},
 {"name": "AWS: Amazon S3", "url": "https://aws.amazon.com/s3/", "opened": "2026-10-28", "notes": "S3 stores objects durably in a bucket the account owns (2.1.2)."}]}
J
cat > home-page/index.html <<'H'
<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Levarum Visibility Tracker</title></head><body>
<h1>See how AI answers mention your clients</h1>
<p data-claim="2.1.1">Each week Levarum asks an AI engine the buyer questions your team approved.</p>
<p data-claim="2.1.2">Every raw answer is stored, so each count links back to what the engine said.</p>
<p data-claim="2.1.3">Mentions and citations are counted per brand, with confidence intervals.</p>
<p data-claim="3.1.1">After you change a page, Levarum measures again and reports what changed.</p>
<a href="#signup">Start tracking</a>
</body></html>
H
