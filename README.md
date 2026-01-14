
# Manim-text-to-video

Generate **complete educational videos** from a text topic using **Manim** and **local Large Language Models (LLMs)**.
This project converts a topic (e.g. *waves*, *Pythagoras theorem*, *fluid mechanics*) into a **fully narrated, visually explained video**, rendered locally with Manim.


---

## Features

* **Text → Educational Video**
  Enter a topic and generate a full explainer video.

* **Scene-wise Explanation**
  Each concept is broken into scenes with:

  * explanation text
  * visuals
  * voice narration

* **Guaranteed Visuals**
  The engine enforces real visuals (graphs, waves, triangles, flows).
  No text-only or silent scenes are allowed.

* **Local LLM Support**
  Uses **Ollama** to run LLMs locally (no API keys, no cost).

* **Audio-Synced Animations**
  Scene duration automatically matches narration length.

* **Manim Rendering**
  Videos are rendered using **Manim Community Edition**.

---

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.10+**
* **Manim**
  Follow the official guide:
  [https://docs.manim.community/en/stable/installation.html](https://docs.manim.community/en/stable/installation.html)
* **FFmpeg** (required for audio)
* **LaTeX (MiKTeX recommended on Windows)**
  Required for MathTex rendering.
* **Ollama**
  Download from: [https://ollama.com/](https://ollama.com/)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Deepanshu-choudhary1/manim-text-to-video.git
cd manim-text-to-video
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull a local LLM model

Example (recommended):

```bash
ollama pull qwen2.5-coder
```

You can use any Ollama-supported model.

---

## Usage

### 1. Generate scenes and narration

```bash
python main.py
```

Enter a topic when prompted, for example:

```
waves
```

or

```
pythagoras theorem
```

This step:

* analyzes the topic
* writes an explanation script
* plans scenes
* generates narration audio
* generates Manim scene files

---

### 2. Merge scenes into one video

```bash
python runtime/merge_scenes.py
```

This creates:

```
output/merged/final_video.py
```

---

### 3. Render the final video

```bash
python -m manim -pql output/merged/final_video.py FinalEducationalVideo
```

The rendered video will appear in:

```
media/videos/
```

---

## Project Structure

```
manim-text-to-video/
│
├── main.py                    # Entry point
│
├── agents/
│   ├── subject_analyzer.py    # Detects subject & level
│   ├── script_writer.py       # Generates teaching script
│   └── scene_director.py      # Converts script → scene plan
│
├── generators/
│   ├── manim_generator.py     # Enforced visuals + audio
│   └── voice_generator.py     # Scene-wise TTS
│
├── runtime/
│   └── merge_scenes.py        # Merges scenes into one video
│
├── llm/
│   └── ollama.py              # Local LLM wrapper
│
├── output/
│   ├── scenes/                # Generated Manim scenes
│   ├── audio/                 # Scene narration (.wav)
│   └── merged/                # Final Manim file
│
├── requirements.txt
└── README.md
```

---

## Visual System

The engine uses a **fixed visual library** to ensure real animations:

Examples:

* Waves (basic, amplitude, wavelength)
* Graphs (quadratic curves)
* Geometry (Pythagoras triangle)
* Physics flows (pressure, direction arrows)

If a scene does not map to a valid visual type, the program **stops with an error**.
This prevents broken or misleading videos.

---

## Contributing

Contributions are welcome.

If you want to:

* add new visual types
* improve animations
* expand subject coverage

Feel free to open a Pull Request.

---

## License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.

---

## Acknowledgments

* **Manim Community** – [https://www.manim.community/](https://www.manim.community/)
* **Ollama** – [https://ollama.com/](https://ollama.com/)
* **Grant Sanderson (3Blue1Brown)** for creating Manim

---

### Note

Generated videos and intermediate files are intentionally excluded from version control.
Run the pipeline locally to generate outputs.

