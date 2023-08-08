from gl.gl import Renderer
import gl.shaders as shaders

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080


# medium shot
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader
renderer.look_at(cam_pos=(0.9, 1, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.gl_load_model(
    filename=f"{models_dir}/bmo.obj",
    texture_name=f"{textures_dir}/bmo.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(16, 16, 16)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/medium_shot.bmp")


# low angle
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader
renderer.look_at(cam_pos=(0, -3, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.gl_load_model(
    filename=f"{models_dir}/bmo.obj",
    texture_name=f"{textures_dir}/bmo.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(16, 16, 16)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/low_angle.bmp")


# high angle
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader
renderer.look_at(cam_pos=(0, 3, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.gl_load_model(
    filename=f"{models_dir}/bmo.obj",
    texture_name=f"{textures_dir}/bmo.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(16, 16, 16)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/high_angle.bmp")


# dutch angle
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader
renderer.look_at(cam_pos=(1, 2.3, 0), eye_pos=(0, 0, -5), rotateZ=-15)
renderer.gl_load_model(
    filename=f"{models_dir}/bmo.obj",
    texture_name=f"{textures_dir}/bmo.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(16, 16, 16)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/dutch_angle.bmp")
