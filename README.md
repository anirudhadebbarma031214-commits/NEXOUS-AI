# NEXOUS AI

**Your Voice. Your Intelligence.**

NEXOUS AI is a personal AI assistant project. The GitHub Pages site is the visual interface; the optional local mode connects it to an actual language model running on your Windows PC.

## What works now

- Cyber-blue responsive chat and voice interface
- Browser speech input where supported and built-in speech output
- **Local AI mode:** Python server forwards prompts to Ollama running on the same PC
- Default model: `qwen2.5:3b` (downloaded by Ollama; no paid API key)
- Local server binds only to `127.0.0.1`, so it is not exposed to the public network
- No Python packages required for the bridge (Python standard library only)

## Run the real local AI brain on Windows

1. Make sure you have several GB of free disk space. The model download can take a while.
2. Install **Ollama for Windows** from https://ollama.com/download
3. Install **Python 3** from https://www.python.org/downloads/windows/ if it is not already installed. During setup, enable **Add Python to PATH**.
4. In this GitHub repository, click the green **Code** button → **Download ZIP**, then extract the ZIP.
5. Open the extracted folder and double-click **START-NEXOUS-LOCAL.bat**.
6. The launcher downloads `qwen2.5:3b` (first run only), starts the local server, and opens http://127.0.0.1:8765.
7. Keep the black launcher window open while using the local AI website.

If Windows asks whether Python can access a network, the server is designed to listen only on this PC (`127.0.0.1`). Do not change it to listen on all network interfaces.

## GitHub Pages versus local AI

GitHub Pages only serves static website files. It cannot run Python or keep Ollama running. The public Pages site therefore remains a browser-only prototype; use the local launcher above for actual model-generated replies. Do not put private keys or personal voice recordings into public repository files.

## What this is—and isn't

The Qwen model is an existing pretrained open model, not a model trained from scratch by NEXOUS. This is the practical first step toward a real brain without paid API usage. Building original model weights from scratch is a separate, much larger research project that requires training data, compute, and substantial time. The local model uses your PC's resources and may respond slowly on modest hardware.

Voice input and voice output use browser features. This version does **not** clone a voice. Any future voice cloning should use a voice you own or have explicit permission to use.

## Project files

- `index.html` — web UI
- `server.py` — local web server and Ollama bridge
- `START-NEXOUS-LOCAL.bat` — Windows launcher and first-time model download
- `.github/workflows/pages.yml` — GitHub Pages deployment
