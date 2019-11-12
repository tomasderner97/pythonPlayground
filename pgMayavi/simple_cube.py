from custom_utils.qt import MayaviWidget, qt_app


if __name__ == "__main__":

    mw = MayaviWidget(None, 1000, 800, bgcolor="w", fgcolor="k")
    mlab = mw.mlab

    x = [
        [-1, -1, -1, -1, -1],
        [-1,  1,  1, -1, -1],
        [-1,  1,  1, -1, -1],
        [-1, -1, -1, -1, -1],
    ]
    y = [
        [-1, -1,  1,  1,  1],
        [-1, -1,  1,  1, -1],
        [-1, -1,  1,  1, -1],
        [-1, -1,  1,  1,  1],

    ]
    z = [
        [ 1,  1,  1,  1,  1],
        [ 1,  1,  1,  1,  1],
        [-1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1],
    ]

    s1 = mlab.mesh(x, y, z)

    qt_app(mw)
