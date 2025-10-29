import bpy
import functools
import numpy as np
import sys

BLACK = (0.0, 0.0, 0.0, 1.0)

def ARGS(args):
    def decorator(func):
        setattr(sys.modules[func.__module__], f"ARGS_{func.__name__.upper()}", args)
        return functools.wraps(func)(lambda *a, **b: func(*a, **b))
    return decorator

def decode(kv_str):
    return {k: float(v) for k, v in [p.split("=") for p in kv_str.split(",")]} if kv_str else {}

def get_default_palette():
    return [(1.0, 0.0, 0.0), (1.0, 0.5, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
            (0.0, 0.5, 1.0), (0.0, 0.0, 1.0), (0.5, 0.0, 1.0)]

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))

def interpolate_color(color1, color2, t):
    r1, g1, b1 = color1[:3]
    r2, g2, b2 = color2[:3]
    red = r1 + (r2 - r1) * t
    green = g1 + (g2 - g1) * t
    blue = b1 + (b2 - b1) * t
    red = clamp(red)
    green = clamp(green)
    blue = clamp(blue)
    return (red, green, blue, 1.0)

def get_palette_color(intensity, color_palette):
    palette_size = len(color_palette)
    if palette_size == 0:
        return (1.0, 1.0, 1.0, 1.0)
    elif palette_size == 1:
        r, g, b = color_palette[0]
        return (r, g, b, 1.0)
    else:
        scaled_intensity = intensity * (palette_size - 1)
        index1 = int(scaled_intensity)
        index2 = min(index1 + 1, palette_size - 1)
        t = scaled_intensity - index1
        return interpolate_color(color_palette[index1], color_palette[index2], t)


@ARGS({"宽度": 10, "速度": 2, "轴": 0, })
def 跑马灯(**kwargs):
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    args = decode(kwargs["args"])
    intensity = (kwargs['position'][int(args["轴"])] - seconds * args["速度"]) % args["宽度"] / args["宽度"]
    return intensity if kwargs["is_color_ramp"] else get_palette_color(intensity, get_default_palette())


@ARGS({"宽度": 10, "速度": 2, })
def 波浪(**kwargs):
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    args = decode(kwargs["args"])
    dist = np.linalg.norm(np.subtract(kwargs['position'], kwargs['center']))
    if (dist - seconds * args["速度"]) % (args["宽度"] * 2) < args["宽度"]:
        intensity = clamp(dist / kwargs['maxdist'])
        return intensity if kwargs["is_color_ramp"] else get_palette_color(intensity, get_default_palette())
    return -1.0 if kwargs["is_color_ramp"] else BLACK


gLastIndexes, gIndexes, gSeed = None, None, None

@ARGS({"间隔": 0.5, "黑色": 0.0, })
def 闪烁(**kwargs):
    global gLastIndexes, gIndexes, gSeed
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    drone_index = kwargs['drone_index']
    drone_count = kwargs['drone_count']
    args = decode(kwargs["args"])

    seed = int(1 + seconds / args["间隔"])
    if seed != gSeed:
        if gSeed is not None:
            gLastIndexes = gIndexes.copy()
        else:
            np.random.seed(seed - 1)
            gLastIndexes = np.arange(drone_count)
            np.random.shuffle(gLastIndexes)
        gSeed = seed
        np.random.seed(gSeed)
        gIndexes = np.arange(drone_count)
        np.random.shuffle(gIndexes)

    np.random.seed(seed + drone_index * 10081)
    intensity = np.random.random()

    if kwargs["is_color_ramp"]:
        return -1.0 if drone_index in gIndexes[:int(args["黑色"]*drone_count)] else intensity

    b1 = drone_index in gLastIndexes[:int(args["黑色"]*drone_count)]
    b2 = drone_index in gIndexes[:int(args["黑色"]*drone_count)]
    np.random.seed(seed - 1 + drone_index * 10081)
    c1 = BLACK if b1 else get_palette_color(np.random.random(), get_default_palette())
    c2 = BLACK if b2 else get_palette_color(intensity, get_default_palette())

    return interpolate_color(c1, c2, seconds % args["间隔"] / args["间隔"])
