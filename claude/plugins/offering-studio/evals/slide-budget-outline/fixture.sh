#!/bin/bash
# ten steps, each with its own approver: the outline must fold them to fit the 22-slide cap without losing a sign-off
cat > notes.md <<'N'
Levarum Visibility Tracker, notes from Tait, October 30, 2026.

Levarum is a product. Agencies use it in Levarum's web app; no one at Levarum does the work for the agency.

Each step below has its own sign-off.

Phase 1, Set up.
Step 1. Account and billing: the agency owner creates the account and pays by card. The agency owner signs off.
Step 2. Brand and competitors: the agency strategist enters a client brand and up to five competitors. The strategist signs off.
Step 3. Question set: Levarum proposes buyer questions; the agency strategist edits and approves the set. The client's marketing lead signs off.

Phase 2, Measure.
Step 4. Weekly run: every week the app runs the approved questions against an AI engine on Levarum's own API key. Levarum's product owner signs off on the run schedule.
Step 5. Answer store: every raw answer is stored with its date, engine and question, in Levarum's database on AWS. Levarum's engineer signs off on retention.
Step 6. Scoring: the app counts mentions and citations per brand with confidence intervals. Levarum's data lead signs off on the method.
Step 7. Weekly report: the app emails a report with links to the stored answers. The agency strategist signs off on the report template.

Phase 3, Act.
Step 8. Fix list: the app ranks the pages on the client's site to change, from the answers. The agency's web lead signs off.
Step 9. Re-measure: after the agency changes the site, the app re-runs the questions. The agency strategist signs off on the re-run.
Step 10. Change report: the app reports what changed between the two runs. The client's marketing lead signs off.

Also include a tiers slide (Starter, Team, Agency plans, no prices) and a panel slide on how the app treats regulated clients such as health and credit.
N
