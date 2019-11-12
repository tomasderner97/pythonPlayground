from glumpy import app, gloo, gl
import numpy as np

# app.use("qt5")
# app.use("pyglet")

vertex = """
    attribute float scale;
    attribute vec2 position;
    attribute vec4 color;
    varying vec4 v_color;
    void main()
    { 
        gl_Position = vec4(scale * position, 0.0, 1.0);
        v_color = color;
    } 
"""

fragment = """
    varying vec4 v_color;
    void main() 
    { 
        gl_FragColor = v_color; 
    } 
"""

window = app.Window()

quad = gloo.Program(vertex, fragment, count=4)

quad['position'] = (-1, +1), (+1, +1), (-1, -1), (+1, -1)
quad['color'] = (1, 1, 0, 1), (1, 0, 0, 1), (0, 0, 1, 1), (0, 1, 0, 1)
quad['scale'] = 1


counter = 0

@window.event
def on_draw(dt):

    global counter
    window.clear()

    scale = np.cos(counter / 100 * np.pi)
    counter += 1

    quad['scale'] = scale

    quad.draw(gl.GL_TRIANGLE_STRIP)


app.run()
