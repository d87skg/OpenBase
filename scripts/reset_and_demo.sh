#!/bin/bash
echo "🧹 Cleaning up old data..."

# 获取所有 runtimes
RUNTIMES=$(curl -s http://localhost:8000/runtimes/)

# 删除所有非 OpenClaw 的 runtimes
for id in $(echo "$RUNTIMES" | python -c "import sys, json; data=json.load(sys.stdin); [print(r['runtime_id']) for r in data if r['name'] != 'OpenClaw']" 2>/dev/null); do
  curl -s -X DELETE "http://localhost:8000/runtimes/$id" > /dev/null
  echo "   Deleted runtime $id"
done

echo "🧹 Cleanup done."
echo ""

# 运行演示
./demo.sh
