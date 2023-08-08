from gl.gl import Renderer
import gl.shaders as shaders

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080

renderer = Renderer(width, height)
renderer.vertex_shader = shaders.vertex_shader
renderer.fragment_shader = shaders.fragment_shader
renderer.look_at(cam_pos=(0, 2, 0), eye_pos=(0, 0, -5))
renderer.gl_load_model(
    filename=f"{models_dir}/phone.obj",
    texture_name=f"{textures_dir}/phone.bmp",
    translate=(0, 0, -5),
    rotate=(0, 0, 0),
    scale=(10, 10, 10)
)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/phone.bmp")
