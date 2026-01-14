import subprocess

def render(scene_file: str, scene_class: str):
    subprocess.run([
        "python", "-m", "manim",
        "-pql", scene_file, scene_class
    ])
