#!/bin/bash
cat > notes.md <<'N'
Levarum. Agencies sign up and pay by card, enter a client brand and its competitors, and approve a set of buyer questions. Every week Levarum runs the questions against an AI engine on its own API key, stores every raw answer, and emails a report: how often the brand is mentioned and cited, with confidence intervals, and links to the stored answers. After the agency fixes its client's site, Levarum re-measures and reports what changed. No one at Levarum does the work for the agency; the app does. Data is held in Levarum's own database on AWS.
N
