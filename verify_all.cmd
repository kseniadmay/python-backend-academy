@echo off
chcp 65001 >nul
echo [1/3] Running E2E DOM tests...
node "%~dp0scripts\test_e2e_dom.js"
if errorlevel 1 goto :fail

echo.
echo [2/3] Running Headless Chrome and JS syntax verification...
python "%~dp0scripts\verify_academy.py"
if errorlevel 1 goto :fail

echo.
echo [3/3] Running 401 IDE tasks and Python snippets tests...
python "%~dp0scripts\test_all_401_tasks.py"
if errorlevel 1 goto :fail

echo.
echo ========================================================
echo   All verifications passed successfully! (100%% PASS)
echo ========================================================
goto :end

:fail
echo.
echo ========================================================
echo   [ERROR] Verification FAILED!
echo ========================================================
exit /b 1

:end
