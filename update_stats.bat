@echo off
cd /d e:\projects\overview

echo Updating README with fixed stats...
"C:\Program Files\Git\bin\git.exe" add README.md

echo Committing changes...
"C:\Program Files\Git\bin\git.exe" commit -m "🔧 Fix GitHub stats display and add quick stats tables"

echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main

echo.
echo ✅ Stats section updated! Your profile will refresh shortly.
echo Visit: https://github.com/sick232
pause
