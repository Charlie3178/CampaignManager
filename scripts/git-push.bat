@echo off
:: Making sure the script is run from the project root directory
CD ..

set /p commit_msg="Enter commit comment: "

:: Check if the user actually entered a message
if "%commit_msg%"=="" (
    echo Error: You must enter a commit message!
    pause
    exit /b
)

echo.
echo [Staging changes...]
git add .

echo [Committing with message: %commit_msg%]
git commit -m "%commit_msg%"

echo.
echo [Pushing to GitHub...]
git push origin main

echo.
echo [Done!]
pause