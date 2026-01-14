from llm.ollama import ollama_generate

def write_script(meta: dict) -> str:
    prompt = f"""
You are a professional teacher.

Subject: {meta['subject']}
Topic: {meta['topic']}
Level: {meta['level']}

Rules:
- Simple language for young students
- Build intuition before formulas
- Use step-by-step explanation
- Scene based narration

Return plain text.
"""
    return ollama_generate(prompt)
