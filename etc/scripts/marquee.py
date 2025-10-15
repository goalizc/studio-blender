#!/usr/bin/env python

LAYER = 10
SPEED = 2
AXIS  = 0

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

def calculate_intensity(position, second):
    return abs(position[AXIS] / LAYER - second) / SPEED % 1.0

def marquee(**kwargs):
    position = kwargs.get('position')
    second = kwargs.get('second')
    if position is None or second is None:
        return (1.0, 1.0, 1.0, 1.0)
    return get_palette_color(calculate_intensity(position, second), get_default_palette())
