"""
OpenBase Registry - Run Server
"""

import sys
import os

# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "registry.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
