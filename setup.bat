@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Installing Playwright browsers...
playwright install chromium
echo.
echo Setup completed! You can now run start.bat
pause
