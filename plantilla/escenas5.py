"""Escenas de caricatura 5 (26-nov-2026): el Rolex arcoíris de Casanova Island (r_*).
Mismo motor y estilo que escenas4. Todo dibujado, sin logos ni marcas en el reloj.
El mapa de la escena 2 se cambia desde el JSON ("mapa")."""
import math, colorsys
from PIL import Image, ImageDraw
import caricatura2 as C
import escenas2 as E
import escenas4 as B
from caricatura import OUT, SS, GREEN, GREEN_D
from caricatura2 import L2, PINK, PINK_D, PINK_L, ORANGE, CREAM, GOLD, WHITE, CYAN, RED
from escenas4 import mk, S, cl, pr, eo, eb, idle, hop, capa, golpe, sombra, G, GA, FLA

R = None
ORO = (240, 186, 150); ORO_D = (196, 134, 110); ORO_L = (255, 224, 196)
MADERA = (150, 96, 70); MADERA_D = (112, 68, 56)


def _mix(a, b, u): return a + (b - a) * u


# =================================================================== EL RELOJ
def _caja(c, m, k=1.):
    """Caja del reloj centrada en m: bisel arcoíris, esfera negra y tres subesferas. Radio base 150."""
    x, y = m; r = 150 * k
    c.rrect(x + r - 8 * k, y - 22 * k, x + r + 30 * k, y + 22 * k, 8 * k, ORO_D, ow=5)          # corona
    for s in (-1, 1):
        c.rrect(x + r * .80, y + s * 70 * k - 14 * k, x + r + 16 * k, y + s * 70 * k + 14 * k, 8 * k, ORO, ow=5)
    c.elipse(x, y, r + 8 * k, r + 8 * k, ORO, ow=6)
    n = 36
    for i in range(n):                                                                          # piedras del bisel
        a = i / n * 2 * math.pi - math.pi / 2
        col = tuple(int(v * 255) for v in colorsys.hsv_to_rgb(i / n, .78, 1.))
        px, py = x + math.cos(a) * 130 * k, y + math.sin(a) * 130 * k
        c.elipse(px, py, 13 * k, 13 * k, col, ow=2)
        c.elipse(px - 4 * k, py - 4 * k, 3.4 * k, 3.4 * k, WHITE, ow=0)
    c.elipse(x, y, 113 * k, 113 * k, ORO_L, ow=4)
    c.elipse(x, y, 103 * k, 103 * k, (22, 16, 36), ow=3)
    for i in range(12):
        a = i * math.pi / 6
        c.linea([(x + math.cos(a) * 82 * k, y + math.sin(a) * 82 * k), (x + math.cos(a) * 95 * k, y + math.sin(a) * 95 * k)], max(2, int(7 * k)), CREAM)
    for (dx, dy) in ((-46, 0), (46, 0), (0, 46)):
        c.elipse(x + dx * k, y + dy * k, 29 * k, 29 * k, ORO, ow=3)
        c.elipse(x + dx * k, y + dy * k, 21 * k, 21 * k, ORO_L, ow=0)
        c.linea([(x + dx * k, y + dy * k), (x + dx * k + 3 * k, y + (dy - 17) * k)], max(2, int(4 * k)), OUT)
    c.linea([(x, y), (x - 44 * k, y - 40 * k)], max(2, int(8 * k)), WHITE)
    c.linea([(x, y), (x + 58 * k, y - 52 * k)], max(2, int(5 * k)), WHITE)
    c.elipse(x, y, 9 * k, 9 * k, ORO, ow=2)
    c.elipse(x - 30 * k, y - 62 * k, 20 * k, 7 * k, (70, 60, 100), ow=0)


def reloj():
    """Reloj completo con extensible. 380x620, centro de la caja en (180, 310)."""
    def f():
        c = L2(380, 620)
        for arriba in (True, False):
            for i in range(4):
                y0 = 130 - i * 36 if arriba else 460 + i * 36
                w = 82 - i * 4
                c.rrect(180 - w, y0, 180 + w, y0 + 34, 8, ORO, ow=5)
                c.rrect(180 - w * .42, y0 + 4, 180 + w * .42, y0 + 30, 6, ORO_L, ow=2)
        _caja(c, (180, 310))
        return c.fin()
    return mk('reloj', f)


