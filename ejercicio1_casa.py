# ejercicio1_casa.py
# Exercise 1: stylized house composed only of DDA lines.
# Output: casa.png (600 x 500 px)
import math
from PIL import Image


def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Draw a line using the DDA algorithm (as presented in class)."""
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:  # both points coincide
        return
    x_inc = dx / pasos
    y_inc = dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Draw a rectangle outline: four DDA lines, one per side."""
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)  # top
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)  # right
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)  # bottom
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)  # left


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Draw a triangle outline: three DDA lines joining the vertices."""
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Draw the door: a rectangle plus a small knob (short line)."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    ym = (y0 + y1) // 2
    dda(pixels, x1 - 10, ym, x1 - 6, ym, color, ancho, alto)  # knob


def dibujar_ventana(pixels, x0, y0, lado, color, ancho, alto):
    """Draw a square window with a cross (4 sides + 2 inner lines)."""
    dibujar_rectangulo(pixels, x0, y0, x0 + lado, y0 + lado, color, ancho, alto)
    m = lado // 2
    dda(pixels, x0 + m, y0, x0 + m, y0 + lado, color, ancho, alto)
    dda(pixels, x0, y0 + m, x0 + lado, y0 + m, color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Draw a sun: n_rayos lines radiating from the center (polar coords)."""
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        x = cx + radio * math.cos(angulo)
        y = cy + radio * math.sin(angulo)  # y grows downward, symmetric anyway
        dda(pixels, cx, cy, round(x), round(y), color, ancho, alto)


def dibujar_piso(pixels, y, color, ancho, alto):
    """Draw the ground line across the whole image width."""
    dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


def dibujar_arbol(pixels, x, y_base, color_tronco, color_copa, ancho, alto):
    """Voluntary extension: tree = rectangular trunk + triangular crown."""
    dibujar_rectangulo(pixels, x - 10, y_base - 40, x + 10, y_base,
                       color_tronco, ancho, alto)
    dibujar_triangulo(pixels, (x - 35, y_base - 40), (x + 35, y_base - 40),
                      (x, y_base - 110), color_copa, ancho, alto)


def dibujar_chimenea(pixels, x0, x1, y_top, y_roof_left, y_roof_right,
                     color, ancho, alto):
    """Voluntary extension: chimney. Sides end exactly on the sloped roof."""
    dda(pixels, x0, y_top, x1, y_top, color, ancho, alto)              # top
    dda(pixels, x0, y_top, x0, y_roof_left, color, ancho, alto)        # left side
    dda(pixels, x1, y_top, x1, y_roof_right, color, ancho, alto)       # right side


def dibujar_humo(pixels, x, y, n_bocanadas, color, ancho, alto):
    """Voluntary extension: smoke as a rising zigzag of short DDA lines."""
    for k in range(n_bocanadas):
        # each puff drifts sideways following a sine wave while going up
        x0 = x + round(10 * math.sin(k))
        y0 = y - k * 14
        x1 = x + round(10 * math.sin(k + 1))
        y1 = y - (k + 1) * 14
        dda(pixels, x0, y0, x1, y1, color, ancho, alto)
        dda(pixels, x0 - 4, y0, x0 + 4, y0, color, ancho, alto)  # small puff mark


def dibujar_nube(pixels, cx, cy, color, ancho, alto):
    """Voluntary extension: cloud = three small polygons (many short lines)."""
    for dx, radio in [(-25, 18), (0, 25), (28, 17)]:
        n = 14
        for i in range(n):
            a0 = 2 * math.pi * i / n
            a1 = 2 * math.pi * (i + 1) / n
            dda(pixels,
                cx + dx + round(radio * math.cos(a0)), cy + round(radio * math.sin(a0)),
                cx + dx + round(radio * math.cos(a1)), cy + round(radio * math.sin(a1)),
                color, ancho, alto)


def dibujar_sol_degradado(pixels, cx, cy, radio, n_rayos, c_ini, c_fin, ancho, alto):
    """Voluntary extension: sun whose rays fade from c_ini to c_fin."""
    for i in range(n_rayos):
        t = i / (n_rayos - 1)
        color = tuple(round(a + (b - a) * t) for a, b in zip(c_ini, c_fin))
        angulo = 2 * math.pi * i / n_rayos
        dda(pixels, cx, cy,
            round(cx + radio * math.cos(angulo)), round(cy + radio * math.sin(angulo)),
            color, ancho, alto)


def dibujar_pasto_degradado(pixels, y_ini, y_fin, c_ini, c_fin, ancho, alto):
    """Voluntary extension: grass made of horizontal DDA lines with a vertical
    color gradient (light green at the horizon, dark green at the bottom)."""
    for y in range(y_ini, y_fin + 1):
        t = (y - y_ini) / (y_fin - y_ini)
        color = tuple(round(a + (b - a) * t) for a, b in zip(c_ini, c_fin))
        dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


# ---------------------------------------------------------------- main program
ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))  # light sky blue
pixels = imagen.load()

# Colors (one per element)
MARRON = (120, 70, 30)     # house body
ROJO = (200, 30, 30)       # roof
NEGRO = (40, 20, 10)       # door
AZUL = (20, 60, 200)       # windows
AMARILLO = (255, 200, 0)   # sun
VERDE = (20, 140, 40)      # ground and tree crowns

PISO_Y = 420

# Gradient grass first (so the ground line and house draw on top)
dibujar_pasto_degradado(pixels, PISO_Y, alto - 1, (120, 220, 90), (20, 100, 40), ancho, alto)
dibujar_piso(pixels, PISO_Y, VERDE, ancho, alto)
dibujar_rectangulo(pixels, 200, 280, 400, PISO_Y, MARRON, ancho, alto)
dibujar_triangulo(pixels, (180, 280), (420, 280), (300, 190), ROJO, ancho, alto)
dibujar_puerta(pixels, 275, 340, 325, PISO_Y, NEGRO, ancho, alto)
dibujar_ventana(pixels, 215, 305, 40, AZUL, ancho, alto)
dibujar_ventana(pixels, 345, 305, 40, AZUL, ancho, alto)
dibujar_sol_degradado(pixels, 520, 80, 50, 16, (255, 230, 0), (255, 120, 0), ancho, alto)
dibujar_chimenea(pixels, 350, 375, 200, 227, 246, ROJO, ancho, alto)
dibujar_humo(pixels, 362, 190, 5, (110, 110, 110), ancho, alto)
dibujar_nube(pixels, 110, 90, (255, 255, 255), ancho, alto)
dibujar_nube(pixels, 300, 55, (255, 255, 255), ancho, alto)
dibujar_arbol(pixels, 90, PISO_Y, MARRON, VERDE, ancho, alto)
dibujar_arbol(pixels, 500, PISO_Y, MARRON, VERDE, ancho, alto)

imagen.save("casa.png")
print("Saved casa.png")
