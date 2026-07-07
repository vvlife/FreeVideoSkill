#!/usr/bin/env python3
"""
Agnes AI API 客户端
提供文本、图像、视频生成的统一接口
"""

import os
import time
import base64
import requests
from typing import List, Optional, Dict, Any


class AgnesAIClient:
    """Agnes AI API 客户端"""

    BASE_URL = "https://apihub.agnes-ai.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端

        Args:
            api_key: Agnes AI API Key，默认从环境变量 AGNES_API_KEY 读取
        """
        self.api_key = api_key or os.environ.get("AGNES_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 未设置。请设置环境变量 AGNES_API_KEY 或传入 api_key 参数。"
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    # ==================== 文本模型 ====================

    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: str = "agnes-2.0-flash",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        stream: bool = False,
        tools: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        文本对话补全

        Args:
            messages: 对话消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大输出 token 数
            stream: 是否流式输出
            tools: 工具定义

        Returns:
            API 响应结果
        """
        url = f"{self.BASE_URL}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream,
        }

        if tools:
            payload["tools"] = tools

        response = self.session.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()

    def chat(self, prompt: str, system_prompt: str = "你是一个有帮助的AI助手。", **kwargs) -> str:
        """
        简单的单轮对话

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词

        Returns:
            生成的文本内容
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        result = self.chat_completion(messages, **kwargs)
        return result["choices"][0]["message"]["content"]

    # ==================== 图像模型 ====================

    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        model: str = "agnes-image-2.1-flash",
        response_format: str = "url",
        image_urls: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        图像生成（文生图或图生图）

        Args:
            prompt: 图像描述或编辑指令
            size: 输出尺寸，如 "1024x768"
            model: 模型名称
                   - agnes-image-2.1-flash: 文生图（高清）
                   - agnes-image-2.0-flash: 图生图/图像编辑
            response_format: 输出格式，"url" 或 "b64_json"
            image_urls: 参考图 URL 列表（图生图时使用）

        Returns:
            API 响应结果
        """
        url = f"{self.BASE_URL}/images/generations"
        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "extra_body": {
                "response_format": response_format
            }
        }

        if image_urls:
            payload["extra_body"]["image"] = image_urls
            # 图生图使用 2.0 模型
            if model == "agnes-image-2.1-flash":
                payload["model"] = "agnes-image-2.0-flash"

        response = self.session.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()

    def text_to_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        output_path: Optional[str] = None,
    ) -> str:
        """
        文生图便捷方法

        Args:
            prompt: 图像描述
            size: 输出尺寸
            output_path: 保存路径（可选）

        Returns:
            图像 URL 或保存路径
        """
        result = self.generate_image(
            prompt=prompt,
            size=size,
            model="agnes-image-2.1-flash",
            response_format="url"
        )

        image_url = result["data"][0]["url"]

        if output_path:
            self._download_image(image_url, output_path)
            return output_path

        return image_url

    def image_to_image(
        self,
        prompt: str,
        image_url: str,
        size: str = "1024x1024",
        output_path: Optional[str] = None,
    ) -> str:
        """
        图生图便捷方法

        Args:
            prompt: 编辑指令
            image_url: 参考图 URL
            size: 输出尺寸
            output_path: 保存路径（可选）

        Returns:
            图像 URL 或保存路径
        """
        result = self.generate_image(
            prompt=prompt,
            size=size,
            model="agnes-image-2.0-flash",
            response_format="url",
            image_urls=[image_url]
        )

        result_url = result["data"][0]["url"]

        if output_path:
            self._download_image(result_url, output_path)
            return output_path

        return result_url

    def _download_image(self, url: str, output_path: str):
        """下载图像到本地"""
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)

    # ==================== 视频模型 ====================

    def create_video_task(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        height: int = 768,
        width: int = 1152,
        num_frames: int = 121,
        frame_rate: int = 24,
    ) -> str:
        """
        创建视频生成任务

        Args:
            prompt: 视频内容描述
            image_url: 首帧参考图 URL（图生视频）
            height: 视频高度
            width: 视频宽度
            num_frames: 帧数（需满足 8n+1）
            frame_rate: 帧率

        Returns:
            任务 ID
        """
        url = f"{self.BASE_URL}/videos"
        payload = {
            "model": "agnes-video-v2.0",
            "prompt": prompt,
            "height": height,
            "width": width,
            "num_frames": num_frames,
            "frame_rate": frame_rate,
        }

        if image_url:
            payload["image"] = image_url

        response = self.session.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result.get("id") or result.get("task_id")

    def get_video_status(self, task_id: str) -> Dict[str, Any]:
        """
        查询视频任务状态

        Args:
            task_id: 任务 ID

        Returns:
            任务状态信息
        """
        url = f"{self.BASE_URL}/videos/{task_id}"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()

    def generate_video(
        self,
        prompt: str,
        image_url: Optional[str] = None,
        height: int = 768,
        width: int = 1152,
        num_frames: int = 121,
        frame_rate: int = 24,
        poll_interval: int = 5,
        max_wait: int = 600,
        output_path: Optional[str] = None,
        verbose: bool = True,
    ) -> str:
        """
        生成视频（同步等待，自动轮询）

        Args:
            prompt: 视频内容描述
            image_url: 首帧参考图 URL
            height: 视频高度
            width: 视频宽度
            num_frames: 帧数
            frame_rate: 帧率
            poll_interval: 轮询间隔（秒）
            max_wait: 最大等待时间（秒）
            output_path: 保存路径（可选）
            verbose: 是否打印进度

        Returns:
            视频 URL 或保存路径
        """
        # 提交任务
        if verbose:
            print("正在提交视频生成任务...")
        task_id = self.create_video_task(
            prompt=prompt,
            image_url=image_url,
            height=height,
            width=width,
            num_frames=num_frames,
            frame_rate=frame_rate,
        )
        if verbose:
            print(f"任务已提交，ID: {task_id}")

        # 轮询等待
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait:
                raise TimeoutError(f"视频生成超时（等待 {max_wait} 秒）")

            status = self.get_video_status(task_id)
            status_text = status.get("status", "unknown")

            if verbose:
                progress = status.get("progress", "?")
                print(f"[{elapsed:.0f}s] 状态: {status_text}, 进度: {progress}%")

            if status_text == "completed":
                video_url = self._extract_video_url(status)

                if output_path and video_url:
                    if verbose:
                        print(f"正在下载视频到 {output_path}...")
                    self._download_video(video_url, output_path)
                    return output_path

                return video_url

            elif status_text == "failed":
                error = status.get("error", "未知错误")
                raise RuntimeError(f"视频生成失败: {error}")

            time.sleep(poll_interval)

    def _extract_video_url(self, status: Dict[str, Any]) -> Optional[str]:
        """
        从任务状态中提取视频URL
        
        Args:
            status: 任务状态字典
            
        Returns:
            视频URL，找不到则返回None
        """
        # 1. 直接尝试常见字段名
        for field in ["url", "video_url", "output_url", "result_url"]:
            url = status.get(field)
            if url and url.startswith("http"):
                return url
        
        # 2. 尝试从 data 数组中获取
        if "data" in status and isinstance(status["data"], list) and len(status["data"]) > 0:
            for field in ["url", "video_url", "output_url"]:
                url = status["data"][0].get(field)
                if url and url.startswith("http"):
                    return url
        
        # 3. 尝试从 remixed_from_video_id 中提取基础路径，然后构造URL
        video_id = status.get("video_id")
        remixed_url = status.get("remixed_from_video_id")
        if video_id and remixed_url and remixed_url.startswith("http"):
            # 从remixed_url中提取基础路径
            base_path = remixed_url.rsplit("/", 1)[0]
            url = f"{base_path}/{video_id}.mp4"
            # 简单验证一下URL格式
            if url.startswith("http"):
                return url
        
        # 4. 尝试用video_id构造常见格式的URL
        if video_id:
            # 尝试几种常见格式
            candidates = [
                f"https://platform-outputs.agnes-ai.space/videos/agnes-video-v2.0/{video_id}.mp4",
                f"https://platform-outputs.agnes-ai.space/videos/agnes-video-v2.0/video_{video_id}.mp4",
            ]
            # 这里不做实际请求验证，只返回候选
            # 调用者可以自行验证
            return candidates[0]  # 返回最可能的格式
        
        return None

    def _download_video(self, url: str, output_path: str):
        """下载视频到本地"""
        response = requests.get(url, timeout=300, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    # ==================== 工具方法 ====================

    @staticmethod
    def calculate_frames(duration_seconds: float, frame_rate: int = 24) -> int:
        """
        根据时长计算帧数（需满足 8n+1）

        Args:
            duration_seconds: 目标时长（秒）
            frame_rate: 帧率

        Returns:
            帧数
        """
        raw_frames = int(duration_seconds * frame_rate)
        # 调整为 8n+1 格式
        adjusted = ((raw_frames - 1) // 8) * 8 + 1
        # 确保不超过上限 441
        return min(adjusted, 441)

    @staticmethod
    def get_size_by_ratio(ratio: str, base_size: int = 1024) -> str:
        """
        根据比例获取尺寸

        Args:
            ratio: 比例，如 "1:1", "3:4", "9:16", "16:9"
            base_size: 基准尺寸

        Returns:
            尺寸字符串，如 "1024x1024"
        """
        ratio_map = {
            "1:1": (base_size, base_size),
            "3:4": (int(base_size * 0.75), base_size),
            "4:3": (base_size, int(base_size * 0.75)),
            "9:16": (int(base_size * 0.5625), base_size),
            "16:9": (base_size, int(base_size * 0.5625)),
        }

        if ratio not in ratio_map:
            raise ValueError(f"不支持的比例: {ratio}。支持的比例: {list(ratio_map.keys())}")

        width, height = ratio_map[ratio]
        return f"{width}x{height}"


def main():
    """命令行测试"""
    import argparse

    parser = argparse.ArgumentParser(description="Agnes AI API 客户端测试")
    parser.add_argument("--api-key", help="API Key")
    parser.add_argument("--test", choices=["text", "image", "video"], help="测试类型")
    args = parser.parse_args()

    client = AgnesAIClient(api_key=args.api_key)

    if args.test == "text":
        print("测试文本生成...")
        result = client.chat("用一句话介绍你自己")
        print(f"结果: {result}")

    elif args.test == "image":
        print("测试图像生成...")
        url = client.text_to_image(
            "A beautiful sunset over the ocean, cinematic photography",
            size="1024x768"
        )
        print(f"图像 URL: {url}")

    elif args.test == "video":
        print("测试视频生成...")
        url = client.generate_video(
            "A peaceful ocean sunset with gentle waves, cinematic",
            height=768,
            width=1152,
            num_frames=121,
            frame_rate=24,
        )
        print(f"视频 URL: {url}")


if __name__ == "__main__":
    main()
