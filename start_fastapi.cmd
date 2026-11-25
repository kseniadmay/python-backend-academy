@echo off
chcp 65001 > nul
title Python Backend Academy - FastAPI Core Server
echo ========================================================
echo   Python Backend Academy - Launching FastAPI Core Server
echo ========================================================
cd /d "%~dp0"
python -m backend.run
pause
