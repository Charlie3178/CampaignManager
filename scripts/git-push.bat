@echo off
:: Navigate to project root
CD ..

echo ========================================
echo   CAMPAIGN MANAGER DEPLOYMENT TOOL
echo ========================================

:: 1. FORCE VERSION INPUT
set /p VERSION="Enter Release Version (e.g., 1.1.1): "
if "%VERSION%"=="" (
    echo [ERROR] Version cannot be blank. Deployment aborted.
    pause
    exit /b
)

:: 2. FORCE COMMIT MESSAGE INPUT
set /p MSG="Enter Release Notes/Commit Message: "
if "%MSG%"=="" (
    echo [ERROR] Commit message cannot be blank. Deployment aborted.
    pause
    exit /b
)

echo.
echo Proceeding with Release v%VERSION%...
echo Message: %MSG%
echo ----------------------------------------

:: 3. CLEANUP
echo [1/5] Evicting rogue agents (desktop.ini/pycache)...
del /s /q /f /a:h desktop.ini >nul 2>&1
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

:: 4. BUILD
echo [2/5] Building Executable for v%VERSION%...
pyinstaller --noconfirm --onefile --add-data "data;data" --add-data "scripts;scripts" --add-data "utils;utils" --name "Campaign Manager" app.py

:: 5. GIT STAGING & COMMIT
echo [3/5] Staging and Committing...
git add .
git commit -m "v%VERSION%: %MSG%"

:: 6. TAGGING
echo [4/5] Creating Legislative Tag v%VERSION%...
git tag -a v%VERSION% -m "%MSG%"

:: 7. PUSH
echo [5/5] Pushing to GitHub (Main + Tags)...
git push origin main --tags

echo.
echo ========================================
echo   SHIP COMPLETE: v%VERSION% is Live.
echo ========================================
pause