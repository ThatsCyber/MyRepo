@echo off
echo Stopping any existing Chrome processes...
taskkill /F /IM chrome.exe >nul 2>&1

echo Starting Chrome with remote debugging and your regular profile...
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--remote-debugging-port=9222"

echo Chrome started with debugging on port 9222 using your regular profile
echo You can now run your automation script!
pause 