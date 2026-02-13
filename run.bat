@echo off
REM MAAZ Food Delivery Application - Quick Start Script
REM This script helps manage the Flask application

setlocal enabledelayedexpansion

:menu
cls
echo.
echo ========================================
echo   MAAZ Food Delivery Application
echo ========================================
echo.
echo 1. Install Dependencies
echo 2. Start Application (Port 5000)
echo 3. Start Application (Port 5001)
echo 4. Start Application (Port 5002)
echo 5. Reset Database (Delete fooddelivery.db)
echo 6. Open Homepage in Browser
echo 7. Open Admin Login in Browser
echo 8. View Documentation
echo 9. Exit
echo.
set /p choice=Enter your choice (1-9): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start5000
if "%choice%"=="3" goto start5001
if "%choice%"=="4" goto start5002
if "%choice%"=="5" goto resetdb
if "%choice%"=="6" goto openhome
if "%choice%"=="7" goto openadmin
if "%choice%"=="8" goto docs
if "%choice%"=="9" goto exit
goto menu

:install
cls
echo Installing dependencies...
pip install -r requirements.txt
pause
goto menu

:start5000
cls
echo Starting application on http://localhost:5000
python app.py
goto menu

:start5001
cls
echo Starting application on http://localhost:5001
python -c "import app as a; a.app.run(debug=True, port=5001)"
goto menu

:start5002
cls
echo Starting application on http://localhost:5002
python -c "import app as a; a.app.run(debug=True, port=5002)"
goto menu

:resetdb
cls
echo Resetting database...
if exist fooddelivery.db (
    del fooddelivery.db
    echo Database deleted. Run the app again to create a fresh database.
) else (
    echo Database not found.
)
pause
goto menu

:openhome
start http://localhost:5000
goto menu

:openadmin
start http://localhost:5000/admin/login
goto menu

:docs
cls
echo Opening README.md...
start notepad README.md
goto menu

:exit
echo Exiting...
exit /b 0
