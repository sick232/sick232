@echo off
cd /d e:\projects\overview

REM Check if files exist
echo Files in repository:
dir /B

echo.
echo Adding all files...
"C:\Program Files\Git\bin\git.exe" add -A

echo.
echo Checking status...
"C:\Program Files\Git\bin\git.exe" status

echo.
echo Committing...
"C:\Program Files\Git\bin\git.exe" commit -m "Add enhanced profile README with LeetCode integration"

echo.
echo Force pushing to GitHub (overwriting any deletions)...
"C:\Program Files\Git\bin\git.exe" push -u origin main -f

echo.
echo ✅ Done! Your profile should update now.
pause
