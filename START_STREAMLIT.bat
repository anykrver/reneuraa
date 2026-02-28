@echo off
REM NeuraEdge Streamlit Dashboard Launcher

cd /d "%~dp0"

echo.
echo ================================================================================
echo         NEURAEDGE IP PLATFORM - STREAMLIT WEB DASHBOARD
echo ================================================================================
echo.
echo Starting Streamlit server...
echo.
echo Dashboard will open in your browser at:
echo   http://localhost:8501
echo.
echo Features:
echo   - Real-time system monitoring
echo   - Interactive inference execution
echo   - Benchmark visualization
echo   - Configuration management
echo   - Full documentation
echo.
echo Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

pip install streamlit -q

streamlit run ui/streamlit_app.py --logger.level=error

pause
