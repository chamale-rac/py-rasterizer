from gl.gl import Renderer
import gl.shaders as shaders

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080


# 4 august
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.flat_shader
renderer.gl_load_model(
    filename=f"{models_dir}/face.obj",
    texture_name=f"{textures_dir}/face.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(1.5, 1.5, 1.5)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/face_4.bmp")
