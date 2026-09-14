#!/usr/bin/env python3
"""Create a video from the Gazebo camera frames saved in ``/tmp/camera_save``."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
from typing import Optional


class VideoFeatures:
    """Utility for converting saved Gazebo camera JPEGs into a video."""

    def __init__(self, frame_directory: str = "/tmp/camera_save") -> None:
        self.frame_directory = Path(frame_directory)

    def get_current_frame_file(self) -> Optional[str]:
        """Return the most recently named frame file, or ``None`` if there is none."""
        frames = [frame for frame in self.frame_directory.iterdir() if frame.is_file()]
        return max(frames).name if frames else None

    def saveVideo(
        self,
        path: str,
        start_file: Optional[str] = None,
        filename: str = "record",
        format: str = "mkv",
        fps: int = 60,
        speedUpDown: float = 1.0,
        remove_jpg: bool = False,
    ) -> Path:
        """Save camera frames as a video and optionally change its playback speed.

        ``speedUpDown > 1`` speeds the video up, while values between zero and one
        slow it down.
        """
        if fps <= 0:
            raise ValueError("fps must be greater than zero")
        if speedUpDown <= 0:
            raise ValueError("speedUpDown must be greater than zero")
        if not self.frame_directory.is_dir():
            raise FileNotFoundError(f"Frame directory does not exist: {self.frame_directory}")

        frames = sorted(self.frame_directory.glob("default_camera_link_my_camera*.jpg"))
        if start_file is not None:
            frames = [frame for frame in frames if frame.name >= start_file]
        if not frames:
            raise FileNotFoundError("No matching camera JPEG frames were found")

        output_directory = Path(path)
        output_directory.mkdir(parents=True, exist_ok=True)
        stem = Path(filename).stem
        video_path = output_directory / f"{stem}.{format}"

        # ffmpeg's glob input preserves the same camera-frame convention used by
        # ExtendedLandingManager, without deleting frames before encoding.
        subprocess.run(
            [
                "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-framerate", str(fps),
                "-pattern_type", "glob", "-i",
                str(self.frame_directory / "default_camera_link_my_camera*.jpg"),
                "-c:v", "libx264", str(video_path),
            ],
            check=True,
        )

        result_path = video_path
        if speedUpDown != 1:
            suffix = str(speedUpDown).replace(".", "")
            result_path = output_directory / f"{stem}{suffix}x.{format}"
            subprocess.run(
                [
                    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(video_path),
                    "-filter:v", f"setpts={1 / speedUpDown}*PTS", str(result_path),
                ],
                check=True,
            )

        if remove_jpg:
            for frame in frames:
                frame.unlink()

        print(f"Video saved: {result_path}")
        return result_path


if __name__ == "__main__":

    #python3 videofeatures.py /path/to/output --fps 60 --speed 2
    parser = argparse.ArgumentParser(description="Convert Gazebo camera JPEG frames into a video.")
    parser.add_argument("output_directory", help="Directory in which to save the video")
    parser.add_argument("--frames", default="/tmp/camera_save", help="Directory containing camera JPEG frames")
    parser.add_argument("--filename", default="record", help="Output filename, without the extension")
    parser.add_argument("--format", default="mkv", help="Output container format (default: mkv)")
    parser.add_argument("--fps", type=int, default=60, help="Frames per second (default: 60)")
    parser.add_argument("--speed", type=float, default=1.0, help="Playback multiplier; 2 is twice as fast")
    parser.add_argument("--start-file", help="Ignore frames alphabetically before this file")
    parser.add_argument("--remove-jpg", action="store_true", help="Remove encoded frames after success")
    args = parser.parse_args()

    VideoFeatures(args.frames).saveVideo(
        args.output_directory,
        start_file=args.start_file,
        filename=args.filename,
        format=args.format,
        fps=args.fps,
        speedUpDown=args.speed,
        remove_jpg=args.remove_jpg,
    )
