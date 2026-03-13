@echo off
:: Making sure the script is run from the project root directory
CD ..

echo [1/5] Initializing Git Repository...
git init

echo [2/5] Creating .gitignore...
(
echo __pycache__/
echo *.pyc
echo *.db
echo .env
echo .vscode/
) > .gitignore

echo [3/5] Adding files...
git add .

echo [4/5] Creating initial commit...
git commit -m "Initial commit: Database schema and project structure"

echo [5/5] Setting main branch...
git branch -M main

echo.
echo Repository initialized successfully.
pause