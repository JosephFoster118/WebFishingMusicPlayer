import pygetwindow as gw
import pyautogui
import time

SECTION_BUTTON_POSITIONS = {
    1: (95,224),
    2: (166, 224),
    3: (257, 224),
    4: (95, 305),
    5: (166, 305),
    6: (257, 305),
    7: (95, 383),
    8: (166, 383),
    9: (257, 383)
}

GUITAR_ROW_START = 188
GUITAR_ROW_END = 1049
GUITAR_ROW_COUNT = 15


GUITAR_ROWS = []
for i in range(0, GUITAR_ROW_COUNT - 1):
    GUITAR_ROWS.append(GUITAR_ROW_START + (GUITAR_ROW_END - GUITAR_ROW_START) / (GUITAR_ROW_COUNT - 1) * i)
GUITAR_ROWS.append(GUITAR_ROW_END)

GUITAR_COLUMNS = [
    354,
    385,
    420,
    450,
    488,
    520
]



# Replace 'Window Title' with the title of the window you want to get the position of
window_title = "WEBFISHING v1.1"
window = gw.getWindowsWithTitle(window_title)

if window:
    win = window[0]
    print(f"Window '{window_title}' position: (x: {win.left}, y: {win.top})")
else:
    print(f"No window found with title '{window_title}'")
    exit(-1)


def clickRelative(x, y):
    pyautogui.click(x=win.left + x, y=win.top + y)

def clickSection(section):
    clickRelative(SECTION_BUTTON_POSITIONS[section][0], SECTION_BUTTON_POSITIONS[section][1])

def clickGuitar(row, column):
    clickRelative(GUITAR_COLUMNS[column], GUITAR_ROWS[row])

time.sleep(5)

#Reset all
for i in range(len(SECTION_BUTTON_POSITIONS)):
    clickSection(i + 1)
    for j in range(len(GUITAR_COLUMNS)):
        clickGuitar(len(GUITAR_ROWS) - 1, j)

#Set first column notes
for i in range(9):
    clickSection(i + 1)
    clickGuitar(i, 0)

#Set second column notes
for i in range(9):
    clickSection(i + 1)
    clickGuitar(i + 4, 1)

#Set third column notes
for i in range(7):
    clickSection(i + 1)
    clickGuitar(i + 8, 2)

#Set fourth column notes
for i in range(5):
    clickSection(i + 1)
    clickGuitar(i + 10, 3)

#Set fifth column notes
for i in range(3):
    clickSection(i + 1)
    clickGuitar(i + 11, 4)

#Set sixth column notes
for i in range(1):
    clickSection(i + 1)
    clickGuitar(i + 12, 5)
