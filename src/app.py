from gl.gl import Renderer
import gl.shaders as shaders

models_dir = "../models"
textures_dir = models_dir + "/textures"

width = 960
height = 540

renderer = Renderer(width, height)

renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader

renderer.gl_load_model(
    filename=f"{models_dir}/face.obj",
    texture_name=f"{textures_dir}/face.bmp",
    translate=(width / 2, height / 2, 0),
    rotate=(0, 90, 0),
    scale=(150, 150, 150)
)


renderer.gl_render()

renderer.gl_finish("output.bmp")
