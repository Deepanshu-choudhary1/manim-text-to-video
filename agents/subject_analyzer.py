import json
import re
from llm.ollama import ollama_generate


def _extract_json(text: str) -> dict:
    """
    Extracts the first JSON object from LLM output safely.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in LLM output:\n{text}")
    return json.loads(match.group())


def analyze_topic(topic: str) -> dict:
    prompt = f"""
Return ONLY valid JSON.
No explanation.
No markdown.

JSON format:
{{
  "subject": "math or physics",
  "topic": "{topic}",
  "level": "primary or middle or high or advanced"
}}

Topic: {topic}
"""

    raw = ollama_generate(prompt)
    return _extract_json(raw)
