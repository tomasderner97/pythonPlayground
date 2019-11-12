import cv2
import os
import re

image_folder = "imgs"
video_name = "mandelbrot.avi"
fps = 20


def key(s):

    r = re.findall("[0-9]+", s)
    return int(r[0])


images = [img for img in os.listdir(image_folder)]
images = sorted(images, key=key)[:-270]

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, -1, fps, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
