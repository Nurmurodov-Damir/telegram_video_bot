@echo off
REM Telegram Video Bot - Automatic Deployment Script
REM This script automatically deploys the bot to a Git repository

echo ==================================================
echo Telegram Video Bot - Automatic Deployment
echo ==================================================

REM Check if Git is installed
echo Checking if Git is installed...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed. Please install Git first.
    pause
    exit /b 1
)

echo Git is installed.

REM Check if we're in a Git repository
echo Checking if this is a Git repository...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo Initializing Git repository...
    git init
    if %errorlevel% neq 0 (
        echo Error: Failed to initialize Git repository.
        pause
        exit /b 1
    )
)

REM Add all files
echo Adding all files to Git...
git add .
if %errorlevel% neq 0 (
    echo Error: Failed to add files to Git.
    pause
    exit /b 1
)

REM Create commit with timestamp
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"

echo Creating commit...
git commit -m "Auto-deploy: %timestamp%"
if %errorlevel% neq 0 (
    echo No changes to commit or commit failed.
)

REM Check if remote repository is set
echo Checking for remote repository...
git remote -v | findstr "origin" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo No remote repository found. Please set up your remote repository:
    echo 1. Create a new repository on GitHub/GitLab
    echo 2. Copy the repository URL
    echo 3. Run the following command with your repository URL:
    echo    git remote add origin YOUR_REPOSITORY_URL
    echo.
    echo Example for GitHub:
    echo    git remote add origin https://github.com/yourusername/telegram-video-bot.git
    echo.
    echo Example for GitLab:
    echo    git remote add origin https://gitlab.com/yourusername/telegram-video-bot.git
    echo.
    echo After setting up the remote repository, run this script again.
    pause
    exit /b 1
)

REM Pull latest changes
echo Pulling latest changes from remote repository...
git pull origin main
if %errorlevel% neq 0 (
    echo Warning: Failed to pull from remote repository. Continuing with push...
)

REM Push to remote repository
echo Pushing to remote repository...
git push -u origin main
if %errorlevel% neq 0 (
    echo Error: Failed to push to remote repository.
    echo Please check your internet connection and repository permissions.
    pause
    exit /b 1
)

echo.
echo ==================================================
echo Deployment completed successfully!
echo ==================================================
echo Your Telegram Video Bot has been deployed to the remote repository.
echo.
echo To run the bot, make sure you have:
echo 1. Created a .env file with your Telegram bot token
echo 2. Installed dependencies with: pip install -r requirements.txt
echo 3. Run the bot with: python run_bot.py
echo.
pause