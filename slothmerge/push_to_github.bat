@echo off
title Push SlothMerge to GitHub
echo ========================================================
echo   Push SlothMerge to GitHub (Automated)
echo ========================================================
echo.
echo Make sure you have created an empty repository on https://github.com/new
echo.
set /p REPO_URL="Paste your GitHub repository URL (e.g. https://github.com/yourname/slothmerge.git): "

if "%REPO_URL%"=="" (
    echo Error: No URL entered.
    pause
    exit /b
)

echo.
echo Initializing Git repository...
git init
git add .
git commit -m "SlothMerge: Open-source AI PR review agent with Gemma 2 and Sentry tracing"
git branch -M main
git remote remove origin 2>nul
git remote add origin %REPO_URL%

echo.
echo Pushing files to GitHub...
git push -u origin main

echo.
echo ========================================================
echo Done! Check your GitHub repository link.
echo ========================================================
pause
