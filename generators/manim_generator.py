from pathlib import Path
import textwrap

SCENE_DIR = Path("output/scenes")

# 🔒 Engine-approved visual types
VISUAL_LIBRARY = {
    "wave_basic",
    "wave_amplitude",
    "wave_wavelength",
    "pythagoras_triangle",
    "flow_pressure",
    "graph_quadratic",
}


def generate_scene(scene_id: int, scene_data: dict):
    """
    Generate a Manim scene that ALWAYS:
    - shows visuals
    - plays narration audio
    - cleans up after itself
    """

    visual_type = scene_data.get("visual_type")
    explanation = scene_data.get("explanation", "").strip()

    if not explanation:
        raise RuntimeError(f"❌ Scene {scene_id}: explanation missing")

    if visual_type not in VISUAL_LIBRARY:
        raise RuntimeError(
            f"❌ Scene {scene_id}: invalid visual_type '{visual_type}'"
        )

    audio_path = f"output/audio/scene_{scene_id}.wav"

    code = build_scene(scene_id, visual_type, explanation, audio_path)

    SCENE_DIR.mkdir(parents=True, exist_ok=True)
    scene_file = SCENE_DIR / f"scene_{scene_id}.py"
    scene_file.write_text(textwrap.dedent(code), encoding="utf-8")


# =========================================================
# UNIVERSAL SCENE BUILDER (NO TEXT-ONLY POSSIBLE)
# =========================================================

def build_scene(scene_id, visual_type, explanation, audio):
    visual_block = VISUAL_BLOCKS[visual_type]()

    return f"""
from manim import *
import numpy as np
from pydub import AudioSegment


def get_audio_duration(path):
    return AudioSegment.from_file(path).duration_seconds


class Scene{scene_id}(Scene):
    def construct(self):
        visuals = VGroup()

{visual_block}

        caption = Text(
            "{explanation}",
            font_size=28,
            line_spacing=1.2
        ).to_edge(DOWN)

        # --- Animate visuals ---
        self.play(*[Create(v) for v in visuals])
        self.play(FadeIn(caption))

        # --- Audio narration ---
        self.add_sound("{audio}")
        self.wait(get_audio_duration("{audio}") + 0.3)

        # --- Cleanup ---
        self.play(FadeOut(caption), FadeOut(visuals))
        self.wait(0.2)
"""


# =========================================================
# VISUAL PRIMITIVES (REAL VISUALS, NOT TEXT)
# =========================================================

def wave_basic():
    return """
        axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4
        )
        wave = axes.plot(lambda x: np.sin(x), color=BLUE)
        visuals.add(axes, wave)
"""


def wave_amplitude():
    return """
        axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1]
        )
        wave = axes.plot(lambda x: np.sin(x), color=BLUE)
        amp = DoubleArrow(ORIGIN, UP*2, color=YELLOW)
        visuals.add(axes, wave, amp)
"""


def wave_wavelength():
    return """
        axes = Axes(
            x_range=[0, 4*PI, PI],
            y_range=[-2, 2, 1]
        )
        wave = axes.plot(lambda x: np.sin(x), color=BLUE)
        brace = Brace(Line(ORIGIN, RIGHT*PI), DOWN)
        visuals.add(axes, wave, brace)
"""


def pythagoras_triangle():
    return """
        A = LEFT*3 + DOWN
        B = RIGHT*2 + DOWN
        C = LEFT*3 + UP*2

        triangle = Polygon(A, B, C, color=BLUE)

        a = MathTex("a").next_to(Line(B, C), RIGHT)
        b = MathTex("b").next_to(Line(A, C), LEFT)
        c = MathTex("c").next_to(Line(A, B), DOWN)

        visuals.add(triangle, a, b, c)
"""


def flow_pressure():
    return """
        container = Rectangle(height=4, width=2)
        arrows = VGroup(
            *[Arrow(UP, DOWN, buff=0.1) for _ in range(5)]
        ).arrange(DOWN)

        arrows.next_to(container, RIGHT)
        visuals.add(container, arrows)
"""


def graph_quadratic():
    return """
        axes = Axes(x_range=[-5, 5, 1], y_range=[-5, 5, 1])
        graph = axes.plot(lambda x: x**2, color=GREEN)
        visuals.add(axes, graph)
"""


VISUAL_BLOCKS = {
    "wave_basic": wave_basic,
    "wave_amplitude": wave_amplitude,
    "wave_wavelength": wave_wavelength,
    "pythagoras_triangle": pythagoras_triangle,
    "flow_pressure": flow_pressure,
    "graph_quadratic": graph_quadratic,
}
