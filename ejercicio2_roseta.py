# ejercicio2_roseta.py
# Exercise 2: geometric rosettes drawn only with Bresenham lines.
# Output: roseta_12.png, roseta_24.png, roseta_36.png, roseta.png
import colorsys
import math
from PIL import Image


def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Generalized Bresenham, integer arithmetic (as presented in class)."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


def generar_puntos_circulo(cx, cy, radio, n):
    """Return n equally spaced points on an imaginary circle."""
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        # round() instead of int() avoids a slight bias toward the center
        x = cx + round(radio * math.cos(angulo))
        y = cy + round(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


def color_gradiente(i, j, n, h_min=0.0, h_max=1.0):
    """Map the chord (i, j) to a color using the index sum as hue.
    h_min/h_max restrict the hue range (default: full rainbow)."""
    t = (i + j) / (2 * n - 3) if n > 1 else 0.0
    h = h_min + (h_max - h_min) * t
    r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))


def dibujar_roseta(pixels, puntos, ancho, alto, h_min=0.0, h_max=1.0):
    """Connect every pair of points with a Bresenham line + color gradient."""
    n = len(puntos)
    lineas = 0
    for i in range(n):
        for j in range(i + 1, n):  # each pair exactly once
            color = color_gradiente(i, j, n, h_min, h_max)
            bresenham(pixels, puntos[i][0], puntos[i][1],
                      puntos[j][0], puntos[j][1], color, ancho, alto)
            lineas += 1
    return lineas


def dibujar_roseta_salto(pixels, puntos, salto, ancho, alto):
    """Voluntary extension: connect each point only with the one `salto` ahead."""
    n = len(puntos)
    for i in range(n):
        j = (i + salto) % n
        bresenham(pixels, puntos[i][0], puntos[i][1],
                  puntos[j][0], puntos[j][1],
                  color_gradiente(min(i, j), max(i, j), n), ancho, alto)


# ---------------------------------------------------------------- main program
ANCHO, ALTO = 700, 700

for n in [12, 24, 36]:
    img = Image.new("RGB", (ANCHO, ALTO), "black")  # black makes colors pop
    pixels = img.load()
    puntos = generar_puntos_circulo(350, 350, 300, n)
    lineas = dibujar_roseta(pixels, puntos, ANCHO, ALTO)
    img.save(f"roseta_{n}.png")
    if n == 24:
        img.save("roseta.png")  # required default output name
    print(f"N={n}: {lineas} lines -> roseta_{n}.png")

# Voluntary extension: 4th rosette, skipping 5 points
img = Image.new("RGB", (ANCHO, ALTO), "black")
pixels = img.load()
dibujar_roseta_salto(pixels, generar_puntos_circulo(350, 350, 300, 24), 5, ANCHO, ALTO)
img.save("roseta_24_salto5.png")
print("Saved roseta_24_salto5.png")

# Voluntary extension: complementary colors.
# Dark blue background (hue ~0.66) with lines in the orange/yellow range
# (hue 0.05 to 0.15), which is the complement of blue.
img = Image.new("RGB", (ANCHO, ALTO), (10, 15, 70))
pixels = img.load()
dibujar_roseta(pixels, generar_puntos_circulo(350, 350, 300, 24), ANCHO, ALTO, 0.05, 0.15)
img.save("roseta_24_complementaria.png")
print("Saved roseta_24_complementaria.png")

# Voluntary extension: animated GIF, 20 rosettes with N growing from 5 to 24.
frames = []
for n in range(5, 25):
    frame = Image.new("RGB", (ANCHO, ALTO), "black")
    dibujar_roseta(frame.load(), generar_puntos_circulo(350, 350, 300, n), ANCHO, ALTO)
    frames.append(frame)
frames[0].save("rosetas.gif", save_all=True, append_images=frames[1:],
               duration=250, loop=0)
print(f"Saved rosetas.gif ({len(frames)} frames)")
