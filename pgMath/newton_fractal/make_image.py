import numpy as np
import pickle
from matplotlib import cm
from PIL import Image


with open("newton.bin", "rb") as f:
    newton = pickle.load(f)

newton = newton / np.max(newton)

colormapped = cm.gist_rainbow(newton)
img = Image.fromarray(np.uint8(colormapped * 255))
img.save(f"newton.png")
