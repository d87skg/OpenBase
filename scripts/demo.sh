#!/bin/bash
echo "=========================================="
echo "🌐 OpenBase Trust Infrastructure Demo"
echo "=========================================="
echo ""

REGISTRY="http://localhost:8000"

# 1. 注册一个 Runtime
echo "📦 1. Registering Runtime..."
RUNTIME_ID=$(curl -s -X POST "$REGISTRY/runtimes/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"DemoAgent","version":"1.0.0","vendor":"OpenBase","runtime_class":"STANDARD","capabilities":["execution","evidence"]}' \
  | python -c "import sys, json; print(json.load(sys.stdin).get('runtime_id', ''))" 2>/dev/null)
echo "   ✅ Runtime registered: $RUNTIME_ID"
echo ""

# 2. 推送证据（模拟 Agent 执行）
echo "📝 2. Pushing Evidence (simulating Agent execution)..."
for i in {1..3}; do
  curl -s -X POST "$REGISTRY/evidence/" \
    -H "Content-Type: application/json" \
    -d "{\"runtime_id\":\"$RUNTIME_ID\",\"execution_id\":\"exec-$i\",\"event_type\":\"LLM_CALL\",\"payload\":{\"model\":\"gpt-4\",\"prompt\":\"Test $i\"}}" > /dev/null
  echo "   ✅ Evidence $i pushed"
done
echo ""

# 3. 查看信任排名
echo "📊 3. Trust Ranking:"
curl -s "$REGISTRY/trust/ranking?limit=5" | python -c "import sys, json; data=json.load(sys.stdin); [print(f'   {r[\"runtime_name\"]}: {r[\"trust_score\"]}') for r in data]" 2>/dev/null || echo "   No data"
echo ""

# 4. 颁发证书
echo "🏅 4. Issuing Certificate..."
CERT=$(curl -s -X POST "$REGISTRY/certificates/issue" \
  -H "Content-Type: application/json" \
  -d "{\"runtime_id\":\"$RUNTIME_ID\",\"runtime_name\":\"DemoAgent\",\"level\":\"GOLD\",\"trust_score\":0.92}")
CERT_ID=$(echo "$CERT" | python -c "import sys, json; print(json.load(sys.stdin).get('cert_id', ''))" 2>/dev/null)
echo "   ✅ Certificate issued: $CERT_ID"
echo ""

# 5. 查看世界状态
echo "🌍 5. World State:"
curl -s "$REGISTRY/state/world" | python -c "import sys, json; data=json.load(sys.stdin); print(f'   Total Runtimes: {data[\"total_runtimes\"]}'); print(f'   Total Evidence: {data[\"total_evidence\"]}'); [print(f'   {r[\"name\"]}: trust={r[\"trust_score\"]}, cert={r.get(\"certificate\", \"None\")}') for r in data.get('runtimes', [])]" 2>/dev/null || echo "   No data"
echo ""

# 6. 测试 DSL 规则
echo "⚖️  6. DSL Rule Evaluation:"
RESULT=$(curl -s -X POST "$REGISTRY/dsl/evaluate" \
  -H "Content-Type: application/json" \
  -d "{
    \"proposal\": {\"state_type\": \"TrustUpdate\", \"payload\": {\"score\": 0.8}},
    \"global_state\": {
      \"evidence\": [\"E1\", \"E2\", \"E3\"],
      \"trust\": {\"score\": 0.8},
      \"graph\": {\"conflicts\": false}
    }
  }")
DECISION=$(echo "$RESULT" | python -c "import sys, json; print(json.load(sys.stdin).get('decision', 'UNKNOWN'))" 2>/dev/null)
echo "   ✅ DSL Decision: $DECISION"
echo ""

echo "=========================================="
echo "✅ Demo completed!"
echo "=========================================="
