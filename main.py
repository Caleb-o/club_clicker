from typing import final
import pyautogui, time
import datetime as dt
import os
from random import randint
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
    pyautogui.click(pos[0], pos[1])
    # Offsets so it doesn't look sus
    time.sleep(WALK_WAIT + randint(-1, 1))

    KEYBOARD.press(MINE_KEY)
    KEYBOARD.release(MINE_KEY)

def get_position() -> tuple:
    return (randint(MIN[0], MAX[0]), randint(MIN[1], MAX[1]))

def clicked(x, y, button, pressed):
    if pressed and len(positions) < 2:
        positions.append(pyautogui.position())
        print(f' | set [{len(positions)}]', end='\r')

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
    print('\033[K\r')


def clear() -> None:
    # Check if Windows or nix
    os.system('cls' if os.name == 'nt' else 'clear')


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

    # Clear the terminal
    clear()

    print(f'Bounds ({MIN[0]}, {MIN[1]}) ({MAX[0]}, {MAX[1]})')
    start = dt.datetime.now()

    global MINE_COUNT

    try:
        while True:
            MINE_COUNT += 1
            pos = get_position()

            click(pos)
            # Offsets so it doesn't look sus
            new_time = randint(MINE_TIME -2, MINE_TIME + 2)
            for current in range(new_time):
                now = (dt.datetime.now() - start).seconds / 60
                print(f'\033[K\r {current * "#"}{(new_time - current) * " "} | {MINE_COUNT} mined | {now:.4} min', end='\r')
                time.sleep(1)


    except KeyboardInterrupt:
        global listener
        listener.stop()

        final_time = dt.datetime.now() - start
        seconds = final_time.seconds
        minutes = seconds / 60
        print(f'\nQuitting. Mined for {minutes:.2} minutes. Potential haul {seconds}-{100 * seconds}')
if __name__ == '__main__':
    main()
