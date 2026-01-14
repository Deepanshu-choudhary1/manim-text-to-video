from agents.subject_analyzer import analyze_topic
from agents.script_writer import write_script
from agents.scene_director import direct_scenes
from generators.manim_generator import generate_scene
from generators.voice_generator import generate_voice


def validate_scene(scene: dict, idx: int):
    """
    Hard validation to prevent silent / text-only videos.
    """
    if "explanation" not in scene or not scene["explanation"].strip():
        raise RuntimeError(f"❌ Scene {idx}: missing explanation text")

    if "visual_type" not in scene or not scene["visual_type"].strip():
        raise RuntimeError(f"❌ Scene {idx}: missing visual_type")


def main():
    topic = input("Enter topic: ").strip()

    # ---------- ANALYSIS ----------
    print("▶ Analyzing topic...")
    meta = analyze_topic(topic)
    print(f"✔ Analysis result: {meta}")

    # ---------- SCRIPT ----------
    print("▶ Generating teaching script...")
    script = write_script(meta)

    if not script or not script.strip():
        raise RuntimeError("❌ Script generation failed (empty output)")

    print("✔ Script generated")

    # ---------- SCENE DIRECTING ----------
    print("▶ Directing scenes (explanation → visuals)...")
    scenes = direct_scenes(script, meta["subject"])

    if not scenes:
        raise RuntimeError("❌ Scene director produced no scenes")

    print(f"✔ {len(scenes)} explanation-driven scenes created")

    # ---------- GENERATION ----------
    print("▶ Generating visuals and narration...")

    for idx, scene in enumerate(scenes, start=1):
        validate_scene(scene, idx)

        explanation = scene["explanation"].strip()
        visual_type = scene["visual_type"]

        print(f"  • Scene {idx}")
        print(f"    - visual_type: {visual_type}")
        print(f"    - narration length: {len(explanation)} chars")

        # --- Voice (MANDATORY) ---
        generate_voice(
            text=explanation,     # FULL explanation
            scene_id=idx
        )

        # --- Visual (MANDATORY) ---
        generate_scene(
            scene_id=idx,
            scene_data=scene
        )

    print("✅ All scenes generated with visuals + narration")
    print("▶ Next steps:")
    print("  1) python runtime/merge_scenes.py")
    print("  2) python -m manim -pql output/merged/final_video.py FinalEducationalVideo")


if __name__ == "__main__":
    main()
