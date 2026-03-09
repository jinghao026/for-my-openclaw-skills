#!/usr/bin/env python3
"""
双模型协作创作工具
Kimi K2.5 分析任务 → 生成 Prompt → DeepSeek 执行生成
"""

import os
import sys
import argparse
from typing import Dict, Optional
from openai import OpenAI


def load_env():
    """加载环境变量"""
    env_paths = [
        os.path.expanduser("~/.openclaw/.env"),
        os.path.expanduser("~/.env"),
        ".env"
    ]
    
    for env_path in env_paths:
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if key not in os.environ:
                            os.environ[key] = value


# 加载环境变量
load_env()


class DualModelCreator:
    """双模型协作创作器 (免费版 - 使用 SiliconFlow)"""
    
    def __init__(self):
        # 使用 SiliconFlow 免费模型
        # 第一步：分析任务 (使用 Qwen2.5-72B - 免费额度)
        self.analyzer = OpenAI(
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url="https://api.siliconflow.cn/v1"
        )
        
        # 第二步：生成内容 (使用 DeepSeek-V2.5 - 免费额度)
        self.generator = OpenAI(
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url="https://api.siliconflow.cn/v1"
        )
        
        # 模型名称
        self.analyzer_model = "Qwen/Qwen2.5-72B-Instruct"
        self.generator_model = "deepseek-ai/DeepSeek-V2.5"
    
    def analyze_with_kimi(self, idea: str, task_type: str) -> Dict:
        """
        使用 Kimi K2.5 分析任务并生成优化 Prompt
        
        Args:
            idea: 用户的想法/思路
            task_type: 任务类型 (writing/coding/analysis/creative/research)
        
        Returns:
            包含分析和优化prompt的字典
        """
        
        # 根据任务类型设计不同的分析框架
        task_frameworks = {
            "writing": {
                "focus": "文章结构、风格定位、目标读者、内容要点",
                "output_format": "文章大纲 + 写作风格指南 + 关键要点"
            },
            "coding": {
                "focus": "功能模块、架构设计、接口定义、技术选型",
                "output_format": "模块设计 + 接口文档 + 实现步骤"
            },
            "analysis": {
                "focus": "分析维度、数据来源、论证逻辑、结论框架",
                "output_format": "分析框架 + 数据需求 + 论证逻辑"
            },
            "creative": {
                "focus": "创意方向、亮点设计、表现形式、执行流程",
                "output_format": "创意方案 + 执行步骤 + 效果预期"
            },
            "research": {
                "focus": "研究问题、方法论、数据来源、报告结构",
                "output_format": "研究提纲 + 方法设计 + 报告框架"
            }
        }
        
        framework = task_frameworks.get(task_type, task_frameworks["writing"])
        
        analysis_prompt = f"""你是一个专业的任务分析师。请分析以下用户需求，并生成一个优化的执行 Prompt。

用户需求：{idea}
任务类型：{task_type}

请完成以下分析：

1. **任务理解**
   - 用户真正需要什么？
   - 核心目标是什么？
   - 潜在难点有哪些？

2. **分析维度**（{framework['focus']}）
   - 列出关键考虑因素
   - 确定质量评估标准
   - 识别潜在风险点

3. **优化 Prompt**
   基于以上分析，为下一步生成任务写一个详细的 Prompt。
   要求：
   - 结构清晰，步骤明确
   - 包含具体的质量要求
   - 指定输出格式
   - 给出示例或参考

请用中文回答，格式如下：

=== 任务分析 ===
（分析内容）

=== 优化 Prompt ===
（给 DeepSeek 使用的详细 Prompt）
"""

        try:
            response = self.analyzer.chat.completions.create(
                model=self.analyzer_model,
                messages=[
                    {"role": "system", "content": "你是专业的任务分析师，擅长将模糊需求转化为可执行的任务规划。"},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis_result = response.choices[0].message.content
            
            # 解析结果，提取优化后的 prompt
            lines = analysis_result.split('\n')
            in_prompt_section = False
            optimized_prompt = []
            
            for line in lines:
                if '=== 优化 Prompt ===' in line or '优化 Prompt' in line or '执行 Prompt' in line:
                    in_prompt_section = True
                    continue
                if in_prompt_section and line.strip() and not line.startswith('==='):
                    optimized_prompt.append(line)
            
            optimized_prompt_text = '\n'.join(optimized_prompt).strip()
            
            return {
                "full_analysis": analysis_result,
                "optimized_prompt": optimized_prompt_text or analysis_result,
                "task_type": task_type
            }
            
        except Exception as e:
            return {
                "error": f"分析失败: {str(e)}",
                "optimized_prompt": f"请根据以下需求完成任务：{idea}",
                "task_type": task_type
            }
    
    def generate_with_deepseek(self, prompt: str, task_type: str) -> str:
        """
        使用 DeepSeek 依据 Prompt 生成最终结果
        
        Args:
            prompt: Kimi 生成的优化 Prompt
            task_type: 任务类型
        
        Returns:
            生成的最终结果
        """
        
        # 根据任务类型调整 DeepSeek 参数
        temperature_map = {
            "writing": 0.8,      # 写作需要创意
            "coding": 0.2,       # 代码需要准确
            "analysis": 0.5,     # 分析需要平衡
            "creative": 0.9,     # 创意需要发散
            "research": 0.4      # 研究需要严谨
        }
        
        temperature = temperature_map.get(task_type, 0.7)
        
        try:
            response = self.generator.chat.completions.create(
                model=self.generator_model,
                messages=[
                    {"role": "system", "content": "你是专业的执行专家，擅长高质量地完成各类创作和分析任务。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"生成失败: {str(e)}"
    
    def create(self, idea: str, task_type: str = "writing") -> Dict:
        """
        完整的双模型协作创作流程
        
        Args:
            idea: 用户的想法
            task_type: 任务类型
        
        Returns:
            包含完整流程结果的字典
        """
        print(f"🎯 开始双模型协作创作")
        print(f"   任务: {idea[:50]}...")
        print(f"   类型: {task_type}")
        
        # 第一步：Kimi 分析
        print("\n🧠 步骤1: Kimi K2.5 分析任务并生成 Prompt...")
        analysis_result = self.analyze_with_kimi(idea, task_type)
        
        if "error" in analysis_result:
            print(f"   ⚠️ {analysis_result['error']}")
        else:
            print("   ✅ 分析完成")
        
        optimized_prompt = analysis_result.get("optimized_prompt", idea)
        
        # 第二步：DeepSeek 生成
        print("\n🚀 步骤2: DeepSeek 依据 Prompt 生成结果...")
        final_output = self.generate_with_deepseek(optimized_prompt, task_type)
        print("   ✅ 生成完成")
        
        return {
            "idea": idea,
            "task_type": task_type,
            "analysis": analysis_result.get("full_analysis", ""),
            "optimized_prompt": optimized_prompt,
            "final_output": final_output
        }


# 便捷函数
def dual_model_create(idea: str, task_type: str = "writing") -> Dict:
    """便捷调用函数"""
    creator = DualModelCreator()
    return creator.create(idea, task_type)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='双模型协作创作工具')
    parser.add_argument('--idea', '-i', required=True, help='你的想法/思路')
    parser.add_argument('--type', '-t', default='writing', 
                       choices=['writing', 'coding', 'analysis', 'creative', 'research'],
                       help='任务类型')
    parser.add_argument('--output', '-o', help='输出文件路径')
    
    args = parser.parse_args()
    
    # 执行创作
    result = dual_model_create(args.idea, args.type)
    
    # 输出结果
    output = f"""
{'='*60}
🎯 双模型协作创作结果
{'='*60}

📋 原始需求:
{result['idea']}

🔍 任务类型:
{result['task_type']}

{'='*60}
🧠 Kimi K2.5 分析:
{'='*60}
{result['analysis']}

{'='*60}
🚀 DeepSeek 生成结果:
{'='*60}
{result['final_output']}

{'='*60}
"""
    
    print(output)
    
    # 保存到文件
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"\n💾 结果已保存到: {args.output}")
    
    return result


if __name__ == "__main__":
    main()
