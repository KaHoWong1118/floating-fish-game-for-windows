# Floating Fish

A beginner-friendly Windows desktop companion: one or two pixel fish swim over your work, with occasional crab and shrimp visitors.

## Run on Windows

1. Install Python 3.12 or newer from https://www.python.org/downloads/windows/ . Include Tcl/Tk and select **Add Python to PATH**.
2. Download this repository using **Code → Download ZIP** and extract it.
3. Double-click `start.bat`. Use the small control panel to pause, change pixel size, or quit.

Or open a terminal in this folder and run `python main.py`.

Animals allow mouse clicks through to your work. The control panel remains clickable; closing it exits the demo. The primary display is supported; full-screen apps may cover the overlay. No third-party packages, accounts, or downloaded art are needed.

On Linux/macOS, run `python main.py --preview` for an ordinary development window. Python needs Tk support. Windows transparency and click-through require validation on Windows.

## Learn and extend

- `aquarium.py` handles movement and population limits.
- `main.py` draws original pixel sprites and provides controls.
- Run `python -m unittest discover -s tests -v` to test the simulation.

Start by changing sprite letters and colors in `main.py`: each letter is a colored pixel and `.` is empty. Then adjust movement speed and visitor timing in `aquarium.py`. Later you can add new species, saved settings, a tray icon, multi-monitor support, and an executable installer.

This is an initial desktop pet prototype. It does not start automatically or collect data.
