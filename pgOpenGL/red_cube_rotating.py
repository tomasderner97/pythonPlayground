import numpy as np
from glumpy import app, gl, glm, gloo

app.use('qt5')

vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
attribute vec4 color;
attribute vec3 position;
varying vec4 v_color;

void main()
{
    v_color = color;
    gl_Position = projection * view * model * vec4(position, 1.0);
}
"""
fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

window = app.Window(width=600, height=600, color=(1, 1, 1, 1))

dtype = [('position', np.float32, 3),
         ('color', np.float32, 4)]
vertices = np.empty(8, dtype)
vertices['position'] = [
    [1, 1, 1],
    [-1, 1, 1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1]
]
vertices['color'] = [
    [0, 1, 1, 1],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1]
]
vertices = vertices.view(dtype=gloo.VertexBuffer)

tris = np.array([
    0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6, 0, 6, 1,
    1, 6, 7, 1, 7, 2, 7, 4, 3, 7, 3, 2, 4, 7, 6, 4, 6, 5
], dtype=np.uint32)
tris = tris.view(dtype=gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
cube['model'] = np.eye(4, dtype=np.float32)
cube['view'] = glm.translation(0, 0, -5)

phi = 0
theta = 0


@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


@window.event
def on_resize(width, height):
    cube['projection'] = glm.perspective(45, width / height, 2, 100)


@window.event
def on_draw(dt):
    global phi, theta
    window.clear()

    cube.draw(gl.GL_TRIANGLES, tris)

    theta += 1
    phi += -1

    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['model'] = model


app.run()
