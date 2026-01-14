import pyttsx3
from pathlib import Path
from config import AUDIO_DIR


def generate_voice(text: str, scene_id: int):
    """
    Production-safe voice generation.
    Creates a fresh engine per call to avoid deadlocks.
    """

    Path(AUDIO_DIR).mkdir(parents=True, exist_ok=True)
    output_path = f"{AUDIO_DIR}/scene_{scene_id}.wav"

    engine = pyttsx3.init()
    engine.setProperty("rate", 150)

    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()
