"""Escenas de caricatura 4 (25-nov-2026): Gratis en GTA VI Parte 3 — el Truffade Thrax (b_*).
Mismo motor y estilo que Neza / 5 ajustes (escenas2). Cada escena con su propio fondo dibujado.
render.py pone en R su propio módulo. El mapa de la escena 3 se cambia desde el JSON ("mapa")."""
import math
from PIL import Image, ImageDraw
import caricatura2 as C
import caricatura as K
import escenas2 as E
from caricatura import OUT, SS, GREEN, GREEN_D
from caricatura2 import L2, PINK, PINK_D, PINK_L, ORANGE, CREAM, GOLD, WHITE, CYAN, RED

R = None
_c = {}
G = E.G                                    # 1165: piso de los personajes
DARK = (26, 16, 48)
TAN = (205, 160, 100); TAN_D = (160, 112, 62)


def mk(key, fn):
    if key not in _c: _c[key] = fn()
    return _c[key]


def S(kind, *a): return E.S(kind, *a)
def cl(x, a=0., b=1.): return max(a, min(b, x))
def pr(t, s, d=.4): return R.prog(t, s, d)
def eo(x): return R.ease_out(x)
def eb(x): return R.ease_back(x)
def idle(t, v=6., a=.02): return 1 + a * math.sin(t * v)
def hop(t, v=11., a=16.): return abs(math.sin(t * v)) * a


def capa(fr, fn):
    """Dibuja con ImageDraw en una capa aparte y la mezcla (para transparencias)."""
    lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay)); fr.alpha_composite(lay)


def golpe(fr, txt, x, y, t, t0, size=90, rot=-6, t1=None):
    p = pr(t, t0, .25)
    if p <= 0: return
    a = cl(p * 3) * (1 - (pr(t, t1, .25) if t1 else 0))
    if a <= 0: return
    im = E.sfx(txt, size)
    R.put(fr, im, x, y, .4 + .6 * eb(p), .4 + .6 * eb(p), rot + math.sin(t * 12) * 3, alpha=a, anchor=(im.width / 2, im.height / 2))


def sombra(fr, x, y, w, a=90):
    ov = Image.new('RGBA', (int(w), 40), (0, 0, 0, 0))
    ImageDraw.Draw(ov).ellipse((0, 0, int(w) - 1, 39), fill=(20, 10, 40, a))
    R.comp(fr, ov, int(x - w / 2), int(y - 20))


# =================================================================== PERSONAJES CON ACCESORIOS
def _cadena(c):
    """Cadena de cartón con medalla de dólar, cinta y orillas chuecas."""
    pts = []
    for i in range(15):
        u = i / 14
        x = 162 + (316 - 162) * u
        y = 322 + 70 * math.sin(math.pi * u)
        pts.append((x, y))
    for k, (x, y) in enumerate(pts):
        if k % 2 == 0: c.elipse(x, y, 13, 9, TAN, ow=4)
        else: c.elipse(x, y, 8, 12, TAN_D, ow=4)
    c.linea([(240, 392), (240, 404)], 6, TAN_D, ow=3)
    c.poli([(204, 404), (276, 400), (282, 470), (208, 474)], TAN, ow=5)          # medalla de cartón (chueca)
    c.texto(243, 438, '$', 54, TAN_D, kind='title')
    c.poli([(196, 414), (230, 398), (236, 410), (202, 426)], (240, 236, 220), ow=3)  # cinta adhesiva
    c.linea([(212, 460), (226, 466)], 3, TAN_D); c.linea([(262, 410), (272, 418)], 3, TAN_D)


def _lentes_gus(c):
    for x0, x1 in ((198, 274), (268, 344)):
        c.rrect(x0, 158, x1, 222, 22, (18, 12, 36), ow=5)
        c.linea([(x0 + 14, 172), (x0 + 32, 166)], 6, (150, 130, 220))
    c.linea([(270, 176), (274, 176)], 6, OUT)
    c.linea([(198, 178), (170, 196)], 6, OUT)


def gus_artista(emo='orgullo', boca=0., pose='bajos', brazos=0., mira=(0, 0), lentes=True):
    key = ('ga', emo, round(boca * 3) / 3, pose, round(brazos * 4) / 4, mira, lentes)
    def f():
        im = C.gus2(emo, round(boca * 3) / 3, pose, round(brazos * 4) / 4, mira, 0., None, None, None, '').copy()
        c = L2(440, 600); _cadena(c)
        if lentes: _lentes_gus(c)
        im.alpha_composite(c.fin()); return im
    return mk(key, f)


def GA(fr, x, y, sc, flip=False, sy=None, rot=0., alpha=1., **k):
    R.put(fr, gus_artista(**k), x, y, sc, sy or sc, rot, flip, alpha, anchor=(220, 590))


def flami_lentes_abajo(emo='asombro', boca=0., cuello=0., ala='reposo', mira=(0, 0)):
    key = ('fla', emo, round(boca * 3) / 3, round(cuello * 3) / 3, ala, mira)
    return mk(key, lambda: C.flami2(emo, round(boca * 3) / 3, 0., round(cuello * 3) / 3, ala, mira, 0, '', 26))


def FLA(fr, x, y, sc, flip=True, sy=None, **k):
    R.put(fr, flami_lentes_abajo(**k), x, y, sc, sy or sc, 0., flip, 1., anchor=(220, 610))


def flami_despeinada(emo='mareo', ala='abre', cuello=0.):
    key = ('fld', emo, ala, round(cuello * 3) / 3)
    def f():
        im = C.flami2(emo, 0., 0., round(cuello * 3) / 3, ala, (0, 0), 1, '').copy()
        hx = 288 + round(cuello * 3) / 3 * 14
        c = L2(440, 620)
        for (a, b, d_) in ((-30, 70, -40), (0, 74, 0), (30, 70, 44), (-60, 62, -70)):
            x0, y0 = hx + 20 + a * .6, 82
            c.curva([(x0, y0), (x0 + d_ * .5, y0 - b * .6), (x0 + d_, y0 - b)], 10, PINK, ow=4)
        im.alpha_composite(c.fin()); return im
    return mk(key, f)


def flami_cel(emo='feliz', cuello=.3, brillo=0):
    """Flami con el celular en el ala (pantalla encendida)."""
    key = ('flc', emo, round(cuello * 3) / 3, brillo)
    def f():
        im = C.flami2(emo, 0., 1., round(cuello * 3) / 3, 'sostiene', (1, 0), 0, '').copy()
        c = L2(440, 620)
        c.rrect(336, 330, 392, 430, 12, (30, 22, 54), ow=5)
        c.rrect(343, 340, 385, 414, 7, (110, 230, 255) if brillo else (80, 160, 210), ow=0)
        for i in range(2):
            for j in range(3): c.rrect(348 + i * 20, 346 + j * 22, 362 + i * 20, 360 + j * 22, 3, (PINK, GOLD, WHITE)[(i + j) % 3], ow=0)
        c.elipse(364, 422, 4, 4, (120, 110, 150), ow=0)
        im.alpha_composite(c.fin()); return im
    return mk(key, f)


