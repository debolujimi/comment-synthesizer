# App Comment Synthesizer

A small Python project for generating Eskom-related response comments from user messages.

## Project layout

- `app.py` — Tkinter desktop application entry point
- `comments_generation_wordnet_rulebased.py` — reusable Eskom response engine
- `api.py` — FastAPI web API that exposes the engine to browsers and mobile clients
- `web_app.html` — simple browser-based demo UI
- `mobile_api_example.dart` — example mobile API call for Flutter-style clients
- `test_comments_generation.py` — basic validation checks
- `research/` — notebook-style analysis scripts kept separate from the app
- `requirements.txt` — dependencies

## Run the desktop app

From the project folder, you can start it with either of these options:

```bash
python app.py
```

On Windows, you can also use the launcher:

```bat
start_app.bat
```

## Run the web API

```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Or use:

```bat
run_web_api.bat
```

Then open `web_app.html` in the browser.

## Run tests

```bash
python -m unittest -q
```

## Typical usage

- Type a message such as "there is load shedding in my area"
- The engine matches the intent and returns a helpful Eskom-style response
- Use the Clear button to reset the chat window
- The same logic can be reused by the web API and mobile clients
