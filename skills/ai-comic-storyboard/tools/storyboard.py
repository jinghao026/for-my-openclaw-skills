#!/usr/bin/env python3
"""
AI 漫剧分镜生成器
将故事文本转换为专业分镜脚本
"""

import sys
import re

# 镜头类型定义
SHOT_TYPES = {
    '特写': ['特写', '面部', '表情', '眼神', '手部', '物品细节'],
    '近景': ['近景', '半身', '胸部以上', '肩以上'],
    '中景': ['中景', '膝盖以上', '腰部以上', '两人对话'],
    '全景': ['全景', '全身', '人物+背景', '场景'],
    '远景': ['远景', '大全景', '环境', ' establishing shot']
}

ANGLES = ['平视', '俯视', '仰视', '倾斜', '鸟瞰', '低角度', '过肩']

STYLES = {
    '日漫': 'anime style, manga, clean lines, expressive eyes, soft colors',
    '美漫': 'american comic style, bold lines, high contrast, dynamic shading, marvel/dc style',
    '国漫': 'chinese anime style, guoman, elegant, detailed backgrounds, vibrant colors',
    '韩漫': 'korean webtoon style, detailed, romantic atmosphere, soft lighting',
    '黑白': 'black and white manga, ink drawing, screentone, high contrast'
}

def parse_story(text):
    """解析故事文本，提取场景和动作"""
    # 按句子分割
    sentences = re.split(r'[。！？\n]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def determine_shot(sentence):
    """根据内容判断景别"""
    sentence = sentence.lower()
    
    # 检查关键词
    if any(kw in sentence for kw in ['眼神', '表情', '脸', '手', '眼泪', '微笑']):
        return '特写'
    elif any(kw in sentence for kw in ['全身', '跑', '跳', '场景', '环境', '背景']):
        return '全景'
    elif any(kw in sentence for kw in ['远处', '天空', '城市', '山脉', '大海']):
        return '远景'
    elif any(kw in sentence for kw in ['对话', '两人', '交流', '站']):
        return '中景'
    else:
        return '近景'

def determine_angle(sentence, index):
    """根据内容和位置判断角度"""
    sentence = sentence.lower()
    
    if '看' in sentence or '望' in sentence:
        return '平视'
    elif '高' in sentence or '上' in sentence or '俯视' in sentence:
        return '俯视'
    elif '低' in sentence or '下' in sentence or '抬头' in sentence:
        return '仰视'
    elif index % 3 == 0:
        return '倾斜'  # 增加变化
    else:
        return '平视'

def generate_ai_prompt(shot, angle, description, style='日漫'):
    """生成 AI 绘图提示词"""
    style_prompt = STYLES.get(style, STYLES['日漫'])
    
    # 景别提示
    shot_prompts = {
        '特写': 'extreme close-up, detailed facial expression',
        '近景': 'close-up, upper body',
        '中景': 'medium shot, waist up',
        '全景': 'full shot, full body, wide view',
        '远景': 'long shot, wide angle, landscape'
    }
    
    # 角度提示
    angle_prompts = {
        '平视': 'eye level shot',
        '俯视': 'high angle, looking down',
        '仰视': 'low angle, looking up, dramatic',
        '倾斜': 'dutch angle, tilted, dynamic',
        '鸟瞰': 'bird eye view, top down',
        '低角度': 'extreme low angle, heroic',
        '过肩': 'over the shoulder shot'
    }
    
    prompt = f"{style_prompt}, {shot_prompts.get(shot, '')}, {angle_prompts.get(angle, '')}, {description}, high quality, detailed --ar 16:9"
    return prompt

def generate_storyboard(text, style='日漫', num_shots=None):
    """生成分镜脚本"""
    sentences = parse_story(text)
    
    # 如果指定了镜头数量，均匀分配
    if num_shots and num_shots < len(sentences):
        step = len(sentences) // num_shots
        sentences = [sentences[i*step] for i in range(num_shots)]
    
    storyboard = []
    
    for i, sentence in enumerate(sentences, 1):
        shot = determine_shot(sentence)
        angle = determine_angle(sentence, i)
        prompt = generate_ai_prompt(shot, angle, sentence, style)
        
        storyboard.append({
            '镜号': i,
            '景别': shot,
            '角度': angle,
            '画面描述': sentence,
            '对白': '',  # 可从句子中提取
            'AI提示词': prompt
        })
    
    return storyboard

def format_output(storyboard, format='table'):
    """格式化输出"""
    if format == 'table':
        # 表格格式
        lines = []
        lines.append('| 镜号 | 景别 | 角度 | 画面描述 | 对白 | AI提示词 |')
        lines.append('|------|------|------|----------|------|----------|')
        
        for shot in storyboard:
            desc = shot['画面描述'][:30] + '...' if len(shot['画面描述']) > 30 else shot['画面描述']
            prompt = shot['AI提示词'][:40] + '...' if len(shot['AI提示词']) > 40 else shot['AI提示词']
            lines.append(f"| {shot['镜号']} | {shot['景别']} | {shot['角度']} | {desc} | {shot['对白']} | {prompt} |")
        
        return '\n'.join(lines)
    
    elif format == 'json':
        import json
        return json.dumps(storyboard, ensure_ascii=False, indent=2)
    
    else:
        # 文本格式
        lines = []
        for shot in storyboard:
            lines.append(f"\n【第{shot['镜号']}镜】")
            lines.append(f"景别：{shot['景别']} | 角度：{shot['角度']}")
            lines.append(f"画面：{shot['画面描述']}")
            lines.append(f"AI提示词：{shot['AI提示词']}")
        return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python storyboard.py '故事内容' [风格] [镜头数]")
        print("示例: python storyboard.py '男孩在雨中奔跑' 日漫 5")
        sys.exit(1)
    
    story = sys.argv[1]
    style = sys.argv[2] if len(sys.argv) > 2 else '日漫'
    num_shots = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    board = generate_storyboard(story, style, num_shots)
    print(format_output(board, 'table'))
