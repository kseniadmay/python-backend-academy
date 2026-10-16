@echo off
chcp 65001 > nul
title Python Backend Academy - Mobile Access Server
echo ========================================================
echo   Python Backend Academy - Launching Mobile Sync Server
echo ========================================================
cd /d "%~dp0"
node scripts\server.js
pause