def brazalete():
    """El reloj puesto como brazalete gigante: aro grande con la caja abajo. 380x460, hueco del brazo en (190, 90)."""
    def f():
        c = L2(380, 460)
        c.d.ellipse([60 * SS, 30 * SS, 320 * SS, 330 * SS], outline=OUT, width=48 * SS)
        c.d.ellipse([66 * SS, 36 * SS, 314 * SS, 324 * SS], outline=ORO, width=36 * SS)
        for i in range(18):
            a = i / 18 * 2 * math.pi
            x, y = 190 + math.cos(a) * 112, 180 + math.sin(a) * 126
            c.linea([(x - math.cos(a) * 17, y - math.sin(a) * 18), (x + math.cos(a) * 17, y + math.sin(a) * 18)], 4, ORO_D)
        _caja(c, (190, 310), .86)
        return c.fin()
    return mk('braz', f)


def rayos(fr, x, y, t, r=420, a=34, n=12):
    def f(d):
        for k in range(n):
            g = t * .7 + k * 2 * math.pi / n
            d.polygon([(x, y), (x + math.cos(g) * r, y + math.sin(g) * r), (x + math.cos(g + .18) * r, y + math.sin(g + .18) * r)], fill=(255, 232, 170, a))
    lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); f(ImageDraw.Draw(lay))
    m = Image.new('L', (R.W, R.H), 0); ImageDraw.Draw(m).rectangle((0, 650, R.W, 1210), fill=255)
    clip = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); clip.paste(lay, (0, 0), m); fr.alpha_composite(clip)


def mano(x, y, sc, hx, hy, flip=False):
    """Posición en pantalla de un punto (hx, hy) del sprite de Gus."""
    dx = (hx - 220) * sc
    return x - dx if flip else x + dx, y + (hy - 590) * sc


def fondo(fr, im, y=1210): R.put(fr, im, 540, y, 1, 1, anchor=(540, im.height))


# =================================================================== FONDOS
def bg_joyeria():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 460, 0, (38, 22, 76), ow=0)
        for x in range(0, 1080, 90): c.rrect(x, 0, x + 46, 460, 20, (52, 30, 100), ow=0)
        for (x0, y0) in ((40, 70), (40, 230), (900, 70)):
            c.rrect(x0, y0, x0 + 140, y0 + 110, 14, (110, 190, 220), ow=6)
            c.poli([(x0 + 44, y0 + 50), (x0 + 58, y0 + 34), (x0 + 82, y0 + 34), (x0 + 96, y0 + 50), (x0 + 70, y0 + 84)], (230, 250, 255), ow=4)
            c.linea([(x0 + 44, y0 + 50), (x0 + 96, y0 + 50)], 3, OUT)
            c.rrect(x0 + 24, y0 + 90, x0 + 116, y0 + 100, 4, PINK_D, ow=3)
            c.linea([(x0 + 18, y0 + 40), (x0 + 48, y0 + 14)], 6, WHITE)
        c.rrect(-10, 460, 1090, 560, 0, (28, 16, 58), ow=0)
        for k in range(8): c.linea([(-40 + k * 170, 560), (60 + k * 140, 462)], 4, (54, 34, 100))
        return c.fin()
    return mk('r1', f)


def pedestal():
    def f():
        c = L2(360, 150)
        c.rrect(60, 40, 300, 140, 12, (122, 63, 191))
        c.rrect(30, 14, 330, 50, 14, (190, 40, 100))
        c.rrect(40, 126, 320, 146, 8, GOLD, ow=4)
        c.linea([(60, 24), (300, 24)], 5, PINK_L)
        return c.fin()
    return mk('pedestal', f)


