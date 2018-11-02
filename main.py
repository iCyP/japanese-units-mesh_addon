"""
Copyright (c) 2018 iCyP
Released under the MIT license
https://opensource.org/licenses/mit-license.php

"""


import bpy
import bmesh
from collections import OrderedDict


def rectangle(xy, add_origin):
    x = xy[0]
    y = xy[1]
    return ((0, 0, 0), (0, y, 0), (x, y, 0), (x, 0, 0))


def make_rect_obj(name, rect):
    m = bpy.data.meshes.new(name)
    m.from_pydata(rect, [], [[0, 1, 2, 3]])
    obj = bpy.data.objects.new(name, m)
    bpy.context.scene.objects.link(obj)
    obj.location = bpy.context.scene.cursor_location


def make_rect_mesh(name, rect):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    vlist = []
    for v in rect:
        vi = bm.verts.new(v)
        for i in range(3):
            vi.co[i] = vi.co[i] + bpy.context.scene.cursor_location[i] - bpy.context.active_object.location[i]
        vlist.append(vi)
    bm.faces.new(vlist)
    bmesh.update_edit_mesh(bpy.context.active_object.data)


def make_mesh(base, adapt):
    make_rect_obj(adapt, rectangle(unitdic[base][adapt], False))
    return


def add_mesh(base, adapt):
    make_rect_mesh(adapt, rectangle(unitdic[base][adapt], True))
    return


sun = 1/33
_syaku = 10*sun

unitdic = OrderedDict(
    (
        (
            "paperA",
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
            )
        ),

        (
            "paperB",
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
            )
        ),

        (
            "tatami",
            OrderedDict(
                (
                    ["Nishi(L)", (1.91, 0.955)],
                    ["Nishi(L) Half", (0.955, 0.955)],
                    ["Higashi(M)", (1.76, 0.878)],
                    ["Higashi(M) Half", (0.878, 0.878)],
                    ["Danchi(S)", (1.70, 0.85)],
                    ["Danchi(S) Half", (0.85, 0.85)]
                )
            )
        ),


        (
            "pillar",
            OrderedDict(
                (
                    ["105mm (≒3.5寸)", (0.105, 0.105)],
                    ["120mm (≒4.0寸)", (0.120, 0.120)]
                )
            )
        ),

        (
            "尺(syaku)",
            OrderedDict(
                (
                    ["1尺(syaku) ≒30cm", (_syaku, _syaku)],
                    ["3尺(syaku) ≒90cm", (3*_syaku, 3*_syaku)],
                    ["6尺(syaku) ≒180cm", (6*_syaku, 6*_syaku)],
                    ["8尺(syaku) ≒240cm", (8*_syaku, 8*_syaku)]
                )
            )
        )

    )
)
