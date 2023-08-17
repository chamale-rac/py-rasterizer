from gl.gl import Renderer
import gl.shaders as shaders
from gl.model import Model

models_dir = "../models"
textures_dir = models_dir + "/textures"
out_dir = "../out"

width = 1920
height = 1080

elephant_camouflage = Model(f"{models_dir}/elephant.obj",
                            translate=(-0.4, -1, -5), scale=(0.09, 0.09, 0.09), rotate=(0, -60, 0))
elephant_camouflage.load_texture(f"{textures_dir}/elephant.bmp")
elephant_camouflage.set_shaders(
    shaders.vertex_shader, shaders.camouflage_shader)
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.look_at(cam_pos=(1, 2, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.add_model(elephant_camouflage)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/camouflage.bmp")


elephant_fractal = Model(f"{models_dir}/elephant.obj",
                         translate=(-0.4, -1, -5), scale=(0.09, 0.09, 0.09), rotate=(0, -60, 0))
elephant_fractal.load_texture(f"{textures_dir}/elephant.bmp")
elephant_fractal.set_shaders(shaders.vertex_shader, shaders.fractal_shader)
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.look_at(cam_pos=(1, 2, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.add_model(elephant_fractal)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/fractal.bmp")

elephant_invert = Model(f"{models_dir}/elephant.obj",
                        translate=(-0.4, -1, -5), scale=(0.09, 0.09, 0.09), rotate=(0, -60, 0))
elephant_invert.load_texture(f"{textures_dir}/elephant.bmp")
elephant_invert.set_shaders(shaders.vertex_shader, shaders.invert_shader)
renderer = Renderer(width, height)
renderer.set_clear_color(32/255, 33/255, 36/255)
renderer.clear()
renderer.look_at(cam_pos=(1, 2, 0), eye_pos=(0, 0, -5), rotateZ=0)
renderer.add_model(elephant_invert)
renderer.gl_render()
renderer.gl_finish(f"{out_dir}/invert.bmp")
