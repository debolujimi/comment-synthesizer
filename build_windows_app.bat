@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" -m pip install pyinstaller
".venv\Scripts\python.exe" -m PyInstaller --clean --noconsole --onefile --name AppCommentSynthesizer desktop_app.spec
if exist dist\AppCommentSynthesizer.exe (
    echo Build complete: dist\AppCommentSynthesizer.exe
) else (
    echo Build failed. Check the output above.
    exit /b 1
)
