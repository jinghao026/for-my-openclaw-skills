// OpenClaw Studio - Frontend JavaScript

// 全局状态
let currentPage = 'dashboard';

// 页面切换
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const page = item.dataset.page;
        navigateTo(page);
    });
});

function navigateTo(page) {
    // 更新导航状态
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // 切换页面
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`page-${page}`).classList.add('active');
    
    // 更新标题
    const titles = {
        'dashboard': '控制面板',
        'agents': 'Agent管理',
        'browser': '浏览器自动化',
        'pixel': '像素工作室',
        'tasks': '任务队列',
        'logs': '系统日志'
    };
    document.getElementById('page-title').textContent = titles[page];
    
    currentPage = page;
    
    // 加载页面数据
    if (page === 'agents') loadAgents();
    if (page === 'tasks') loadTasks();
    if (page === 'logs') loadLogs();
}

// 刷新数据
function refreshData() {
    fetch('/api/status')
        .then(res => res.json())
        .then(data => {
            document.getElementById('total-agents').textContent = 
                Object.keys(data.agents).length;
            document.getElementById('completed-tasks').textContent = 
                data.total_tasks - data.active_tasks;
            document.getElementById('pending-tasks').textContent = 
                data.active_tasks;
            document.getElementById('browser-status').textContent = 
                data.playwright_available ? '就绪' : '未安装';
        });
}

// 加载Agent列表
function loadAgents() {
    fetch('/api/agents')
        .then(res => res.json())
        .then(agents => {
            const container = document.getElementById('agents-list');
            container.innerHTML = '';
            
            for (const [id, info] of Object.entries(agents)) {
                const statusClass = info.status === 'idle' ? 'online' : 
                                   info.status === 'working' ? 'busy' : 'offline';
                
                const card = document.createElement('div');
                card.className = 'agent-card';
                card.innerHTML = `
                    <div class="agent-card-header">
                        <i class="fas fa-robot"></i>
                        <div>
                            <h4>${id.replace(/-/g, ' ').toUpperCase()}</h4>
                            <span class="agent-status ${statusClass}">
                                ${info.status === 'idle' ? '待机中' : 
                                  info.status === 'working' ? '工作中' : '离线'}
                            </span>
                        </div>
                    </div>
                    <p>最后任务: ${info.last_task || '无'}</p>
                `;
                container.appendChild(card);
            }
        });
}

// 加载任务列表
function loadTasks() {
    fetch('/api/tasks')
        .then(res => res.json())
        .then(tasks => {
            const container = document.getElementById('tasks-container');
            container.innerHTML = '';
            
            if (tasks.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#64748b">暂无任务</p>';
                return;
            }
            
            tasks.reverse().forEach(task => {
                const statusClass = task.status;
                const statusText = {
                    'pending': '待处理',
                    'running': '进行中',
                    'completed': '已完成'
                }[task.status];
                
                const item = document.createElement('div');
                item.className = 'task-item';
                item.innerHTML = `
                    <div>
                        <h4>${task.description}</h4>
                        <p style="color:#64748b;font-size:0.875rem">
                            ${task.agent} | ${new Date(task.created_at).toLocaleString()}
                        </p>
                    </div>
                    <span class="task-status ${statusClass}">${statusText}</span>
                `;
                container.appendChild(item);
            });
        });
}

// 加载日志
function loadLogs() {
    fetch('/api/logs')
        .then(res => res.json())
        .then(logs => {
            const container = document.getElementById('logs-container');
            container.innerHTML = '';
            
            if (logs.length === 0) {
                container.innerHTML = '<p style="text-align:center;color:#64748b">暂无日志</p>';
                return;
            }
            
            logs.reverse().forEach(log => {
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                
                const match = log.match(/\[(.*?)\]\s*(.*)/);
                if (match) {
                    entry.innerHTML = `
                        <span class="log-time">${match[1]}</span>
                        <span class="log-message">${match[2]}</span>
                    `;
                } else {
                    entry.innerHTML = `<span class="log-message">${log}</span>`;
                }
                
                container.appendChild(entry);
            });
            
            // 更新最近日志
            const recentLogs = document.getElementById('recent-logs');
            if (recentLogs && logs.length > 0) {
                const lastLog = logs[logs.length - 1];
                const match = lastLog.match(/\[(.*?)\]\s*(.*)/);
                if (match) {
                    recentLogs.innerHTML = `
                        <div class="log-entry">
                            <span class="log-time">${match[1]}</span>
                            <span class="log-message">${match[2]}</span>
                        </div>
                    `;
                }
            }
        });
}

// 清空日志
function clearLogs() {
    if (confirm('确定要清空所有日志吗？')) {
        fetch('/api/logs', { method: 'DELETE' })
            .then(() => loadLogs());
    }
}

// 创建任务模态框
function showCreateTaskModal() {
    document.getElementById('create-task-modal').classList.add('active');
}

function closeCreateTaskModal() {
    document.getElementById('create-task-modal').classList.remove('active');
}

