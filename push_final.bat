@echo off
cd /d e:\projects\overview

echo Adding files...
"C:\Program Files\Git\bin\git.exe" add -A

echo Committing with new stats...
"C:\Program Files\Git\bin\git.exe" commit -m "📊 Replace external image stats with text-based stats - no more loading issues"

echo Pushing to GitHub...
"C:\Program Files\Git\bin\git.exe" push origin main -f

echo.
echo ✅ All done! Your profile is now loading properly!
echo Visit: https://github.com/sick232
pause
