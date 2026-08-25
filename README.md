# Comment Synthesizer

A Python-based Eskom response assistant for generating context-aware customer replies to loadshedding, outage, billing, and power-related messages.

This project includes:
- a desktop Tkinter chat app
- a FastAPI web API
- a browser demo
- a reusable rule-based response engine for Eskom-related comment generation

## Features

- Detects common Eskom customer concerns such as loadshedding, outages, billing, and no-power events
- Normalizes user input and expands keyword variants for real-world phrasing
- Provides helpful fallback responses when the message is vague or unrelated
- Supports desktop, web, and mobile-friendly API access through a shared backend

## Project layout

- `app.py` — desktop GUI entry point
- `comments_generation_wordnet_rulebased.py` — core response and keyword-matching logic
- `api.py` — FastAPI backend for web and mobile integration
- `web_app.html` — browser demo UI
- `web_app_react.html` — alternate browser chat interface
- `mobile_api_example.dart` — example mobile API client
- `test_comments_generation.py` — validation tests
- `research/` — historical analysis scripts kept separate from the app
- `requirements.txt` — Python dependencies
- `desktop_app.spec` — PyInstaller packaging config

## Quick start

### Desktop app

```powershell
cd "C:\Users\pc\Desktop\App Comment Synthesizer"
.\.venv\Scripts\python.exe app.py
```

Or run:

```bat
start_app.bat
```

### Web API

```powershell
cd "C:\Users\pc\Desktop\App Comment Synthesizer"
.\.venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Or run:

```bat
run_web_api.bat
```

Then open `web_app.html` in a browser.

### Windows app build

```powershell
cd "C:\Users\pc\Desktop\App Comment Synthesizer"
.\.venv\Scripts\python.exe -m PyInstaller desktop_app.spec
```

The packaged app is created under the `dist` folder.

## Testing

```powershell
cd "C:\Users\pc\Desktop\App Comment Synthesizer"
.\.venv\Scripts\python.exe -m unittest -q
```

## Example usage

- "there is load shedding in my area"
- "power outage in my area"
- "no electricity"
- "my bill is overdue"

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
