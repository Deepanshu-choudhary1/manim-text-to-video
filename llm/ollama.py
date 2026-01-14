import subprocess
import time
from config import MODEL_NAME


def ollama_generate(prompt: str, timeout: int = 120, retries: int = 2):
    """
    Production-safe Ollama wrapper.
    - timeout: seconds (default 120)
    - retries: retry on timeout
    """

    for attempt in range(retries + 1):
        try:
            print(f"🧠 Ollama thinking... (attempt {attempt + 1})", flush=True)

            result = subprocess.run(
                ["ollama", "run", MODEL_NAME],
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout
            )

            if result.returncode != 0:
                raise RuntimeError(result.stderr)

            output = result.stdout.strip()
            if not output:
                raise RuntimeError("❌ Ollama returned empty output")

            print("✅ Ollama response received\n", flush=True)
            return output

        except subprocess.TimeoutExpired:
            if attempt == retries:
                raise RuntimeError(f"❌ Ollama timed out after {timeout}s")
            print("⚠️ Timeout, retrying...", flush=True)
            time.sleep(3)
