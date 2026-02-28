@echo off
REM NeuraEdge Web Dashboard Launcher
REM Start server on localhost:8080

cd /d "%~dp0"

echo.
echo ================================================================================
echo                    NEURAEDGE IP PLATFORM - WEB DASHBOARD
echo ================================================================================
echo.
echo Starting server on http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

python ui/server.py

pause
