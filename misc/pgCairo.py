import gizeh
surface = gizeh.Surface(width=320, height=260, bg_color=(0,0,0))
circle = gizeh.circle(r=30, xy=[40, 40], fill=(1, 0, 0))
circle.draw(surface)
surface.ipython_display()