from gl.gl import Renderer
import gl.shaders as shaders

from gl.model import Model

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 960
height = 540


# 4 august
model = Model(f"{models_dir}/face.obj",
              translate=(-3, 0, -5), scale=(1.5, 1.5, 1.5))
model.load_texture(f"{textures_dir}/face.bmp")
model.set_shaders(shaders.vertex_shader, shaders.flat_shader)

model1 = Model(f"{models_dir}/face.obj",
               translate=(3, 0, -5), scale=(1.5, 1.5, 1.5))
model1.load_texture(f"{textures_dir}/face.bmp")
model1.set_shaders(shaders.vertex_shader, shaders.fragment_shader)


renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.add_model(model)
renderer.add_model(model1)

renderer.gl_render()
renderer.gl_finish(f"{out_dir}/face_4.bmp")
