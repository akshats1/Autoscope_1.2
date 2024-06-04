import logging
import numpy as np
import cv2
from PIL import Image
import io
from time import sleep
from datetime import datetime
import subprocess
#import main
from movement import board, movezclock, movezanticlock, movexclock, movexanticlock, movey

def variance(image):
    bg = cv2.GaussianBlur(image, (11, 11), 0)
    v = cv2.Laplacian(bg, cv2.CV_64F).var()
    return v

def auto():
    logging.info("[Autofocus] Starting AutoFocus")
    global z
    z = 0
    var = []
    _ = board.write("init".encode())
    while True:
        data = board.readline()
        if data == b'Done\r\n':
            break
    _ = board.write("zcclk,{}".format(14500).encode())
    z += 14500
    while True:
        data = board.readline()
        if data == b'Done\r\n':
            break
    for i in range(25):
        image = np.empty((240 * 320 * 3), dtype=np.uint8)
        image = main.cam.capture('image')
        with open("/srv/autoscope/api/thumbs/gallery_data/default/image.jpg", 'rb') as file:
            image = file.read()
        image = io.BytesIO(image)
        image = Image.open(image)
        image = np.array(image)
        image = image.reshape((240, 320, 3))
        var.append(variance(image))
        _ = board.write("zcclk,{}".format(50).encode())
        z += 50
        logging.info("[autofocus] Moving z motor anticlockwise")
        while True:
            data = board.readline()
            if data == b'Done\r\n':
                break
    var = np.array(var)
    l = np.argmax(var)
    sleep(.5)
    _ = board.write("zclk,{}".format(1290 - l * 50).encode())
    z -= 1290 - l * 50
    logging.info("[autofocus] Moving to focused position")
    while True:
        data = board.readline()
        if data == b'Done\r\n':
            break

def scan():
    global scan_count
    scan_count = 0
    cur_time = datetime.now()
    dir_path = "/srv/autoscope/api/gallery_data/scan_{}/".format(cur_time.strftime("%Y%m%d_%H%M"))
    subprocess.run(["mkdir", dir_path])
    logging.info("[Scan] First Autofocus")
    auto()
    for i in range(10):
        for j in range(15):
            if j == 7:
                auto()
            if i % 2 == 0:
                main.cam.scan_capture(dir_path + "imagerow{0},{1}.jpg".format(i, j))
                scan_count += 1
                movexclock(15)
            else:
                main.cam.scan_capture(dir_path + "imagerow{0},{1}.jpg".format(i, 14 - j))
                scan_count += 1
                movexanticlock(15)
        movey(12)
        logging.info("[Scan] Changing y Pos")
    board.write("init".encode())
    while True:
        data = board.readline()
        if data == b'Done\r\n':
            break
    stitch_images(dir_path, dir_path + 'complete_slide.jpg', 10, 15)

def stitch_images(image_paths, output_path, rows, cols):
    images = []
    max_width = 0
    max_height = 0
    for i in range(rows):
        for j in range(cols):
            image = Image.open(image_paths + "imagerow{},{}.jpg".format(i, j))
            images.append(image)
            max_width = max(max_width, image.width)
            max_height = max(max_height, image.height)
    stitched_width = max_width * cols
    stitched_height = max_height * rows
    stitched_image = Image.new('RGB', (stitched_width, stitched_height), (255, 255, 255))
    for i, image in enumerate(images):
        row = i // cols
        col = i % cols
        x = col * max_width
        y = row * max_height
        stitched_image.paste(image, (x, y))
    stitched_image.save(output_path)

