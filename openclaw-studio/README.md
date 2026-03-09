# OpenClaw Studio - Agent管理工作室 🎮

**方案A + 方案B 组合实现：浏览器自动化 + Web管理面板**

---

## 📋 项目概述

OpenClaw Studio 是一个基于 Web 的 Agent 管理工作室，集成了：
- ✅ **浏览器自动化** (Playwright) - 真实浏览器操作
- ✅ **Web 管理面板** (Flask) - 可视化管理界面
- ✅ **Agent 协调管理** - 统一管理多个专业 Agent
- ✅ **像素艺术生成** - 集成的像素工作室功能

---

## 🚀 功能特性

### 1. 浏览器自动化 (方案A)
- 📸 **网页截图** - 自动截取任意网页
- 📄 **内容提取** - 提取网页文本内容
- 🖱️ **浏览器导航** - 点击、输入等操作
- 🔍 **页面分析** - 获取页面标题、URL

### 2. Web 管理面板 (方案B)
- 📊 **控制面板** - 系统状态概览
- 🤖 **Agent 管理** - 查看所有 Agent 状态
- 📋 **任务队列** - 创建和跟踪任务
- 📝 **系统日志** - 实时日志查看

### 3. 集成功能
- 🎨 **像素工作室** - 生成像素艺术图片
- 📧 **邮件发送** - 集成邮件功能
- 🔧 **扩展接口** - 易于添加新功能

---

## 🛠️ 技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 后端 | Flask (Python) | Web 服务和 API |
| 前端 | HTML/CSS/JS | 用户界面 |
| 浏览器自动化 | Playwright | 控制真实浏览器 |
| 图像生成 | Pollinations AI | 免费图像生成 |
| UI 框架 | Font Awesome | 图标库 |

---

## 📦 安装部署

### 1. 安装依赖

```bash
# 安装 Python 依赖
pip install flask flask-cors requests pillow playwright

# 安装浏览器（只需一次）
playwright install chromium
```

### 2. 启动服务

```bash
# 方法1：使用启动脚本
./start.sh

# 方法2：直接启动
cd openclaw-studio
python3 app.py
```

### 3. 访问服务

- **本地访问**: http://localhost:5000
- **网络访问**: http://[服务器IP]:5000

---

## 📱 界面预览

### 控制面板
- 系统状态统计
- 快速操作入口
- 最近日志显示

### Agent 管理
- 所有 Agent 状态一览
- 在线/离线/忙碌状态
- 最后任务记录

### 浏览器自动化
- 网页截图工具
- 内容提取工具
- 浏览器导航控制

### 像素工作室
- 像素艺术生成
- 8-bit/16-bit 风格
- 快速模板选择

---

## 🔧 API 接口

### 系统状态
```http
GET /api/status
```

### Agent 管理
```http
GET    /api/agents
POST   /api/agents/{id}/status
```

### 任务管理
```http
GET    /api/tasks
POST   /api/tasks
```

### 浏览器自动化
```http
POST   /api/browser/screenshot
POST   /api/browser/navigate
POST   /api/browser/extract
```

### 像素艺术
```http
POST   /api/pixel-art/generate
```

### 系统日志
```http
GET    /api/logs
```

---

## 💡 使用示例

### 1. 网页截图
```bash
curl -X POST http://localhost:5000/api/browser/screenshot \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.zhihu.com"}' \
  --output screenshot.png
```

### 2. 生成像素艺术
```bash
curl -X POST http://localhost:5000/api/pixel-art/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "勇敢的骑士", "style": "8-bit"}' \
  --output knight.png
```

### 3. 创建任务
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "type": "research",
    "agent": "coding-agent",
    "description": "调研 Python 异步编程"
  }'
```

---

## 🌐 响应式设计

OpenClaw Studio 支持多种设备：
- 💻 **桌面端** - 完整功能体验
- 📱 **手机端** - 自适应布局
- 📲 **平板端** - 触摸友好的界面

---

## 🔒 安全提示

1. **生产环境** - 建议使用 Nginx + Gunicorn 部署
2. **访问控制** - 添加身份验证机制
3. **浏览器安全** - 不要访问恶意网站
4. **频率限制** - 避免过于频繁的请求

---

## 📝 目录结构

```
openclaw-studio/
├── app.py              # Flask 主应用
├── start.sh            # 启动脚本
├── README.md           # 本说明文档
├── templates/
│   └── dashboard.html  # 主页面模板
└── static/
    ├── css/
    │   └── style.css   # 样式文件
    └── js/
        └── app.js      # 前端脚本
```

---

## 🎯 未来扩展

- [ ] WebSocket 实时通信
- [ ] 用户认证系统
- [ ] 数据持久化存储
- [ ] 更多 Agent 类型
- [ ] 定时任务调度
- [ ] 移动端 App

---

## 📄 许可证

MIT License - 自由使用和修改

---

**创建日期**: 2026-03-09
**版本**: v1.0.0

*OpenClaw Studio - 让 AI Agent 管理变得简单直观 🚀*
