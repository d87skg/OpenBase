#!/bin/bash
echo "Generating OpenBase Status Report..."

curl -s http://localhost:8000/state/world > /tmp/world.json

cat > /tmp/report.html << 'HTML'
<!DOCTYPE html>
<html>
<head><title>OpenBase Status Report</title>
<style>body{font-family:sans-serif;margin:40px;background:#f5f5f5;}
h1{color:#2c3e50;}
.card{background:white;padding:20px;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);margin:10px 0;}
.runtime{display:flex;justify-content:space-between;border-bottom:1px solid #eee;padding:8px 0;}
.trust{color:#27ae60;font-weight:bold;}
.cert{background:#f1c40f;padding:2px 10px;border-radius:12px;font-size:12px;}
</style></head>
<body>
<h1>🌐 OpenBase Status Report</h1>
<div class="card" id="content">Loading...</div>
<script>
fetch('/tmp/world.json')
  .then(r => r.json())
  .then(data => {
    let html = `<h2>World State</h2><p>Total Runtimes: ${data.total_runtimes}</p><p>Total Evidence: ${data.total_evidence}</p>`
    html += `<h3>Runtimes</h3>`
    data.runtimes.forEach(r => {
      html += `<div class="runtime"><span>${r.name}</span><span class="trust">${r.trust_score}</span><span class="cert">${r.certificate || 'None'}</span></div>`
    })
    document.getElementById('content').innerHTML = html
  })
</script>
</body></html>
HTML

echo "Report generated at /tmp/report.html"
echo "Open in browser: file:///tmp/report.html"
