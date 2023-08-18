from gl.gl import Renderer
import gl.shaders as shaders
from gl.model import Model

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080

gouraud_camouflage = Model(f"{models_dir}/elephant.obj",
                           translate=(-0.4, -1, -5), scale=(0.09, 0.09, 0.09), rotate=(0, -60, 0))
gouraud_camouflage.load_texture(f"{textures_dir}/elephant.bmp")
gouraud_camouflage.set_shaders(
    shaders.vertex_shader, shaders.gouraud_shader)
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.look_at(cam_pos=(1, 2, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.gl_background_texture(f"{textures_dir}/sabana.bmp")
renderer.gl_clear_background()
renderer.add_model(gouraud_camouflage)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/gouraud.bmp")
