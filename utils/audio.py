from pydub import AudioSegment


def get_audio_duration(audio_path: str) -> float:
    """
    Returns duration in seconds.
    """
    audio = AudioSegment.from_file(audio_path)
    return audio.duration_seconds
