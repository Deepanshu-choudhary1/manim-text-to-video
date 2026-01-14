def split_scenes(script: str):
    blocks = [b.strip() for b in script.split("\n\n") if b.strip()]
    return [
        {"id": i + 1, "text": block}
        for i, block in enumerate(blocks)
    ]
