---
name: pixel-studio
description: |
  像素工作室 - 像素艺术创作工具（部署指南版）
  本skill记录了如何创建和部署一个像素艺术创作工具的完整过程
  可作为创建类似创作工具的参考模板
---

# Pixel Studio - 像素工作室部署指南 🎮

## 项目概述

像素工作室是一个基于AI的像素艺术创作工具，支持生成8-bit/16-bit风格的像素艺术图像、游戏素材和复古艺术作品。

## 部署前准备

### 1. 环境要求
- Python 3.8+
- 网络连接（访问图像生成API）
- 可选：API Key（如需使用高级功能）

### 2. 依赖安装
```bash
pip install requests pillow
```

### 3. 目录结构
```
skills/pixel-studio/
├── SKILL.md              # 本说明文档
├── README.md             # 项目介绍
├── pixel_generator.py    # 像素生成脚本
├── examples/             # 示例输出
│   ├── characters/       # 角色示例
│   ├── scenes/           # 场景示例
│   └── items/            # 道具示例
└── templates/            # 提示词模板
```

## 核心功能实现

### 图像生成接口
本工具支持多种图像生成方式：

#### 方式一：Pollinations AI（免费）
- 无需API Key
- 支持FLUX、SD等模型
- 适合快速原型和测试

```python
import requests
import urllib.parse

def generate_pixel_art_pollinations(prompt, width=512, height=512, style="8-bit"):
    """使用Pollinations生成像素艺术"""
    
    # 添加像素风格关键词
    full_prompt = f"pixel art, {style} style, {prompt}, game asset, crisp edges, limited color palette"
    
    encoded_prompt = urllib.parse.quote(full_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    
    params = {
        "width": width,
        "height": height,
        "model": "flux",
        "nologo": "true"
    }
    
    response = requests.get(url, params=params, timeout=120)
    return response.content
```

#### 方式二：SiliconFlow API（高质量）
- 需要API Key
- 支持FLUX、SD3.5等高质量模型
- 适合生产环境

```python
import os
import requests

def generate_pixel_art_siliconflow(prompt, model="FLUX.1-schnell"):
    """使用SiliconFlow生成像素艺术"""
    
    api_key = os.environ.get("SILICONFLOW_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    full_prompt = f"pixel art, 8-bit style, {prompt}, video game asset"
    
    payload = {
        "model": f"black-forest-labs/{model}",
        "prompt": full_prompt,
        "image_size": "1024x1024"
    }
    
    response = requests.post(
        "https://api.siliconflow.cn/v1/images/generations",
        headers=headers,
        json=payload
    )
    
    result = response.json()
    return result["images"][0]["url"]
```

## 使用示例

### 生成游戏角色
```python
# 8-bit勇士角色
prompt = "brave knight in red armor, holding sword, standing pose"
image = generate_pixel_art_pollinations(prompt, 256, 256, "8-bit")

# 保存图片
with open("knight_8bit.png", "wb") as f:
    f.write(image)
```

### 生成游戏场景
```python
# 像素风格场景
prompt = "Japanese RPG style village, cherry blossom trees, sunset, warm atmosphere"
image = generate_pixel_art_pollinations(prompt, 512, 512, "16-bit")

with open("village_scene.png", "wb") as f:
    f.write(image)
```

### 生成道具图标
```python
# 游戏道具
prompt = "pixel art potion bottle, red liquid, magic glow, item icon"
image = generate_pixel_art_pollinations(prompt, 64, 64, "8-bit")

with open("potion_icon.png", "wb") as f:
    f.write(image)
```

## 提示词模板

### 角色类模板
```
pixel art, [8-bit/16-bit] style, [角色描述], [动作/姿势], 
[颜色主题], [背景], game character sprite
```

### 场景类模板
```
pixel art, [8-bit/16-bit] style, [场景描述], [时间/天气], 
[氛围], [游戏类型] game background
```

### 道具类模板
```
pixel art, [8-bit/16-bit] style, [道具名称], [材质/效果], 
[item/icon], transparent background
```

## 风格关键词

### 像素风格
- `8-bit` - 经典8位像素风格
- `16-bit` - 超级任天堂风格
- `32-bit` - 更精细的像素
- `dithering` - 抖动效果
- `limited color palette` - 有限调色板

### 游戏类型
- `retro gaming` - 复古游戏
- `JRPG style` - 日式RPG
- `platformer` - 平台游戏
- `top-down RPG` - 俯视RPG

## 批量生成脚本

```python
# batch_generate.py
import os
from concurrent.futures import ThreadPoolExecutor

def batch_generate(characters, output_dir="outputs"):
    """批量生成角色"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    def generate_one(char_name, description):
        prompt = f"pixel art character, {description}, 8-bit style"
        image = generate_pixel_art_pollinations(prompt, 128, 128)
        
        output_path = os.path.join(output_dir, f"{char_name}.png")
        with open(output_path, "wb") as f:
            f.write(image)
        
        return f"Generated: {char_name}"
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(generate_one, name, desc)
            for name, desc in characters.items()
        ]
        
        for future in futures:
            print(future.result())

# 使用示例
characters = {
    "warrior": "brave knight with sword and shield",
    "mage": "wizard with staff and blue robe",
    "archer": "elf archer with bow",
    "healer": "cleric with holy symbol"
}

batch_generate(characters, "my_game_characters")
```

## 注意事项

### 免费服务限制
- Pollinations有速率限制
- 建议添加延迟避免被封
- 重要项目建议使用付费API

### 版权问题
- 生成的图像可用于个人/商业项目
- 建议二次编辑确保独特性
- 遵守各平台使用条款

### 优化建议
1. **明确指定尺寸** - 像素艺术需要精确尺寸
2. **使用风格关键词** - 帮助AI理解像素风格
3. **限制颜色数量** - 更真实的像素效果
4. **后期处理** - 使用图像编辑软件微调

## 扩展功能

### 1. 像素化现有图片
```python
from PIL import Image

def pixelate_image(input_path, output_path, pixel_size=8):
    """将普通图片转换为像素风格"""
    img = Image.open(input_path)
    
    # 缩小
    small = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        Image.Resampling.BILINEAR
    )
    
    # 放大回原始尺寸
    result = small.resize(
        (img.width, img.height),
        Image.Resampling.NEAREST
    )
    
    result.save(output_path)
```

### 2. 创建精灵表
```python
def create_sprite_sheet(images, columns=4):
    """将多个角色合并为精灵表"""
    # 实现精灵表生成逻辑
    pass
```

### 3. 动画帧生成
```python
def generate_animation_frames(base_prompt, frames=4):
    """生成角色动画帧"""
    # 为每个帧添加动作描述
    pass
```

## 参考资料

- [Pollinations AI](https://pollinations.ai/)
- [SiliconFlow](https://cloud.siliconflow.cn/)
- [像素艺术教程](https://lospec.com/)
- [游戏设计模式](https://gameprogrammingpatterns.com/)

---

*Pixel Studio - 让每个人都成为像素艺术家 ✨*
*部署日期：2026-03-09*
