def plan_pedagogy(meta: dict) -> str:
    if meta["difficulty"] == "primary":
        return "storytelling, no formulas, visual intuition"
    if meta["subject"] == "physics":
        return "real-life example → animation → simple formula"
    if meta["subject"] == "math":
        return "visual intuition → relation → example"
    return "definition → derivation → example"
