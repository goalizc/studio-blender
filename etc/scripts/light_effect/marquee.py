import bpy

ARGS = {
    "宽度": 10,
    "速度": 2,
    "轴": 0,
}

def decode(kv_str):
    return {k: float(v) for k, v in [p.split("=") for p in kv_str.split(",")]} if kv_str else {}

def get_default_palette():
    return [(1.0, 0.0, 0.0), (1.0, 0.5, 0.0), (1.0, 1.0, 0.0), (0.0, 1.0, 0.0),
            (0.0, 0.5, 1.0), (0.0, 0.0, 1.0), (0.5, 0.0, 1.0)]

def clamp(value, min_value=0.0, max_value=1.0):
    return max(min_value, min(max_value, value))

def interpolate_color(color1, color2, t):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    red = r1 + (r2 - r1) * t
    green = g1 + (g2 - g1) * t
    blue = b1 + (b2 - b1) * t
    red = clamp(red)
    green = clamp(green)
    blue = clamp(blue)
    return (red, green, blue)

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
        color = interpolate_color(color_palette[index1], color_palette[index2], t)
        return (*color, 1.0)

def calculate_intensity(args, second, position):
    return abs(position[int(args["轴"])] / args["宽度"] - second) / args["速度"] % 1.0

def marquee(**kwargs):
    args = decode(kwargs.get("args") or "") or ARGS
    second = kwargs.get('frame', 0) / bpy.context.scene.render.fps
    position = kwargs.get('position')
    if second is None or position is None:
        return (1.0, 1.0, 1.0, 1.0)
    return get_palette_color(calculate_intensity(args, second, position), get_default_palette())
