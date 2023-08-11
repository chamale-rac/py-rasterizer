from gl.gl import Renderer
import gl.shaders as shaders
from gl.model import Model

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080

# left = Model(f"{models_dir}/face.obj",
#              translate=(-3, 0, -5), scale=(1.5, 1.5, 1.5))
# left.load_texture(f"{textures_dir}/face.bmp")
# left.set_shaders(shaders.vertex_shader, shaders.flat_shader)

center = Model(f"{models_dir}/face.obj",
               translate=(0, 0, -5), scale=(1.5, 1.5, 1.5))
center.load_texture(f"{textures_dir}/face.bmp")
center.set_shaders(shaders.vertex_shader, shaders.toon_shader)

# right = Model(f"{models_dir}/face.obj",
#               translate=(3, 0, -5), scale=(1.5, 1.5, 1.5))
# right.load_texture(f"{textures_dir}/face.bmp")
# right.set_shaders(shaders.vertex_shader, shaders.fragment_shader)


renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
# renderer.add_model(left)
renderer.add_model(center)
# renderer.add_model(right)

renderer.gl_render()
renderer.gl_finish(f"{out_dir}/face_4.bmp")
