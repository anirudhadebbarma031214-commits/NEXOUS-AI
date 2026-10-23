#!/usr/bin/env python3
"""NEXOUS AI local bridge: serves the web UI and talks to Ollama on this PC."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import os

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8765
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = os.environ.get("NEXOUS_MODEL", "qwen2.5:3b")
SYSTEM_PROMPT = (
    "You are NEXOUS AI, a helpful personal assistant. Be clear, honest, friendly, "
    "and concise. The user may be a beginner. Never claim you performed an action "
    "you did not perform. If unsure, say so. You are running locally through Ollama."
)

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print("[NEXOUS] " + (fmt % args))

    def _json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/health":
            try:
                with urlopen("http://127.0.0.1:11434/api/tags", timeout=3) as r:
                    tags = json.loads(r.read().decode("utf-8"))
                names = [m.get("name", "") for m in tags.get("models", [])]
                ready = any(n == MODEL or n.startswith(MODEL + ":") for n in names)
                self._json(200, {"ok": True, "ollama": True, "model": MODEL, "model_available": ready})
            except Exception:
                self._json(503, {"ok": False, "ollama": False, "model": MODEL, "model_available": False})
            return
        if self.path == "/":
            self.path = "/index.html"
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/chat":
            self._json(404, {"error": "Unknown endpoint"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 2 or length > 20000:
                self._json(400, {"error": "Message must be between 1 and 20,000 bytes."})
                return
            body = json.loads(self.rfile.read(length).decode("utf-8"))
            message = str(body.get("message", "")).strip()
            if not message:
                self._json(400, {"error": "Please enter a message."})
                return
            if len(message) > 4000:
                self._json(400, {"error": "Please keep each message under 4,000 characters."})
                return
            payload = {
                "model": MODEL,
                "stream": False,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                "options": {"temperature": 0.7, "num_ctx": 4096}
            }
            req = Request(OLLAMA_URL, data=json.dumps(payload).encode("utf-8"),
                          headers={"Content-Type": "application/json"}, method="POST")
            with urlopen(req, timeout=180) as response:
                result = json.loads(response.read().decode("utf-8"))
            reply = result.get("message", {}).get("content", "").strip()
            if not reply:
                self._json(502, {"error": "The model returned an empty reply."})
                return
            self._json(200, {"reply": reply, "model": MODEL, "local": True})
        except HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            self._json(502, {"error": "Ollama error: " + detail})
        except URLError:
            self._json(503, {"error": "Ollama is not running. Start Ollama and try again."})
        except (ValueError, UnicodeDecodeError):
            self._json(400, {"error": "Invalid request."})
        except TimeoutError:
            self._json(504, {"error": "The model took too long. Try a shorter message."})
        except Exception as e:
            self._json(500, {"error": "Local AI error: " + str(e)[:300]})

if __name__ == "__main__":
    print("NEXOUS AI local brain")
    print("Open http://127.0.0.1:%s in your browser." % PORT)
    print("Model:", MODEL)
    print("This server accepts connections only from this PC.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
