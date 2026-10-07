# taller5g-unidad3-barrios

Tarea práctica de la Unidad III (Conversión por rastreo) de la materia Taller de Programación de 5.ª Generación I, Universidad Americana.

- **Alumno:** Federico Barrios
- **Docente:** Prof. Mgtr. Alberto F. Giménez Méndez

## Contenido

| Archivo | Descripción |
|---|---|
| `ejercicio1_casa.py` | Ejercicio 1: casa estilizada dibujada solo con líneas del algoritmo DDA. Genera `casa.png`. |
| `ejercicio2_roseta.py` | Ejercicio 2: rosetas geométricas dibujadas con el algoritmo de Bresenham. Genera las imágenes de roseta. |
| `casa.png` | Imagen de 600 × 500 px generada por el Ejercicio 1. |
| `roseta_12.png`, `roseta_24.png`, `roseta_36.png` | Rosetas de 700 × 700 px con N = 12, 24 y 36. |
| `roseta.png` | Copia de la roseta con N = 24 (nombre de salida pedido en el enunciado). |

## Cómo ejecutar

Requiere Python 3 y la biblioteca Pillow:

```bash
pip install pillow
python ejercicio1_casa.py
python ejercicio2_roseta.py
```

Los archivos se guardan en la carpeta desde donde se ejecutan los scripts. El segundo script tarda unos segundos porque también genera el GIF animado.

## Solución implementada

**Ejercicio 1 (DDA).** Se reutiliza `dda()` tal como se presentó en clase, sin modificar su firma. Cada elemento es una función separada que se apoya en ella: `dibujar_rectangulo` (4 líneas), `dibujar_triangulo` (3 líneas), `dibujar_puerta`, `dibujar_ventana`, `dibujar_sol` (bucle con coordenadas polares) y `dibujar_piso`. La puerta y las ventanas reutilizan el rectángulo. La composición usa 6 colores distintos.

**Ejercicio 2 (Bresenham).** Se reutiliza `bresenham()` sin modificar su firma. `generar_puntos_circulo(cx, cy, radio, n)` devuelve n puntos equiespaciados con `math.cos` y `math.sin`, y `dibujar_roseta(pixels, puntos, ancho, alto)` conecta cada par de puntos una sola vez (para N = 24 son 276 líneas). El color de cada línea sale de un tono HSV calculado a partir de los índices de sus extremos, lo que produce el gradiente.

## Extensiones voluntarias

**Ejercicio 1**
- Árboles (tronco rectangular y copa triangular).
- Nubes compuestas por múltiples líneas cortas.
- Chimenea con humo en zigzag.
- Gradientes de color en los rayos del sol (de amarillo a naranja) y en el pasto (de verde claro a oscuro).

**Ejercicio 2**
- Cuarta roseta que conecta cada punto solo con el que está 5 posiciones adelante: `roseta_24_salto5.png`.
- Fondo azul oscuro con líneas en tonos naranjas, que son su color complementario: `roseta_24_complementaria.png`.
- Animación `rosetas.gif` con 20 rosetas, con N creciente de 5 a 24.