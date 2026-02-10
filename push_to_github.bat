@echo off
cd /d e:\projects\overview

REM Configure Git
"C:\Program Files\Git\bin\git.exe" config --global user.email "piyush.maurya.132@gmail.com"
"C:\Program Files\Git\bin\git.exe" config --global user.name "Piyush Maurya"

REM Initialize repository
"C:\Program Files\Git\bin\git.exe" init

REM Add all files
"C:\Program Files\Git\bin\git.exe" add .

REM Commit
"C:\Program Files\Git\bin\git.exe" commit -m "🎨 Enhanced GitHub Profile with LeetCode Integration and Auto-Update Workflow"

REM Add remote
"C:\Program Files\Git\bin\git.exe" remote add origin https://github.com/sick232/sick232.git

REM Push to main branch
"C:\Program Files\Git\bin\git.exe" branch -M main
"C:\Program Files\Git\bin\git.exe" push -u origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo Repository: https://github.com/sick232/sick232
pause
