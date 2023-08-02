# By: Krish Rajchal, and Rajesh Rajchal
# Krish Rajchal, and Rajesh Rajchal present
# CUBE!!!
# It is just a game that has a cone that you have to click.
# Then, you will win!!!

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.trail_renderer import TrailRenderer as tr
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

application.asset_folder = application.asset_folder.parent

from random import randint as r

import math

app = Ursina()

player=fpc(model='cube', collider='box', texture='white_cube',
    color=color.green,
    speed=30,
    eternal=True
    )

do = True

point = Entity(model='sphere', color=color.red,
               scale=1,
               position=Vec3(1, 2, 0),
               shader=bls)

def pos3d(x1, y1, z1, x2, y2, z2, speed=.5):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    
    x = x1 + (x2-x1)/distance * speed
    y = y1 + (y2-y1)/distance * speed
    z = z1 + (z2-z1)/distance * speed
    
    return (x, y, z)

def done():
    global do
    if do:
        text = """
        Well, you did it! You killed the already easy boss by
        clicking the boss. Note: This is still not done, I
        was not able to finish this in time since there was so
        much to add to this game. 
        """
        root = ScrolledText(master=tk.Tk(), height=15, width=35)
        root.insert("end", text)
        root.winfo_toplevel().title("Finished")
        root.config(state='disabled')
        root.pack(fill='both', side="left", expand=True)
        root.focus_set()
        do = False

class game():
    def __init__(self):
        self.num = 2
        self.tri = Entity(model='cone.obj',
                     collider='box',
                     shader=bls,
                     scale=5,
                     position=(5, 1, 0))

    def clear(self):
        scene.clear()

    def rh(self):return '#{:02x}{:02x}{:02x}'.format(r(0, 255), r(0, 255), r(0, 255))
    
    def rs(self):shape = ['cube', 'cube_uv_top', 'sky_dome', 'sphere'];return shape[r(0, len(shape)-1)]

    def shaper(self):
        for x in range(1500):
            Entity(model=self.rs(), texture='white_cube',
                   collider='box',
                   color=color.orange,
                   position=(r(-1000, 1000), .5, r(-1000, 1000)),
                   rotation=(r(0, 360), r(0, 360), r(0, 360)),
                   scale=(self.num, self.num, self.num),
                   shader=bls)
            self.num = r(2,5)

    def room(self, pos, fun):
        target = Entity(model='sphere',
                   position=pos)

        # Left side of the house
        Entity(model='cube',
               scale=(100, 100, 1),
               position=(pos[0]+50, pos[1], pos[2]),
               color=color.rgb(257, 257, 257),
               shader=bls,
               collider='box')

        Entity(model='cube',
               scale=())
        
        def b():
            x = target.x - player.x
            y = target.y - player.y
            z = target.z - player.z
            d = ((x**2) + (y**2) + (z**2)) ** .5
            if d > 143:
                fun()

        target.update = b

    def boss(self):
        tr(target=self.tri)

        def face():
            def toInvoke():
                if distance(self.tri, player) <= 3.5:
                    return True
                
                self.tri.look_at(player)
                self.tri.position = pos3d(self.tri.x, self.tri.y, self.tri.z,
                                          player.x, player.y, player.z, 0.27)
                
            toInvoke()
            if toInvoke():
                done()
                return

        self.tri.update = face

    def input(self, key):
        if self.tri.hovered:
            if key == 'left mouse down':
                done()
                destroy(self.tri)
                raise
                

def updat():
    x = player.x - point.x
    y = player.y - point.y
    z = player.z - point.z
    d = ((x**2) + (y**2) + (z**2)) ** .5
    if d < 2:
        destroy(point)

def d():
    Entity(model='cube',
           scale=(1, 40, 30),
           position=Vec3(-135.1, 0, 34),
           color=color.rgb(257, 257, 257),
           shader=bls,
           collider='box')
        
a = game()
#a.room(Vec3(0, 0, 0), d)
a.shaper()
a.boss()

point.update = updat

window.title = "CUBE"
window.borderless = False
window.vsync = False

Entity(model='plane', collider='box',
       color=color.blue,
       texture='white_cube',
       texture_scale=(1000,1000),
       scale=(1000,1,1000),
       eternal=True)

Sky()

app.run()

