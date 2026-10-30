@echo off
chcp 65001 >nul
rem [1/3] RemNote Platinum 525-file Package and Card Verification (verify_platinum.py)
rem [2/3] Canonical Benchmark and JS Syntax Verification (verify_academy.py)
rem [3/3] 401 IDE tasks and Python snippets tests (test_all_401_tasks.py)

python "%~dp0verify_all.py" %*
if errorlevel 1 goto :fail
goto :end

:fail
echo.
echo ========================================================
echo   [ERROR] Verification FAILED!
echo ========================================================
exit /b 1

:end
exit /b 0
