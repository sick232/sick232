@echo off
cd /d e:\projects\overview
"C:\Program Files\Git\bin\git.exe" log --oneline -5
"C:\Program Files\Git\bin\git.exe" remote -v
pause
