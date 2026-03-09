#!/usr/bin/env python3
"""
OpenClaw Studio - Web版Agent管理工作室
支持浏览器自动化 + Web管理面板
"""

from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import os
import json
import threading
import time
from datetime import datetime
import requests
import urllib.parse

# 尝试导入Playwright
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not available, browser automation disabled")

app = Flask(__name__)
CORS(app)

# 全局状态存储
studio_state = {
    "agents": {
        "coding-agent": {"status": "idle", "last_task": None},
        "frontend-design-agent": {"status": "idle", "last_task": None},
        "legal-agent": {"status": "idle", "last_task": None},
        "customer-service-agent": {"status": "idle", "last_task": None},
        "finance-agent": {"status": "idle", "last_task": None},
        "ecommerce-coordinator": {"status": "idle", "last_task": None},
    },
    "tasks": [],
    "browser_sessions": {},
    "logs": []
}

def log_event(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    studio_state["logs"].append(log_entry)
    print(log_entry)

# ==================== 路由定义 ====================

@app.route('/')
def dashboard():
    """主控制面板"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """获取系统状态"""
    return jsonify({
        "status": "running",
        "playwright_available": PLAYWRIGHT_AVAILABLE,
        "agents": studio_state["agents"],
        "active_tasks": len([t for t in studio_state["tasks"] if t["status"] == "running"]),
        "total_tasks": len(studio_state["tasks"])
    })

@app.route('/api/agents')
def get_agents():
    """获取所有Agent状态"""
    return jsonify(studio_state["agents"])

@app.route('/api/agents/<agent_id>/status', methods=['POST'])
def update_agent_status(agent_id):
    """更新Agent状态"""
    if agent_id in studio_state["agents"]:
        data = request.json
        studio_state["agents"][agent_id]["status"] = data.get("status", "idle")
        studio_state["agents"][agent_id]["last_task"] = data.get("task")
        log_event(f"Agent {agent_id} status updated to {data.get('status')}")
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Agent not found"})

@app.route('/api/tasks', methods=['GET', 'POST'])
def handle_tasks():
    """处理任务"""
    if request.method == 'GET':
        return jsonify(studio_state["tasks"])
    
    elif request.method == 'POST':
        data = request.json
        task = {
            "id": len(studio_state["tasks"]) + 1,
            "type": data.get("type"),
            "agent": data.get("agent"),
            "description": data.get("description"),
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        studio_state["tasks"].append(task)
        log_event(f"New task created: {task['description']}")
        
        # 启动异步任务处理
        threading.Thread(target=process_task, args=(task,)).start()
        
        return jsonify({"success": True, "task": task})

@app.route('/api/logs')
def get_logs():
    """获取日志"""
    return jsonify(studio_state["logs"][-50:])  # 最近50条

# ==================== 浏览器自动化功能 ====================

@app.route('/api/browser/screenshot', methods=['POST'])
def browser_screenshot():
    """浏览器截图"""
    if not PLAYWRIGHT_AVAILABLE:
        return jsonify({"success": False, "error": "Playwright not available"})
    
    data = request.json
    url = data.get("url", "https://www.example.com")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(url, wait_until="networkidle")
            
            # 截图保存
            screenshot_path = f"/tmp/screenshot_{int(time.time())}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()
            
            log_event(f"Screenshot taken: {url}")
            return send_file(screenshot_path, mimetype='image/png')
    
    except Exception as e:
        log_event(f"Screenshot error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/browser/navigate', methods=['POST'])
def browser_navigate():
    """浏览器导航"""
    if not PLAYWRIGHT_AVAILABLE:
        return jsonify({"success": False, "error": "Playwright not available"})
    
    data = request.json
    url = data.get("url")
    action = data.get("action", "goto")  # goto, click, type
    selector = data.get("selector")
    text = data.get("text")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            if action == "goto":
                page.goto(url)
                result = {"title": page.title(), "url": page.url}
            
            elif action == "click":
                page.goto(url)
                page.click(selector)
                result = {"message": f"Clicked {selector}"}
            
            elif action == "type":
                page.goto(url)
                page.fill(selector, text)
                result = {"message": f"Typed into {selector}"}
            
            browser.close()
            
            log_event(f"Browser action: {action} on {url}")
            return jsonify({"success": True, "result": result})
    
    except Exception as e:
        log_event(f"Browser error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/browser/extract', methods=['POST'])
def browser_extract():
    """提取网页内容"""
    if not PLAYWRIGHT_AVAILABLE:
        return jsonify({"success": False, "error": "Playwright not available"})
    
    data = request.json
    url = data.get("url")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, wait_until="networkidle")
            
            # 提取页面内容
            title = page.title()
            content = page.content()
            text = page.inner_text("body")
            
            browser.close()
            
            result = {
                "title": title,
                "url": url,
                "text_preview": text[:1000] + "..." if len(text) > 1000 else text
            }
            
            log_event(f"Content extracted from: {url}")
            return jsonify({"success": True, "result": result})
    
    except Exception as e:
        log_event(f"Extraction error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# ==================== 像素艺术生成功能 ====================

@app.route('/api/pixel-art/generate', methods=['POST'])
def generate_pixel_art():
    """生成像素艺术"""
    data = request.json
    prompt = data.get("prompt", "pixel art character")
    style = data.get("style", "8-bit")  # 8-bit, 16-bit
    width = data.get("width", 512)
    height = data.get("height", 512)
    
    try:
        # 构建完整提示词
        full_prompt = f"pixel art, {style} style, {prompt}, game asset, crisp edges, limited color palette"
        
        # 使用Pollinations免费API
        encoded_prompt = urllib.parse.quote(full_prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        params = {
            "width": width,
            "height": height,
            "model": "flux",
            "nologo": "true",
            "seed": int(time.time())
        }
        
        response = requests.get(url, params=params, timeout=120)
        
        # 保存图片
        image_path = f"/tmp/pixel_art_{int(time.time())}.png"
        with open(image_path, "wb") as f:
            f.write(response.content)
        
        log_event(f"Pixel art generated: {prompt}")
        return send_file(image_path, mimetype='image/png')
    
    except Exception as e:
        log_event(f"Pixel art error: {str(e)}")
        return jsonify({"success": False, "error": str(e)})

# ==================== 任务处理 ====================

def process_task(task):
    """异步处理任务"""
    task["status"] = "running"
    log_event(f"Task {task['id']} started: {task['description']}")
    
    # 模拟处理时间
    time.sleep(3)
    
    # 根据任务类型处理
    if task["type"] == "research":
        # 模拟研究工作
        time.sleep(5)
    elif task["type"] == "code":
        # 模拟代码编写
        time.sleep(4)
    elif task["type"] == "design":
        # 模拟设计工作
        time.sleep(3)
    
    task["status"] = "completed"
    task["completed_at"] = datetime.now().isoformat()
    log_event(f"Task {task['id']} completed")

# ==================== 启动服务 ====================

if __name__ == '__main__':
    log_event("OpenClaw Studio started")
    print(f"🚀 OpenClaw Studio running at http://0.0.0.0:5000")
    print(f"📊 Dashboard: http://0.0.0.0:5000/")
    print(f"🔧 Playwright available: {PLAYWRIGHT_AVAILABLE}")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
