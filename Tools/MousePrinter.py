import pyautogui
import pygetwindow as gw
import time




# Replace 'Window Title' with the title of the window you want to get the position of
window_title = "WEBFISHING v1.1"
window = gw.getWindowsWithTitle(window_title)

if window:
    win = window[0]
    print(f"Window '{window_title}' position: (x: {win.left}, y: {win.top})")
else:
    print(f"No window found with title '{window_title}'")
    exit(-1)

while True:
    # Get the current position of the mouse cursor
    cursor_position = pyautogui.position()
    relative_x = cursor_position.x - win.left
    relative_y = cursor_position.y - win.top
    print(f"Cursor position: (x: {relative_x}, y: {relative_y})")
    time.sleep(0.2)
