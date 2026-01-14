from pathlib import Path
import re

SCENES_DIR = Path("output/scenes")
AUDIO_DIR = Path("output/audio")
MERGED_DIR = Path("output/merged")
MERGED_FILE = MERGED_DIR / "final_video.py"


def extract_construct_body(scene_code: str) -> str:
    """
    Extracts code inside construct() method.
    """
    match = re.search(
        r"def construct\(self\):([\s\S]*)",
        scene_code
    )
    if not match:
        raise ValueError("No construct() found in scene file")

    body = match.group(1)

    # indent properly for merged file
    return "\n".join("        " + line for line in body.splitlines())


def merge_scenes():
    MERGED_DIR.mkdir(parents=True, exist_ok=True)

    scene_files = sorted(SCENES_DIR.glob("scene_*.py"))
    if not scene_files:
        raise RuntimeError("No scene files found")

    methods = []

    for idx, scene_file in enumerate(scene_files, start=1):
        code = scene_file.read_text(encoding="utf-8")
        body = extract_construct_body(code)

        audio_path = AUDIO_DIR / f"scene_{idx}.wav"

        method = f"""
    def play_scene_{idx}(self):
{body}
        self.wait(0.5)
"""
        methods.append(method)

    final_code = f"""
from manim import *

class FinalEducationalVideo(Scene):
{''.join(methods)}

    def construct(self):
"""

    for i in range(1, len(methods) + 1):
        final_code += f"        self.play_scene_{i}()\n"

    MERGED_FILE.write_text(final_code.strip(), encoding="utf-8")

    print(f"✅ Merged video file created at: {MERGED_FILE}")


if __name__ == "__main__":
    merge_scenes()
