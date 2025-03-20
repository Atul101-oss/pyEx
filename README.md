# To-Do SVG Generator

This script generates or update a `todo.svg` file from a text file (`todo.txt`) and sets it as a wallpaper. Ensure the `todo.svg`(wallpaper_behind_the_todo-list) file is stored in the same directory as the script.

## Instructions

1. Place your to-do list in `todo.txt`.
2. Run the script:
   ```bash
   python3 todo.py
   ```
3. The script will generate `todo.svg` in the same directory. Set this SVG as your wallpaper.

## Auto-Run on Startup

### Windows
1. Create a batch file (`run_todo.bat`) with the following content:
   ```batch
   python "C:\path\to\todo.py"
   ```
2. Place the batch file in the Windows Startup folder:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   ```

### Linux
1. Create a `.desktop` file in `~/.config/autostart/`:
   ```bash
   nano ~/.config/autostart/todo.desktop
   ```
2. Add the following content:
   ```ini
   [Desktop Entry]
   Type=Application
   Exec=python /path/to/todo.py
   Hidden=false
   NoDisplay=false
   X-GNOME-Autostart-enabled=true
   Name=To-Do SVG Generator
   ```
3. Save and exit.

## Notes
- Ensure Python is installed and accessible in your system's PATH.
- Set the generated `todo.svg` as your wallpaper using your system's wallpaper settings.
