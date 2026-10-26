@echo off
title SlothMerge Server
echo ========================================================
echo   Starting SlothMerge PR Review Agent...
echo ========================================================
echo.
echo Installing dependencies if needed...
py -m pip install -r requirements.txt
echo.
echo Starting web server at http://localhost:8000
start http://localhost:8000
py app.py
pause
