from mayavi import mlab
import numpy as np

def implicit_plot(expr, ext_grid, fig_handle=None, Nx=101, Ny=101, Nz=101,
                  col_isurf=(50 / 255, 199 / 255, 152 / 255), col_osurf=(240 / 255, 36 / 255, 87 / 255),
                  opa_val=0.8, opaque=True, ori_axis=True, **kwargs):

    if fig_handle == None:  # create a new figure
        fig = mlab.figure(1, bgcolor=(0.97, 0.97, 0.97), fgcolor=(0, 0, 0), size=(800, 800))
    else:
        fig = fig_handle
    xl, xr, yl, yr, zl, zr = ext_grid
    x, y, z = np.mgrid[xl:xr:eval('{}j'.format(Nx)),
              yl:yr:eval('{}j'.format(Ny)),
              zl:zr:eval('{}j'.format(Nz))]
    scalars = eval(expr)
    src = mlab.pipeline.scalar_field(x, y, z, scalars)
    if opaque:
        delta = 1.e-5
        opa_val = 1.0
    else:
        delta = 0.0
        # col_isurf = col_osurf
    # In order to render different colors to the two sides of the algebraic surface,
    # the function plots two contour3d surfaces at a &quot;distance&quot; of delta from the value
    # of the solution.
    # the second surface (contour3d) is only drawn if the algebraic surface is specified
    # to be opaque.
    cont1 = mlab.pipeline.iso_surface(src, color=col_isurf, contours=[0 - delta],
                                      transparent=False, opacity=opa_val)
    cont1.compute_normals = False  # for some reasons, setting this to true actually cause
    # more unevenness on the surface, instead of more smooth
    if opaque:  # the outer surface is specular, the inner surface is not
        cont2 = mlab.pipeline.iso_surface(src, color=col_osurf, contours=[0 + delta],
                                          transparent=False, opacity=opa_val)
        cont2.compute_normals = False
        cont1.actor.property.backface_culling = True
        cont2.actor.property.frontface_culling = True
        cont2.actor.property.specular = 0.2  # 0.4 #0.8
        cont2.actor.property.specular_power = 55.0  # 15.0
    else:  # make the surface (the only surface) specular
        cont1.actor.property.specular = 0.2  # 0.4 #0.8
        cont1.actor.property.specular_power = 55.0  # 15.0

    # Scene lights (4 lights are used)
    engine = mlab.get_engine()
    scene = engine.current_scene
    cam_light_azimuth = [78, -57, 0, 0]
    cam_light_elevation = [8, 8, 40, -60]
    cam_light_intensity = [0.72, 0.48, 0.60, 0.20]
    for i in range(4):
        camlight = scene.scene.light_manager.lights[i]
        camlight.activate = True
        camlight.azimuth = cam_light_azimuth[i]
        camlight.elevation = cam_light_elevation[i]
        camlight.intensity = cam_light_intensity[i]
    # axis through the origin
    if ori_axis:
        len_caxis = int(1.05 * np.max(np.abs(np.array(ext_grid))))
        caxis = mlab.points3d(0.0, 0.0, 0.0, len_caxis, mode='axes', color=(0.15, 0.15, 0.15),
                              line_width=1.0, scale_factor=1., opacity=1.0)
        caxis.actor.property.lighting = False
    # if no figure is passed, the function will create a figure.
    if fig_handle == None:
        # Setting camera
        cam = fig.scene.camera
        cam.elevation(-20)
        cam.zoom(1.0)  # zoom should always be in the end.
        mlab.show()