# =================================================================== OBJETOS
def thrax():
    """Hiperdeportivo (Truffade Thrax, dibujado propio). 780x270, ruedas en (170,232) y (620,232) r56.
    La ventana es hueca para ver a quien maneja."""
    def f():
        c = L2(780, 270)
        for wx in (170, 620): c.elipse(wx, 228, 72, 64, (16, 10, 30), ow=0)
        body = [(40, 236), (34, 172), (58, 140), (150, 118), (272, 74), (430, 60), (548, 96), (664, 128), (742, 152), (766, 190), (760, 236)]
        c.poli(body, (64, 76, 210))
        c.poli([(560, 236), (520, 160), (600, 136), (664, 128), (742, 152), (766, 190), (760, 236)], (28, 30, 96), ow=0)   # frente oscuro (dos tonos)
        c.curva([(372, 82), (282, 112), (300, 200), (372, 228)], 14, CREAM, ow=0)                                          # la "C" del costado
        c.poli([(312, 140), (360, 134), (372, 196), (330, 204)], (24, 18, 50), ow=4)                                        # toma de aire
        c.d.polygon(c.P([(292, 86), (430, 72), (522, 104), (470, 130), (304, 130)]), fill=(0, 0, 0, 0))                  # ventana hueca
        c.d.line(c.P([(292, 86), (430, 72), (522, 104), (470, 130), (304, 130), (292, 86)]), fill=OUT, width=5 * SS, joint='curve')
        c.linea([(408, 74), (414, 130)], 5, OUT)
        c.poli([(26, 118), (128, 110), (130, 124), (34, 134)], (40, 30, 90), ow=4)                                         # alerón
        c.linea([(90, 124), (100, 142)], 6, OUT)
        c.poli([(700, 156), (756, 172), (754, 182), (698, 170)], CREAM, ow=3)                                              # faro
        c.d.arc([(732 - 14) * SS, (206 - 16) * SS, (732 + 14) * SS, (206 + 16) * SS], 200, 340, fill=CREAM, width=6 * SS)  # parrilla de herradura
        c.d.ellipse([(732 - 13) * SS, (210 - 15) * SS, (732 + 13) * SS, (210 + 15) * SS], outline=CREAM, width=5 * SS)
        c.elipse(46, 190, 8, 14, RED, ow=3)
        c.linea([(80, 236), (740, 236)], 6, OUT)
        c.linea([(470, 150), (548, 146)], 4, (120, 130, 240))
        return c.fin()
    return mk('thrax', f)


def pickup():
    """Pickup naranja mirando a la derecha. 640x300, ruedas en (150,290) y (500,290) r52. Ventana hueca."""
    def f():
        c = L2(640, 300)
        for wx in (150, 500): c.elipse(wx, 262, 66, 60, (20, 12, 36), ow=0)
        c.rrect(26, 128, 330, 250, 16, (255, 140, 60))
        c.rrect(26, 120, 330, 138, 6, (220, 100, 40))
        c.poli([(318, 250), (318, 74), (350, 52), (462, 52), (504, 124), (604, 134), (630, 166), (632, 250)], (255, 140, 60))
        c.d.polygon(c.P([(348, 70), (454, 70), (488, 124), (348, 124)]), fill=(0, 0, 0, 0))
        c.d.line(c.P([(348, 70), (454, 70), (488, 124), (348, 124), (348, 70)]), fill=OUT, width=5 * SS, joint='curve')
        c.rrect(26, 190, 632, 208, 0, CREAM, ow=0)
        c.linea([(26, 190), (632, 190)], 4, OUT); c.linea([(26, 208), (632, 208)], 4, OUT)
        c.linea([(420, 130), (420, 248)], 4, OUT)
        c.rrect(436, 140, 470, 150, 4, (90, 60, 40), ow=3)
        c.elipse(616, 168, 12, 14, GOLD, ow=4); c.elipse(34, 150, 8, 14, RED, ow=3)
        c.rrect(596, 222, 640, 246, 8, (210, 210, 228), ow=5)
        c.rrect(10, 222, 40, 246, 8, (210, 210, 228), ow=5)
        return c.fin()
    return mk('pickup', f)


def sello_goma():
    """Sello de goma gigante con GUÁRDALO al frente. 380x400, cara de hule abajo en y=388."""
    def f():
        c = L2(380, 400)
        c.elipse(190, 58, 54, 50, (205, 140, 78))
        c.linea([(160, 40), (178, 30)], 7, (240, 200, 150))
        c.rrect(158, 100, 222, 240, 14, (180, 116, 60))
        c.rrect(24, 232, 356, 344, 20, (205, 140, 78))
        c.rrect(36, 344, 344, 388, 10, RED)
        c.texto(190, 290, 'GUÁRDALO', 60, CREAM, kind='title')
        c.linea([(60, 246), (90, 246)], 6, (240, 200, 150))
        return c.fin()
    return mk('sello', f)


def marca_sello():
    def f():
        im = R.pill('GUÁRDALO', R.F('title', 70), fg=DARK, padx=40, pady=16)
        return im
    return mk('marca', f)


def guardia(var=0, paso=0):
    key = ('guardia', var, paso)
    def f():
        c = L2(180, 350); piel = (58, 36, 96); traje = (24, 18, 44)
        dx = 14 if paso else 0
        c.rrect(56 - dx, 230, 84 - dx, 334, 10, traje); c.rrect(96 + dx, 230, 124 + dx, 334, 10, traje)
        c.rrect(48 - dx, 322, 92 - dx, 342, 8, (10, 6, 20)); c.rrect(90 + dx, 322, 134 + dx, 342, 8, (10, 6, 20))
        c.rrect(30, 106, 150, 256, 36, traje)
        c.poli([(72, 108), (108, 108), (90, 160)], WHITE, ow=3)
        c.poli([(86, 118), (94, 118), (98, 170), (90, 180), (82, 170)], RED if var % 2 else PINK_D, ow=3)
        c.elipse(90, 66, 42, 44, piel)
        c.rrect(52, 52, 128, 74, 10, (8, 6, 18), ow=4)
        c.linea([(60, 58), (76, 56)], 4, CYAN)
        c.curva([(48, 70), (40, 100), (52, 120)], 4, CYAN, ow=0)
        c.elipse(48, 70, 7, 9, CYAN, ow=3)
        if var % 2: c.poli([(52, 40), (66, 20), (114, 20), (128, 40)], (10, 6, 20), ow=4)
        sw = -24 if paso else 24
        c.linea([(36, 124), (20 + sw * .3, 210)], 26, traje, ow=4); c.linea([(144, 124), (160 - sw * .3, 210)], 26, traje, ow=4)
        return c.fin()
    return mk(key, f)


def arbusto(ojos=True, mira=0):
    key = ('arb', ojos, mira)
    def f():
        c = L2(330, 280)
        for (x, y, r, col) in ((80, 200, 74, GREEN_D), (250, 196, 76, GREEN_D), (165, 150, 96, (70, 170, 110)), (100, 130, 64, GREEN),
                               (232, 126, 66, GREEN), (165, 74, 58, (110, 215, 140)), (165, 214, 90, GREEN)):
            c.elipse(x, y, r, r * .9, col, ow=5)
        for (x, y) in ((70, 150), (120, 90), (210, 82), (270, 150), (160, 236), (90, 236), (240, 236)):
            c.curva([(x - 14, y), (x, y - 14), (x + 14, y)], 5, (40, 120, 80), ow=0)
        if ojos:
            for ex in (138, 190):
                c.elipse(ex, 150, 20, 22, CREAM, ow=4)
                c.elipse(ex + mira * 9, 152, 8, 9, OUT, ow=0)
        return c.fin()
    return mk(key, f)


