"""
Copyright (c) 2018 iCyP
Released under the MIT license
https://opensource.org/licenses/mit-license.php

"""


import bpy
import bmesh
from collections import OrderedDict
from math import sqrt

def rectangle(xy, dir):
    x = xy[0]
    y = xy[1]
    if dir == "xy":
        return ((-x/2, -y/2, 0), (-x/2, y/2, 0), (x/2, y/2, 0), (x/2, -y/2, 0))
    elif dir == "xz":
        return ((-x/2, 0, -y/2), (-x/2, 0, y), (x/2, 0, y), (x/2, 0, -y/2))


def make_rect_obj(name, rect_points):
    m = bpy.data.meshes.new(name)
    m.from_pydata(rect_points, [], [[0, 1, 2, 3]])
    obj = bpy.data.objects.new(name, m)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = bpy.context.scene.cursor.location


def make_rect_mesh(name, rect_points):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    vlist = []
    for v in rect_points:
        vi = bm.verts.new(v)
        for i in range(3):
            vi.co[i] = vi.co[i] + bpy.context.scene.cursor.location[i] - \
                bpy.context.active_object.location[i]
        vlist.append(vi)
    bm.faces.new(vlist)
    bmesh.update_edit_mesh(bpy.context.active_object.data)

def cubic(xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]
    return (
        (-x/2,-y/2,0),
        (-x/2,y/2,0),
        (x/2,y/2,0),
        (x/2,-y/2,0),

        (-x/2,-y/2,z),
        (-x/2,y/2,z),
        (x/2,y/2,z),
        (x/2,-y/2,z),
    )

cube_loop = [
    [0,1,2,3],
    [4,5,6,7],
    [0,1,5,4],
    [2,3,7,6],
    [1,2,6,5],
    [0,3,7,4]
]

def make_cubic_obj(name, cubec_points):
    m = bpy.data.meshes.new(name)
    m.from_pydata(cubec_points, [], cube_loop)
    obj = bpy.data.objects.new(name, m)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = bpy.context.scene.cursor.location


def make_cubic_mesh(name,cubec_points):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    vlist = []
    for v in cubec_points:
        vi = bm.verts.new(v)
        for i in range(3):
            vi.co[i] = vi.co[i] + bpy.context.scene.cursor.location[i] - \
                bpy.context.active_object.location[i]
        vlist.append(vi)

    for cl in cube_loop:
        bm.faces.new([vlist[i] for i in cl])
    bm.normal_update()
    bmesh.update_edit_mesh(bpy.context.active_object.data)

from math import sin,cos,radians
def make_cylinder_obj(name,radius,width):
    ring_a = [(0,sin(radians(t*10))*radius,cos(radians(t*10))*radius) for t in range(36)]
    ring_b = [(width,sin(radians(t*10))*radius,cos(radians(t*10))*radius) for t in range(36)]
    ring_a.extend(ring_b)
    cylinder_points = ring_a
    cylinder_index = [list(range(36)),list(range(36,72))]
    for i in range(35):
        cylinder_index.append([i,i+1,i+37,i+36])
    cylinder_index.append([35,0,36,71])
    m = bpy.data.meshes.new(name)
    m.from_pydata(cylinder_points, [], cylinder_index)
    obj = bpy.data.objects.new(name, m)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = bpy.context.scene.cursor.location

def make_cubic_mesh(name,radius,width):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    ring_a = []
    for t in range(36):
        v = (0,sin(radians(t*10))*radius,cos(radians(t*10))*radius)
        vi = bm.verts.new(v)
        for i in range(3):
            vi.co[i] = vi.co[i] + bpy.context.scene.cursor.location[i] - \
                bpy.context.active_object.location[i]
        ring_a.append(vi)
    ring_b = []
    for t in range(36):
        v = (width,sin(radians(t*10))*radius,cos(radians(t*10))*radius)
        vi = bm.verts.new(v)
        for i in range(3):
            vi.co[i] = vi.co[i] + bpy.context.scene.cursor.location[i] - \
                bpy.context.active_object.location[i]
        ring_b.append(vi)
    
    bm.faces.new(ring_a)
    bm.faces.new(ring_b)
    ring_a.extend(ring_b)
    rim_index = []
    for i in range(35):
        rim_index.append([i,i+1,i+37,i+36])
    rim_index.append([35,0,36,71])
    for index in rim_index:
        bm.faces.new([ring_a[id] for id in index])

    bm.normal_update()
    bmesh.update_edit_mesh(bpy.context.active_object.data)

def make_mesh(base, adapt):
    if unitdic[base][1] == "xyz":
        make_cubic_obj(adapt,cubic(unitdic[base][0][adapt]))
    elif unitdic[base][1] == "cylinder":
        make_cylinder_obj(adapt,unitdic[base][0][adapt][1]/2,unitdic[base][0][adapt][0])
    else:
        make_rect_obj(adapt, rectangle(unitdic[base][0][adapt], unitdic[base][1]))
    return


