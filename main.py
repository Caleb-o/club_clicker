from typing import final
import pyautogui, time, datetime
from random import randint as range
from pynput.mouse import Listener
from pynput.keyboard import Controller

WALK_WAIT: float  = 3.0 # Time to wait before button press
MINE_TIME: float = 15.0
MINE_KEY = 'd'

MINE_COUNT: int = 0

KEYBOARD = Controller()
positions = []
listener = None

def click(pos: tuple) -> None:
    old_pos = pyautogui.position()
    pyautogui.click(pos[0], pos[1])
    pyautogui.move(old_pos[0], old_pos[1])
    # Offsets so it doesn't look sus
    time.sleep(WALK_WAIT + range(-1, 1))

    KEYBOARD.press(MINE_KEY)
    KEYBOARD.release(MINE_KEY)

def get_position() -> tuple:
    return (range(MIN[0], MAX[0]), range(MIN[1], MAX[1]))

def clicked(x, y, button, pressed):
    if pressed and len(positions) < 2:
        positions.append(pyautogui.position())
        print(f' | Set position : [{len(positions)}]')

def get_bounds():
    global listener
    listener = Listener(on_click=clicked)
    listener.start()

    print('Click a start and end position:')

    try:
        while len(positions) < 2:
            pos = pyautogui.position()
            print(f'\033[K\rPosition x:{pos[0]}, y:{pos[1]}', end='')
    except KeyboardInterrupt:
        listener.stop()
        print("\nQuitting.")
        return
    print()


def main() -> None:
    get_bounds()

    if len(positions) < 2:
        return

    global MIN
    global MAX
    
    MIN = positions[0]
    MAX = positions[1]

    # Reverse
    if MAX[0] < MIN[0] or MAX[1] < MIN[1]:
        MAX = positions[0]
        MIN = positions[1]

    print('Starting...')
    start = datetime.datetime.now()

    global MINE_COUNT

    try:
        while True:
            MINE_COUNT += 1
            pos = get_position()

            click(pos)
            # Offsets so it doesn't look sus
            time.sleep(MINE_TIME + range(-2, 2))

            print(f'\033[K\rGoing to {pos} to mine. Count: {MINE_COUNT}', end='\r')
    except KeyboardInterrupt:
        global listener
        listener.stop()

        final_time = datetime.datetime.now() - start
        seconds = final_time.seconds
        print(f'\nQuitting. Mined for {seconds} seconds. Potential haul {seconds}-{100 * seconds}')

if __name__ == '__main__':
    main()