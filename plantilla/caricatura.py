"""Escena de caricatura (experimento, 23-nov-2026).
Personajes propios y originales, dibujados con código (sin imágenes externas):
  FLAMI: flamenco rosa con lentes oscuros.   GUS: cocodrilo verde y nervioso.
Cada escena "cartoon" lleva "accion" (la coreografía) y "burbujas" (texto en pantalla).
"""
import math
from PIL import Image, ImageDraw

OUT = (26, 16, 48)
CREAM = (255, 241, 234); ORANGE = (255, 179, 107); PINK = (255, 107, 139)
PINK_L = (255, 160, 182); PINK_D = (226, 74, 115)
GREEN = (96, 205, 134); GREEN_D = (58, 160, 100); BELLY = (255, 232, 176)
SS = 2                                 # superresolución del dibujo


class Lienzo:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.im = Image.new('RGBA', (w * SS, h * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts): return [(x * SS, y * SS) for x, y in pts]

    def elipse(self, cx, cy, rx, ry, fill, ow=6):
        self.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS],
                       fill=fill, outline=OUT if ow else None, width=ow * SS)

    def poli(self, pts, fill, ow=6):
        p = self.P(pts)
        self.d.polygon(p, fill=fill)
        if ow:
            self.d.line(p + [p[0]], fill=OUT, width=ow * SS, joint='curve')
            for x, y in p: self.d.ellipse([x - ow * SS / 2, y - ow * SS / 2, x + ow * SS / 2, y + ow * SS / 2], fill=OUT)

    def rrect(self, x0, y0, x1, y1, r, fill, ow=6):
        self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS, fill=fill,
                                 outline=OUT if ow else None, width=ow * SS)

    def linea(self, pts, w, fill, ow=0):
        p = self.P(pts)
        if ow: self.d.line(p, fill=OUT, width=(w + 2 * ow) * SS, joint='curve')
        self.d.line(p, fill=fill, width=w * SS, joint='curve')
        if ow:
            for x, y in (p[0], p[-1]): self.d.ellipse([x - (w / 2 + ow) * SS, y - (w / 2 + ow) * SS, x + (w / 2 + ow) * SS, y + (w / 2 + ow) * SS], fill=OUT)
        for x, y in (p[0], p[-1]): self.d.ellipse([x - w / 2 * SS, y - w / 2 * SS, x + w / 2 * SS, y + w / 2 * SS], fill=fill)

    def curva(self, pts, w, fill, ow=6, n=40):
        """Línea gruesa suave que pasa por puntos de control (Bézier)."""
        def bez(t):
            q = list(pts)
            while len(q) > 1: q = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(q, q[1:])]
            return q[0]
        path = [bez(i / n) for i in range(n + 1)]
        for r, col in ((w / 2 + ow, OUT), (w / 2, fill)):
            if r == w / 2 + ow and not ow: continue
            for x, y in path:
                self.d.ellipse([(x - r) * SS, (y - r) * SS, (x + r) * SS, (y + r) * SS], fill=col)

    def fin(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


# ------------------------------------------------------------------ FLAMI
def flami(emocion='feliz', boca=0., gafas=1., cuello=0., pico=0.):
    """Sprite 440x620, anclado en los pies (220, 610). Mira a la derecha."""
    c = Lienzo(440, 620)
    # patas
    for px in (190, 250):
        c.linea([(px, 420), (px - 6, 520), (px + 4, 600)], 11, PINK_D, ow=4)
        c.poli([(px - 6, 603), (px + 44, 603), (px + 30, 586), (px + 2, 590)], ORANGE, ow=4)
    # cola y cuerpo
    c.poli([(95, 330), (45, 365), (70, 395), (125, 392)], PINK_D)
    c.elipse(215, 360, 118, 82, PINK)
    c.elipse(190, 368, 66, 44, PINK_L)
    c.poli([(125, 378), (100, 410), (160, 405)], PINK_D, ow=4)
    # cuello (S)
    sw = cuello * 14
    cx0, cy0 = 270, 320
    hx, hy = 288 + sw, 128
    c.curva([(cx0, cy0), (215 - sw, 250), (330 + sw, 200), (hx, hy + 30)], 38, PINK, ow=6)
    # cabeza
    c.elipse(hx, hy, 56, 52, PINK)
    # pico
    ab = pico * 14
    c.poli([(hx + 40, hy - 12), (hx + 128, hy + 14 - ab * .2), (hx + 112, hy + 40 + ab), (hx + 38, hy + 34)], ORANGE)
    c.poli([(hx + 104, hy + 6), (hx + 128, hy + 14 - ab * .2), (hx + 112, hy + 40 + ab), (hx + 96, hy + 30)], OUT, ow=0)
    # ojos / lentes
    ey = hy - 8
    if gafas < .5 or emocion == 'asombro':
        for ex in (hx + 6, hx + 44):
            c.elipse(ex, ey, 17, 19, CREAM, ow=4)
            c.elipse(ex + 3, ey + 2, 7, 8, OUT, ow=0)
    gy = ey - gafas * 0 + (1 - gafas) * -58
    rot = (1 - gafas) * 0
    c.rrect(hx - 14, gy - 16, hx + 26, gy + 22, 14, (34, 22, 60), ow=5)
    c.rrect(hx + 28, gy - 16, hx + 68, gy + 22, 14, (34, 22, 60), ow=5)
    c.linea([(hx + 24, gy - 6), (hx + 30, gy - 6)], 6, OUT)
    c.linea([(hx - 10, gy - 8), (hx + 4, gy - 12)], 5, (255, 255, 255))
    c.linea([(hx + 32, gy - 8), (hx + 46, gy - 12)], 5, (255, 255, 255))
    # mejilla / boca
    c.elipse(hx + 18, hy + 30, 11, 7, PINK_L, ow=0)
    if boca > .1:
        c.elipse(hx + 78, hy + 26, 14 * boca + 6, 10 * boca + 4, OUT, ow=0)
    return c.fin()


# ------------------------------------------------------------------ GUS
def gus(emocion='nervioso', boca=0., brazos=0.):
    """Sprite 440x600, anclado en los pies (220, 590). Mira a la derecha."""
    c = Lienzo(440, 600)
    # cola
    c.poli([(120, 470), (30, 520), (20, 560), (110, 540), (150, 520)], GREEN_D)
    # patas
    for px in (190, 260):
        c.rrect(px - 24, 520, px + 24, 592, 16, GREEN_D)
        c.rrect(px - 28, 572, px + 42, 596, 12, GREEN_D)
    # cuerpo + panza
    c.elipse(220, 400, 104, 140, GREEN)
    c.elipse(238, 420, 66, 100, BELLY, ow=0)
    for i in range(4):   # picos del lomo
        y = 300 + i * 52
        c.poli([(122 + i * 3, y - 18), (92 + i * 2, y + 6), (124 + i * 3, y + 28)], GREEN_D, ow=4)
    # brazos (suben a tapar los oídos)
    a = brazos
    sh = (300, 380)
    hand = (300 + 20 * (1 - a) - 28 * a, 470 - 190 * a)
    c.linea([sh, ((sh[0] + hand[0]) / 2 + 34, (sh[1] + hand[1]) / 2), hand], 30, GREEN, ow=5)
    c.elipse(hand[0], hand[1], 20, 20, GREEN, ow=5)
    # cabeza + hocico
    c.elipse(228, 250, 100, 74, GREEN)
    c.rrect(230, 232, 410, 300, 32, GREEN)
    c.elipse(380, 246, 7, 6, OUT, ow=0)
    # boca
    b = 8 + boca * 40
    c.rrect(238, 292, 408, 292 + b + 16, 16, (120, 30, 60) if boca > .15 else GREEN_D)
    c.poli([(252, 292), (268, 292), (260, 308 + boca * 6)], CREAM, ow=3)
    c.poli([(300, 292), (316, 292), (308, 308 + boca * 6)], CREAM, ow=3)
    c.poli([(350, 292), (366, 292), (358, 308 + boca * 6)], CREAM, ow=3)
    # ojos saltones
    big = 1.25 if emocion == 'asombro' else 1.0
    for ex in (236, 306):
        c.elipse(ex, 190, 33 * big, 35 * big, CREAM)
        c.elipse(ex + 8, 194, 11 * big, 12 * big, OUT, ow=0)
    # cejas
    if emocion in ('nervioso', 'asombro'):
        c.linea([(206, 138), (250, 156)], 9, OUT)
        c.linea([(338, 138), (292, 156)], 9, OUT)
    else:
        c.linea([(206, 150), (254, 146)], 9, OUT)
        c.linea([(338, 150), (290, 146)], 9, OUT)
    # gota de sudor
    if emocion == 'nervioso':
        c.poli([(176, 130), (162, 162), (176, 172), (190, 162)], (150, 210, 255), ow=4)
    return c.fin()


# ------------------------------------------------------------------ COCHE
def coche(llama=0., luces=0, reflejo=0.):
    """Sprite 760x330, mira a la derecha, ruedas apoyadas en y=320. luces: 0 apagadas, 1 rojo, 2 azul."""
    c = Lienzo(760, 330)
    # llamas del nitro (a la izquierda)
    if llama > 0:
        L = 40 + 190 * llama
        c.poli([(70, 238), (70 - L, 228), (70 - L * .55, 246), (70 - L * .85, 258), (70, 262)], (255, 122, 60), ow=0)
        c.poli([(70, 242), (70 - L * .6, 236), (70 - L * .4, 250), (70, 256)], (255, 224, 138), ow=0)
    body = (38, 30, 58)
    c.poli([(52, 262), (50, 196), (74, 176), (214, 168), (256, 110), (300, 94), (460, 94), (520, 168),
            (664, 178), (706, 214), (708, 262)], body)
    # franja con colores de marca
    c.poli([(56, 232), (700, 232), (702, 250), (56, 250)], PINK, ow=0)
    c.poli([(56, 242), (700, 242), (702, 250), (56, 250)], ORANGE, ow=0)
    # ventanas
    c.poli([(268, 122), (306, 106), (386, 106), (386, 168), (246, 168)], (96, 80, 150), ow=5)
    c.poli([(400, 106), (452, 106), (496, 168), (400, 168)], (96, 80, 150), ow=5)
    # reflejo
    if reflejo:
        x = 260 + reflejo * 200
        c.poli([(x, 110), (x + 26, 110), (x - 8, 168), (x - 34, 168)], (255, 255, 255), ow=0)
    # motor por fuera del cofre (soplador) + toma
    c.rrect(560, 126, 640, 176, 10, (170, 170, 190), ow=6)
    c.rrect(574, 108, 626, 134, 8, (210, 210, 225), ow=5)
    for i in range(3): c.linea([(582 + i * 18, 140), (582 + i * 18, 168)], 5, OUT)
    # escapes
    for i in range(3): c.elipse(150 + i * 44, 262, 12, 9, (170, 170, 190), ow=4)
    # tanque de nitro (naranja) visible atrás
    c.rrect(140, 132, 190, 176, 14, ORANGE, ow=5)
    c.linea([(148, 146), (182, 146)], 6, CREAM)
    # luces de la alarma
    col = {0: (255, 241, 234), 1: (255, 70, 70), 2: (70, 160, 255)}[luces]
    c.elipse(692, 202, 14, 12, col if luces else (255, 232, 176), ow=4)
    c.elipse(66, 204, 13, 11, col if luces else (255, 70, 70), ow=4)
    # ruedas
    for wx in (180, 566):
        c.elipse(wx, 262, 62, 62, (24, 18, 40), ow=6)
        c.elipse(wx, 262, 36, 36, CREAM, ow=5)
        c.elipse(wx, 262, 12, 12, OUT, ow=0)
    return c.fin()


# ------------------------------------------------------------------ DECORADO
def palmera(rama=0.):
    c = Lienzo(360, 700)
    c.curva([(190, 690), (230, 520), (170, 360), (200, 220)], 40, (150, 90, 140), ow=6)
    for ang, ln in ((-170, 150), (-130, 160), (-95, 150), (-50, 160), (-10, 150), (30, 120)):
        a = math.radians(ang + math.sin(rama) * 5)
        x1, y1 = 200 + math.cos(a) * ln, 215 + math.sin(a) * ln * .8
        mx, my = 200 + math.cos(a) * ln * .5, 215 + math.sin(a) * ln * .5 - 40
        c.curva([(200, 215), (mx, my), (x1, y1 + 30)], 30, GREEN, ow=5)
    return c.fin()


def casa(tono=(122, 63, 191)):
    c = Lienzo(380, 300)
    c.poli([(20, 290), (20, 140), (190, 30), (360, 140), (360, 290)], tono, ow=6)
    c.poli([(0, 150), (190, 12), (380, 150), (350, 150), (190, 50), (30, 150)], (60, 30, 100), ow=5)
    c.rrect(60, 170, 140, 240, 8, ORANGE, ow=5)
    c.rrect(230, 170, 320, 290, 8, (60, 30, 100), ow=5)
    return c.fin()


def estrellas_mareo(t):
    """Anillo de estrellitas que giran (sprite 220x90)."""
    c = Lienzo(220, 90)
    for i in range(4):
        a = t * 5 + i * math.pi / 2
        x, y = 110 + math.cos(a) * 80, 45 + math.sin(a) * 22
        s = 14
        pts = []
        for k in range(10):
            r = s if k % 2 == 0 else s * .45
            ang = -math.pi / 2 + k * math.pi / 5
            pts.append((x + math.cos(ang) * r, y + math.sin(ang) * r))
        c.poli(pts, (255, 224, 138), ow=3)
    return c.fin()


def explosion(radio=1.):
    r = 120 * radio
    c = Lienzo(int(2 * r + 40), int(2 * r + 40))
    cx = cy = r + 20
    pts, pts2 = [], []
    for k in range(24):
        rr = r if k % 2 == 0 else r * .58
        a = k * math.pi / 12
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        rr2 = rr * .72
        pts2.append((cx + math.cos(a) * rr2, cy + math.sin(a) * rr2))
    c.poli(pts, (255, 122, 60))
    c.poli(pts2, (255, 224, 138), ow=0)
    return c.fin()


def icono_chat(tam=150):
    c = Lienzo(tam, tam)
    c.rrect(8, 8, tam - 8, tam - 40, 26, CREAM)
    c.poli([(40, tam - 42), (30, tam - 8), (74, tam - 42)], CREAM)
    for i in range(3): c.elipse(tam * .3 + i * tam * .2, (tam - 32) / 2 + 4, 9, 9, OUT, ow=0)
    return c.fin()


# ------------------------------------------------------------------ PORTALES (serie 23-nov-2026)
PURPLE = (122, 63, 191); PURPLE_D = (42, 20, 72)


def portal(fase=0, w=520, h=700):
    """Portal morado vertical con espiral que gira (fase 0..11)."""
    c = Lienzo(w, h)
    cx, cy, rx, ry = w / 2, h / 2, w / 2 - 20, h / 2 - 20
    for k, col in enumerate([(70, 30, 120), (96, 44, 150), PURPLE, (150, 80, 215), (194, 89, 255)]):
        f = 1 - k * .1
        c.elipse(cx, cy, rx * f, ry * f, col, ow=8 if k == 0 else 0)
    for arm in range(4):
        col = (PINK, ORANGE, CREAM, (255, 224, 138))[arm]
        for i in range(26):
            r = .92 - i * .032
            a = arm * math.pi / 2 + fase * math.pi / 6 + (1 - r) * 5.2
            x, y = cx + math.cos(a) * rx * r * .92, cy + math.sin(a) * ry * r * .92
            rad = 3 + 13 * r
            c.d.ellipse([(x - rad) * SS, (y - rad) * SS, (x + rad) * SS, (y + rad) * SS], fill=col)
    c.elipse(cx, cy, 34, 52, CREAM, ow=0)
    c.elipse(cx, cy, 18, 30, (255, 224, 138), ow=0)
    return c.fin()


def reloj_roto(w=210):
    c = Lienzo(w, w)
    m = w / 2
    c.elipse(m, m, m - 10, m - 10, CREAM)
    for k in range(12):
        a = k * math.pi / 6
        c.linea([(m + math.cos(a) * (m - 30), m + math.sin(a) * (m - 30)), (m + math.cos(a) * (m - 22), m + math.sin(a) * (m - 22))], 5, OUT)
    c.linea([(m, m), (m, m - 52)], 8, OUT)
    c.linea([(m, m), (m + 38, m + 14)], 8, OUT)
    c.linea([(m - 40, m - 70), (m - 10, m - 30), (m - 34, m + 6), (m + 6, m + 44), (m - 14, m + 80)], 6, PINK)
    return c.fin()


def planta(w=1000, h=520):
    """Planta nuclear de caricatura: dos torres de enfriamiento, domo y cerca."""
    c = Lienzo(w, h)
    base = h - 12
    for ox, tono in ((70, (176, 150, 214)), (560, (160, 132, 204))):
        pts = [(ox, base), (ox + 330, base), (ox + 262, base - 170), (ox + 250, base - 300), (ox + 272, base - 430),
               (ox + 58, base - 430), (ox + 80, base - 300), (ox + 68, base - 170)]
        c.poli(pts, tono)
        c.linea([(ox + 66, base - 428), (ox + 264, base - 428)], 14, (230, 210, 250), ow=0)
        c.linea([(ox + 120, base - 360), (ox + 108, base - 40)], 8, (150, 120, 196))
        c.linea([(ox + 200, base - 360), (ox + 216, base - 40)], 8, (150, 120, 196))
    # edificio central + domo
    c.rrect(400, base - 190, 560, base, 6, (96, 80, 150))
    c.d.pieslice([410 * SS, (base - 300) * SS, 550 * SS, (base - 80) * SS], 180, 360, fill=(120, 100, 176), outline=OUT, width=6 * SS)
    for i in range(3):
        c.rrect(420 + i * 46, base - 150, 450 + i * 46, base - 118, 4, ORANGE, ow=4)
    # símbolo de radiación
    sx, sy, r = 480, base - 232, 34
    c.elipse(sx, sy, r, r, (255, 224, 138), ow=5)
    for a0 in (-30, 90, 210):
        c.d.pieslice([(sx - r * .8) * SS, (sy - r * .8) * SS, (sx + r * .8) * SS, (sy + r * .8) * SS], a0, a0 + 60, fill=OUT)
    c.elipse(sx, sy, 8, 8, (255, 224, 138), ow=0)
    # cerca
    for x in range(20, w - 20, 44):
        c.linea([(x, base), (x, base - 54)], 6, (200, 190, 220), ow=3)
    c.linea([(20, base - 40), (w - 20, base - 40)], 6, (200, 190, 220), ow=3)
    return c.fin()


def humo(r=60):
    c = Lienzo(r * 3, r * 3)
    for dx, dy, rr in ((0, 0, r), (-r * .6, r * .5, r * .7), (r * .65, r * .45, r * .75)):
        c.elipse(r * 1.5 + dx, r * 1.4 + dy, rr, rr, (236, 226, 246), ow=0)
    return c.fin()


def ciudad_pixel():
    """Vice City antiguo en pixel art (135x80 px escalado x8 = 1080x640)."""
    import random
    rnd = random.Random(11)
    W0, H0 = 135, 80
    im = Image.new('RGBA', (W0, H0), (0, 0, 0, 255)); d = ImageDraw.Draw(im)
    bandas = [(48, 22, 96), (92, 34, 130), (160, 52, 150), (236, 84, 140), (255, 128, 120), (255, 179, 107), (255, 224, 138)]
    for i, col in enumerate(bandas):
        d.rectangle([0, i * 7, W0, i * 7 + 7], fill=col)
    d.ellipse([46, 18, 84, 56], fill=(255, 241, 190))
    for y in range(34, 56, 4):
        d.rectangle([40, y, 90, y + 1], fill=bandas[min(6, y // 7)])
    x = 0
    while x < W0:
        w = rnd.randint(9, 16); h = rnd.randint(18, 46)
        col = rnd.choice([(30, 16, 64), (42, 20, 80), (58, 28, 100)])
        d.rectangle([x, 70 - h, x + w, 70], fill=col)
        for wy in range(70 - h + 3, 67, 5):
            for wx in range(x + 2, x + w - 1, 4):
                if rnd.random() < .5:
                    d.rectangle([wx, wy, wx + 1, wy + 2], fill=rnd.choice([(255, 224, 138), (255, 107, 139), (110, 230, 255)]))
        x += w + rnd.randint(0, 2)
    d.rectangle([0, 70, W0, H0], fill=(30, 14, 56))
    d.rectangle([0, 70, W0, 71], fill=(255, 107, 139))
    for xx in range(2, W0, 14):
        d.rectangle([xx, 76, xx + 6, 77], fill=(255, 241, 234))
    for px in (14, 118):
        for y in range(48, 71):
            d.point((px, y), fill=(96, 50, 30))
        for ang in (-2.6, -2.0, -1.2, -0.5):
            for k in range(1, 11):
                d.point((int(px + math.cos(ang) * k * 1.2), int(48 + math.sin(ang) * k * .8 + k * k * .03)), fill=(40, 170, 110))
    return im.resize((W0 * 8, H0 * 8), Image.NEAREST)


def portal_mini(encendido=True, size=150):
    c = Lienzo(size, size)
    m = size / 2
    if encendido:
        c.elipse(m, m, m - 8, m - 8, PURPLE)
        c.elipse(m, m, m * .62, m * .62, (194, 89, 255), ow=0)
        c.elipse(m, m, m * .28, m * .28, CREAM, ow=0)
    else:
        c.elipse(m, m, m - 8, m - 8, (58, 40, 96))
        c.linea([(m - 14, m - 14), (m + 14, m + 14)], 8, (130, 110, 160))
        c.linea([(m + 14, m - 14), (m - 14, m + 14)], 8, (130, 110, 160))
    return c.fin()