def pelota():
    def f():
        c = L2(110, 110); m = 55; r = 48
        cols = [PINK, CREAM, CYAN, GOLD, CREAM, ORANGE]
        for k in range(6):
            c.d.pieslice([(m - r) * SS, (m - r) * SS, (m + r) * SS, (m + r) * SS], k * 60, (k + 1) * 60, fill=cols[k])
        c.d.ellipse([(m - r) * SS, (m - r) * SS, (m + r) * SS, (m + r) * SS], outline=OUT, width=5 * SS)
        c.elipse(m, m, 11, 11, WHITE, ow=4)
        c.linea([(m - 30, m - 30), (m - 22, m - 36)], 5, WHITE)
        return c.fin()
    return mk('pelota', f)


def porton(w=340, h=345):
    def f():
        c = L2(w, h)
        c.rrect(4, 4, w - 4, h - 4, 10, (240, 232, 250), ow=6)
        for y in range(40, h - 10, 38):
            c.linea([(12, y), (w - 12, y)], 5, (170, 150, 200))
            c.linea([(12, y + 6), (w - 12, y + 6)], 3, WHITE)
        c.rrect(w / 2 - 34, h - 50, w / 2 + 34, h - 34, 6, (150, 140, 180), ow=4)
        return c.fin()
    return mk(('porton', w, h), f)


