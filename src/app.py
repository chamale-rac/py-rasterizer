from gl.model import Model
import gl.shaders as shaders
from gl.gl import Renderer
import time

start_time = time.time()


models_dir = "../models"
textures_dir = models_dir + "/textures"
normals_dir = models_dir + "/normals"
out_dir = "../out"

width = 1920
height = 1080

rock = Model(f"../last/objs/rock_f.obj",
             translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
rock.load_texture(f"../last/textures/rock.bmp")
rock.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)

land = Model(f"../last/objs/land_f.obj",
             translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
land_small = Model(f"../last/objs/land_s.obj",
                   translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))

land.load_texture(f"../last/textures/land.bmp")
land_small.load_texture(f"../last/textures/land.bmp")
land.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)
land_small.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)

close_tables = Model(f"../last/objs/close_tables.obj",
                     translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
far_tables = Model(f"../last/objs/far_tables.obj",
                   translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))

sarcofago = Model(f"../last/objs/sarcofago.obj",
                  translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
sarcofago.load_texture(f"../last/textures/sarcofago.bmp")
sarcofago.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)


close_tables.load_texture(f"../last/textures/tables.bmp")
far_tables.load_texture(f"../last/textures/tables.bmp")
close_tables.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)
far_tables.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)

tree = Model(f"../last/objs/tree.obj",
             translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
tree.load_texture(f"../last/textures/tree_dark.bmp")
tree.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)

home = Model(f"../last/objs/home.obj",
             translate=(0, 0, -8), scale=(1, 1, 1), rotate=(0, 0, 0))
home.load_texture(f"../last/textures/casita_dark.bmp")
home.set_shaders(shaders.vertex_shader, shaders.gouraud_shader)

renderer = Renderer(width, height)
renderer.set_directional_light(-1, -1, -1)
renderer.set_clear_color(7/255, 116/255, 143/255)
renderer.clear()
renderer.look_at(cam_pos=(1, 5, 0), eye_pos=(0, 0, -7.5), rotateZ=0)


renderer.add_model(land_small)
renderer.add_model(home)

renderer.add_model(land)
renderer.add_model(rock)
renderer.add_model(close_tables)
renderer.add_model(far_tables)
renderer.add_model(sarcofago)
renderer.add_model(tree)

renderer.gl_render()
renderer.gl_finish(f"{out_dir}/new_{str(start_time).split('.')[0]}.bmp")

end_time = time.time()
print(f"Execution took {end_time - start_time:.2f} seconds to run.")
