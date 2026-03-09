---
name: dual-model-creator
description: |
  双模型协作创作工具（免费版）
  使用 SiliconFlow 免费模型：
  - 第一步：Qwen2.5-72B 分析任务并生成优化 Prompt
  - 第二步：DeepSeek-V2.5 依据 Prompt 生成最终结果
  
  适用于：复杂创作、深度分析、多步骤任务
  完全免费，使用 SiliconFlow 免费额度
---

# Dual Model Creator - 双模型协作创作（免费版）

## 工作原理

```
用户想法 → Qwen2.5-72B (分析+生成Prompt) → DeepSeek-V2.5 (执行生成) → 最终结果
```

**第一步：Qwen2.5-72B 分析** (SiliconFlow 免费)
- 理解用户需求
- 分析任务复杂度
- 生成结构化 Prompt
- 设计执行流程

**第二步：DeepSeek-V2.5 生成** (SiliconFlow 免费)
- 依据 Qwen 设计的 Prompt
- 生成高质量内容
- 输出最终结果

## 配置

设置 SiliconFlow API Key（免费注册）：

```bash
# ~/.openclaw/.env
SILICONFLOW_API_KEY=your_siliconflow_api_key
```

获取方式：
1. 访问 https://siliconflow.cn/
2. 注册账号（送 2000 万 Token 免费额度）
3. 创建 API Key
4. 复制到配置文件

## 使用方法

### Python 调用

```python
from skills.dual_model_creator.dual_model_creator import dual_model_create

# 简单调用
result = dual_model_create(
    idea="写一篇关于人工智能的科普文章",
    task_type="writing"
)

print(result['analysis'])      # Qwen 的分析和 Prompt
print(result['final_output'])  # DeepSeek 的生成结果
```

### 命令行使用

```bash
# 写作任务
python3 skills/dual_model_creator/dual_model_creator.py \
  --idea "写一个小红书文案，关于职场新人成长" \
  --type writing

# 代码任务
python3 skills/dual_model_creator/dual_model_creator.py \
  --idea "写一个Python爬虫，抓取知乎热榜" \
  --type coding

# 分析任务
python3 skills/dual_model_creator/dual_model_creator.py \
  --idea "分析2024年AI行业发展趋势" \
  --type analysis
```

## 支持的任务类型

| 类型 | 说明 | Qwen 职责 | DeepSeek 职责 |
|------|------|-----------|---------------|
| writing | 写作创作 | 设计文章结构、风格、要点 | 撰写具体内容 |
| coding | 代码生成 | 设计架构、模块、接口 | 编写具体代码 |
| analysis | 深度分析 | 设计分析框架、维度 | 执行分析输出 |
| creative | 创意策划 | 设计创意方向、亮点 | 生成创意内容 |
| research | 研究报告 | 设计研究提纲、方法 | 撰写研究报告 |

## 使用的模型

| 步骤 | 模型 | 提供商 | 费用 |
|------|------|--------|------|
| 分析 | Qwen2.5-72B-Instruct | SiliconFlow | 免费额度 |
| 生成 | DeepSeek-V2.5 | SiliconFlow | 免费额度 |

**免费额度**：SiliconFlow 新用户送 2000 万 Token，足够大量使用。

## 优势

1. **完全免费**：使用 SiliconFlow 免费额度
2. **思路清晰**：Qwen 先规划，DeepSeek 后执行
3. **质量更高**：经过两次优化，结果更精准
4. **可控性强**：可以查看中间 Prompt，随时调整
5. **适用广泛**：写作、代码、分析、创意都适用

## 依赖

- Python 3.8+
- openai 库
- SiliconFlow API Key（免费）

安装依赖：
```bash
pip install openai
```

## 更新日志

- 2026-03-06: 初始版本，支持双模型协作
- 2026-03-06: 更新为免费版，使用 SiliconFlow 免费模型