def regla():
    def f():
        c = L2(330, 70)
        c.rrect(6, 10, 324, 62, 8, GOLD, ow=5)
        for k in range(31):
            x = 18 + k * 10
            c.linea([(x, 14), (x, 14 + (22 if k % 5 == 0 else 12))], 3, OUT)
        for k in range(0, 31, 10): c.texto(18 + k * 10 + (10 if k == 0 else 0), 50, str(k // 10 * 10), 18, OUT, kind='800')
        return c.fin()
    return mk('regla', f)


def dona(parte='atras'):
    def f():
        c = L2(220, 130); m = (110, 70)
        if parte == 'atras':
            c.elipse(110, 70, 100, 54, (255, 190, 120))
            c.elipse(110, 64, 92, 46, PINK_L, ow=0)
            c.elipse(110, 66, 40, 18, (40, 90, 160), ow=5)
        else:
            c.d.chord([10 * SS, 16 * SS, 210 * SS, 124 * SS], 0, 180, fill=(255, 190, 120), outline=OUT, width=6 * SS)
            c.d.chord([18 * SS, 18 * SS, 202 * SS, 110 * SS], 0, 180, fill=PINK_L)
            for (x, y, col) in ((40, 78, GOLD), (70, 96, CYAN), (110, 104, WHITE), (150, 96, GOLD), (182, 80, CYAN), (128, 92, ORANGE), (90, 88, WHITE)):
                c.linea([(x - 6, y - 3), (x + 6, y + 3)], 5, col)
        return c.fin()
    return mk(('dona', parte), f)


def remo():
    def f():
        c = L2(60, 260)
        c.linea([(30, 10), (30, 190)], 9, (205, 140, 78), ow=4)
        c.elipse(30, 214, 22, 40, (205, 140, 78), ow=5)
        return c.fin()
    return mk('remo', f)


def pluma(col=PINK):
    def f():
        c = L2(90, 40)
        c.afilada([(8, 20), (40, 6), (82, 20)], 12, 3, col, ow=3)
        return c.fin()
    return mk(('pluma', col), f)


def flash(r=60):
    def f():
        c = L2(2 * r + 10, 2 * r + 10); m = r + 5
        c.poli([(m, m - r), (m + r * .16, m - r * .16), (m + r, m), (m + r * .16, m + r * .16), (m, m + r), (m - r * .16, m + r * .16), (m - r, m), (m - r * .16, m - r * .16)], (255, 255, 240), ow=0)
        return C.glow(c.fin(), 10, 1.2)
    return mk(('flash', r), f)


def camara_foto():
    def f():
        c = L2(150, 110)
        c.rrect(10, 26, 140, 100, 14, (40, 30, 70))
        c.rrect(30, 12, 70, 30, 6, (40, 30, 70))
        c.elipse(80, 64, 28, 28, (120, 110, 160), ow=5); c.elipse(80, 64, 12, 12, (30, 20, 50), ow=0)
        c.rrect(110, 34, 130, 46, 3, GOLD, ow=3)
        return c.fin()
    return mk('cam', f)


# =================================================================== FONDOS DIBUJADOS
def bg_alfombra():
    """Escena 1: alfombra roja de artista (telón, muro de fotos, cuerdas)."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 460, 0, (70, 26, 90), ow=0)
        for x in range(0, 1080, 60):
            c.rrect(x, 0, x + 34, 460, 16, (92, 36, 118), ow=0)
        for j in range(4):
            for i in range(9):
                x = 60 + i * 120 + (60 if j % 2 else 0); y = 70 + j * 92
                if x < 1060: c.estrella(x, y, 16, (150, 80, 170))
        c.rrect(-10, 0, 1090, 30, 0, (40, 14, 56), ow=0)
        c.rrect(-10, 460, 1090, 560, 0, (34, 16, 60), ow=0)
        c.poli([(380, 460), (700, 460), (900, 560), (180, 560)], (210, 50, 70), ow=0)
        c.poli([(400, 460), (680, 460), (690, 470), (390, 470)], (240, 90, 100), ow=0)
        for x in (110, 970):
            c.rrect(x - 10, 360, x + 10, 520, 6, GOLD, ow=4)
            c.elipse(x, 352, 18, 18, GOLD, ow=4)
            c.rrect(x - 30, 512, x + 30, 530, 6, GOLD, ow=4)
        c.curva([(122, 380), (200, 440), (300, 400)], 12, (190, 40, 70), ow=4)
        c.curva([(958, 380), (880, 440), (780, 400)], 12, (190, 40, 70), ow=4)
        return c.fin()
    return mk('bg1', f)


def bg_showroom():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (40, 24, 80), ow=0)
        for x in range(30, 1080, 150): c.rrect(x, 40, x + 110, 400, 14, (58, 34, 104), ow=0)
        c.linea([(0, 30), (1080, 30)], 8, PINK)
        c.linea([(0, 420), (1080, 420)], 6, CYAN)
        c.rrect(-10, 440, 1090, 560, 0, (30, 18, 62), ow=0)
        for k in range(6): c.linea([(80 + k * 190, 450), (20 + k * 200, 556)], 5, (52, 34, 96))
        return c.fin()
    return mk('bg2', f)


def mapa_isla(isla='ISLA STARFISH', vecina='ISLA WAXMAN'):
    """Mapa dibujado (provisional). 940x560. Isla ovalada inclinada, calzada al sur y autopista en la costa."""
    def f():
        c = L2(940, 560)
        c.rrect(6, 6, 934, 554, 40, (60, 140, 205), ow=7)
        def ovalo(cx, cy, rx, ry, ang, n=60):
            a = math.radians(ang); out = []
            for i in range(n):
                u = i / n * 2 * math.pi; x, y = rx * math.cos(u), ry * math.sin(u)
                out.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
            return out
        c.poli(ovalo(560, 240, 300, 170, -22), (90, 170, 225), ow=0)                 # aguas bajas
        c.poli([(30, 440), (200, 470), (420, 440), (700, 470), (910, 430), (910, 548), (30, 548)], (90, 170, 225), ow=0)
        c.poli([(14, 470), (220, 500), (430, 470), (690, 500), (926, 460), (926, 546), (14, 546)], (226, 206, 170), ow=5)   # costa
        c.linea([(14, 500), (220, 528), (430, 500), (690, 528), (926, 492)], 16, WHITE)                                    # autopista
        c.linea([(14, 500), (220, 528), (430, 500), (690, 528), (926, 492)], 4, (190, 180, 200))
        c.poli(ovalo(130, 410, 90, 44, -8), (226, 206, 170))                                                                # isla vecina
        c.linea([(150, 452), (170, 486)], 12, WHITE, ow=4)
        c.linea([(430, 340), (410, 494)], 18, WHITE, ow=5)                                                                  # calzada
        c.poli(ovalo(560, 240, 250, 124, -22), (238, 222, 180))                                                             # arena
        c.poli(ovalo(560, 240, 234, 110, -22), (150, 205, 160), ow=0)                                                       # pasto
        rd = ovalo(560, 240, 160, 34, -22, 50)
        c.d.line(c.P(rd + [rd[0]]), fill=WHITE, width=12 * SS, joint='curve')
        for k in range(10):                                                                                              # calles y mansiones
            u = -1 + k * .22; a = math.radians(-22)
            bx, by = 560 + u * 150 * math.cos(a), 240 + u * 150 * math.sin(a)
            for sgn in (-1, 1):
                ex, ey = bx + sgn * 60 * math.sin(a) * -1, by + sgn * 60 * math.cos(a)
                c.linea([(bx - sgn * 30 * math.sin(a) * -1, by + sgn * 30 * math.cos(a)), (ex, ey)], 7, WHITE)
                c.rrect(ex - 18, ey - 12, ex + 18, ey + 12, 4, (150, 120, 200), ow=3)
        c.d.rounded_rectangle([6 * SS, 6 * SS, 934 * SS, 554 * SS], radius=40 * SS, outline=OUT, width=7 * SS)
        im = c.fin()
        return im
    return mk(('mapa', isla, vecina), f)


def bg_mansion():
    """Escena 4: mansión blanca con palmeras y pasto (nada arriba de y=60 para no tapar el título)."""
    def f():
        c = L2(1080, 600)
        c.rrect(140, 196, 940, 470, 10, (245, 240, 250))
        c.rrect(300, 96, 800, 200, 10, (245, 240, 250))
        c.rrect(120, 180, 960, 204, 6, (200, 186, 226))
        c.rrect(280, 80, 820, 102, 6, (200, 186, 226))
        for i in range(4):
            x0 = 180 + i * 190
            c.rrect(x0, 236, x0 + 150, 330, 8, (150, 120, 220) if i % 2 else (255, 214, 150))
            c.linea([(x0 + 75, 236), (x0 + 75, 330)], 4, OUT)
        for i in range(3):
            x0 = 330 + i * 150
            c.rrect(x0, 118, x0 + 120, 184, 8, (150, 120, 220), ow=5)
        c.rrect(490, 350, 590, 470, 8, (130, 90, 60))
        c.elipse(574, 414, 6, 6, GOLD, ow=2)
        c.rrect(-10, 430, 1090, 490, 0, (40, 120, 80), ow=0)
        for x in range(-20, 1100, 70): c.elipse(x, 440, 46, 34, (50, 140, 90), ow=4)
        c.rrect(-10, 470, 1090, 600, 0, (70, 160, 110), ow=0)
        for x in range(0, 1080, 120): c.rrect(x, 470, x + 60, 600, 0, (80, 172, 120), ow=0)
        c.poli([(470, 470), (610, 470), (700, 600), (380, 600)], (230, 214, 190), ow=0)
        im = c.fin()
        for (x, s) in ((70, .76), (1010, .8)):
            p = R.spr('palmera', 0.); p = p.resize((int(p.width * s), int(p.height * s)), Image.LANCZOS)
            im.alpha_composite(p, (int(x - 190 * s), int(510 - 690 * s)))
        return im
    return mk('bg4', f)


def bg_garaje():
    """Escena 5: costado de la mansión con el portón del garaje (x 720-1060)."""
    def f():
        c = L2(1080, 600)
        c.rrect(-10, 60, 1090, 540, 0, (232, 218, 242), ow=0)
        for y in range(100, 540, 46): c.linea([(0, y), (1080, y)], 2, (214, 198, 230))
        c.rrect(-10, 30, 1090, 80, 0, (74, 38, 120), ow=0)
        for x in range(0, 1100, 54): c.elipse(x, 80, 27, 16, (74, 38, 120), ow=0)
        c.rrect(70, 170, 280, 330, 10, (150, 120, 220), ow=6)
        c.linea([(175, 170), (175, 330)], 4, OUT); c.linea([(70, 250), (280, 250)], 4, OUT)
        c.rrect(60, 326, 290, 344, 6, (200, 186, 226), ow=4)
        c.rrect(700, 170, 1080, 200, 4, (74, 38, 120), ow=5)
        c.elipse(660, 220, 20, 26, GOLD, ow=4); c.linea([(660, 194), (660, 176)], 6, OUT)
        c.rrect(-10, 535, 1090, 600, 0, (96, 84, 130), ow=0)
        for x in range(0, 1080, 160): c.linea([(x, 540), (x - 40, 600)], 4, (120, 108, 156))
        c.rrect(330, 450, 400, 535, 10, (205, 140, 78))
        for (dx, dy) in ((-20, -20), (0, -40), (20, -16)): c.elipse(365 + dx, 440 + dy, 30, 26, GREEN, ow=4)
        im = c.fin()
        im.alpha_composite(porton(340, 335), (720, 200))
        return im
    return mk('bg5', f)


GAP = (440, 770, 870)          # escena 6: x donde empieza el portón, y de arriba y abajo del hueco (en pantalla)


def bg_hueco(top=600):
    """Escena 6: acercamiento al portón con el hueco arriba."""
    def f():
        c = L2(1080, 620)
        y = lambda Y: Y - top
        c.rrect(-10, y(680), 1090, 562, 0, (232, 218, 242), ow=0)
        for yy in range(y(680) + 30, 560, 46): c.linea([(0, yy), (1080, yy)], 2, (214, 198, 230))
        c.rrect(GAP[0] - 20, y(700), 1100, y(GAP[1]), 6, (74, 38, 120))                    # dintel
        c.rrect(GAP[0], y(GAP[1]), 1100, y(GAP[2]), 0, (14, 8, 30), ow=5)                  # hueco oscuro
        c.rrect(GAP[0] + 10, y(GAP[1]) + 8, 1100, y(GAP[1]) + 20, 0, (40, 26, 70), ow=0)
        im_p = porton(700, 300)
        c.elipse(250, y(760), 26, 32, GOLD, ow=4); c.linea([(250, y(728)), (250, y(708))], 6, OUT)
        c.rrect(-10, 562, 1090, 620, 0, (96, 84, 130), ow=0)
        im = c.fin()
        im.alpha_composite(im_p, (GAP[0], y(GAP[2]) - 4))
        return im
    return mk('bg6', f)


def bg_interior():
    def f():
        c = L2(1080, 600)
        c.rrect(-10, 50, 1090, 520, 0, (64, 44, 104), ow=0)
        for x in range(0, 1080, 90): c.linea([(x, 50), (x, 520)], 3, (74, 52, 118))
        c.rrect(80, 140, 420, 380, 12, (90, 70, 140), ow=5)
        for i in range(10):
            for j in range(7): c.elipse(104 + i * 33, 160 + j * 32, 3, 3, (60, 44, 96), ow=0)
        c.linea([(130, 190), (130, 300)], 12, CREAM, ow=3); c.rrect(110, 176, 150, 200, 6, CREAM, ow=3)        # martillo
        c.linea([(220, 180), (250, 320)], 10, CREAM, ow=3); c.elipse(216, 176, 16, 16, CREAM, ow=3)            # llave
        c.linea([(320, 190), (320, 330)], 8, CREAM, ow=3); c.poli([(300, 190), (340, 190), (330, 230), (310, 230)], CREAM, ow=3)
        for (x0, x1) in ((60, 440), (560, 860)):
            c.rrect(x0, 66, x1, 88, 11, (255, 230, 250))
        for k in range(3): c.elipse(500, 470 - k * 44, 70, 26, (30, 22, 50), ow=5); c.elipse(500, 470 - k * 44, 30, 10, (60, 50, 90), ow=0)
        c.rrect(880, 160, 1100, 520, 0, (255, 214, 170), ow=6)
        c.elipse(990, 250, 46, 46, (255, 240, 200), ow=0)
        c.rrect(-10, 520, 1090, 600, 0, (44, 30, 76), ow=0)
        for i in range(0, 1080, 90):
            c.rrect(i, 520, i + 45, 560, 0, (60, 42, 100), ow=0); c.rrect(i + 45, 560, i + 90, 600, 0, (60, 42, 100), ow=0)
        im = c.fin()
        lu = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lu)
        for (x0, x1) in ((60, 440), (560, 860)): d.polygon([(x0, 88), (x1, 88), (x1 + 80, 520), (x0 - 80, 520)], fill=(255, 230, 250, 26))
        im.alpha_composite(lu)
        return im
    return mk('bg7', f)


# =================================================================== 1 · GANCHO
def b_hook(s):
    D = s['dur']; gratis = s.get('t_gratis', D - 1.0)
    def draw(fr, t):
        R.put(fr, bg_alfombra(), 540, 1210, 1, 1, alpha=eo(pr(t, 0, .3)), anchor=(540, 560))
        # reflectores
        def luces(d):
            for k, (x0, ph) in enumerate(((120, 0), (960, 1.7))):
                tx = 380 + math.sin(t * 2.2 + ph) * 60
                d.polygon([(x0 - 20, 660), (x0 + 20, 660), (tx + 150, 1180), (tx - 150, 1180)], fill=(255, 240, 200, 34))
        capa(fr, luces)
        E.titulo(fr, t, '¿EL BUGATTI DE *BAD BUNNY*?', 96, 560, .05)
        # Gus de artista: poses y caras que cambian
        poses = (('celebra', 'orgullo', 0.), ('cadera', 'feliz', .6), ('senala', 'orgullo', .3), ('celebra', 'feliz', .9))
        k = min(len(poses) - 1, int(t / .75))
        pose, emo, boca = poses[k]
        if t >= gratis: pose, emo, boca = 'celebra', 'asombro', 1.
        snap = 1 + .05 * math.sin(math.pi * cl((t - k * .75) / .15)) if t < gratis else 1
        GA(fr, 380, G, .74 * snap, sy=.74 * snap * idle(t, 7), emo=emo, boca=boca, pose=pose, brazos=1., mira=(1, 0) if k % 2 else (0, 0))
        # cámaras y flashes
        for i, (x, y, rot) in enumerate(((150, 1010, 10), (690, 1000, -10))):
            u = eb(pr(t, .2 + i * .1, .3))
            if u > 0: R.put(fr, camara_foto(), x, y + math.sin(t * 5 + i) * 6, .8 * u, .8 * u, rot=rot, anchor=(75, 55))
        flashes = (.35, .8, 1.25, 1.7, 2.15)
        for i, tf in enumerate(flashes):
            q = pr(t, tf, .22)
            if 0 < q < 1:
                xx, yy = (190, 940) if i % 2 == 0 else (660, 930)
                R.put(fr, flash(60), xx, yy, .5 + 1.2 * q, .5 + 1.2 * q, rot=q * 45, alpha=1 - q, anchor=(65, 65))
                if q < .5: E.rect(fr, (0, 700, R.W, 1210), (255, 250, 240, int(70 * (1 - q * 2))))
        # Flami con los lentes abajo; al "gratis" se le hacen corazones los ojos
        if t < gratis:
            FLA(fr, 900, G, .7, emo='asombro' if t < .9 else 'enojo', boca=0., cuello=.3 + .1 * math.sin(t * 3), ala='cadera', mira=(-1, 0), sy=.7 * idle(t, 5))
        else:
            E.FL(fr, 900, G - hop(t, 12, 18), .7, 'amor', boca=1., gafas=0, cuello=.6, ala='arriba', flip=True, sy=.7 * idle(t, 12, .03))
        # GRATIS: sello grande
        if t >= gratis:
            p = pr(t, gratis, .3)
            im = E.pilg('GRATIS', 110, 54, 20)
            k_ = (2.2 - 1.2 * eo(p)) * (1 + .04 * math.sin(t * 10))
            R.put(fr, im, 600, 790, k_, k_, rot=-8, alpha=cl(p * 3), anchor=(im.width / 2, im.height / 2))
            for i in range(5):
                a = i * 2 * math.pi / 5 + .3
                E.destello(fr, 600 + math.cos(a) * 300, 790 + math.sin(a) * 110, t, i * .2, 1.2)
        if gratis - .05 < t < gratis + .18:
            E.rect(fr, (0, 700, R.W, 1210), (255, 241, 234, int(120 * cl(1 - abs(t - gratis - .05) / .13))))
    return draw


# =================================================================== 2 · TRUFFADE THRAX + GUÁRDALO
def b_thrax(s):
    D = s['dur']; cae = s.get('t_sello', .75)
    def draw(fr, t):
        R.put(fr, bg_showroom(), 540, 1210, 1, 1, anchor=(540, 560))
        E.titulo(fr, t, 'TRUFFADE *THRAX*', 104, 560)
        # plataforma giratoria con rayos
        def rayos(d):
            for k in range(8):
                a = t * .8 + k * math.pi / 4
                x1 = 640 + math.cos(a) * 520; y1 = 900 + math.sin(a) * 260
                x2 = 640 + math.cos(a + .14) * 520; y2 = 900 + math.sin(a + .14) * 260
                d.polygon([(640, 960), (x1, y1), (x2, y2)], fill=(255, 224, 160, 20))
            d.ellipse((310, G - 40, 970, G + 40), fill=(122, 63, 191, 255), outline=(26, 16, 48, 255), width=6)
            d.ellipse((330, G - 32, 950, G + 28), fill=(150, 90, 220, 255))
        capa(fr, rayos)
        ce = eo(pr(t, 0, .45))
        cx = 640 + (1 - ce) * 600
        sc = .72
        R.put(fr, thrax(), cx, G - 8, sc, sc, anchor=(390, 236))
        for wx in (170, 620):
            R.put(fr, S('rueda', 64), cx + (wx - 390) * sc, G - 8 + (232 - 236) * sc, sc * .86, sc * .86, rot=-(1 - ce) * 600, anchor=(70, 70))
        E.destello(fr, cx + 140, G - 160, t, 0, 1.2); E.destello(fr, cx - 120, G - 120, t, .5, 1.)
        # Gus admira el coche... y le cae el sello
        gx = 190
        q = pr(t, cae, .22)                      # caída
        imp = cae + .22
        if t < imp:
            E.GU(fr, gx, G, .64, 'amor' if t > .35 else 'asombro', boca=.6, pose='pecho', brazos=1., mira=(1, 0), sy=.64 * idle(t, 9, .03))
        else:
            rec = pr(t, imp + .55, .45)
            sqy = .64 * (.24 + .76 * eb(rec)); sqx = .64 * (1.35 - .35 * eo(rec))
            E.GU(fr, gx, G, sqx, 'asombro' if rec <= 0 else 'confuso', boca=.6, pose='encoge', brazos=1., sy=sqy)
            if rec > 0: R.put(fr, K.estrellas_mareo(t), gx, G - 400 * sqy / .64 - 20, 1, 1, anchor=(110, 45))
        # el sello (entra arriba de la zona segura y cae)
        if t > cae - .12:
            st = sello_goma(); ss_ = .82
            if t < imp:
                y = 640 + (G - 640) * (q ** 2) if t >= cae else 640 - 60 * (1 - (t - cae + .12) / .12)
                a = cl((t - (cae - .12)) / .1)
                sombra(fr, gx, G + 4, 120 + 200 * q, int(60 + 80 * q))
            else:
                lift = eo(pr(t, imp + .3, .35))
                y = G - 520 * lift; a = 1 - lift
            if a > 0: R.put(fr, st, gx, y, ss_, ss_, rot=0, alpha=a, anchor=(190, 388))
        if t >= imp:
            golpe(fr, '[¡PLAF!]', gx + 40, 900, t, imp, 86, -8, imp + .6)
            m = marca_sello(); p = pr(t, imp + .45, .3)
            if p > 0:
                k_ = (1.8 - .8 * eo(p)) * .9
                R.put(fr, m, 560, 790, k_, k_, rot=-7, alpha=cl(p * 3), anchor=(m.width / 2, m.height / 2))
            for i in range(6):
                u = pr(t, imp, .5)
                if 0 < u < 1:
                    a_ = i * math.pi / 5 + math.pi
                    R.put(fr, S('nube_polvo', 46), gx + math.cos(a_) * 170 * eo(u), G - 20 + math.sin(a_) * 40 * eo(u), .7 + u * .6, .7 + u * .6, alpha=1 - u, anchor=(69, 46))
        # Flami se ríe
        fe = 'guino' if t > imp + .1 else 'feliz'
        E.FL(fr, 960, G, .56, fe, boca=.8 if t > imp + .1 else .2, gafas=0 if fe == 'guino' else 1, cuello=.3 + (.2 * math.sin(t * 14) if t > imp + .1 else 0), ala='senala' if t > imp + .1 else 'reposo', flip=True, sy=.56 * idle(t, 10 if t > imp else 5, .03))
    return draw


# =================================================================== 3 · MAPA ISLA STARFISH (provisional)
def b_mapa(s):
    D = s['dur']
    cfg = s.get('mapa', {})
    isla = cfg.get('isla', 'ISLA STARFISH'); vecina = cfg.get('vecina', 'ISLA WAXMAN')
    pin = cfg.get('pin', [700, 186]); ruta = cfg.get('ruta', [[60, 290], [290, 330]])
    MX0, MY0 = 540 - 470, 930 - 280
    def draw(fr, t):
        E.titulo(fr, t, '1 · MANSIÓN EN *ISLA STARFISH*', 80, 548)
        pe = eo(pr(t, 0, .35))
        R.put(fr, mapa_isla(isla, vecina), 540, 930, .8 + .2 * pe, .8 + .2 * pe, alpha=cl(pe * 2), anchor=(470, 280))
        if pe < 1: return
        # olas
        d = ImageDraw.Draw(fr)
        for k in range(7):
            x = MX0 + 60 + (k * 131 + t * 40) % 800; y = MY0 + 60 + (k * 67) % 120
            if x < MX0 + 880: d.arc((x - 16, y - 6, x + 16, y + 10), 200, 340, fill=(200, 235, 255, 255), width=4)
        # etiquetas
        R.anim_in(fr, E.pil(isla, 34, bg=(74, 38, 120)), MX0 + cfg.get('etiqueta', [330, 80])[0], MY0 + cfg.get('etiqueta', [330, 80])[1], t, .25, 'pop', .25)
        R.anim_in(fr, E.pil(vecina, 24, bg=(74, 38, 120), padx=16, pady=6), MX0 + 130, MY0 + 352, t, .35, 'pop', .25)
        # pin de la mansión
        u = pr(t, .45, .4)
        if u > 0:
            px, py = MX0 + pin[0], MY0 + pin[1]
            r = (t - .8) % 1.0
            if t > .8:
                d.ellipse((px - 14 - 46 * r, py - 7 - 20 * r, px + 14 + 46 * r, py + 7 + 20 * r), outline=(255, 241, 234, int(230 * (1 - r))), width=5)
            R.put(fr, S('pin', PINK, 70), px, py + (1 - eo(u)) * -180, 1.1 * eb(u), 1.1 * eb(u), anchor=(35, 90))
            if t > .7: R.put(fr, _mini_mansion(), px + 70, py - 30, .9 * eb(pr(t, .7, .3)), .9 * eb(pr(t, .7, .3)), anchor=(50, 60))
        # Gus remando en su dona
        a, b = ruta
        w = eo(cl(t / (D * .8)))
        gx = MX0 + a[0] + (b[0] - a[0]) * w; gy = MY0 + a[1] + (b[1] - a[1]) * w + math.sin(t * 6) * 4
        for k in range(4):
            q = (t * 1.6 + k * .25) % 1
            d.ellipse((gx - 70 - 60 * q - 40 * k * 0, gy - 6 - 10 * q, gx - 10 - 20 * q, gy + 14 + 10 * q), outline=(220, 240, 255, int(200 * (1 - q))), width=3)
        sc = .62
        R.put(fr, dona('atras'), gx, gy, sc, sc, anchor=(110, 70))
        E.GU(fr, gx, gy + 6, .27, 'concentrado' if t < D * .7 else 'feliz', boca=0 if t < D * .7 else .6, pose='agarra', brazos=1., recorte=True, rot=math.sin(t * 7) * 6)
        R.put(fr, remo(), gx + 40, gy - 10, .5, .5, rot=-40 + math.sin(t * 7) * 35, anchor=(30, 100))
        R.put(fr, dona('frente'), gx, gy, sc, sc, anchor=(110, 70))
    return draw


def _mini_mansion():
    def f():
        c = L2(100, 70)
        c.rrect(8, 26, 92, 64, 6, (245, 240, 250), ow=4)
        c.rrect(26, 8, 74, 30, 5, (245, 240, 250), ow=4)
        for i in range(3): c.rrect(16 + i * 26, 36, 32 + i * 26, 52, 3, GOLD, ow=2)
        return c.fin()
    return mk('minim', f)


# =================================================================== 4 · QUITA A LOS GUARDIAS
def b_guardias(s):
    D = s['dur']; tiro = s.get('t_tiro', .3)
    def draw(fr, t):
        R.put(fr, bg_mansion(), 540, 1230, 1, 1, anchor=(540, 600))
        E.titulo(fr, t, '2 · QUITA A LOS *GUARDIAS*', 88, 548)
        # pelota de playa: sale del ala de Flami y vuela a la izquierda
        bp = pr(t, tiro, .9)
        bx = 830 - 1000 * bp; by = 900 - 260 * math.sin(math.pi * bp) + (0 if bp < 1 else 0)
        # guardias
        corre = tiro + .35
        for k, x0 in enumerate((560, 720)):
            if t < corre:
                R.put(fr, guardia(k, 0), x0, G + 4, .92, .92, anchor=(90, 340))
                if t > tiro + .1: R.put(fr, S('signo', '!', 110, GOLD), x0, 790, eb(pr(t, tiro + .1, .2)), eb(pr(t, tiro + .1, .2)), anchor=(50, 66))
            else:
                tt = t - corre
                x = x0 - 900 * eo(cl(tt / 1.1)) - 200 * tt
                if x > -150:
                    R.put(fr, guardia(k, int(t * 10) % 2), x, G + 4 - hop(t, 14, 22), .92, .92, rot=8, flip=True, anchor=(90, 340))
                    for j in range(3):
                        q = (t * 3 + j * .33 + k * .5) % 1
                        R.put(fr, S('nube_polvo', 46), x + 60 + q * 120, G - 10, .4 + q * .5, .4 + q * .5, alpha=(1 - q) * .7, anchor=(69, 46))
        if bp > 0 and bx > -120:
            R.put(fr, pelota(), bx, by, 1, 1, rot=-t * 600, anchor=(55, 55))
        # Gus disfrazado de arbusto
        sale = s.get('t_sale', D - .9)
        ax = 300 + math.sin(t * 3) * 6
        if t > sale:
            u = eb(pr(t, sale, .35))
            E.GU(fr, ax, G - 40 - 150 * u, .55, 'feliz', boca=.7, pose='celebra', brazos=1., recorte=True)
        mira = 1 if (t < tiro + .2) else -1
        R.put(fr, arbusto(t <= sale, mira), ax, G + 10, .95, .95 * (1 + .03 * math.sin(t * 9)), rot=math.sin(t * 8) * 2, anchor=(165, 270))
        if t > sale + .2: R.pop_burbuja(fr, E.bub('¡Libre!', 0, 50), ax, G - 330, t, sale + .2)
        # Flami lanza la pelota
        lanz = tiro - .15 < t < tiro + .3
        E.FL(fr, 930, G, .62, 'guino' if t > tiro + .3 else 'feliz', boca=.4, gafas=0 if t > tiro + .3 else 1, cuello=.3, ala='arriba' if lanz else ('senala' if t > tiro + .3 else 'sostiene'),
             flip=True, sy=.62 * idle(t, 6))
        if t < tiro: R.put(fr, pelota(), 870, 930, .8, .8, anchor=(55, 55))
    return draw


# =================================================================== 5 · PICKUP EN LA PUERTA
def b_pickup(s):
    D = s['dur']; llega = s.get('t_llega', .9)
    def draw(fr, t):
        R.put(fr, bg_garaje(), 540, 1230, 1, 1, anchor=(540, 600))
        E.titulo(fr, t, '3 · PICKUP EN LA *PUERTA*', 88, 548)
        sc = .78; nose = 620; door = 720
        xf = door - (nose - 320) * sc
        p = cl(t / llega)
        x = xf - (1 - eo(p)) * 900
        rebote = 0.
        if t > llega:
            q = t - llega
            rebote = -26 * math.exp(-q * 6) * math.sin(q * 18)
        x += rebote
        sq = 1 + (.05 * math.exp(-(t - llega) * 6) * math.sin((t - llega) * 22) if t > llega else 0)
        sombra(fr, x, G + 4, 470)
        body = pickup()
        f = lambda px, py: (x + (px - 320) * sc, G + (py - 290) * sc * sq)
        x0, y0 = f(348, 70); x1, y1 = f(488, 124)
        hb = abs(math.sin((t - llega) * 16)) * 14 * math.exp(-(t - llega) * 4) if t > llega else 0
        def gu_in(L, ox, oy):
            gx, gy = f(410, 150)
            E.GU(L, gx + ox, gy + oy - hb, sc * .36, 'feliz' if t < llega else ('asombro' if t < llega + .5 else 'orgullo'), boca=.5, pose='agarra', brazos=1., recorte=True)
        E.clip(fr, (x0, y0, x1, y1), gu_in)
        R.put(fr, body, x, G, sc, sc * sq, anchor=(320, 290))
        for wx in (150, 500):
            R.put(fr, S('rueda', 64), f(wx, 262)[0], f(wx, 262)[1], sc * .8, sc * .8, rot=(-(eo(p) * 900)) % 360, anchor=(70, 70))
        if t < llega:
            for k in range(3):
                q = (t * 2 + k * .33) % 1
                R.put(fr, S('nube_polvo', 46), x - 260 - q * 120, G - 20, .5 + q * .6, .5 + q * .6, alpha=(1 - q) * .8, anchor=(69, 46))
        golpe(fr, '[¡TOC!]', 640, 880, t, llega, 84, 8, llega + .45)
        # Flami mide con la regla
        fl = pr(t, llega + .3, .4)
        if fl > 0:
            fx = 1150 - 260 * eo(fl)
            E.FL(fr, fx, G + 10, .5, 'feliz' if t < llega + 1.0 else 'guino', boca=.3, gafas=1 if t < llega + 1.0 else 0, cuello=.4, ala='senala', flip=True, sy=.5 * idle(t, 6))
            R.put(fr, regla(), fx - 104, G + 10 + (346 - 610) * .5, .62 * eb(fl), .62 * eb(fl), rot=math.sin(t * 6) * 2, anchor=(300, 35))
            if t > llega + .8:
                R.anim_in(fr, E.pilg('0 CM', 54, 28, 10), 720, 930, t, llega + .8, 'pop', .25)
        E.sello(fr, t, max(llega + 1.2, D - .8), 300, 820, .7)
    return draw


# =================================================================== 6 · SALTA AL HUECO + CELULAR
def b_hueco(s):
    D = s['dur']; salto = s.get('t_salto', .35); atora = salto + .4; cel = s.get('t_cel', atora + .35)
    def draw(fr, t):
        R.put(fr, bg_hueco(600), 540, 1220, 1, 1, anchor=(540, 620))
        E.titulo(fr, t, '4 · SALTA AL *HUECO* + CELULAR', 80, 548)
        sc = 1.0; nose = 620
        x = GAP[0] - (nose - 320) * sc + 6
        R.put(fr, pickup(), x, G + 40, sc, sc, anchor=(320, 290))
        roof = G + 40 - (290 - 52) * sc
        gsc = .58
        if t < salto:
            E.GU(fr, x - 60, roof + 6, gsc, 'concentrado', pose='bajos', brazos=0., sy=gsc * (1 - .12 * pr(t, 0, salto)))
        elif t < atora:
            q = (t - salto) / (atora - salto)
            sx0, sy0 = x - 60, roof + 6
            ex, ey = GAP[0] - 150, (GAP[1] + GAP[2]) / 2 - 40
            gx = sx0 + (ex - sx0) * q; gy = sy0 + (ey - sy0) * q - 220 * math.sin(math.pi * q)
            E.GU(fr, gx, gy, gsc, 'grito', boca=1., pose='orejas', brazos=1., rot=-90 * eo(q))
        else:
            wig = math.sin(t * 20) * 7
            fx, fy = GAP[0] - 150, (GAP[1] + GAP[2]) / 2 - 40
            def gu_in(L, ox, oy):
                E.GU(L, fx + ox, fy + oy, gsc, 'grito', boca=1., pose='orejas', brazos=.5 + .5 * math.sin(t * 16), rot=-90 + wig)
            E.clip(fr, (0, 0, GAP[0], R.H), gu_in)
            golpe(fr, '[¡ATORADO!]', 640, 1000, t, atora, 70, -6)
            for k in range(3):
                q = (t * 2.4 + k * .33) % 1
                R.put(fr, S('signo', '!', 70, GOLD), GAP[0] - 260 - k * 30, GAP[1] - 30 - q * 60, .8, .8, alpha=1 - q, anchor=(32, 42))
        # Flami saca el celular, tranquilo
        if t < cel:
            E.FL(fr, 880, G + 10, .6, 'feliz', boca=0., gafas=1, cuello=.2, ala='reposo', flip=True, sy=.6 * idle(t, 4))
        else:
            R.put(fr, flami_cel('feliz', .2 + .05 * math.sin(t * 2), int(t * 4) % 2), 880, G + 10, .6, .6 * idle(t, 4), 0, True, 1., anchor=(220, 610))
            u = eb(pr(t, cel, .3))
            R.pop_burbuja(fr, E.bub('Tranqui...', 0, 46), 760, 860, t, cel + .25)
    return draw


# =================================================================== 7 · APARECES ADENTRO: LLÉVATELO
def b_adentro(s):
    D = s['dur']; pop_t = s.get('t_pop', .25); arranca = s.get('t_arranca', 1.0)
    def draw(fr, t):
        R.put(fr, bg_interior(), 540, 1240, 1, 1, anchor=(540, 600))
        E.titulo(fr, t, '5 · APARECES ADENTRO: *LLÉVATELO*', 76, 548)
        sc = .62
        q = cl((t - arranca) / 1.0)
        cx = 420 + 1100 * q ** 2
        sombra(fr, cx, G + 4, 470)
        f = lambda px, py: (cx + (px - 390) * sc, G - 8 + (py - 236) * sc)
        if t >= arranca - .25:
            x0, y0 = f(292, 64); x1, y1 = f(522, 132)
            def gu_in(L, ox, oy):
                gx, gy = f(400, 150)
                E.GU(L, gx + ox, gy + oy, sc * .34, 'feliz', boca=.8, pose='agarra', brazos=1., recorte=True)
            E.clip(fr, (x0, y0, x1, y1), gu_in)
        R.put(fr, thrax(), cx, G - 8, sc, sc, anchor=(390, 236))
        for wx in (170, 620):
            R.put(fr, S('rueda', 64), f(wx, 232)[0], f(wx, 232)[1], sc * .86, sc * .86, rot=-(q * 1400) % 360, anchor=(70, 70))
        if q > 0:
            E.lineas_vel(fr, t, 900, 1150, 8, int(180 * cl(q * 3)))
            for k in range(4):
                u = (t * 2.2 + k * .25) % 1
                R.put(fr, S('nube_polvo', 46), cx - 270 - u * 160, G - 20, .6 + u * .7, .6 + u * .7, alpha=(1 - u) * .8, anchor=(69, 46))
        # Gus aparece con "pop" y salta al coche
        if pop_t <= t < arranca - .25:
            u = eb(pr(t, pop_t, .25))
            j = pr(t, arranca - .55, .3)
            E.GU(fr, 150 + 120 * eo(j), G - 160 * math.sin(math.pi * j), .6 * u, 'asombro' if t < pop_t + .35 else 'feliz', boca=.8, pose='celebra', brazos=1., sy=.6 * u * idle(t, 12, .03))
        E.poof(fr, 150, G - 150, t, pop_t - .05)
        golpe(fr, '[¡POP!]', 170, 860, t, pop_t, 90, -8, pop_t + .7)
        # Flami en la salida: el coche pasa y la despeina
        pasa = arranca + .45
        if t < pasa:
            E.FL(fr, 980, G + 10, .56, 'asombro' if t > arranca else 'feliz', boca=.6 if t > arranca else 0, gafas=1, cuello=.3, ala='abre' if t > arranca else 'reposo', flip=True, sy=.56 * idle(t, 5))
        else:
            v = pr(t, pasa, .5)
            rot = 360 * eo(v) * 2
            R.put(fr, flami_despeinada('mareo', 'abre', .3), 980, G + 10, .56, .56, rot=rot if v < 1 else math.sin(t * 6) * 6, flip=True, anchor=(220, 610))
            for k in range(6):
                u = pr(t, pasa + k * .05, .8)
                if 0 < u < 1:
                    R.put(fr, pluma([PINK, PINK_L, PINK_D][k % 3]), 980 - 60 + k * 20 + u * 200 * math.cos(k), 900 - u * 160 + math.sin(u * 9 + k) * 20, 1, 1, rot=u * 400 + k * 50, alpha=1 - u, anchor=(45, 20))
            golpe(fr, '[¡FIUUU!]', 760, 870, t, pasa, 74, 6, pasa + .6)
    return draw


# =================================================================== 8 · CIERRE
def b_cierre(s):
    D = s['dur']
    def draw(fr, t):
        # costa al atardecer: mar, arena y carretera
        def costa(d):
            d.rectangle((0, 760, R.W, 960), fill=(70, 80, 170, 235))
            for k in range(14):
                x = (k * 173 - t * 60) % (R.W + 200) - 100; y = 790 + (k * 37) % 150
                d.line([(x, y), (x + 70, y)], fill=(255, 214, 190, 160), width=4)
            d.rectangle((0, 960, R.W, 1030), fill=(232, 200, 160, 245))
            d.rectangle((0, 1030, R.W, 1210), fill=(42, 20, 72, 245))
            d.rectangle((0, 1030, R.W, 1040), fill=(122, 63, 191, 255))
            for x in range(-140 + int(-t * 500) % 220, R.W, 220): d.rectangle((x, 1120, x + 110, 1130), fill=(255, 241, 234, 170))
        capa(fr, costa)
        for k, xs in enumerate((80, 480, 880)):
            x = (xs - t * 180) % (R.W + 300) - 150
            R.put(fr, R.spr('palmera', math.sin(t * 2 + k)), x, 1035, .5, .5, anchor=(190, 690))
        E.titulo(fr, t, '¿YA LO *TIENES*?', 110, 548)
        # Gus pasa tocando el claxon (ida y vuelta)
        sc = .5
        for (t0, t1, izq) in ((.2, 2.0, False), (2.4, D - .3, True)):
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                cx = -450 + (R.W + 900) * u if not izq else R.W + 450 - (R.W + 900) * u
                y = G - 30 + math.sin(t * 20) * 2
                f = lambda px, py: (cx + ((px - 390) if not izq else (390 - px)) * sc, y + (py - 236) * sc)
                x0, y0 = f(292, 64); x1, y1 = f(522, 132)
                if izq: x0, x1 = x1, x0
                def gu_in(L, ox, oy):
                    gx, gy = f(400, 150)
                    E.GU(L, gx + ox, gy + oy, sc * .34, 'feliz', boca=.9, pose='saluda', brazos=1., recorte=True, flip=izq)
                E.clip(fr, (x0, y0, x1, y1), gu_in)
                R.put(fr, thrax(), cx, y, sc, sc, flip=izq, anchor=(390, 236))
                for wx in (170, 620):
                    p_ = f(wx, 232); R.put(fr, S('rueda', 64), p_[0], p_[1], sc * .86, sc * .86, rot=-(t * 900) % 360 * (1 if not izq else -1), anchor=(70, 70))
                if .3 < u < .7: golpe(fr, '[¡PIII PIII!]', cx, 920, t, t0 + (t1 - t0) * .3, 64, -5 if not izq else 5)
        # Flami saluda; al final pregunta por el primer viaje
        E.FL(fr, 900, G - 30, .58, 'feliz' if t < 2.2 else 'amor', boca=.4, gafas=1, cuello=.3, ala='saluda' if int(t * 3) % 2 else 'arriba', lente='estrella', flip=True, sy=.58 * idle(t, 6))
        R.pop_burbuja(fr, E.bub('¡Mándaselo!', 0, 48), 760, 900, t, 2.2)
    return draw
