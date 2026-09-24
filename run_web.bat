@echo off
cd /d "%~dp0web"
start "StudyPlanAnalyzer Web Server" /b cmd /c "python -m http.server 8765"
timeout /t 1 /nobreak >nul
start "" "http://127.0.0.1:8765"
