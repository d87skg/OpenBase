#!/bin/bash
echo "🚀 Starting OpenBase Control Plane..."

# 启动 Registry
python -c "import uvicorn; uvicorn.run('registry.app:app', host='0.0.0.0', port=8000, reload=False)" &
REGISTRY_PID=$!

echo "✅ Registry started (PID: $REGISTRY_PID)"

# 等待 Registry 就绪
sleep 3

# 注册默认 Runtime（如果需要）
python openbase-cli/main.py runtime register --name OpenClaw --version 1.0.0 --vendor OpenBase --runtime-class REFERENCE --capabilities execution,evidence,replay,verification,determinism,certification 2>/dev/null

echo "✅ OpenClaw Runtime registered"
echo ""
echo "📌 可用命令："
echo "  - 查看信任排名: python openbase-cli/main.py trust ranking"
echo "  - 构建 Reality Graph: python openbase-cli/main.py reality build --runtime-id <RUNTIME_ID>"
echo "  - 查询现实: python openbase-cli/main.py reality query --claim 'EXEC_X_SUCCESS'"
echo "  - 查看冲突: python openbase-cli/main.py reality conflicts"
echo ""
echo "按 Ctrl+C 停止所有进程"

wait $REGISTRY_PID
