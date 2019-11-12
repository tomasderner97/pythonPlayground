from custom_utils.matplotlib import make_sliders, SliderSetup, Measurement
from custom_utils.science.imports import *

fig, ax = plt.subplots()


def init(i):

    i["x"] = sp.linspace(0, 10, 100)

    i["line"], = i["ax"].plot(i["x"], i["x"])


def update(i, changed=None):

    amp = i["ampSlider"].val
    freq = i["freqSlider"].val

    i["line"].set_ydata(amp * sp.sin(freq * i["x"]))


ampSlider = SliderSetup("ampSlider", "Amplitude", maxv=10, init=1)
freqSlider = SliderSetup("freqSlider", "Frequency", minv=0.1, maxv=5, init=1)

items = make_sliders(fig, ax, [ampSlider, freqSlider], update, init, flags=["noasc", "tight"])

m = Measurement(fig, ax)

plt.show()
