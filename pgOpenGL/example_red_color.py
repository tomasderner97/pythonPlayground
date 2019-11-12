from glumpy import app, gloo, gl

app.use("qt5")

vertex = """
    attribute vec2 position;
    void main(){ gl_Position = vec4(position, 0.0, 1.0); } """

fragment = """
    void main() { gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0); } """

window = app.Window()

quad = gloo.Program(vertex, fragment, count=4)

quad['position'] = (-1, +1), (+1, +1), (-1, -1), (+1, -1)


@window.event
def on_draw(dt):
    window.clear()
    quad.draw(gl.GL_TRIANGLE_STRIP)


app.run()
