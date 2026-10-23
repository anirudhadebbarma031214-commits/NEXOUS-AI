@echo off
title NEXOUS AI - Local Brain
cd /d "%~dp0"
echo.
echo  NEXOUS AI - LOCAL BRAIN SETUP
echo  This runs an AI model on your PC; it is not a cloud API.
echo.

where ollama >nul 2>nul
if errorlevel 1 (
  echo Ollama is not installed yet.
  echo Please install Ollama for Windows from https://ollama.com/download
  echo Then double-click this file again.
  pause
  exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  echo Install Python 3 from https://www.python.org/downloads/windows/
  echo During installation, select "Add python.exe to PATH".
  pause
  exit /b 1
)

if exist "D:\\" (
  set "OLLAMA_MODELS=D:\\NEXOUS-AI-Models"
  if not exist "D:\\NEXOUS-AI-Models" mkdir "D:\\NEXOUS-AI-Models"
  echo Model files will be stored on D: to avoid filling the Windows drive.
) else (
  echo WARNING: D: drive not found. Ollama may store model files on C:.
  echo Make sure C: has several GB free before continuing.
)
echo.
echo Starting Ollama with the selected model folder...
taskkill /IM ollama.exe /F >nul 2>nul
start "NEXOUS Ollama" /min cmd /c "set OLLAMA_MODELS=%OLLAMA_MODELS% && ollama serve"
timeout /t 8 /nobreak >nul
echo.
echo Checking/downloading the Qwen 2.5 3B model.
echo The download needs several GB of free disk space and may take time.
ollama pull qwen2.5:3b
if errorlevel 1 (
  echo Model download failed. Check your internet connection and free disk space.
  pause
  exit /b 1
)
echo.
echo Starting the NEXOUS local website.
echo Keep this window open while using NEXOUS.
echo Your browser will open at http://127.0.0.1:8765
start "" "http://127.0.0.1:8765"
python server.py
pause
