@echo off
chcp 65001 >nul
echo [1/4] Running RemNote Platinum 525-file Package and Card Verification...
python "%~dp0scripts\verify_platinum.py"
if errorlevel 1 goto :fail

echo.
echo [2/4] Running E2E DOM and Invariant tests...
node "%~dp0scripts\test_e2e_dom.js"
if errorlevel 1 goto :fail

echo.
echo [3/4] Running Headless Chrome and JS syntax verification...
python "%~dp0scripts\verify_academy.py"
if errorlevel 1 goto :fail

echo.
echo [4/4] Running 401 IDE tasks and Python snippets tests...
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
