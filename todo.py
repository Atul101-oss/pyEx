import base64
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import numpy as np

# File paths
TEXT_FILE = "/home/arya/Desktop/todo.txt"
SVG_FILE = "/home/arya/Desktop/pyEx/todo.svg"
wallpaper_file = "/home/arya/Desktop/pyEx/todo"

# Function to calculate inverted color
def invertColor(image_path):
    with Image.open(image_path) as image:
        if image.mode != "RGB":
            image = image.convert("RGB")
        im_arr = np.array(image)
        avg_color = im_arr.mean(axis=(0, 1))
        inverted = abs(255 - (avg_color+50))
        return tuple(map(int, inverted))

# Base64 encode the wallpaper image (corrected)
def encode_wallpaper_base64(image_path, size=(1366, 768)):
    with Image.open(image_path) as img:
        img = img.resize(size)  # Resize the image
        # Save resized image to bytes in memory
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

# Generate Base64 for wallpaper and calculate inverted color
wallpaper_base64 = encode_wallpaper_base64(wallpaper_file)
invert_color = invertColor(wallpaper_file)

# Function to convert text lines to <tspan> elements
def txt_to_tspan(lines):
    svg_text = ""
    for line in lines:
        svg_text += f"<tspan x='10' dy='20'>{line}</tspan>"
    return svg_text

# Function to generate SVG from the text file
def generate_svg_from_text():
    try:
        with open(TEXT_FILE, "r", encoding="utf-8") as file:
            text_content = file.read()

        # Process the text into <tspan> elements
        lines = text_content.split("\n")
        svg_text_content = txt_to_tspan(lines)

        # SVG template
        svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1366" height="768" xmlns:xlink="http://www.w3.org/1999/xlink">
            <!-- Embed wallpaper as background -->
            <image href="data:image/jpeg;base64,{wallpaper_base64}" x="0" y="0" width="100%" height="100%" />
            <!-- Overlay text -->
            <text x="10" y="40" font-family="Arial" font-size="18" fill="rgb({invert_color[0]}, {invert_color[1]}, {invert_color[2]})">
                {svg_text_content}
            </text>
        </svg>'''

        # Write to SVG file
        with open(SVG_FILE, "w", encoding="utf-8") as svg_file:
            svg_file.write(svg_template)
        print(f"SVG updated: {SVG_FILE}")
    except Exception as e:
        print(f"Error generating SVG: {e}")

# Event handler for monitoring file changes
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TEXT_FILE):
            time.sleep(0.5)  # Delay to handle file save buffering
            print(f"Detected change in {TEXT_FILE}. Regenerating SVG...")
            generate_svg_from_text()

# Set up the file observer
if __name__ == "__main__":
    generate_svg_from_text()  # Initial generation
    observer = Observer()
    event_handler = FileChangeHandler()
    observer.schedule(event_handler, os.path.dirname(TEXT_FILE), recursive=False)  # Monitor the directory containing TEXT_FILE
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
