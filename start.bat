@echo off
cd /d "%~dp0"
python main.py
if errorlevel 1 (
  echo Could not start Floating Fish. Install Python with Tcl/Tk and add Python to PATH.
  pause
)