def bg_casa():
    """Recibidor de la casa de lujo."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 450, 0, (236, 220, 244), ow=0)
        for x in range(0, 1080, 120): c.linea([(x, 0), (x, 450)], 3, (218, 200, 232))
        c.rrect(40, 90, 290, 460, 14, (26, 16, 48), ow=6)                      # puerta (hueco)
        c.rrect(54, 104, 276, 460, 8, (90, 80, 170), ow=0)
        c.elipse(215, 170, 34, 34, (255, 240, 200), ow=0)
        c.rrect(390, 80, 580, 220, 10, GOLD, ow=6); c.rrect(406, 96, 564, 204, 6, (110, 190, 220), ow=3)
        c.poli([(406, 204), (460, 140), (500, 180), (530, 150), (564, 204)], (80, 160, 120), ow=3)
        c.elipse(700, 40, 70, 22, GOLD, ow=5)
        for i in range(5): c.elipse(644 + i * 28, 70, 8, 16, (255, 245, 210), ow=2)
        c.rrect(-10, 450, 1090, 560, 0, (110, 80, 150), ow=0)
        for i in range(0, 1080, 100):
            c.rrect(i, 450, i + 50, 505, 0, (130, 98, 172), ow=0); c.rrect(i + 50, 505, i + 100, 560, 0, (130, 98, 172), ow=0)
        c.linea([(-10, 450), (1090, 450)], 6, OUT)
        c.rrect(60, 470, 270, 500, 12, (190, 40, 100), ow=4)
        return c.fin()
    return mk('r3', f)


def puerta_hoja():
    def f():
        c = L2(232, 370)
        c.rrect(6, 6, 226, 366, 10, MADERA)
        for y0 in (34, 196): c.rrect(34, y0, 198, y0 + 130, 10, MADERA_D, ow=4)
        c.elipse(196, 190, 12, 12, GOLD, ow=4)
        return c.fin()
    return mk('hoja', f)


def alarma():
    """Alarma de juguete con el compartimento de pilas abierto y vacío. 260x320."""
    def f():
        c = L2(260, 320)
        c.rrect(40, 120, 220, 300, 26, GOLD)
        c.poli([(52, 130), (60, 60), (100, 24), (160, 24), (200, 60), (208, 130)], RED)
        c.linea([(80, 70), (104, 46)], 10, (255, 190, 190))
        c.elipse(130, 18, 16, 14, CYAN, ow=4)
        c.rrect(66, 170, 194, 268, 12, (40, 26, 66), ow=5)
        for y in (194, 240):
            c.rrect(84, y - 15, 170, y + 15, 12, (70, 56, 104), ow=0)
            c.linea([(86, y - 8), (96, y), (86, y + 8)], 4, (200, 200, 220))
            c.linea([(168, y - 12), (168, y + 12)], 6, (200, 200, 220))
        c.poli([(196, 262), (244, 292), (216, 316), (176, 280)], (255, 190, 80), ow=4)  # tapa colgando
        return c.fin()
    return mk('alarma', f)


def bg_escalera():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 560, 0, (82, 52, 128), ow=0)
        for x in range(0, 1080, 100): c.rrect(x, 0, x + 44, 560, 0, (92, 60, 142), ow=0)
        c.rrect(850, 30, 1010, 190, 10, MADERA, ow=6); c.elipse(878, 116, 10, 10, GOLD, ow=3)      # puerta de arriba
        for i in range(8):                                                                         # escalones
            x0 = 180 + i * 80; y0 = 500 - i * 44
            c.rrect(x0, y0, 1100, 566, 0, (236, 214, 190), ow=5)
            c.rrect(x0, y0, x0 + 96, y0 + 14, 4, (190, 40, 100), ow=3)
        c.rrect(-10, 530, 1090, 570, 0, (44, 30, 76), ow=0)
        c.linea([(190, 380), (770, 60)], 14, GOLD, ow=5)
        for i in range(5):
            x = 230 + i * 130; y = 358 - i * 72
            c.linea([(x, y), (x, y + 110)], 8, GOLD, ow=3)
        c.rrect(80, 80, 230, 220, 10, GOLD, ow=5); c.rrect(94, 94, 216, 206, 6, PINK_L, ow=3)
        c.elipse(155, 150, 34, 34, ORANGE, ow=3)
        return c.fin()
    return mk('r4', f)


def bg_cuarto():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 450, 0, (60, 74, 150), ow=0)
        for j in range(5):
            for i in range(10): c.elipse(60 + i * 112 + (56 if j % 2 else 0), 50 + j * 84, 6, 6, (86, 102, 184), ow=0)
        c.rrect(420, 60, 660, 250, 14, (22, 16, 52), ow=6)                      # ventana nocturna
        c.elipse(600, 112, 28, 28, (255, 240, 200), ow=0)
        for i in range(6): c.rrect(436 + i * 36, 200 - (i * 37 % 70), 464 + i * 36, 244, 3, (122, 63, 191), ow=0)
        c.linea([(540, 60), (540, 250)], 5, OUT)
        c.poli([(398, 46), (450, 46), (430, 270), (398, 280)], PINK_D, ow=5)
        c.poli([(682, 46), (630, 46), (650, 270), (682, 280)], PINK_D, ow=5)
        c.rrect(700, 230, 1100, 440, 30, MADERA, ow=6)                          # cabecera y cama
        c.rrect(640, 360, 1110, 480, 24, (244, 236, 250), ow=6)
        c.rrect(900, 320, 1060, 386, 28, CREAM, ow=5)
        c.rrect(640, 400, 960, 486, 18, (190, 40, 100), ow=5)
        c.rrect(-10, 450, 1090, 560, 0, (44, 30, 76), ow=0) if False else None
        c.rrect(-10, 486, 1090, 566, 0, MADERA_D, ow=0)
        for x in range(0, 1080, 150): c.linea([(x, 490), (x - 30, 560)], 4, (90, 54, 46))
        c.rrect(90, 372, 350, 400, 8, MADERA, ow=5)                             # mesa de noche (izquierda)
        c.rrect(108, 398, 332, 500, 8, MADERA_D, ow=5)
        c.rrect(128, 418, 312, 454, 8, MADERA, ow=3); c.elipse(220, 436, 8, 8, GOLD, ow=2)
        for x in (120, 316): c.rrect(x - 8, 498, x + 8, 530, 4, MADERA_D, ow=4)
        c.linea([(128, 372), (128, 260)], 10, GOLD, ow=4)                       # lámpara
        c.poli([(76, 268), (96, 190), (160, 190), (180, 268)], (255, 214, 150), ow=5)
        return c.fin()
    return mk('r5', f)


def bg_malecon():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 300, 0, (122, 63, 160), ow=0)
        c.elipse(540, 270, 150, 150, (255, 179, 107), ow=0)
        for y in (250, 278, 300): c.linea([(380, y), (700, y)], 8, (122, 63, 160))
        for i, (x, h) in enumerate(((40, 150), (140, 210), (250, 120), (760, 170), (860, 240), (970, 140))):
            c.rrect(x, 310 - h, x + 80, 310, 8, (60, 34, 110), ow=4)
            for j in range(int(h / 44)): c.rrect(x + 16, 326 - h + j * 40, x + 64, 338 - h + j * 40, 3, (GOLD, CYAN, PINK)[(i + j) % 3], ow=0)
        c.rrect(-10, 310, 1090, 420, 0, (70, 80, 170), ow=0)
        c.rrect(-10, 420, 1090, 560, 0, (236, 200, 170), ow=0)
        c.linea([(-10, 420), (1090, 420)], 7, OUT)
        for x in range(0, 1100, 130): c.linea([(x, 424), (x - 60, 556)], 4, (206, 164, 142))
        return c.fin()
    return mk('r6', f)


# =================================================================== MAPA
def mapa_base():
    """940x560: mar, isla vecina (izquierda, vertical) y Casanova Island (derecha, horizontal) con sus calles."""
    def f():
        c = L2(940, 560)
        c.rrect(6, 6, 934, 554, 40, (60, 140, 205), ow=7)
        c.rrect(60, 66, 330, 494, 132, (90, 170, 225), ow=0)
        c.rrect(362, 126, 912, 434, 150, (90, 170, 225), ow=0)
        c.linea([(14, 280), (926, 280)], 22, WHITE, ow=5)                            # puente
        for (x0, y0, x1, y1) in ((80, 86, 310, 474), (382, 146, 892, 414)):
            r = (min(x1 - x0, y1 - y0)) / 2 - 6
            c.rrect(x0, y0, x1, y1, r, (238, 222, 180), ow=6)
            c.rrect(x0 + 14, y0 + 14, x1 - 14, y1 - 14, r - 14, (150, 205, 160), ow=0)
        calle = lambda pts: c.d.line(c.P(pts), fill=WHITE, width=12 * SS, joint='curve')
        calle([(80, 280), (310, 280)])
        calle([(164, 150), (226, 150), (226, 410), (164, 410), (164, 150)])
        calle([(382, 280), (892, 280)])
        calle([(450, 280), (520, 250), (760, 250), (824, 280), (760, 312), (520, 312), (450, 280)])
        calle([(640, 250), (640, 312)])
        casa = lambda x, y, w=40, h=30, col=(150, 120, 200): c.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 6, col, ow=3)
        for (x, y) in ((160, 118), (226, 118), (122, 166), (270, 166), (116, 216), (270, 216), (116, 340), (270, 340), (122, 392), (270, 392), (164, 442), (226, 442)):
            casa(x, y, 38, 32)
        casa(195, 220, 30, 44, (190, 120, 190)); casa(195, 344, 30, 44, (190, 120, 190))
        for (x, y) in ((470, 196), (528, 180), (706, 180), (766, 182), (820, 206), (434, 232), (848, 244),
                       (434, 330), (848, 318), (470, 364), (532, 376), (590, 376), (648, 376), (706, 376), (766, 368), (816, 348)):
            casa(x, y, 42, 30)
        casa(690, 281, 50, 30, (190, 120, 190))
        c.d.rounded_rectangle([6 * SS, 6 * SS, 934 * SS, 554 * SS], radius=40 * SS, outline=OUT, width=7 * SS)
        return c.fin()
    return mk('rmapa', f)


def casa_meta():
    def f():
        c = L2(96, 74)
        c.rrect(10, 30, 86, 68, 6, (255, 241, 234), ow=5)
        c.poli([(4, 34), (48, 6), (92, 34)], PINK, ow=5)
        c.rrect(38, 44, 58, 68, 3, GOLD, ow=3)
        return c.fin()
    return mk('rmeta', f)


# =================================================================== 1 · GANCHO
def r_hook(s):
    D = s['dur']
    def draw(fr, t):
        fondo(fr, bg_joyeria())
        rx, ry = 600, 905
        rayos(fr, rx, ry, t)
        E.titulo(fr, t, '¿UN ROLEX DE *MEDIO MILLÓN*?', 96, 540, .0)
        R.put(fr, pedestal(), rx, G + 40, .95, .95, anchor=(180, 146))
        k = .66 * (.85 + .15 * eb(pr(t, 0, .35))) * (1 + .025 * math.sin(t * 5))
        R.put(fr, reloj(), rx, ry + math.sin(t * 3) * 8, k, k, rot=math.sin(t * 2) * 5, anchor=(180, 310))
        for i, (dx, dy) in enumerate(((-150, -150), (150, -110), (-130, 90), (160, 130), (0, -200))):
            E.destello(fr, rx + dx, ry + dy, t, i * .23, 1.3)
        # Gus con su cadena de cartón: asombro → amor → quiere tocarlo
        paso = 0 if t < D * .35 else (1 if t < D * .7 else 2)
        emo, boca, pose = (('asombro', .7, 'pecho'), ('amor', .9, 'celebra'), ('concentrado', 0., 'agarra'))[paso]
        gx = 200 + (50 * eo(pr(t, D * .7, .5)))
        GA(fr, gx, G + 20, .62, emo=emo, boca=boca, pose=pose, brazos=1., mira=(1, 0), lentes=False, sy=.62 * idle(t, 9 if paso else 6, .025))
        # Flami se asoma con los lentes abajo
        u = eb(pr(t, .55, .45))
        if u > 0:
            fx = 1220 - 270 * u
            FLA(fr, fx, G + 30, .66, emo='asombro' if t < D * .7 else 'guino', cuello=.8 + .2 * math.sin(t * 4), ala='reposo', mira=(1, 0))
        # contador del precio
        q = eo(pr(t, .35, 1.3))
        if q > 0:
            val = int(round(500 * q)) * 1000
            im = R.pill(f'${val:,}', R.F('800', 58), fg=R.BG, padx=30, pady=10)
            R.put(fr, im, 250, 700, 1, 1, rot=-6 + math.sin(t * 6) * 2, alpha=cl(q * 4), anchor=(im.width / 2, im.height / 2))
    return draw


# =================================================================== 2 · MAPA
def r_mapa(s):
    D = s['dur']
    cfg = s.get('mapa', {})
    isla = cfg.get('isla', 'CASANOVA ISLAND')
    pin = cfg.get('pin', [590, 228]); et = cfg.get('etiqueta', [638, 62]); ruta = cfg.get('ruta', [[320, 500], [520, 448]])
    MX0, MY0 = 540 - 470, 930 - 280
    def draw(fr, t):
        E.titulo(fr, t, '1. *CASANOVA ISLAND*', 92, 548)
        pe = eo(pr(t, 0, .35))
        R.put(fr, mapa_base(), 540, 930, .8 + .2 * pe, .8 + .2 * pe, alpha=cl(pe * 2), anchor=(470, 280))
        if pe < 1: return
        d = ImageDraw.Draw(fr)
        for k in range(10):
            x = MX0 + 60 + (k * 131 + t * 45) % 800; y = MY0 + (40 + (k * 23) % 40 if k % 2 else 470 + (k * 31) % 60)
            d.arc((x - 16, y - 6, x + 16, y + 10), 200, 340, fill=(200, 235, 255, 255), width=4)
        R.anim_in(fr, E.pil(isla, 40, bg=(74, 38, 120)), MX0 + et[0], MY0 + et[1], t, .25, 'pop', .25)
        px, py = MX0 + pin[0], MY0 + pin[1]
        u = pr(t, .55, .4)
        if u > 0:
            R.put(fr, casa_meta(), px, py + 6, .95 * eb(u), .95 * eb(u), anchor=(48, 40))
            if t > .9:
                for j in (0, .5):
                    r = (t - .9 + j) % 1.0
                    d.ellipse((px - 40 - 60 * r, py + 10 - 20 - 30 * r, px + 40 + 60 * r, py + 10 + 20 + 30 * r), outline=(255, 107, 139, int(255 * (1 - r))), width=7)
            R.put(fr, S('pin', PINK, 70), px, py - 30 + (1 - eo(u)) * -180 - abs(math.sin(t * 6)) * 12, 1.15 * eb(u), 1.15 * eb(u), anchor=(35, 90))
        # Gus llega en flotador
        a, b = ruta
        w = eo(cl(t / (D * .75)))
        gx = MX0 + _mix(a[0] - 220, b[0], w); gy = MY0 + _mix(a[1], b[1], w) + math.sin(t * 6) * 5
        for k in range(3):
            q = (t * 1.6 + k * .33) % 1
            d.ellipse((gx - 80 - 70 * q, gy - 8 - 10 * q, gx - 10 - 20 * q, gy + 16 + 10 * q), outline=(220, 240, 255, int(210 * (1 - q))), width=4)
        sc = .86; llego = t > D * .75
        R.put(fr, B.dona('atras'), gx, gy, sc, sc, anchor=(110, 70))
        E.GU(fr, gx, gy + 8, .37, 'feliz' if llego else 'concentrado', boca=.8 if llego else 0, pose='celebra' if llego else 'agarra', brazos=1., recorte=True, rot=math.sin(t * 7) * 6)
        if not llego: R.put(fr, B.remo(), gx + 56, gy - 14, .66, .66, rot=-40 + math.sin(t * 9) * 35, anchor=(30, 100))
        R.put(fr, B.dona('frente'), gx, gy, sc, sc, anchor=(110, 70))
        if llego: golpe(fr, '[¡PLOP!]', gx + 190, gy - 10, t, D * .75, 60, 7)
        # Flami cruza volando
        v = cl((t - .5) / (D - .5))
        if v > 0:
            E.FL(fr, -120 + 1320 * v, 790 + math.sin(t * 5) * 20, .26, 'feliz', gafas=1, cuello=.8, ala='arriba' if int(t * 7) % 2 else 'abre', rot=-18)
    return draw


# =================================================================== 3 · SIN ALARMA
def r_alarma(s):
    D = s['dur']; clic = s.get('t_clic', D * .45)
    def draw(fr, t):
        fondo(fr, bg_casa())
        E.titulo(fr, t, '2. *SIN ALARMA*', 104, 548)
        ab = eo(pr(t, 0, .6))                                      # la puerta se abre
        R.put(fr, puerta_hoja(), 108, 1110, 1 - .82 * ab, 1, anchor=(6, 366))
        # alarma de juguete
        ax, ay = 760, 900
        sh = math.sin(t * 70) * 7 if clic < t < clic + .2 else math.sin(t * 2) * 1.5
        R.put(fr, alarma(), ax + sh, ay, .82, .82, rot=sh * .6, anchor=(130, 160))
        if t >= clic:
            golpe(fr, '[clic.]', 650, 710, t, clic, 82, -8)
            R.anim_in(fr, E.pilg('SIN PILAS', 46, 28, 10), ax, 1085, t, clic + .45, 'pop', .25)
        # Gus de puntitas; cuando suena el clic se asusta y luego lootea feliz
        fin = clic + .9
        w = cl(t / clic)
        gx = 150 + 270 * w if t < fin else 420
        paso = abs(math.sin(t * 8)) * 34 if t < clic else 0
        if t < clic: emo, boca, pose = 'concentrado', 0., 'pecho'
        elif t < fin: emo, boca, pose = 'grito', 1., 'orejas'
        else: emo, boca, pose = 'feliz', .8, 'agarra'
        sombra(fr, gx, G + 18, 180)
        E.GU(fr, gx, G + 14 - paso, .6, emo, boca=boca, pose=pose, brazos=1., mira=(1, 0), rot=math.sin(t * 8) * 6 if t < clic else 0, sy=.6 * idle(t, 16 if clic < t < fin else 7, .03))
        if t < clic:
            R.pop_burbuja(fr, E.bub('Shhh...', 0, 46), gx + 40, 815, t, .5, clic - .15)
            for k in range(3):
                if t > .4 + k * .35: R.put(fr, S('nube_polvo', 46), gx - 90 - k * 55, G + 6, .4, .4, alpha=max(0, .8 - (t - .4 - k * .35)), anchor=(69, 46))
        if t >= fin:                                               # botín que salta a sus brazos
            mx, my = mano(gx, G + 14, .6, 392, 424)
            for k, col in enumerate((GOLD, CYAN, PINK_L)):
                u = eb(pr(t, fin + k * .15, .35))
                if u > 0:
                    R.put(fr, S('destellos', 34), mx + 20 + k * 26, my - 20 - k * 34 - math.sin(t * 9 + k) * 12, u, u, rot=t * 120 + k * 30, anchor=(39, 39))
            R.pop_burbuja(fr, E.bub('¡Tranqui!', 0, 46), gx + 40, 815, t, fin + .1)
        # Flami mira la alarma, confundida
        if t < clic:
            E.FL(fr, 975, G + 20, .54, 'feliz', gafas=1, cuello=.2, ala='cadera', flip=True, mira=(1, 0), sy=.54 * idle(t, 5))
        else:
            FLA(fr, 975, G + 20, .54, emo='asombro', cuello=.5 + .5 * math.sin(t * 5), ala='cadera', mira=(1, 0), sy=.54 * idle(t, 5))
            R.put(fr, E.sfx('[¿?]', 90), 975, 730 + math.sin(t * 6) * 10, eb(pr(t, clic + .25, .3)), eb(pr(t, clic + .25, .3)), rot=math.sin(t * 4) * 10, anchor=(E.sfx('[¿?]', 90).width / 2, 50))
    return draw


# =================================================================== 4 · ESCALERAS
def r_escaleras(s):
    D = s['dur']; resbala = s.get('t_resbala', D * .42)
    def draw(fr, t):
        fondo(fr, bg_escalera())
        E.titulo(fr, t, '3. *SUBE LAS ESCALERAS*', 84, 548)
        d = ImageDraw.Draw(fr)
        for k in range(3):                                          # flechas que suben
            u = (t * 1.4 + k / 3) % 1
            x, y = 300 + 420 * u, 930 - 232 * u
            d.line([(x - 30, y - 6), (x, y - 18), (x - 8, y + 14)], fill=(255, 241, 234, int(255 * math.sin(math.pi * u))), width=10, joint='curve')
        P = [(220, 1150), (300, 1106), (380, 1062), (460, 1018)]
        gsc = .44
        if t < resbala:
            u = cl(t / resbala) * 3; i = min(2, int(u)); v = u - i
            gx = _mix(P[i][0], P[i + 1][0], v); gy = _mix(P[i][1], P[i + 1][1], v) - 60 * math.sin(math.pi * v)
            E.GU(fr, gx, gy, gsc, 'orgullo' if t < resbala * .6 else 'concentrado', pose='celebra' if int(u * 2) % 2 else 'cadera', brazos=1.)
        else:
            q = pr(t, resbala, .55)
            gx = _mix(P[3][0], 200, eo(q)); gy = _mix(P[3][1], 1175, q * q) - 120 * math.sin(math.pi * q)
            if q < 1:
                E.GU(fr, gx, gy - 40 * math.sin(math.pi * q), gsc, 'grito', boca=1., pose='orejas', brazos=1., rot=360 * eo(q) * .22 + 20 * math.sin(q * 12))
            else:
                E.GU(fr, gx, 1180, gsc, 'confuso', boca=.5, pose='encoge', brazos=1., rot=math.sin(t * 5) * 4, sy=gsc * .84)
                R.put(fr, S_estrellas(t), gx + 30, 920, 1, 1, anchor=(110, 45))
            golpe(fr, '[¡FIUM!]', 520, 1080, t, resbala, 82, -10, resbala + .8)
            golpe(fr, '[¡PUM!]', 380, 880, t, resbala + .55, 82, 8)
        # Flami sube volando
        v = eo(cl((t - .25) / (D * .72)))
        fx = _mix(1000, 860, v) - 260 * math.sin(math.pi * v); fy = _mix(1190, 890, v) + math.sin(t * 8) * 14
        llego = v > .97
        E.FL(fr, fx, fy, .42, 'guino' if llego else 'feliz', boca=.3 if llego else 0, gafas=0 if llego else 1, cuello=.5,
             ala='saluda' if llego else ('arriba' if int(t * 8) % 2 else 'abre'), flip=True, rot=0 if llego else -10)
        if not llego:
            for k in range(3):
                u = (t * 2 + k * .33) % 1
                R.put(fr, B.pluma([PINK, PINK_L, PINK_D][k]), fx + 70 + u * 60, fy - 80 + u * 90 + k * 10, .8, .8, rot=u * 300, alpha=1 - u, anchor=(45, 20))
    return draw


def S_estrellas(t):
    import caricatura as K
    return K.estrellas_mareo(t)


# =================================================================== 5 · EL RELOJ EN LA HABITACIÓN IZQUIERDA
def r_cuarto(s):
    D = s['dur']; toma = s.get('t_pone', D * .58)
    def draw(fr, t):
        fondo(fr, bg_cuarto())
        E.titulo(fr, t, '4. HABITACIÓN IZQUIERDA: *EL ROLEX*', 82, 540)
        rx, ry = 242, 940
        if t < toma:
            rayos(fr, rx, ry, t, 300, 40, 10)
            k = .42 * (1 + .06 * math.sin(t * 7))
            R.put(fr, reloj(), rx, ry + math.sin(t * 4) * 6, k, k, rot=math.sin(t * 2.5) * 8, anchor=(180, 310))
            for i, (dx, dy) in enumerate(((-90, -90), (100, -60), (80, 40))):
                E.destello(fr, rx + dx, ry + dy, t, i * .31, 1.1)
            u = eb(pr(t, .35, .3))
            if u > 0:
                R.put(fr, S('signo', '↓', 110, GOLD), rx, 750 + abs(math.sin(t * 7)) * 24, u, u, anchor=(50, 66)) if False else None
                x, y = rx, 748 + abs(math.sin(t * 7)) * 20
                ImageDraw.Draw(fr).polygon([(x - 22, y - 60), (x + 22, y - 60), (x + 22, y - 12), (x + 46, y - 12), (x, y + 36), (x - 46, y - 12), (x - 22, y - 12)], fill=GOLD + (255,), outline=OUT + (255,), width=6)
        gsc = .6
        if t < toma:
            w = eo(cl(t / (toma * .9)))
            gx = 790 - 340 * w
            E.GU(fr, gx, G + 20 - abs(math.sin(t * 10)) * 22 * (1 - w), gsc, 'amor' if w > .6 else 'asombro', boca=.6, pose='agarra', brazos=w, flip=True, mira=(1, 0))
        else:
            q = t - toma
            cae = pr(t, toma + .25, .25)
            gx = 450
            hund = eo(cae)
            emo = 'feliz' if q < .25 else ('grito' if q < .9 else 'orgullo')
            rot = -10 * hund * (1 if q < .9 else max(0, 1 - (q - .9) * 2))
            E.GU(fr, gx, G + 20, gsc, emo, boca=.8, pose='senala', brazos=1., rot=rot, sy=gsc * (1 - .06 * hund * math.exp(-max(0, q - .5) * 4)))
            mx, my = mano(gx, G + 20, gsc, 446, 350)
            j = eb(pr(t, toma, .25))
            cx = _mix(rx, mx, cl(j)); cy = _mix(ry, my, cl(j))
            col = 14 * eo(cae) if q < .9 else 14 - 14 * eo(pr(t, toma + .9, .35))
            R.put(fr, brazalete(), cx, cy + col * .55, .54 * (.7 + .3 * j), .54 * (.7 + .3 * j), rot=math.sin(t * 9) * 9 * math.exp(-q * 1.2), anchor=(190, 90))
            golpe(fr, '[¡CLANK!]', 720, 780, t, toma + .45, 76, -7, toma + 1.5)
            for i in range(4):
                E.destello(fr, cx + (-120, 130, -60, 90)[i], cy + (40, 60, 150, 140)[i], t, i * .25, 1.1)
        E.FL(fr, 930, G + 30, .54, 'feliz' if t < toma + .45 else 'amor', boca=0 if t < toma + .45 else .8, gafas=1, cuello=.3,
             ala='senala' if t < toma else 'arriba', flip=True, sy=.54 * idle(t, 6 if t < toma else 12, .025))
    return draw


# =================================================================== 6 · CIERRE
def r_cierre(s):
    D = s['dur']
    def draw(fr, t):
        fondo(fr, bg_malecon())
        for k, x0 in enumerate((110, 950)):
            R.put(fr, R.spr('palmera', math.sin(t * 2 + k)), x0, 1075, .52, .52, anchor=(190, 690))
        E.titulo(fr, t, '¿YA LO *TIENES*?', 110, 548)
        # Flami aplaude atrás
        golpea = int(t * 6) % 2
        E.FL(fr, 880, 1110 - golpea * 14, .52, 'amor' if t > D * .55 else 'feliz', boca=.7, gafas=1, cuello=.4, ala='sostiene' if golpea else 'arriba', lente='estrella', flip=True, sy=.52 * idle(t, 12))
        if golpea:
            for k, (dx, dy) in enumerate(((-150, -260), (-175, -190))):
                R.put(fr, S('destellos', 34), 880 + dx, 1110 + dy, 1.1, 1.1, rot=k * 40, anchor=(39, 39))
        golpe(fr, '[¡CLAP CLAP!]', 800, 710, t, .5, 60, 7)
        # Gus pasa presumiendo
        gx = -90 + 640 * eo(cl(t / (D * .8))) + 90 * cl((t - D * .8) / (D * .2))
        gy = 1180 - abs(math.sin(t * 7)) * 22
        gsc = .66
        pose = 'senala'
        sombra(fr, gx, 1196, 220)
        GA(fr, gx, gy, gsc, emo='orgullo' if int(t * 1.5) % 2 == 0 else 'feliz', boca=.5, pose=pose, brazos=1., rot=math.sin(t * 7) * 4)
        mx, my = mano(gx, gy, gsc, 446, 350)
        R.put(fr, brazalete(), mx, my, .54, .54, rot=math.sin(t * 7 + 1) * 14, anchor=(190, 90))
        for i, (dx, dy) in enumerate(((-90, 60), (100, 40), (40, 190))):
            E.destello(fr, mx + dx, my + dy, t, i * .3, 1.2)
    return draw
