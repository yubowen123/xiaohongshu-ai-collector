#!/bin/bash

# 小红书 AI 内容采集器 - 启动脚本

echo "=================================================="
echo "小红书 AI 内容采集器"
echo "=================================================="
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "❌ 虚拟环境不存在，请先运行: python3 -m venv venv"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，请从 .env.example 复制并配置"
    echo "   cp .env.example .env"
    exit 1
fi

# 启动应用
echo "🚀 启动采集器..."
python main.py start
