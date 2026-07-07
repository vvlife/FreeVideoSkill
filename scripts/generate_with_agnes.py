#!/usr/bin/env python3
"""
Agnes AI 视频创作便捷工具
提供图像和视频生成的命令行接口
"""

import os
import sys
import argparse
from pathlib import Path

# 添加脚本所在目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from agnes_ai_client import AgnesAIClient


def generate_image(args):
    """生成图像"""
    client = AgnesAIClient(api_key=args.api_key)

    print(f"正在生成图像...")
    print(f"  提示词: {args.prompt}")
    print(f"  尺寸: {args.size}")
    print(f"  模型: {args.model}")

    if args.reference:
        print(f"  参考图: {args.reference}")
        result = client.image_to_image(
            prompt=args.prompt,
            image_url=args.reference,
            size=args.size,
            output_path=args.output,
        )
    else:
        result = client.text_to_image(
            prompt=args.prompt,
            size=args.size,
            output_path=args.output,
        )

    print(f"\n✅ 生成完成！")
    print(f"结果: {result}")
    return result


def generate_video(args):
    """生成视频"""
    client = AgnesAIClient(api_key=args.api_key)

    # 计算帧数
    if args.duration:
        num_frames = client.calculate_frames(args.duration, args.fps)
    else:
        num_frames = args.num_frames

    print(f"正在生成视频...")
    print(f"  提示词: {args.prompt}")
    print(f"  分辨率: {args.width}x{args.height}")
    print(f"  帧数: {num_frames}")
    print(f"  帧率: {args.fps}")
    print(f"  预计时长: {num_frames / args.fps:.1f} 秒")

    if args.image:
        print(f"  首帧图: {args.image}")

    result = client.generate_video(
        prompt=args.prompt,
        image_url=args.image,
        height=args.height,
        width=args.width,
        num_frames=num_frames,
        frame_rate=args.fps,
        poll_interval=args.poll_interval,
        max_wait=args.max_wait,
        output_path=args.output,
        verbose=True,
    )

    print(f"\n✅ 视频生成完成！")
    print(f"结果: {result}")
    return result


def generate_character_asset(args):
    """生成角色资产图（快捷方式）"""
    client = AgnesAIClient(api_key=args.api_key)

    print(f"正在生成角色设定图...")
    print(f"  角色: {args.name}")
    print(f"  描述: {args.description}")
    print(f"  风格: {args.style}")

    # 构建提示词
    prompt = f"""
Character design sheet of {args.name}, {args.description}.
{args.style} style.
Left side: close-up front view of the face, detailed facial features.
Right side: full body three-view turnaround (front, side, back).
Pure white background, professional character design sheet.
High quality, detailed, clean lines.
""".strip()

    size = "1792x1024"  # 16:9 横版

    output = args.output or f"{args.name}_character_sheet.png"

    result = client.text_to_image(
        prompt=prompt,
        size=size,
        output_path=output,
    )

    print(f"\n✅ 角色设定图生成完成！")
    print(f"结果: {result}")
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Agnes AI 视频创作工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 文生图
  python generate_with_agnes.py image -p "一只可爱的猫" -s 1024x1024 -o cat.png

  # 图生图
  python generate_with_agnes.py image -p "改成赛博朋克风格" -r https://example.com/img.png

  # 文生视频
  python generate_with_agnes.py video -p "海边日落" --duration 10 -o sunset.mp4

  # 图生视频
  python generate_with_agnes.py video -p "人物慢慢转头" -i https://example.com/frame.png

  # 生成角色设定图
  python generate_with_agnes.py character -n "小明" -d "年轻男性，黑色短发，穿黑色西装" --style "真人电影"
        """
    )

    parser.add_argument("--api-key", help="Agnes AI API Key（也可通过 AGNES_API_KEY 环境变量设置）")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # ===== 图像生成 =====
    image_parser = subparsers.add_parser("image", help="生成图像")
    image_parser.add_argument("-p", "--prompt", required=True, help="图像描述")
    image_parser.add_argument("-s", "--size", default="1024x1024", help="尺寸，默认 1024x1024")
    image_parser.add_argument("-m", "--model", default="agnes-image-2.1-flash", help="模型名称")
    image_parser.add_argument("-r", "--reference", help="参考图 URL（图生图模式）")
    image_parser.add_argument("-o", "--output", help="输出文件路径")
    image_parser.set_defaults(func=generate_image)

    # ===== 视频生成 =====
    video_parser = subparsers.add_parser("video", help="生成视频")
    video_parser.add_argument("-p", "--prompt", required=True, help="视频描述")
    video_parser.add_argument("-i", "--image", help="首帧参考图 URL")
    video_parser.add_argument("--width", type=int, default=1152, help="宽度，默认 1152")
    video_parser.add_argument("--height", type=int, default=768, help="高度，默认 768")
    video_parser.add_argument("--duration", type=float, help="目标时长（秒），自动计算帧数")
    video_parser.add_argument("--num-frames", type=int, default=121, help="帧数，默认 121（约5秒）")
    video_parser.add_argument("--fps", type=int, default=24, help="帧率，默认 24")
    video_parser.add_argument("--poll-interval", type=int, default=5, help="轮询间隔（秒），默认 5")
    video_parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间（秒），默认 600")
    video_parser.add_argument("-o", "--output", help="输出文件路径")
    video_parser.set_defaults(func=generate_video)

    # ===== 角色设定图 =====
    char_parser = subparsers.add_parser("character", help="生成角色设定图（快捷方式）")
    char_parser.add_argument("-n", "--name", required=True, help="角色名称")
    char_parser.add_argument("-d", "--description", required=True, help="角色描述")
    char_parser.add_argument("--style", default="真人电影", help="艺术风格，默认 真人电影")
    char_parser.add_argument("-o", "--output", help="输出文件路径")
    char_parser.set_defaults(func=generate_character_asset)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    try:
        args.func(args)
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
