@echo off
chcp 65001 >nul
echo ==========================================
echo    AudiobookMaker - AI有声书制作工具
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found, please install Python 3.8+
    pause
    exit /b 1
)

echo [1/4] Installing backend dependencies...
cd backend
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [Error] Backend dependencies installation failed
    pause
    exit /b 1
)

echo [2/4] Creating directories...
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist temp mkdir temp

echo [3/4] Starting backend server...
start "AudiobookMaker Backend" cmd /k "python -m app.main"

echo [4/4] Starting frontend server...
cd ..\frontend
if exist node_modules (
    start "AudiobookMaker Frontend" cmd /k "npx serve . -p 3000"
) else (
    echo Installing frontend dependencies...
    npm install --quiet
    start "AudiobookMaker Frontend" cmd /k "npx serve . -p 3000"
)

echo.
echo ==========================================
echo  Servers started!
echo  Backend API: http://localhost:8000
echo  Frontend: http://localhost:3000
echo ==========================================
echo.
echo Please open browser and visit http://localhost:3000
echo.
pause