function createTask() {
    const type = document.getElementById('task-type').value;
    const agent = document.getElementById('task-agent').value;
    const description = document.getElementById('task-description').value;
    
    if (!description) {
        alert('请输入任务描述');
        return;
    }
    
    fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, agent, description })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            closeCreateTaskModal();
            document.getElementById('task-description').value = '';
            alert('任务创建成功！');
            if (currentPage === 'tasks') loadTasks();
            refreshData();
        }
    });
}

// 浏览器功能
function takeScreenshot() {
    const url = document.getElementById('screenshot-url').value;
    const resultArea = document.getElementById('screenshot-result');
    
    resultArea.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> 正在截图...</p>';
    
    fetch('/api/browser/screenshot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    })
    .then(res => {
        if (res.ok) return res.blob();
        return res.json().then(data => { throw new Error(data.error); });
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        resultArea.innerHTML = `
            <img src="${url}" style="max-width:100%;border-radius:0.5rem;box-shadow:0 4px 6px rgba(0,0,0,0.1)">
            <p style="margin-top:1rem">
                <a href="${url}" download="screenshot.png" class="btn btn-primary">
                    <i class="fas fa-download"></i> 下载截图
                </a>
            </p>
        `;
    })
    .catch(err => {
        resultArea.innerHTML = `<p style="color:#ef4444">错误: ${err.message}</p>`;
    });
}

function extractContent() {
    const url = document.getElementById('extract-url').value;
    const resultArea = document.getElementById('extract-result');
    
    resultArea.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> 正在提取...</p>';
    
    fetch('/api/browser/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            resultArea.innerHTML = `
                <div style="text-align:left;width:100%">
                    <h4>${data.result.title}</h4>
                    <p style="color:#64748b">${data.result.url}</p>
                    <hr style="margin:1rem 0;border:none;border-top:1px solid #e2e8f0">
                    <pre style="white-space:pre-wrap;word-break:break-word;background:#f8fafc;padding:1rem;border-radius:0.5rem;font-size:0.875rem">${data.result.text_preview}</pre>
                </div>
            `;
        } else {
            resultArea.innerHTML = `<p style="color:#ef4444">错误: ${data.error}</p>`;
        }
    });
}

function navigateBrowser() {
    const url = document.getElementById('navigate-url').value;
    const action = document.getElementById('navigate-action').value;
    const selector = document.getElementById('navigate-selector').value;
    const text = document.getElementById('navigate-text').value;
    const resultArea = document.getElementById('navigate-result');
    
    resultArea.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> 正在执行...</p>';
    
    fetch('/api/browser/navigate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, action, selector, text })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            resultArea.innerHTML = `
                <div style="text-align:left;width:100%">
                    <p><i class="fas fa-check-circle" style="color:#10b981"></i> 操作成功</p>
                    <pre style="background:#f8fafc;padding:1rem;border-radius:0.5rem;font-size:0.875rem;margin-top:0.5rem">${JSON.stringify(data.result, null, 2)}</pre>
                </div>
            `;
        } else {
            resultArea.innerHTML = `<p style="color:#ef4444">错误: ${data.error}</p>`;
        }
    });
}

// 像素艺术功能
function generatePixelArt() {
    const prompt = document.getElementById('pixel-prompt').value;
    const style = document.getElementById('pixel-style').value;
    const size = document.getElementById('pixel-size').value;
    const resultArea = document.getElementById('pixel-result');
    
    if (!prompt) {
        alert('请输入描述');
        return;
    }
    
    resultArea.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> 正在生成像素艺术...</p>';
    
    fetch('/api/pixel-art/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            prompt, 
            style, 
            width: parseInt(size), 
            height: parseInt(size) 
        })
    })
    .then(res => {
        if (res.ok) return res.blob();
        return res.json().then(data => { throw new Error(data.error); });
    })
    .then(blob => {
        const url = URL.createObjectURL(blob);
        resultArea.innerHTML = `
            <div style="text-align:center">
                <img src="${url}" style="max-width:100%;border-radius:0.5rem;box-shadow:0 4px 6px rgba(0,0,0,0.1);image-rendering:pixelated">
                <p style="margin-top:1rem">
                    <a href="${url}" download="pixel-art.png" class="btn btn-primary">
                        <i class="fas fa-download"></i> 下载图片
                    </a>
                </p>
            </div>
        `;
    })
    .catch(err => {
        resultArea.innerHTML = `<p style="color:#ef4444">错误: ${err.message}</p>`;
    });
}

function setPixelTemplate(type) {
    const templates = {
        'character': '勇敢的骑士，红色盔甲，持剑站立，游戏角色',
        'scene': '日式RPG风格，樱花树下的小村庄，夕阳，温馨氛围',
        'item': '魔法药水，红色液体，发光，游戏道具图标',
        'icon': '复古游戏金币，金色，闪闪发光'
    };
    
    document.getElementById('pixel-prompt').value = templates[type];
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    refreshData();
    loadLogs();
    
    // 定时刷新
    setInterval(() => {
        refreshData();
        if (currentPage === 'tasks') loadTasks();
        if (currentPage === 'logs') loadLogs();
    }, 5000);
});

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('create-task-modal');
    if (event.target === modal) {
        closeCreateTaskModal();
    }
}
