#!/bin/bash

# OpenClaw Studio 启动脚本

echo "🚀 正在启动 OpenClaw Studio..."
echo ""

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import flask, playwright" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖，正在安装..."
    pip install flask flask-cors requests pillow playwright --break-system-packages
    playwright install chromium
fi

# 创建工作目录
echo "📁 创建工作目录..."
mkdir -p /tmp/openclaw-studio

# 启动服务
echo ""
echo "🌐 启动 Web 服务..."
echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 访问地址:"
echo "   - 本地访问: http://localhost:5000"
echo "   - 网络访问: http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "⚠️  注意: 如果无法访问，请检查防火墙设置"
echo ""

# 启动应用
cd "$(dirname "$0")"
python3 app.py
