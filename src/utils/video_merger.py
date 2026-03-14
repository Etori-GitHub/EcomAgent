"""视频拼接工具 - 将多个 MP4 视频按顺序合并成一个"""

try:
    # moviepy 2.x API
    from moviepy import VideoFileClip, concatenate_videoclips
    MOVIEPY_AVAILABLE = True
except ImportError:
    try:
        # moviepy 1.x API (fallback)
        from moviepy.editor import VideoFileClip, concatenate_videoclips
        MOVIEPY_AVAILABLE = True
    except ImportError:
        MOVIEPY_AVAILABLE = False

from pathlib import Path
from typing import List, Union


def merge_vovies(
    video_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    fps: int = 30
) -> dict:
    """
    将多个视频按顺序合并成一个

    Args:
        video_paths: 视频文件路径列表，按顺序拼接
        output_path: 输出视频路径
        fps: 输出视频帧率（默认 30）

    Returns:
        {
            "status": "success" | "error",
            "output_path": str,
            "error": {...}
        }
    """
    if not MOVIEPY_AVAILABLE:
        import sys
        return {
            "status": "error",
            "error": {
                "message": f"moviepy not installed in {sys.executable}. Run: {sys.executable} -m pip install moviepy"
            }
        }

    try:
        # 验证输入
        if not video_paths:
            return {"status": "error", "error": {"message": "No video paths provided"}}

        valid_paths = []
        for vp in video_paths:
            p = Path(vp)
            if p.exists():
                valid_paths.append(str(p.resolve()))
            else:
                return {"status": "error", "error": {"message": f"Video not found: {vp}"}}

        if len(valid_paths) < 1:
            return {"status": "error", "error": {"message": "At least 1 video required"}}

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 加载所有视频片段
        print(f"Loading {len(valid_paths)} videos...")
        clips = []
        for vp in valid_paths:
            print(f"  Loading: {Path(vp).name}")
            clip = VideoFileClip(vp)
            clips.append(clip)

        # 拼接视频
        print("Merging videos...")
        final_clip = concatenate_videoclips(clips, method="compose")

        # 写入输出文件
        print(f"Writing to: {output_path}")
        final_clip.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        # 关闭所有 clips 释放资源
        for clip in clips:
            clip.close()
        final_clip.close()

        return {
            "status": "success",
            "output_path": str(output_path),
            "duration": final_clip.duration
        }

    except Exception as e:
        return {
            "status": "error",
            "error": {"message": str(e)}
        }


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='合并多个视频文件')
    parser.add_argument('videos', nargs='+', help='输入视频文件路径（按顺序）')
    parser.add_argument('-o', '--output', required=True, help='输出视频路径')
    parser.add_argument('--fps', type=int, default=30, help='输出帧率（默认30）')

    args = parser.parse_args()

    result = merge_movies(args.videos, args.output, args.fps)

    if result['status'] == 'success':
        print(f"✓ 视频合并成功: {result['output_path']}")
        print(f"  时长: {result.get('duration', 'unknown')}s")
    else:
        print(f"✗ 视频合并失败: {result['error']['message']}")
        sys.exit(1)