def add_mesh(base, adapt):
    if unitdic[base][1] == "xyz":
        make_cubic_mesh(adapt,cubic(unitdic[base][0][adapt]))
    elif unitdic[base][1] == "cylinder":
        make_cubic_mesh(adapt,unitdic[base][0][adapt][1]/2,unitdic[base][0][adapt][0])
    else:
        make_rect_mesh(adapt, rectangle(unitdic[base][0][adapt], unitdic[base][1]))
    return


sun = 1/33  # 寸
_syaku = 10 * sun
inti = 0.0254 #cm

unitdic = OrderedDict(
    (
        (
            "paperA",
            [
                OrderedDict(
                    (
                        ["A6", (0.105, 0.148)],
                        ["A5", (0.148, 0.210)],
                        ["A4", (0.210, 0.297)],
                        ["A3", (0.297, 0.420)],
                        ["A2", (0.420, 0.594)],
                        ["A1", (0.594, 0.841)],
                        ["A0", (0.841, 1.189)]
                    )
                ), "xy"
            ]
        ),

        (
            "paperB", [
                OrderedDict(
                    (
                        ["B6", (0.128, 0.182)],
                        ["B5", (0.182, 0.257)],
                        ["B4", (0.257, 0.364)],
                        ["B3", (0.364, 0.515)],
                        ["B2", (0.515, 0.728)],
                        ["B1", (0.728, 1.030)],
                        ["B0", (1.030, 1.456)]
                    )
                ),
                "xy"
            ]
        ),

        (
            "tatami", [
                OrderedDict(
                    (
                        ["Nishi(L)", (1.91, 0.955)],
                        ["Nishi(L) Half", (0.955, 0.955)],
                        ["Higashi(M)", (1.76, 0.878)],
                        ["Higashi(M) Half", (0.878, 0.878)],
                        ["Danchi(S)", (1.70, 0.85)],
                        ["Danchi(S) Half", (0.85, 0.85)]
                    )
                ),
                "xy"
            ]
        ),
        (
            "Door", [
                OrderedDict(
                    (
                        ["Husuma(襖)", (0.9,1.8)],
                        ["Indoor(室内) S", (0.734, 1.983)],
                        ["Indoor(室内) L", (0.868, 1.983)],
                        ["Entrance(玄関) S", (0.78, 2)],
                        ["Entrance(玄関) L", (0.94, 2.312)]
                    )
                ),
                "xz"
            ]
        ),

        (
            "Pillar", [
                OrderedDict(
                    (
                        ["105mm角 (≒3.5寸)", (0.105, 0.105)],
                        ["120mm角 (≒4.0寸)", (0.120, 0.120)]
                    )
                ),
                "xy"
            ]
        ),
        (
            "Bed", [
                OrderedDict(
                    (
                        ["Single", (0.97, 1.95)],
                        ["SemiDouble", (1.20,1.95)],
                        ["Double", (1.40, 1.95)],
                        ["Queen", (1.60, 1.95)],
                        ["King", (1.80, 1.95)],
                    )
                ),
                "xy"
            ]
        ),
        (
            "TV", [
                OrderedDict(
                    (
                        ["21.5in", (21.5*inti/sqrt(337) * 16, 21.5*inti/sqrt(337) * 9)], 
                        ["23.8in", (23.8*inti/sqrt(337) * 16, 23.8*inti/sqrt(337) * 9)],
                        ["31.0in", (31*inti/sqrt(337) * 16, 31*inti/sqrt(337) * 9)],
                        ["43.0in", (43*inti/sqrt(337) * 16, 43*inti/sqrt(337) * 9)],
                        ["49.0in", (49*inti/sqrt(337) * 16, 49*inti/sqrt(337) * 9)],
                        ["55.0in", (55*inti/sqrt(337) * 16, 55*inti/sqrt(337) * 9)],
                    )
                ),
                "xz"
            ]
        ),
        (
            "尺(syaku)", [
                OrderedDict(
                    (
                        ["1尺(syaku) ≒30cm", (_syaku, _syaku)],
                        ["3尺(syaku) ≒90cm", (3*_syaku, 3*_syaku)],
                        ["6尺(syaku) ≒180cm", (6*_syaku, 6*_syaku)],
                        ["8尺(syaku) ≒240cm", (8*_syaku, 8*_syaku)]
                    )
                ),
                "xy"
            ]
        ),
        (
            "Car", [
                OrderedDict(
                    (
                        ["KEI4", (1.48,3.4,2.0)],
                        ["3Num",(1.7,4.7,2.0)],
                        ["GTlike",(1.9,5.0,1.4)]
                    )
                ),
                "xyz"
            ]
        ),
        (
            "Tire", [
                OrderedDict(
                    (
                        ["KEI4", (0.165,0.562)], #w,2r
                        ["Normal Basic",(0.195,0.634)],
                        ["Normal Van",(0.195,0.693)],
                        ["Normal Sports",(0.245,0.656)],
                        ["GT",(0.300,0.604)],
                    )
                ),
                "cylinder"
            ]
        )


    )
)
