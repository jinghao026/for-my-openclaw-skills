# OpenClaw 记忆系统技能合集

本仓库收集了多种 OpenClaw 记忆功能 skill，供不同场景使用。

---

## 📚 技能列表

### 1. local-memory ⭐ 推荐
**基础本地文件记忆系统**

- 用途：入门首选，无需额外配置
- 特点：基于 Markdown 文件，简单易用
- 文件：
  - `memory/USER.md` - 用户信息
  - `memory/HISTORY.md` - 对话历史
  - `memory/YYYY-MM-DD.md` - 每日日志
  - `MEMORY.md` - 长期记忆

**适合场景**：新手入门、轻量级使用

---

### 2. openclaw-memory-system ⭐ 推荐
**完整的记忆系统实现**

基于非凡产研卓然的教程《06 记忆系统：从失忆到永生》

- 双层记忆架构：
  - 短期记忆层 (memory/YYYY-MM-DD.md)
  - 长期智慧层 (MEMORY.md)
- 自动注入：SOUL.md、USER.md、TOOLS.md
- 群聊隔离：安全设计，群聊不加载私人记忆

**适合场景**：生产环境、完整功能需求

---

### 3. memory-lite
**轻量级记忆管理（无需向量搜索）**

- 无嵌入、无向量搜索
- 纯本地文件操作
- 关键字搜索（grep）
- 本地摘要生成

**适合场景**：低资源环境、简单需求、无配置更改

---

### 4. openclaw-persistent-memory
**持久化记忆系统（含语义搜索）**

- 自动捕获：智能提取重要信息
- 自动回忆：相关记忆自动注入上下文
- SQLite + FTS5：快速全文搜索
- 语义搜索：基于嵌入的相似度检索

**工具**：`memory_search`、`memory_get`、`memory_store`、`memory_delete`

**适合场景**：需要智能检索、自动记忆管理

---

### 5. memory-pipeline
**结构化记忆流水线**

- 记忆简报：任务前自动加载相关上下文
- 检查清单：结构化提示确保一致性
- 行动后回顾：自动记录任务完成情况
- 工具过滤：根据上下文限制危险工具

**适合场景**：复杂任务、团队协作、流程化管理

---

### 6. memory-hygiene
**记忆卫生维护**

- 清理重复条目
- 删除过期信息
- 合并相似记忆
- 优化存储空间

**适合场景**：长期运行、记忆库维护

---

### 7. self-improving-agent ⭐ 推荐
**自我迭代记忆**

- 错误记录与反思
- 经验积累与复用
- 持续优化改进
- 学习能力增强

**适合场景**：长期运行、自我进化需求

---

## 🚀 快速开始

### 选择合适的技能

| 需求 | 推荐技能 |
|------|----------|
| 刚入门，简单使用 | local-memory |
| 完整功能，生产环境 | openclaw-memory-system |
| 低资源，轻量级 | memory-lite |
| 智能检索，自动管理 | openclaw-persistent-memory |
| 复杂任务，流程化 | memory-pipeline |
| 长期维护，清理优化 | memory-hygiene |
| 自我进化 | self-improving-agent |

### 安装技能

```bash
# 方式1：复制到 skills/ 目录
cp -r skills/local-memory ~/.openclaw/workspace/skills/

# 方式2：使用 clawhub（如支持）
clawhub install local-memory
```

### 配置记忆系统

1. **基础配置**（必需）
   - 确保 `memory/` 目录存在
   - 创建 `MEMORY.md` 和 `memory/USER.md`

2. **高级配置**（可选）
   - 安装 SQLite 支持（用于语义搜索）
   - 配置 `openclaw.plugin.json`

---

## 📖 记忆文件结构

```
workspace/
├── MEMORY.md                 # 长期记忆（仅主会话加载）
├── SOUL.md                   # 人格定义
├── USER.md                   # 用户画像
├── TOOLS.md                  # 工具配置
├── AGENTS.md                 # Agent 规范
├── memory/
│   ├── USER.md              # 用户详细信息
│   ├── HISTORY.md           # 对话历史
│   ├── TASKS.md             # 任务追踪
│   ├── 2026-03-09.md        # 今日日志
│   ├── 2026-03-08.md        # 昨日日志
│   └── archives/            # 归档目录
│       └── 2026-02/
└── skills/
    ├── local-memory/
    ├── openclaw-memory-system/
    ├── memory-lite/
    └── ...
```

---

## 📝 使用规范

### Text > Brain 原则

> 想记住什么，就写进文件，不要靠脑子记

- 重要信息 → `MEMORY.md`
- 用户信息 → `memory/USER.md`
- 今日事项 → `memory/YYYY-MM-DD.md`
- 经验教训 → `SOUL.md` 或 `TOOLS.md`

### 记忆触发条件

| 触发条件 | 写入位置 | 示例 |
|----------|----------|------|
| 发现高频问题 | MEMORY.md | 第3次有人问如何部署 |
| 验证有效方案 | TOOLS.md | 找到更好的邮件发送方式 |
| 用户画像更新 | USER.md | 发现用户新偏好 |
| 重要讨论结论 | memory/YYYYMMDD.md | 达成某个决策 |
| 犯了错误 | SOUL.md + memory/ | 记录避免再犯 |

---

## 🔧 工具使用

OpenClaw 提供两个核心记忆工具：

### memory_search
语义检索，支持自然语言查询。

示例：
```
查询："上周关于服务器配置的决策"
返回：相关片段及文件位置
```

### memory_get
精确读取，指定文件路径和行范围。

通常在 `memory_search` 后使用，获取完整上下文。

---

## 📚 参考资料

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [非凡产研 - 记忆系统教程](https://100aiapps.cn)
- [ClawHub Skill 市场](https://clawhub.com)

---

## 📄 许可证

各技能遵循其原始许可证（主要为 MIT）。

---

**最后更新**: 2026-03-09
