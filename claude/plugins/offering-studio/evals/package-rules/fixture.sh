#!/bin/bash
mkdir -p home-page
cat > spec.json <<'S'
{"phases":[{"number":1,"steps":[{"number":"1.1","tasks":[{"number":"1.1.1","tag":"platform"},{"number":"1.1.2","tag":"own"},{"number":"1.1.3","tag":"open"}]}]}],"all_phases":[],"sources":[]}
S
cat > home-page/index.html <<'H'
<!doctype html><html><head><title>Test</title></head><body>
<p data-claim="1.1.1">Backed claim.</p>
<p data-claim="1.1.3">Claim on an open card.</p>
<p data-claim="9.9.9">Claim on no card.</p>
<p>Plans from $79 per month.</p>
</body></html>
H
