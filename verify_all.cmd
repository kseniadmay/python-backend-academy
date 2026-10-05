@echo off
chcp 65001 >nul
rem [1/5] RemNote Platinum 525-file Package and Card Verification (verify_platinum.py)
rem [2/5] E2E DOM and Invariant tests (test_e2e_dom.js)
rem [3/5] PWA Offline, Manifest and Service Worker Verification (test_pwa_offline.js)
rem [4/5] Headless Chrome and JS syntax verification (verify_academy.py)
rem [5/5] 401 IDE tasks and Python snippets tests (test_all_401_tasks.py)

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
