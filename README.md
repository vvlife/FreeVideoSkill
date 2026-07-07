# 创意视频综合套件 (doubao-creative-video-suite)

一个综合视频创作全流程 Skill，支持短剧/剧情视频和通用商业视频两大类视频生成。

## 功能特性

### 两大创作分支

| 分支 | 适用场景 |
|---|---|
| **短剧/剧情视频** | 短剧、动画、微电影、剧情视频、影视化、动态漫、预告片 |
| **商业视频** | 产品广告、UGC口播、带货视频、企业宣传、品牌形象片 |

### 完整工作流

- **剧本创作**：故事构思、角色设定、剧情发展
- **分镜设计**：镜头语言、节奏控制、画面描述
- **资产设定**：角色、场景、道具的视觉设定
- **关键帧生成**：基于分镜的关键画面
- **视频生成**：最终视频输出

### Agnes AI 集成

内置 Agnes AI API 支持，提供免费的文本、图像、视频生成能力：

- `agnes-2.0-flash` - 文本模型（512K上下文）
- `agnes-image-2.1-flash` - 文生图（最高4K）
- `agnes-image-2.0-flash` - 图生图/图像编辑
- `agnes-video-v2.0` - 视频生成

## 目录结构

```
doubao-creative-video-suite/
├── SKILL.md                          # Skill 主入口
├── README.md                         # 项目说明
├── examples/                         # 示例视频
│   ├── README.md                     # 示例说明
│   ├── 01_ocean_sunset.mp4           # 风景类文生视频示例
│   └── 02_city_walk.mp4              # 人物类文生视频示例
├── references/
│   ├── drama/                        # 短剧/剧情视频分支
│   │   ├── scriptwriter.md           # 剧本创作
│   │   ├── storyboard.md             # 分镜切分
│   │   ├── assets.md                 # 资产设定
│   │   ├── frame.md                  # 关键帧生成
│   │   └── prompt.md                 # 视频提示词
│   ├── commercial/                   # 商业视频分支
│   │   ├── ugc-talking-video-ref.md      # UGC口播视频
│   │   ├── product-marketing-ad-video-no-storyboard-ref.md  # 产品营销广告
│   │   └── corporate-business-video-ref.md  # 企业商务宣传
│   └── agnes-ai-api.md               # Agnes AI API 文档
└── scripts/
    ├── agnes_ai_client.py            # Agnes AI Python 客户端
    └── generate_with_agnes.py        # 便捷命令行工具
```

## 快速开始

### Agnes AI 配置

1. 访问 [Agnes AI 控制台](https://platform.agnes-ai.com) 注册账号
2. 获取 API Key
3. 设置环境变量：

```bash
export AGNES_API_KEY="your-api-key"
```

### 使用命令行工具

```bash
# 文生图
python scripts/generate_with_agnes.py image -p "一只可爱的猫" -s 1024x1024

# 图生图
python scripts/generate_with_agnes.py image -p "改成赛博朋克风格" -r https://example.com/img.png

# 文生视频（10秒）
python scripts/generate_with_agnes.py video -p "海边日落" --duration 10

# 图生视频
python scripts/generate_with_agnes.py video -p "人物慢慢转头" -i https://example.com/frame.png

# 生成角色设定图
python scripts/generate_with_agnes.py character -n "小明" -d "年轻男性，黑色短发" --style "真人电影"
```

### 使用 Python 客户端

```python
from scripts.agnes_ai_client import AgnesAIClient

client = AgnesAIClient(api_key="your-api-key")

# 文本生成
result = client.chat("用一句话介绍你自己")

# 文生图
image_url = client.text_to_image(
    "A beautiful sunset over the ocean",
    size="1024x768"
)

# 视频生成
video_url = client.generate_video(
    "A peaceful ocean sunset with gentle waves",
    height=768,
    width=1152,
    num_frames=121,
    frame_rate=24,
)
```

## 核心规则

### 视频生成门禁

生成视频前必须确认四个要素：
- **时长**：视频长度
- **比例**：画面比例（16:9、9:16、1:1 等）
- **详细内容**：画面主体、动作、场景、风格
- **数量**：一次最多 2 个

### 确认机制

必须输出参数摘要并等待用户明确确认后才能生成。

### 即时输出原则

每生成完一张图或一个视频，立即展示返回，不批量打包。

### 图片质量审查

- 人设图：面部正脸、三视图一致
- 关键帧：剧情匹配、人物场景道具一致

## 示例视频

本目录包含使用本 Skill 生成的示例视频，展示不同类型的视频创作效果。

### 01_ocean_sunset.mp4 — 风景类（文生视频）

**类型**：风景/自然  
**比例**：16:9（横屏）  
**时长**：约 5 秒  
**分辨率**：1280x704

**Prompt**：
```
A cinematic shot of a beautiful sunset over the ocean, golden hour light, gentle waves, seagulls flying, slow camera pan, movie still quality, 4K
```

<a href="examples/01_ocean_sunset.mp4">
  <video src="examples/01_ocean_sunset.mp4" width="640" controls style="max-width:100%; border-radius:8px;"></video>
</a>

---

### 02_city_walk.mp4 — 人物类（文生视频）

**类型**：人物/街拍  
**比例**：9:16（竖屏）  
**时长**：约 5 秒  
**分辨率**：704x1280

**Prompt**：
```
A young woman walking down a city street at dusk, wearing a stylish coat, cinematic lighting, slow motion, shallow depth of field, movie still quality
```

<a href="examples/02_city_walk.mp4">
  <video src="examples/02_city_walk.mp4" width="320" controls style="max-width:100%; border-radius:8px;"></video>
</a>

---

> 💡 点击视频即可直接播放，也可以右键另存下载到本地。

## 相关资源

- [Agnes AI 官方文档](https://wiki.agnes-ai.com/)
- [Agnes AI 控制台](https://platform.agnes-ai.com/)

## 许可证

MIT License
