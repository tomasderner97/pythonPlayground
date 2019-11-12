import gizeh
import moviepy.editor as mpy
import numpy as np


def make_frame(t):
    surface = gizeh.Surface(854, 480)
    radius = np.sin(t) * 100
    circle = gizeh.circle(radius, xy=(200, 200), fill=(1, 0, 0))
    circle.draw(surface)
    return surface


for t in range(100):
    make_frame(t / 10).write_to_png(f"out/{t:03}.png")
    print(t)
