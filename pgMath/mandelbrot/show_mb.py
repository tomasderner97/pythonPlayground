import numpy as np
import pickle
from matplotlib import cm
from PIL import Image


with open("mb.bin", "rb") as f:
    mandelbrot = pickle.load(f)

for i in np.int32(np.exp((np.arange(1000) + 562) * np.log(1.00841))):

    arr = mandelbrot.copy()

    arr[arr > i] = i

    arr = arr / np.max(arr)

    colormapped = cm.gist_rainbow(arr)
    img = Image.fromarray(np.uint8(colormapped * 255))
    img.save(f"imgs/mandelbrot_{i}.png")
