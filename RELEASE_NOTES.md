# Release Notes

## Historical v1.0.0 development baseline

### Highlights
- Added a desktop Tkinter app for generating Eskom-related responses.
- Built a reusable keyword-matching engine for loadshedding, outage, billing, and no-power messages.
- Exposed the logic via a FastAPI backend for web and mobile integration.
- Included browser demos for quick testing and UI validation.
- Added Windows app packaging support with PyInstaller.
- Added automated test coverage for the response logic.

### Included in this release
- Desktop app launcher and Windows build support
- Web API endpoint for browser and mobile clients
- Browser demos for quick interaction
- Example mobile client call pattern
- Documentation and GitHub release polish

### Example response flow
- Input: "there is load shedding in my area"
- Output: a contextual Eskom-style response explaining the current loadshedding status and next steps

### Validation
- Python unit tests pass with the project’s local venv.
- Core logic works in desktop, API, and browser modes.

### Notes
- The v1.0.0 label in this document describes the earlier private development baseline; no Git tag or GitHub Release currently exists for it.
- The backend uses a rule-based system designed for explainability and fast local deployment.
- This version is suitable for local Windows use, web integration, and further extension into broader response intelligence.
