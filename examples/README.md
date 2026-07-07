# 示例视频

本目录包含使用本 Skill 生成的示例视频，展示不同类型的视频创作效果。

## 示例列表

### 01_ocean_sunset.mp4 - 风景类（文生视频）

**类型**：风景/自然
**比例**：16:9（横屏）
**时长**：约 5 秒
**分辨率**：1280x704

**Prompt**：
```
A cinematic shot of a beautiful sunset over the ocean, golden hour light, gentle waves, seagulls flying, slow camera pan, movie still quality, 4K
```

**说明**：展示文生视频的风景创作能力，适合电影感的自然场景。

---

### 02_city_walk.mp4 - 人物类（文生视频）

**类型**：人物/街拍
**比例**：9:16（竖屏）
**时长**：约 5 秒
**分辨率**：704x1280

**Prompt**：
```
A young woman walking down a city street at dusk, wearing a stylish coat, cinematic lighting, slow motion, shallow depth of field, movie still quality
```

**说明**：展示人物动态视频生成，适合短剧、剧情类视频的人物镜头。

---

### 03_product_showcase.mp4 - 产品展示类（文生视频）

**类型**：产品/商业
**比例**：1:1（方形）
**时长**：约 5 秒
**分辨率**：1024x1024

**Prompt**：
```
A luxury perfume bottle rotating slowly on a reflective surface, soft studio lighting, elegant, product shot, commercial quality
```

**说明**：展示产品视频生成能力，适合电商、广告类视频。

---

## 生成参数说明

### 帧数与时长对应关系

| 帧数 | 24fps | 30fps |
|---|---|---|
| 121 帧 | 约 5 秒 | 约 4 秒 |
| 241 帧 | 约 10 秒 | 约 8 秒 |
| 361 帧 | 约 15 秒 | 约 12 秒 |
| 441 帧 | 约 18 秒 | 约 15 秒 |

> 注意：帧数需满足 8n+1 格式

### 常用分辨率

| 比例 | 分辨率 | 适用场景 |
|---|---|---|
| 16:9 | 1280x720 / 1920x1080 | 横屏视频、电影感 |
| 9:16 | 720x1280 / 1080x1920 | 竖屏视频、短视频 |
| 1:1 | 1024x1024 | 方形视频、社交媒体 |
| 4:3 | 1024x768 | 复古风格 |

## 使用方法

### 使用命令行工具生成

```bash
# 文生视频
python scripts/generate_with_agnes.py video -p "你的描述" --duration 10

# 图生视频
python scripts/generate_with_agnes.py video -p "动作描述" -i "图片URL"

# 生成角色设定图
python scripts/generate_with_agnes.py character -n "角色名" -d "角色描述"
```

### 使用 Python 客户端

```python
from scripts.agnes_ai_client import AgnesAIClient

client = AgnesAIClient(api_key="your-api-key")

# 生成视频
video_url = client.generate_video(
    prompt="A beautiful sunset over the ocean",
    height=768,
    width=1280,
    num_frames=121,
    frame_rate=24,
    output_path="output.mp4"
)
```

## 注意事项

1. 视频生成是异步的，通常需要 2-5 分钟
2. 建议先生成短时长（5秒）的视频测试效果
3. 图生视频的效果通常比纯文生视频更好
4. 可以通过调整 prompt 来控制视频风格和内容
5. 生成的视频 URL 有时效性，请及时下载保存
