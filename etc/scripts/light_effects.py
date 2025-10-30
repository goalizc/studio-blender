import bpy
import numpy as np
import sys

BLACK = (0.0, 0.0, 0.0, 1.0)

class ColorRamp:
    def __init__(self):
        self.palette = ((1.0, 0.0, 0.0), (1.0, 0.5, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
                        (0.0, 0.5, 1.0), (0.0, 0.0, 1.0), (0.5, 0.0, 1.0))
        self.num_points = len(self.palette)

    @staticmethod
    def interpolate_color(c1, c2, t):
        r1, g1, b1 = c1[:3]
        r2, g2, b2 = c2[:3]
        r = np.clip(r1 + (r2 - r1) * t, 0.0, 1.0)
        g = np.clip(g1 + (g2 - g1) * t, 0.0, 1.0)
        b = np.clip(b1 + (b2 - b1) * t, 0.0, 1.0)
        return (r, g, b, 1.0)

    def evaluate(self, intensity):
        if self.num_points == 0:
            return (1.0, 1.0, 1.0, 1.0)
        if self.num_points == 1:
            r, g, b = self.palette[0]
            return (r, g, b, 1.0)
        scaled = intensity * (self.num_points - 1)
        index1 = int(scaled)
        index2 = min(index1 + 1, self.num_points - 1)
        return self.interpolate_color(self.palette[index1], self.palette[index2], scaled - index1)

color_ramp = ColorRamp()

def ARGS(mark, args):
    assert mark in ("FN", "CR")
    def decorator(func):
        funcname = f"{mark}_{func.__name__}"
        setattr(sys.modules[func.__module__], funcname, func)
        setattr(sys.modules[func.__module__], f"ARGS_{funcname}", args)
        return None
    return decorator

def get_color_ramp(kwargs):
    return kwargs["color_ramp"] if kwargs["use_color_ramp"] else color_ramp

def get_args(args, names):
    return [args[name] for name in names]

@ARGS("CR", {"宽度": 10, "速度": 2, "轴": 0, })
def 跑马灯(**kwargs):
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    width, speed, axis = get_args(kwargs["args"], ("宽度", "速度", "轴"))
    return (kwargs['position'][int(axis)] - seconds * speed) % width / width

@ARGS("FN", {"宽度": 10, "速度": 2, "轴": 0, })
def 跑马灯(**kwargs):
    return get_color_ramp(kwargs).evaluate(CR_跑马灯(**kwargs))

@ARGS("FN", {"宽度": 10, "速度": 2, })
def 波浪(**kwargs):
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    width, speed = get_args(kwargs["args"], ("宽度", "速度"))
    dist = np.linalg.norm(np.subtract(kwargs['position'], kwargs['center']))
    if (dist - seconds * speed) % (width * 2) < width:
        return get_color_ramp(kwargs).evaluate(dist / kwargs['maxdist'])
    return BLACK

gLastIndexes, gIndexes, gSeed = None, None, None

@ARGS("FN", {"间隔": 0.5, "黑色": 0.0, })
def 闪烁(**kwargs):
    global gLastIndexes, gIndexes, gSeed
    seconds = kwargs['frame'] / bpy.context.scene.render.fps
    drone_index = kwargs['drone_index']
    drone_count = kwargs['drone_count']
    interval, black_scale = get_args(kwargs["args"], ("间隔", "黑色"))

    seed = int(1 + seconds / interval)
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

    color_ramp = get_color_ramp(kwargs)
    b1 = drone_index in gLastIndexes[:int(black_scale*drone_count)]
    b2 = drone_index in gIndexes[:int(black_scale*drone_count)]
    np.random.seed(seed + drone_index * 10081 - 1)
    c1 = BLACK if b1 else color_ramp.evaluate(np.random.random())
    np.random.seed(seed + drone_index * 10081)
    c2 = BLACK if b2 else color_ramp.evaluate(np.random.random())

    return ColorRamp.interpolate_color(c1, c2, seconds % interval / interval)
