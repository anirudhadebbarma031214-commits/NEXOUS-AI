# NEXOUS AI

**Your Voice. Your Intelligence.**

NEXOUS AI is an early, browser-based voice assistant prototype designed as a starting point for a personal AI project.

## Current features
- Responsive dark cyber-blue interface
- Browser speech recognition where supported
- Browser text-to-speech
- Text chat with simple local starter responses
- No API key or account required

## Important: current limitations
This first build is **not yet a trained AI model** and does not clone a person's voice. Its replies use simple built-in rules. Browser speech features vary by browser/device, and speech recognition may send audio to the browser provider depending on implementation.

## Run it
Open `index.html` in a current browser, or enable GitHub Pages for this repository (Settings → Pages → Deploy from a branch → `main` → `/(root)`).

## Roadmap
1. Publish the web prototype with GitHub Pages.
2. Connect a real language model through a small server-side backend (never put private API keys in browser code).
3. Add local/offline model support where hardware allows.
4. Research consent-based voice cloning using a voice sample you own and have permission to use.
5. Explore training a small model from scratch as a separate research project.

GitHub Pages hosts static files; it does not train or run a large AI model by itself.
