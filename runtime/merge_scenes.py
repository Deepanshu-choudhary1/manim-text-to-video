from pathlib import Path

SCENES_DIR = Path("output/scenes")
MERGED_DIR = Path("output/merged")
MERGED_FILE = MERGED_DIR / "final_video.py"


def extract_construct_body(lines):
    """
    Extract construct() body safely and return
    lines WITHOUT leading indentation.
    """
    inside = False
    body = []
    base_indent = None

    for line in lines:
        if line.lstrip().startswith("def construct"):
            inside = True
            base_indent = len(line) - len(line.lstrip())
            continue

        if inside:
            if line.strip() == "":
                body.append("")
                continue

            indent = len(line) - len(line.lstrip())
            if indent <= base_indent:
                break

            body.append(line[base_indent + 4 :])

    if not body:
        raise ValueError("construct() body not found")

    return body


def merge_scenes():
    MERGED_DIR.mkdir(parents=True, exist_ok=True)

    scene_files = sorted(SCENES_DIR.glob("scene_*.py"))
    if not scene_files:
        raise RuntimeError("No scene files found")

    merged_lines = [
        "from manim import *",
        "import numpy as np",
        "from pydub import AudioSegment",
        "",
        "def get_audio_duration(path: str) -> float:",
        "    audio = AudioSegment.from_file(path)",
        "    return audio.duration_seconds",
        "",
        "",
        "class FinalEducationalVideo(Scene):",
        "",
    ]

    # -------------------------------
    # Per-scene methods
    # -------------------------------
    for idx, scene_file in enumerate(scene_files, start=1):
        lines = scene_file.read_text(encoding="utf-8").splitlines()
        body = extract_construct_body(lines)

        merged_lines.append(f"    def play_scene_{idx}(self):")

        for line in body:
            merged_lines.append(f"        {line}")

        # Safety cleanup (always)
        merged_lines.append("        self.clear()")
        merged_lines.append("        self.wait(0.2)")
        merged_lines.append("")

    # -------------------------------
    # Main construct
    # -------------------------------
    merged_lines.append("    def construct(self):")
    for idx in range(1, len(scene_files) + 1):
        merged_lines.append(f"        self.play_scene_{idx}()")

    MERGED_FILE.write_text("\n".join(merged_lines), encoding="utf-8")
    print(f"✅ Merged video file created at: {MERGED_FILE}")


if __name__ == "__main__":
    merge_scenes()
