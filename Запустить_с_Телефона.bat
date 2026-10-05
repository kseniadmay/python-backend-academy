@echo off
chcp 65001 > nul
title Python Backend Academy - Доступ с Телефона
echo ========================================================
echo    Запуск сервера Python Backend Academy...
echo ========================================================
cd /d "%~dp0"
node scripts\server.js
pause
