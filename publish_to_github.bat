@echo off
echo One-click GitHub publish
set /p REPO_URL=Enter your GitHub repo URL: 
if "%REPO_URL%"=="" exit /b
git init
git branch -M main
git add .
git commit -m "Initial commit: Modern Online Banking Auth System"
git remote remove origin >nul 2>&1
git remote add origin %REPO_URL%
git push -u origin main
pause
