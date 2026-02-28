@echo off
cd /d "%~dp0"
echo Starting NeuraEdge Streamlit Dashboard...
echo Dashboard will open at http://localhost:8501
echo.
pip install streamlit -q
streamlit run streamlit_app.py
pause
