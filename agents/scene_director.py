from llm.ollama import ollama_generate
import json
import re


# 🔒 ALLOWED VISUAL TYPES (ENGINE CONTRACT)
ALLOWED_VISUAL_TYPES = {
    "wave_basic",
    "wave_amplitude",
    "wave_wavelength",
    "pythagoras_triangle",
    "flow_pressure",
    "graph_quadratic",
}


def extract_json_array(text: str):
    """
    Extract FIRST valid JSON array from LLM output.
    """
    match = re.search(r"\[\s*{[\s\S]*?}\s*\]", text)
    if not match:
        raise ValueError(
            f"❌ No valid JSON array found in LLM output:\n{text}"
        )

    try:
        return json.loads(match.group())
    except json.JSONDecodeError as e:
        raise ValueError(
            f"❌ Invalid JSON returned by LLM:\n{match.group()}"
        ) from e


def chunk_script(script: str, max_chars=1000):
    """
    Break long scripts into manageable chunks.
    """
    chunks = []
    current = ""

    for paragraph in script.split("\n\n"):
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) > max_chars:
            chunks.append(current)
            current = paragraph
        else:
            current += "\n\n" + paragraph if current else paragraph

    if current.strip():
        chunks.append(current)

    return chunks


def validate_scene(scene: dict, index: int):
    """
    Enforce scene contract strictly.
    """
    if "explanation" not in scene or not scene["explanation"].strip():
        raise RuntimeError(
            f"❌ Scene {index}: missing explanation"
        )

    if "visual_type" not in scene:
        raise RuntimeError(
            f"❌ Scene {index}: missing visual_type"
        )

    if scene["visual_type"] not in ALLOWED_VISUAL_TYPES:
        raise RuntimeError(
            f"❌ Scene {index}: invalid visual_type "
            f"'{scene['visual_type']}'.\n"
            f"Allowed: {sorted(ALLOWED_VISUAL_TYPES)}"
        )


def direct_scenes(script: str, subject: str):
    """
    Convert teaching script → validated scene plan.
    """
    chunks = chunk_script(script)
    all_scenes = []

    for chunk_index, chunk in enumerate(chunks, start=1):
        prompt = f"""
You are a professional educational video director.

Subject: {subject}

Your task:
Split the lesson into scenes.

For EACH scene output a JSON object with:
- explanation: string (what is explained)
- visual_type: ONE of the following ONLY:
  {sorted(ALLOWED_VISUAL_TYPES)}

STRICT RULES (MANDATORY):
- Output ONLY a JSON array
- No text outside JSON
- No markdown
- No explanations
- visual_type MUST be from the list

Lesson part:
{chunk}
"""

        raw = ollama_generate(prompt, timeout=300, retries=1)
        scenes = extract_json_array(raw)

        if not isinstance(scenes, list):
            raise RuntimeError("❌ LLM did not return a list of scenes")

        for i, scene in enumerate(scenes, start=1):
            validate_scene(scene, len(all_scenes) + 1)
            all_scenes.append(scene)

    if not all_scenes:
        raise RuntimeError("❌ Scene director produced zero valid scenes")

    return all_scenes
