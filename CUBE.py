# By: Krish Rajchal, and Rajesh Rajchal
# Krish Rajchal, and Rajesh Rajchal present
# CUBE!!!
# It is just a game that has a cone that you have to click.
# Then, you will win!!!

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from ursina.shaders import basic_lighting_shader as bls
from ursina.prefabs.trail_renderer import TrailRenderer as tr
from ursina.prefabs.health_bar import HealthBar as hb

application.asset_folder = application.asset_folder.parent

from random import randint as r

import math

from pyautogui import hotkey as ht

app = Ursina()

player=fpc(model='cube', collider='box', texture='white_cube',
    color=color.green,
    speed=30,
    eternal=True
    )

player_health = hb(max_value=100000,
                   value=100000,
                   position=(0, -700))

boss_health = hb(max_value=1000,
                 value=1000)

updater = Entity(pos=(1000000, -100000000, 10000000),
                 color=color.rgb(0, 0, 0, 0))

do = True

entitys = [i for i in range(1000)]

for i in range(len(entitys)):
    entitys[i] = Entity(model='sphere', color=color.red,
                   scale=1,
                   position=Vec3(r(-1000, 1000), 2, r(-1000, 1000)),
                   shader=bls)

tri = Entity(model='cone.obj',
                shader=bls,
                scale=5,
                color=color.gray,
                position=(5, 1, 0))

def pos3d(x1, y1, z1, x2, y2, z2, speed=.5):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    
    x = x1 + (x2-x1)/distance * speed
    y = y1 + (y2-y1)/distance * speed
    z = z1 + (z2-z1)/distance * speed
    
    return (x, y, z)

class game():
    def __init__(self):
        self.num = 2

    def clear(self):
        scene.clear()

    def rh(self):return '#{:02x}{:02x}{:02x}'.format(r(0, 255), r(0, 255), r(0, 255))
    
    def rs(self):shape = ['cube', 'cube_uv_top', 'sky_dome', 'sphere'];return shape[r(0, len(shape)-1)]

    def shaper(self):
        for x in range(100):
            Entity(model=self.rs(), texture='white_cube',
                   collider='box',
                   color=color.orange,
                   position=(r(-10000, 10000), .5, r(-10000, 10000)),
                   rotation=(r(0, 360), r(0, 360), r(0, 360)),
                   scale=(self.num, self.num, self.num),
                   shader=bls)
            self.num = r(2,5)

    def room(self, pos, fun):
        target = Entity(model='cube',
               scale=100,
               position=pos,
               color=color.rgb(257, 257, 257),
               shader=bls,
               collider='box')
        
        def b():
            x = target.x - player.x
            y = target.y - player.y
            z = target.z - player.z
            d = ((x**2) + (y**2) + (z**2)) ** .5
            if d > 5:
                fun()

        target.update = b

    def boss(self, player_ded, boss_ded):
        tr(target=tri)

        def face():
            def sub_health(duration):
                player_health.value -= 10
                
            def toInvoke():
                if distance(tri, player) <= 3.5:
                    invoke(sub_health, duration=100)
                    return
                
                tri.look_at(player)
                tri.position = pos3d(tri.x, tri.y, tri.z,
                                          player.x, player.y, player.z, 0.27)

            if player_health.value == 0:
                player_ded()

            if boss_health.value == 0:
                boss_ded()
                
            toInvoke()
            print(mouse.hovered_entity == tri)

        tri.update = face

def collide(i):
    x = player.x - entitys[i].x
    y = player.y - entitys[i].y
    z = player.z - entitys[i].z
    d = ((x**2) + (y**2) + (z**2)) ** .5
    if d < 2:
        destroy(entitys[i])
        player_health.value += 10
        
    '''
    if distance(player.position, entitys[i].position) < 2:
        destroy(entitys[i])
        player_health.value += 10
    '''

def col():
    for i in range(len(entitys)):
        collide(i)

def d():
    Entity(model='cube',
           scale=(1, 40, 30),
           position=Vec3(-135.1, 0, 34),
           color=color.rgb(257, 257, 257),
           shader=bls,
           collider='box')

def good():
    print('pihfndzb;niujshugbnpaongprboniapiouegpiuadfbpjapiehfoihnadfinboauigfoiuhaoignendraobadorgood')
    ht('alt', 'f4')

def bad():
    print('############################################################################################')
    ht('alt', 'f4')

def input(key):
    if mouse.hovered_entity == tri:
        if mouse.left == True:
            boss_health.value -= 10
        
a = game()
#a.shaper()
#a.boss(bad, good)

#for i in range(len(entitys)):
#    entitys[i].update = col

window.title = "CUBE"
window.borderless = False
window.vsync = False

Entity(model='plane', collider='box',
       color=color.blue,
       texture='white_cube',
       texture_scale=(10000,10000),
       scale=(10000,1,10000),
       eternal=True)

Sky()

app.run()
