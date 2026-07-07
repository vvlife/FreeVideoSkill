# Agnes AI API 集成指南

本文件详细说明如何将 Agnes AI API 集成到视频创作工作流中。

## 概述

Agnes AI 是新加坡 Sapiens AI 团队开发的多模态 AI 平台，提供文本、图像、视频三大模态的 API 服务，目前无限期免费开放。

**Base URL**: `https://apihub.agnes-ai.com/v1`

**认证方式**: 请求头中添加 `Authorization: Bearer YOUR_API_KEY`

## 快速开始

### 1. 获取 API Key

1. 访问 [Agnes AI 控制台](https://platform.agnes-ai.com) 注册账号
2. 进入 API Key 管理页面
3. 创建并复制你的 API Key

### 2. 配置方式

**环境变量配置**（推荐）：
```bash
export AGNES_API_KEY="your-api-key-here"
```

**直接传入**：
在调用脚本时通过 `--api-key` 参数传入。

## 模型列表

| 模型名称 | 类型 | 用途 | 价格 |
|---|---|---|---|
| `agnes-2.0-flash` | 文本 | 对话、推理、代码、工具调用、图像理解 | 免费 |
| `agnes-image-2.1-flash` | 图像 | 文生图（高清，最高4K） | 免费 |
| `agnes-image-2.0-flash` | 图像 | 图生图、图像编辑、多图合成 | 免费 |
| `agnes-video-v2.0` | 视频 | 文生视频、图生视频、关键帧动画 | 免费 |

---

## 文本模型 API

### 接口信息

- **Endpoint**: `POST /v1/chat/completions`
- **模型**: `agnes-2.0-flash`
- **上下文窗口**: 512K tokens
- **最大输出**: 65.5K tokens

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 固定为 `agnes-2.0-flash` |
| `messages` | array | 是 | 对话消息数组 |
| `temperature` | number | 否 | 随机性控制，默认 0.7 |
| `top_p` | number | 否 | 核采样参数 |
| `max_tokens` | number | 否 | 最大输出 token 数 |
| `stream` | boolean | 否 | 是否流式输出，默认 false |
| `tools` | array | 否 | 工具调用定义 |
| `tool_choice` | string/object | 否 | 工具调用控制 |

### 请求示例

```bash
curl https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.0-flash",
    "messages": [
      {
        "role": "system",
        "content": "你是一个专业的短剧编剧。"
      },
      {
        "role": "user",
        "content": "帮我写一个90秒的短剧故事大纲"
      }
    ],
    "temperature": 0.8,
    "max_tokens": 2048
  }'
```

### 图像理解

支持通过图像 URL 输入视觉内容：

```json
{
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": "描述这张图片的内容"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/image.jpg"
      }
    }
  ]
}
```

### 响应格式

```json
{
  "id": "chatcmpl_xxx",
  "object": "chat.completion",
  "created": 1774432125,
  "model": "agnes-2.0-flash",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "生成的文本内容..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 35,
    "completion_tokens": 58,
    "total_tokens": 93
  }
}
```

### 在视频创作中的应用

- **剧本创作**：生成短剧故事、角色设定、对话台词
- **分镜设计**：将剧本转换为分镜表
- **提示词优化**：优化图像和视频生成的 prompt
- **图像理解**：分析参考图、资产图，提取视觉特征

---

## 图像模型 API

### 接口信息

- **Endpoint**: `POST /v1/images/generations`
- **文生图模型**: `agnes-image-2.1-flash`（推荐，支持4K）
- **图生图模型**: `agnes-image-2.0-flash`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 模型名称 |
| `prompt` | string | 是 | 图像描述或编辑指令 |
| `size` | string | 是 | 输出尺寸，如 `1024x768`、`1024x1024` |
| `extra_body.image` | string[] | 图生图必填 | 输入图像 URL 或 Base64 数组 |
| `extra_body.response_format` | string | 否 | 输出格式：`url`（默认）或 `b64_json` |
| `return_base64` | boolean | 否 | 是否返回 Base64 |

### 文生图示例

```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "A cinematic portrait of a young man in a black suit, standing in a modern office, dramatic lighting, movie still",
    "size": "1024x1536",
    "extra_body": {
      "response_format": "url"
    }
  }'
```

### 图生图示例

```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "prompt": "Change the background to a cyberpunk city at night, keep the person face and outfit unchanged",
    "size": "1024x1536",
    "extra_body": {
      "image": [
        "https://example.com/input-image.png"
      ],
      "response_format": "url"
    }
  }'
```

### 多图合成示例

```bash
curl https://apihub.agnes-ai.com/v1/images/generations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "prompt": "Combine character1 and character2 into an intense battle scene, dynamic lighting, cinematic composition",
    "size": "1024x768",
    "extra_body": {
      "image": [
        "https://example.com/character1.png",
        "https://example.com/character2.png"
      ],
      "response_format": "url"
    }
  }'
```

### 响应格式

```json
{
  "created": 1780000000,
  "data": [
    {
      "url": "https://storage.googleapis.com/agnes-aigc/xxx.png",
      "b64_json": null,
      "revised_prompt": null
    }
  ]
}
```

### 常用尺寸对照表

| 比例 | 尺寸（1K） | 尺寸（2K） | 适用场景 |
|---|---|---|---|
| 1:1 | 1024x1024 | 2048x2048 | 头像、方形海报 |
| 3:4 | 768x1024 | 1536x2048 | 小红书、竖版海报 |
| 4:3 | 1024x768 | 2048x1536 | 横版图片 |
| 9:16 | 576x1024 | 1152x2048 | 短剧竖屏、抖音 |
| 16:9 | 1024x576 | 2048x1152 | 横屏视频、电影感 |

### 在视频创作中的应用

- **角色资产图**：生成角色设定图（正面、侧面、背面）
- **场景资产图**：生成场景全景、中景、不同视角
- **道具资产图**：生成关键道具的三视图
- **关键帧生成**：基于分镜生成片段关键帧
- **图像编辑**：修改角色表情、动作、场景光照

### 提示词最佳实践

**文生图结构**：
```
[主体描述] + [场景/背景] + [艺术风格] + [光照] + [构图] + [质量要求]
```

**图生图结构**：
```
[编辑指令] + [需要保留的元素] + [目标风格/场景] + [光照] + [构图] + [质量要求]
```

---

## 视频模型 API

### 接口信息

- **提交任务**: `POST /v1/videos`
- **查询状态**: `GET /v1/videos/{task_id}`
- **模型**: `agnes-video-v2.0`
- **工作模式**: 异步任务（提交 → 轮询 → 获取结果）

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `model` | string | 是 | 固定为 `agnes-video-v2.0` |
| `prompt` | string | 是 | 视频内容描述 |
| `image` | string | 否 | 首帧参考图 URL（图生视频） |
| `height` | number | 否 | 视频高度，默认 768 |
| `width` | number | 否 | 视频宽度，默认 1152 |
| `num_frames` | number | 否 | 帧数，需满足 8n+1，默认 121 |
| `frame_rate` | number | 否 | 帧率，1-60，默认 24 |

### 视频时长计算

```
时长(秒) = num_frames / frame_rate
```

**常见配置**：

| 时长 | num_frames | frame_rate | 说明 |
|---|---|---|---|
| 5秒 | 121 | 24 | 短视频 |
| 10秒 | 241 | 24 | 标准短视频 |
| 15秒 | 361 | 24 | 较长短视频 |
| 18秒 | 441 | 24 | 最长（441帧上限） |

### 文生视频示例

```bash
# 第一步：提交任务
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "A cinematic shot of a young man walking through a modern office at night, dramatic lighting, slow motion, movie still quality",
    "height": 1024,
    "width": 576,
    "num_frames": 121,
    "frame_rate": 24
  }'

# 返回：
# {
#   "id": "task_xxx",
#   "status": "queued"
# }
```

```bash
# 第二步：轮询任务状态
curl https://apihub.agnes-ai.com/v1/videos/task_xxx \
  -H "Authorization: Bearer YOUR_API_KEY"

# 进行中：
# {
#   "id": "task_xxx",
#   "status": "in_progress",
#   "progress": 50
# }

# 完成：
# {
#   "id": "task_xxx",
#   "status": "completed",
#   "video_url": "https://.../output.mp4"
# }
```

### 图生视频示例

```bash
curl -X POST https://apihub.agnes-ai.com/v1/videos \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "The character slowly turns his head and looks forward, subtle facial expression change, cinematic lighting",
    "image": "https://example.com/first-frame.png",
    "height": 1024,
    "width": 576,
    "num_frames": 121,
    "frame_rate": 24
  }'
```

### 轮询最佳实践

- **轮询间隔**: 5-10 秒
- **最大等待时间**: 10 分钟
- **状态值**: `queued` → `in_progress` → `completed` / `failed`

### 在视频创作中的应用

- **短剧片段生成**：基于关键帧和分镜生成视频片段
- **UGC 口播视频**：生成产品口播视频
- **产品广告视频**：生成产品展示、营销视频
- **角色动画**：让静态角色图动起来
- **场景运镜**：生成场景的推拉摇移镜头

---

## 与现有工作流的对应关系

| 创作阶段 | 系统内置工具 | Agnes AI 替代方案 |
|---|---|---|
| 剧本/分镜策划 | 内置文本能力 | `agnes-2.0-flash` |
| 角色/场景资产图 | `image_gen` | `agnes-image-2.1-flash`（文生图） |
| 关键帧生成 | `image_edit`（I2I） | `agnes-image-2.0-flash`（图生图） |
| 视频生成 | `text_to_video` / `image_to_video` | `agnes-video-v2.0` |

## 使用建议

### 什么时候用 Agnes AI

1. **需要免费额度时**：Agnes AI 目前完全免费
2. **需要高分辨率图像时**：支持最高 4K 图像生成
3. **需要多图合成时**：支持多张参考图组合生成
4. **需要 OpenAI 兼容接口时**：方便迁移现有代码

### 什么时候用系统内置工具

1. **需要更稳定的服务时**：系统内置工具集成度更高
2. **需要更复杂的视频生成时**：系统工具可能有更多高级功能
3. **需要与平台深度集成时**：如 notify_hunman 等平台特性

### 混合使用策略

- **策划阶段**：用 Agnes AI 文本模型生成剧本、分镜、提示词
- **资产阶段**：用 Agnes AI 图像模型生成角色、场景、道具图
- **关键帧阶段**：用 Agnes AI 图生图能力生成关键帧
- **视频阶段**：根据需求选择 Agnes AI 或系统内置视频工具

---

## 错误处理

### 常见错误码

| 错误 | 原因 | 解决方案 |
|---|---|---|
| 401 Unauthorized | API Key 无效 | 检查 API Key 是否正确 |
| 400 Bad Request | 参数错误 | 检查请求参数格式 |
| 429 Too Many Requests | 频率限制 | 降低请求频率，添加重试逻辑 |
| 500 Internal Error | 服务端错误 | 稍后重试 |

### 重试策略

- 网络错误：指数退避重试（1s, 2s, 4s, 8s, 最多 5 次）
- 频率限制：等待 Retry-After 头指定的时间
- 视频生成失败：检查 prompt 是否包含违规内容，简化后重试

---

## 安全注意事项

1. **API Key 保密**：不要在代码、截图、公开文档中暴露真实 API Key
2. **环境变量**：推荐使用环境变量存储 API Key
3. **服务端调用**：不要在前端客户端代码中直接使用 API Key
4. **定期轮换**：定期更换 API Key，特别是怀疑泄露时

---

## 相关资源

- [官方文档](https://wiki.agnes-ai.com/)
- [控制台](https://platform.agnes-ai.com/)
- [API 状态页](https://status.agnes-ai.com/)
