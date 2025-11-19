# perlin_simple.py
# Gera uma imagem 500x500 usando Perlin noise (implementação self-contained).
# pillow (pip install pillow)

from PIL import Image
import math
import random
import numpy as np

def fade(t):
    # fade function 6t^5 - 15t^4 + 10t^3
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(a, b, t):
    return a + t * (b - a)

def grad(hash, x, y):
    # usa 4 direções básicas
    h = hash & 3
    if h == 0:
        return  x + y
    elif h == 1:
        return -x + y
    elif h == 2:
        return  x - y
    else:
        return -x - y

class Perlin2D:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        # permutation table
        p = list(range(256))
        random.shuffle(p)
        self.p = p + p  # duplica para evitar overflow

    def noise(self, x, y):
        # encontra o "canto" da célula
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255

        # posições relativas dentro da célula
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        # fade curves
        u = fade(xf)
        v = fade(yf)

        # hashes dos cantos
        aa = self.p[self.p[xi] + yi]
        ab = self.p[self.p[xi] + yi + 1]
        ba = self.p[self.p[xi + 1] + yi]
        bb = self.p[self.p[xi + 1] + yi + 1]

        # gradientes e suas contribuições
        x1 = lerp(grad(aa, xf, yf),      grad(ba, xf - 1, yf),    u)
        x2 = lerp(grad(ab, xf, yf - 1),  grad(bb, xf - 1, yf - 1),u)
        value = lerp(x1, x2, v)

        # value tende a ficar aproximadamente na faixa [-1,1]
        return value

# --- gera imagem ---
def generate_perlin_image(width=500, height=500, scale=0.01, seed=None, filename="perlin.png"):
    perlin = Perlin2D(seed=seed)
    arr = np.zeros((height, width), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            n = perlin.noise(x * scale, y * scale)  # aproximadamente [-1,1]
            n = (n + 1.0) * 0.5  # transforma para [0,1]
            c = int(round(255 * max(0.0, min(1.0, n))))
            arr[y, x] = c

    img = Image.fromarray(arr, mode="L")  # "L" grayscale
    img.save(filename)
    print(f"Salvo: {filename}")

if __name__ == "__main__":
    generate_perlin_image(width=500, height=500, scale=0.01, seed=42, filename="perlin_selfcontained.png")
