@echo off
echo =====================================================
echo  AI Product Strategy Assistant
echo =====================================================
cd /d "%~dp0"

echo.
echo [1/3] Starting frontend on http://localhost:3001 ...
start "Frontend" cmd /k "D:\AI_FDE\venv\Scripts\python.exe %~dp0frontend\server.py"

echo.
echo [2/3] Waiting for frontend...
timeout /t 2 /nobreak >nul

echo.
echo [3/3] Opening browser...
start "" http://localhost:3001

echo.
echo Starting FastAPI backend on http://localhost:8001
echo Swagger docs: http://localhost:8001/docs
echo.
echo Press CTRL+C to stop.
echo =====================================================
D:\AI_FDE\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload
