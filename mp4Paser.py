import curses
import time
import cv2
from PIL import Image
import numpy as np
import os

ASCII_CHARS = np.array(list(" .,-~:;=!*#$@"))
IMG_WIDTH = 50

def image_parser(video_path: str, fps: int):
    output_dir = 'output_frames'
    os.makedirs(output_dir, exist_ok=True)
    ascii_arts = []

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % fps == 0:
            frame_path = os.path.join(output_dir, f'{frame_count:04d}.png')
            cv2.imwrite(frame_path, frame)
            # ascii_art = ascii_parser(frame)
            # ascii_arts.append(ascii_art)
        
        frame_count += 1

    cap.release()
    return frame_count



def main():
    print("please input the path of the vedio")
    video_path = input()
    print("please input the fps you want")
    fps = int(input())
    frame_count = image_parser(video_path, fps)
    ascii_arts = []
    for i in range(0, int(frame_count/fps)):
        frame_path = os.path.join('output_frames', f'{i*fps:04d}.png')
        ascii_art = ascii_parser(frame_path)
        ascii_arts.append(ascii_art)

    curses.wrapper(display_ascii_arts, ascii_arts, fps)


def ascii_parser(img_path: str):
    img = Image.open(img_path).convert("L")
    img = img.resize((IMG_WIDTH * 2, int(IMG_WIDTH * img.height / img.width)))
    ascii_art = ASCII_CHARS[(np.array(img) / 255 * (len(ASCII_CHARS) - 1)).astype(int)]
    return "\n".join("".join(row) for row in ascii_art)

def display_ascii_arts(stdscr, ascii_arts, fps):
    stdscr.clear()
    for ascii_art in ascii_arts:
        stdscr.clear()
        stdscr.addstr(0, 0, ascii_art)
        stdscr.refresh()
        time.sleep(1 / fps)

if __name__ == "__main__":
    main()