"""Escenas de caricatura 6 (26-nov-2026): la patrulla Tempesta de Vice Beach (v_*).
Mismo motor y estilo que escenas4/5. Todo dibujado, sin logos ni marcas.
El mapa de la escena 2 se cambia desde el JSON ("mapa")."""
import math
from PIL import Image, ImageDraw
import caricatura2 as C
import escenas2 as E
import escenas4 as B
from caricatura import OUT, SS, GREEN
from caricatura2 import L2, PINK, PINK_D, PINK_L, ORANGE, CREAM, GOLD, WHITE, CYAN, RED
from escenas4 import mk, S, cl, pr, eo, eb, idle, hop, capa, golpe, sombra, G, FLA

R = None
AZUL = (38, 60, 150); AZUL_D = (24, 34, 92); AZUL_L = (90, 130, 240)
ROJO_S = (255, 60, 80); AZUL_S = (60, 140, 255)


def _mix(a, b, u): return a + (b - a) * u


def fondo(fr, im, y=1210): R.put(fr, im, 540, y, 1, 1, anchor=(540, im.height))


# =================================================================== GORRA Y GUS POLICÍA
def _gorra(c, dy=0):
    """Gorra de policía gigante sobre la cabeza de Gus (coordenadas del sprite 440x600)."""
    y = lambda v: v + dy
    X = lambda x: 250 + (x - 250) * 1.18
    poli, linea, estrella = c.poli, c.linea, c.estrella
    c = type('G', (), {})()
    c.poli = lambda p, *a, **k: poli([(X(x), v) for x, v in p], *a, **k)
    c.linea = lambda p, *a, **k: linea([(X(x), v) for x, v in p], *a, **k)
    c.estrella = lambda x, v, *a, **k: estrella(X(x), v, *a, **k)
    c.poli([(96, y(96)), (150, y(30)), (262, y(8)), (372, y(34)), (420, y(98)), (340, y(124)), (170, y(124))], AZUL)
    c.linea([(158, y(46)), (232, y(26))], 8, AZUL_L)
    c.poli([(120, y(112)), (396, y(112)), (388, y(158)), (130, y(158))], AZUL_D)
    c.linea([(130, y(124)), (390, y(124))], 6, GOLD, ow=0)
    c.estrella(262, y(76), 34, GOLD, ow=4)
    c.poli([(228, y(150)), (400, y(144)), (436, y(176)), (418, y(192)), (300, y(180)), (232, y(172))], (18, 14, 40))
    c.linea([(300, y(162)), (386, y(164))], 5, (110, 100, 170))


def gus_poli(emo='orgullo', boca=0., pose='bajos', brazos=0., mira=(0, 0), dy=0):
    dy = int(round(dy / 6.) * 6)
    key = ('vgus', emo, round(boca * 3) / 3, pose, round(brazos * 4) / 4, mira, dy)
    def f():
        im = C.gus2(emo, round(boca * 3) / 3, pose, round(brazos * 4) / 4, mira, 0., None, None, None, '').copy()
        out = Image.new('RGBA', (490, 600), (0, 0, 0, 0)); out.paste(im, (0, 0))
        c = L2(490, 600); _gorra(c, dy); out.alpha_composite(c.fin()); return out
    return mk(key, f)


def GP(fr, x, y, sc, flip=False, sy=None, rot=0., alpha=1., recorte=False, **k):
    im = gus_poli(**k)
    if recorte: im = im.crop((0, 0, 490, 430))
    R.put(fr, im, x, y, sc, sy or sc, rot, flip, alpha, anchor=(220, 430 if recorte else 590))


def mano(x, y, sc, hx, hy, flip=False):
    dx = (hx - 220) * sc
    return x - dx if flip else x + dx, y + (hy - 590) * sc


# =================================================================== PATRULLA
def patrulla():
    """Superdeportivo patrulla (dibujo propio). 780x300, ruedas en (170,262) y (620,262). Mira a la derecha, ventana hueca."""
    def f():
        c = L2(780, 300)
        for wx in (170, 620): c.elipse(wx, 258, 72, 64, (16, 10, 30), ow=0)
        body = [(36, 266), (30, 190), (66, 164), (190, 150), (300, 98), (436, 88), (540, 128), (690, 170), (756, 204), (766, 248), (750, 266)]
        c.poli(body, (246, 244, 252))
        c.poli([(30, 190), (66, 164), (190, 150), (262, 160), (214, 266), (36, 266)], (28, 30, 66), ow=0)       # cola oscura
        c.poli([(592, 150), (690, 170), (756, 204), (766, 248), (750, 266), (640, 266)], (28, 30, 66), ow=0)   # frente oscuro
        c.poli([(228, 192), (652, 184), (668, 212), (216, 224)], AZUL_S, ow=4)                                  # franja policial
        c.linea([(232, 230), (650, 220)], 8, ROJO_S, ow=0)
        c.texto(432, 205, 'POLICÍA', 34, WHITE, kind='title')
        vent = [(316, 112), (430, 102), (516, 136), (482, 156), (276, 160)]
        c.d.polygon(c.P(vent), fill=(0, 0, 0, 0))
        c.d.line(c.P(vent + [vent[0]]), fill=OUT, width=5 * SS, joint='curve')
        c.poli([(20, 138), (122, 132), (126, 148), (28, 156)], (28, 30, 66), ow=4)                              # alerón
        c.linea([(72, 148), (86, 170)], 7, OUT)
        c.poli([(694, 188), (748, 208), (744, 218), (690, 200)], GOLD, ow=3)                                    # faro
        c.poli([(210, 178), (252, 170), (236, 196)], (28, 30, 66), ow=3)                                        # toma de aire
        c.elipse(42, 212, 8, 14, RED, ow=3)
        c.d.line(c.P(body + [body[0]]), fill=OUT, width=6 * SS, joint='curve')
        c.rrect(322, 76, 428, 94, 8, (60, 60, 90), ow=4)                                                        # base de la torreta
        return c.fin()
    return mk('vpatrulla', f)


def torreta(fase):
    def f():
        c = L2(120, 52)
        c.rrect(8, 14, 62, 46, 14, ROJO_S if fase else (120, 30, 50))
        c.rrect(58, 14, 112, 46, 14, AZUL_S if not fase else (30, 60, 130))
        c.linea([(22, 24), (38, 22)], 5, WHITE, ow=0); c.linea([(74, 24), (90, 22)], 5, WHITE, ow=0)
        return c.fin()
    return mk(('vtorreta', fase), f)


def luz(fr, x, y, t, r=360, a=70):
    """Resplandor de sirena: dos haces rojo y azul que giran."""
    def f(d):
        for k, col in enumerate((ROJO_S, AZUL_S)):
            g = t * 6.5 + k * math.pi
            d.polygon([(x, y), (x + math.cos(g - .28) * r, y + math.sin(g - .28) * r * .7), (x + math.cos(g + .28) * r, y + math.sin(g + .28) * r * .7)], fill=col + (a,))
    lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); f(ImageDraw.Draw(lay))
    clip = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0))
    clip.paste(lay.crop((0, 650, R.W, 1210)), (0, 650)); fr.alpha_composite(clip)


def auto(fr, t, cx, base, sc, giro=0., chofer=None, sirena=True):
    """Patrulla con el piso de las ruedas en y=base. chofer: (emo, boca) para ver a Gus manejando."""
    f = lambda px, py: (cx + (px - 390) * sc, base + (py - 294) * sc)
    sombra(fr, cx, base + 2, 760 * sc)
    if sirena: luz(fr, *f(375, 66), t, 330 * sc + 80, 60)
    if chofer:
        x0, y0 = f(276, 100); x1, y1 = f(516, 160)
        def gu_in(L, ox, oy):
            gx, gy = f(392, 186)
            GP(L, gx + ox, gy + oy, sc * .34, emo=chofer[0], boca=chofer[1], pose='agarra', brazos=1., recorte=True, dy=12)
        E.clip(fr, (x0, y0, x1, y1), gu_in)
    R.put(fr, patrulla(), cx, base, sc, sc, anchor=(390, 294))
    for wx in (170, 620):
        R.put(fr, S('rueda', 64), f(wx, 262)[0], f(wx, 262)[1], sc * .86, sc * .86, rot=-giro % 360, anchor=(70, 70))
    fase = int(t * 6) % 2
    R.put(fr, torreta(fase), *f(375, 66), sc * 1.1, sc * 1.1, anchor=(60, 30))
    if sirena:
        x, y = f(348 if fase else 402, 62)
        E.destello(fr, x, y, t, 0, 1.3 * sc + .3)


# =================================================================== OBJETOS
def clonador():
    """Aparatito con antena y pantalla; la llave brillante se dibuja aparte. 200x280."""
    def f():
        c = L2(200, 280)
        c.linea([(146, 70), (166, 20)], 9, (200, 198, 230), ow=4); c.elipse(168, 16, 13, 13, PINK, ow=4)
        c.rrect(26, 60, 174, 268, 28, (122, 63, 191))
        c.rrect(44, 82, 156, 176, 14, (20, 40, 60), ow=5)
        for i, (x, col) in enumerate(((68, CYAN), (100, GOLD), (132, PINK))): c.elipse(x, 208, 12, 12, col, ow=3)
        c.rrect(60, 234, 140, 250, 8, (60, 30, 100), ow=3)
        return c.fin()
    return mk('vclon', f)


def llave():
    def f():
        c = L2(130, 70)
        c.elipse(34, 35, 24, 24, GOLD, ow=5); c.elipse(34, 35, 9, 9, (20, 40, 60), ow=3)
        c.rrect(52, 28, 118, 44, 5, GOLD, ow=4)
        c.rrect(90, 40, 100, 58, 3, GOLD, ow=4); c.rrect(106, 40, 116, 54, 3, GOLD, ow=4)
        return C.glow(c.fin(), 9, 1.5)
    return mk('vllave', f)


def rosquilla():
    def f():
        c = L2(120, 110)
        c.elipse(60, 58, 52, 46, (222, 160, 96))
        c.elipse(60, 50, 46, 36, PINK_L, ow=4)
        c.elipse(60, 52, 16, 12, (74, 38, 100), ow=5)
        for (x, y, col) in ((32, 40, GOLD), (52, 24, CYAN), (82, 30, WHITE), (92, 52, ORANGE), (30, 62, WHITE), (70, 74, GOLD)):
            c.linea([(x - 6, y - 3), (x + 6, y + 3)], 5, col, ow=0)
        return c.fin()
    return mk('vdona', f)


def mono():
    def f():
        c = L2(260, 190)
        c.poli([(112, 96), (66, 176), (96, 168), (112, 186), (136, 104)], (214, 40, 70))
        c.poli([(148, 96), (194, 176), (164, 168), (148, 186), (124, 104)], (214, 40, 70))
        c.poli([(130, 90), (30, 30), (14, 70), (20, 116), (40, 138)], ROJO_S)
        c.poli([(130, 90), (230, 30), (246, 70), (240, 116), (220, 138)], ROJO_S)
        c.linea([(42, 62), (84, 80)], 7, (255, 170, 180), ow=0); c.linea([(218, 62), (176, 80)], 7, (255, 170, 180), ow=0)
        c.rrect(106, 66, 154, 116, 18, (230, 46, 74))
        return c.fin()
    return mk('vmono', f)


# =================================================================== FONDOS
def bg_noche():
    """Escena 1: calle de noche frente a hoteles y palmeras."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (24, 16, 62), ow=0)
        for k in range(26): c.estrella((k * 191) % 1060 + 10, (k * 67) % 150 + 14, 5 + k % 3, (255, 240, 220))
        for i, (x, w, h, col) in enumerate(((20, 190, 300, (74, 38, 120)), (230, 150, 220, (96, 50, 140)), (700, 160, 250, (96, 50, 140)), (880, 190, 330, (74, 38, 120)))):
            c.rrect(x, 440 - h, x + w, 440, 14, col, ow=5)
            c.linea([(x + 10, 440 - h + 22), (x + w - 10, 440 - h + 22)], 6, (PINK, CYAN)[i % 2], ow=0)
            for j in range(int((h - 60) / 54)):
                for m in range(int((w - 30) / 52)):
                    c.rrect(x + 22 + m * 52, 440 - h + 44 + j * 54, x + 52 + m * 52, 440 - h + 72 + j * 54, 4, (GOLD, (40, 24, 80), CYAN)[(i + j * 2 + m) % 3], ow=0)
        c.rrect(-10, 440, 1090, 560, 0, (46, 36, 76), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        for x in range(0, 1080, 190): c.rrect(x, 520, x + 100, 534, 4, GOLD, ow=0)
        return c.fin()
    return mk('v1', f)


def bg_lote():
    """Escena 3: estacionamiento de la comisaría al atardecer."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 420, 0, (150, 74, 160), ow=0)
        c.elipse(180, 190, 86, 86, (255, 190, 120), ow=0)
        c.rrect(430, 110, 1100, 420, 14, (214, 200, 240), ow=6)
        c.rrect(414, 92, 1100, 130, 8, AZUL, ow=6)
        c.rrect(560, 150, 950, 214, 14, AZUL_D, ow=5); c.texto(755, 183, 'COMISARÍA', 46, CREAM)
        for x in (470, 610, 860, 990):
            c.rrect(x, 250, x + 90, 340, 8, (110, 190, 220), ow=5); c.linea([(x + 45, 250), (x + 45, 340)], 4, OUT)
        c.rrect(730, 270, 826, 420, 8, AZUL_D, ow=5)
        for x in range(0, 400, 52): c.linea([(x + 10, 330), (x + 10, 420)], 7, (80, 60, 120), ow=0)
        c.linea([(0, 350), (400, 350)], 8, (80, 60, 120), ow=0)
        c.rrect(-10, 420, 1090, 560, 0, (66, 54, 100), ow=0)
        c.linea([(-10, 420), (1090, 420)], 7, OUT)
        for x in range(60, 1100, 220): c.linea([(x, 430), (x - 60, 556)], 8, (235, 230, 250), ow=0)
        return c.fin()
    return mk('v3', f)


def bg_calle():
    """Escena 4: avenida de día frente a la comisaría."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 400, 0, (110, 180, 232), ow=0)
        for (x, y) in ((150, 90), (620, 60), (930, 130)):
            for (dx, dy, r) in ((0, 0, 36), (40, 8, 28), (-40, 10, 26)): c.elipse(x + dx, y + dy, r, r * .7, WHITE, ow=0)
        c.rrect(60, 150, 520, 400, 12, (240, 232, 250), ow=6)
        c.poli([(40, 160), (290, 76), (540, 160)], AZUL, ow=6)
        c.estrella(290, 124, 24, GOLD, ow=4)
        c.rrect(120, 178, 460, 232, 12, AZUL_D, ow=5); c.texto(290, 206, 'COMISARÍA', 40, CREAM)
        for x in (110, 190, 360, 440): c.rrect(x, 250, x + 30, 400, 6, (200, 186, 230), ow=4)
        c.rrect(250, 290, 332, 400, 8, AZUL_D, ow=5)
        for x, h, col in ((600, 180, PINK_L), (760, 240, (255, 214, 150)), (920, 160, (150, 230, 210))):
            c.rrect(x, 400 - h, x + 140, 400, 10, col, ow=5)
            for j in range(int(h / 60)): c.rrect(x + 22, 420 - h + j * 54, x + 118, 446 - h + j * 54, 6, (90, 140, 200), ow=3)
        c.rrect(-10, 400, 1090, 450, 0, (226, 206, 190), ow=0)
        c.rrect(-10, 450, 1090, 560, 0, (74, 66, 104), ow=0)
        c.linea([(-10, 450), (1090, 450)], 7, OUT)
        for x in range(0, 1100, 170): c.rrect(x, 532, x + 90, 546, 4, CREAM, ow=0)
        return c.fin()
    return mk('v4', f)


def bg_garaje():
    """Escena 5: garaje propio, portón abierto a la derecha apagado y pared de herramientas."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (74, 52, 118), ow=0)
        for y in range(40, 440, 56): c.linea([(0, y), (1080, y)], 3, (86, 62, 134), ow=0)
        c.rrect(50, 60, 330, 250, 14, (120, 96, 170), ow=6)
        for i in range(7):
            for j in range(5): c.elipse(76 + i * 38, 82 + j * 36, 3, 3, (80, 60, 120), ow=0)
        c.linea([(100, 100), (100, 205)], 11, CREAM, ow=3); c.rrect(80, 88, 122, 114, 6, CREAM, ow=3)
        c.linea([(180, 100), (205, 215)], 10, CREAM, ow=3); c.elipse(178, 96, 17, 17, CREAM, ow=3)
        c.linea([(270, 98), (270, 222)], 9, GOLD, ow=3)
        c.rrect(420, 40, 700, 62, 11, (255, 236, 250), ow=4)
        c.rrect(850, 150, 1040, 440, 8, (58, 40, 96), ow=6)
        for y in (230, 310, 390): c.rrect(860, y, 1030, y + 14, 4, (205, 140, 78), ow=3)
        for (x, y, col) in ((880, 186, PINK), (950, 186, CYAN), (905, 266, GOLD), (975, 346, ORANGE)): c.rrect(x, y, x + 50, y + 44, 8, col, ow=4)
        c.rrect(-10, 440, 1090, 560, 0, (46, 34, 78), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        c.rrect(150, 470, 880, 540, 30, (62, 48, 102), ow=0)
        return c.fin()
    return mk('v5', f)


def bg_playa():
    """Escena 6: playa de Vice Beach al atardecer."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 300, 0, (200, 84, 150), ow=0)
        c.rrect(-10, 0, 1090, 110, 0, (112, 56, 150), ow=0)
        c.elipse(790, 250, 130, 130, GOLD, ow=0)
        c.rrect(-10, 262, 1090, 380, 0, (70, 90, 180), ow=0)
        for k in range(16): c.linea([((k * 211) % 1040, 284 + (k * 29) % 80), ((k * 211) % 1040 + 60, 284 + (k * 29) % 80)], 5, (255, 200, 190), ow=0)
        c.rrect(-10, 360, 1090, 440, 0, (240, 206, 170), ow=0)
        for x, col in ((90, CYAN), (330, GOLD), (980, PINK_L)):
            c.linea([(x, 300), (x, 396)], 8, CREAM, ow=3)
            c.poli([(x - 70, 312), (x, 262), (x + 70, 312)], col, ow=5)
        c.rrect(-10, 440, 1090, 560, 0, (70, 54, 100), ow=0)
        c.linea([(-10, 440), (1090, 440)], 8, CREAM)
        for x in range(0, 1100, 170): c.rrect(x, 528, x + 90, 542, 4, GOLD, ow=0)
        return c.fin()
    return mk('v6', f)


# =================================================================== MAPA
def mapa_base(parque):
    """940x560: costa de Vice Beach (mar a la derecha), calles en cuadrícula y un parque."""
    def f():
        c = L2(940, 560)
        c.rrect(6, 6, 934, 554, 40, (238, 222, 180), ow=7)
        c.rrect(6, 6, 90, 554, 30, (90, 170, 225), ow=0)                                       # canal al oeste
        c.rrect(66, 6, 700, 554, 0, (126, 96, 168), ow=0)                                      # ciudad
        for x in range(76, 680, 104):
            for y in range(18, 540, 92):
                c.rrect(x, y, x + 84, y + 70, 10, ((168, 134, 214), (190, 150, 220), (150, 120, 200))[(x // 104 + y // 92) % 3], ow=3)
        for x in range(170, 700, 104): c.linea([(x - 1, 10), (x - 1, 550)], 9, WHITE, ow=0)
        for y in range(103, 540, 92): c.linea([(70, y), (696, y)], 9, WHITE, ow=0)
        x0, y0, x1, y1 = parque
        c.rrect(x0, y0, x1, y1, 26, (110, 200, 130), ow=5)
        for k in range(9):
            px = x0 + 26 + (k % 3) * (x1 - x0 - 52) / 2; py = y0 + 26 + (k // 3) * (y1 - y0 - 52) / 2
            c.elipse(px, py, 17, 17, (52, 140, 90), ow=3)
        costa = [(700, 6), (736, 110), (712, 230), (748, 350), (720, 460), (742, 554)]
        c.poli(costa + [(934, 554), (934, 6)], (60, 140, 205), ow=0)
        c.linea(costa, 34, (240, 214, 160), ow=0)
        c.linea([(x + 24, y) for x, y in costa], 7, (190, 235, 255), ow=0)
        c.d.rounded_rectangle([6 * SS, 6 * SS, 934 * SS, 554 * SS], radius=40 * SS, outline=OUT, width=7 * SS)
        return c.fin()
    return mk(('vmapa',) + tuple(parque), f)


def comisaria_icono():
    def f():
        c = L2(150, 120)
        c.rrect(16, 46, 134, 112, 8, (245, 240, 252))
        c.poli([(6, 52), (75, 8), (144, 52)], AZUL)
        c.estrella(75, 36, 14, GOLD, ow=3)
        c.rrect(60, 76, 90, 112, 4, AZUL_D, ow=4)
        for x in (28, 100): c.rrect(x, 66, x + 22, 90, 4, CYAN, ow=3)
        return c.fin()
    return mk('vcomi', f)


# =================================================================== 1 · GANCHO
def v_hook(s):
    D = s['dur']
    def draw(fr, t):
        fondo(fr, bg_noche())
        luz(fr, 640, 880, t, 620, 80)
        E.titulo(fr, t, '¿UNA PATRULLA *TEMPESTA*?', 98, 548, .0)
        ce = eo(pr(t, .15, .5))
        auto(fr, t, 630 + (1 - ce) * 650, 1090, .64, (1 - ce) * 700)
        # Gus: la gorra gigante se le cae sobre los ojos, la sube y se le vuelve a caer
        u = (t % 1.5) / 1.5
        dy = 42 * eo(cl(u / .35)) if u < .62 else 42 * (1 - eo(cl((u - .62) / .18))) - 6
        tapado = dy > 24
        GP(fr, 260, G + 25, .66, emo='confuso' if tapado else 'orgullo', boca=.4 if tapado else .8,
           pose='orejas' if tapado else 'celebra', brazos=1., dy=dy, sy=.66 * idle(t, 8, .025), rot=math.sin(t * 6) * 3 if tapado else 0)
        FLA(fr, 975, G + 30, .58, emo='asombro' if t < D * .6 else 'guino', cuello=.7 + .3 * math.sin(t * 5), ala='cadera', mira=(-1, 0), sy=.6 * idle(t, 5))
        golpe(fr, '[¡WIU WIU!]', 800, 710, t, .35, 62, 8)
        R.put(fr, E.sfx('[¿?]', 90), 120, 760 + math.sin(t * 6) * 10, eb(pr(t, 1., .3)), eb(pr(t, 1., .3)), rot=math.sin(t * 4) * 10, anchor=(E.sfx('[¿?]', 90).width / 2, 50))
    return draw


# =================================================================== 2 · MAPA
def v_mapa(s):
    D = s['dur']
    cfg = s.get('mapa', {})
    zona = cfg.get('zona', 'VICE BEACH'); parque = cfg.get('parque', [178, 106, 372, 286])
    pin = cfg.get('pin', [430, 330]); et = cfg.get('etiqueta', [510, 66]); et2 = cfg.get('etiqueta_pin', 'COMISARÍA')
    ruta = cfg.get('ruta', [[850, 480], [740, 360]])
    MX0, MY0 = 540 - 470, 930 - 280
    def draw(fr, t):
        E.titulo(fr, t, 'COMISARÍA DE *VICE BEACH*', 70, 548)
        pe = eo(pr(t, 0, .35))
        R.put(fr, mapa_base(parque), 540, 930, .8 + .2 * pe, .8 + .2 * pe, alpha=cl(pe * 2), anchor=(470, 280))
        if pe < 1: return
        d = ImageDraw.Draw(fr)
        for k in range(9):
            x = MX0 + 790 + (k * 37) % 110; y = MY0 + 40 + (k * 61 + t * 30) % 480
            d.arc((x - 16, y - 6, x + 16, y + 10), 200, 340, fill=(200, 235, 255, 255), width=4)
        R.anim_in(fr, E.pil(zona, 42, bg=(74, 38, 120)), MX0 + et[0], MY0 + et[1], t, .25, 'pop', .25)
        px, py = MX0 + pin[0], MY0 + pin[1]
        u = pr(t, .45, .4)
        if u > 0:
            if t > .8:
                for j in (0, .5):
                    r = (t - .8 + j) % 1.0
                    d.ellipse((px - 60 - 70 * r, py + 20 - 24 - 34 * r, px + 60 + 70 * r, py + 20 + 24 + 34 * r), outline=(255, 60, 90, int(255 * (1 - r))), width=8)
            R.put(fr, comisaria_icono(), px, py + 40, .95 * eb(u), .95 * eb(u), anchor=(75, 112))
            R.put(fr, S('pin', PINK, 70), px, py - 76 + (1 - eo(u)) * -190 - abs(math.sin(t * 6)) * 14, 1.2 * eb(u), 1.2 * eb(u), anchor=(35, 90))
            R.anim_in(fr, E.pilg(et2, 36, 22, 8), px, py + 80, t, .75, 'pop', .25)
        # Gus llega flotando, brinca y se baja en la comisaría
        (ax, ay), (bx, by) = ruta
        llega = D * .5; baja = llega + .45
        w = eo(cl(t / llega))
        gx = MX0 + _mix(ax, bx, w); gy = MY0 + _mix(ay, by, w) + (math.sin(t * 6) * 5 if t < llega else 0)
        sc = .85
        for k in range(3):
            q = (t * 1.6 + k * .33) % 1
            if t < llega: d.ellipse((gx - 20 + 30 * q, gy + 4 - 10 * q, gx + 70 + 80 * q, gy + 26 + 10 * q), outline=(220, 240, 255, int(210 * (1 - q))), width=4)
        R.put(fr, B.dona('atras'), gx, gy, sc, sc, anchor=(110, 70))
        if t < llega:
            GP(fr, gx, gy + 10, .36, emo='concentrado', pose='agarra', brazos=1., recorte=True, rot=math.sin(t * 7) * 6, flip=True)
        R.put(fr, B.dona('frente'), gx, gy, sc, sc, anchor=(110, 70))
        if t >= llega:
            q = cl((t - llega) / (baja - llega))
            fx = _mix(gx, px + 140, eo(q)); fy = _mix(gy + 10, py + 96, eo(q)) - 150 * math.sin(math.pi * q)
            GP(fr, fx, fy, .38, emo='asombro' if q < 1 else 'feliz', boca=.8, pose='celebra', brazos=1., flip=True, sy=.38 * idle(t, 12, .04), rot=360 * q if q < 1 else math.sin(t * 7) * 5)
            golpe(fr, '[¡PLOP!]', px + 200, py - 100, t, baja, 58, 7)
    return draw


# =================================================================== 3 · CLONADOR
def v_clonador(s):
    D = s['dur']; toma = s.get('t_toma', D * .45)
    def draw(fr, t):
        fondo(fr, bg_lote())
        E.titulo(fr, t, '*CLONADOR* DE LLAVES', 94, 548)
        auto(fr, t, 640, 1030, .46, 0, sirena=False)
        # Flami saca el aparato
        FLA(fr, 940, G + 35, .6, emo='guino' if t < toma else 'feliz', boca=.3, cuello=.4 + .2 * math.sin(t * 3), ala='senala', flip=True, sy=.6 * idle(t, 6))
        u = eb(pr(t, .2, .35))
        gsc = .66
        if t < toma:
            cx, cy = 600, 900 + math.sin(t * 4) * 8
            rayos_(fr, cx, cy - 20, t)
            if u > 0:
                R.put(fr, clonador(), cx, cy, 1.0 * u, 1.0 * u, rot=math.sin(t * 3) * 7, anchor=(100, 164))
                R.put(fr, llave(), cx, cy - 36, u, u, rot=-20 + math.sin(t * 8) * 12, anchor=(92, 62))
                for i, (dx, dy) in enumerate(((-130, -110), (120, -140), (140, 60))): E.destello(fr, cx + dx, cy + dy, t, i * .3, 1.2)
            GP(fr, 250, G + 25, gsc, emo='asombro', boca=.7, pose='pecho', brazos=1., mira=(1, 0), dy=0, sy=gsc * idle(t, 8))
        else:
            # Gus lo prueba y le hace cosquillas
            risa = abs(math.sin(t * 17))
            gx = 310 + math.sin(t * 23) * 12; gy = G + 25 - risa * 26
            GP(fr, gx, gy, gsc, emo='feliz', boca=.4 + .6 * risa, pose='agarra', brazos=1., rot=math.sin(t * 19) * 7, dy=18 + 18 * math.sin(t * 11), sy=gsc * (1 + .04 * math.sin(t * 17)))
            q = eo(pr(t, toma, .2))
            mx, my = mano(gx, gy, gsc, 380, 424)
            cx = _mix(600, mx + 26, q); cy = _mix(900, my + math.sin(t * 40) * 9, q)
            R.put(fr, clonador(), cx, cy, .72, .72, rot=math.sin(t * 36) * 16, anchor=(100, 164))
            R.put(fr, llave(), cx, cy - 26, .72, .72, rot=math.sin(t * 30) * 40, anchor=(92, 62))
            for i in range(3):
                w = (t * 2.6 + i / 3) % 1
                R.put(fr, E.sfx('[¡JI!]', 62), 140 + i * 190, 840 - w * 130 + i % 2 * 30, 1, 1, rot=(-12, 8, -6)[i], alpha=math.sin(math.pi * w), anchor=(E.sfx('[¡JI!]', 62).width / 2, 36))
            d = ImageDraw.Draw(fr)
            for i in range(5):
                a = i * 1.26 + t * 9
                x0, y0 = cx + math.cos(a) * 92, cy + math.sin(a) * 100
                d.line([(x0, y0), (x0 + math.cos(a + .6) * 26, y0 + math.sin(a + .6) * 26), (x0 + math.cos(a) * 54, y0 + math.sin(a) * 54)], fill=CYAN + (255,), width=7, joint='curve')
            golpe(fr, '[¡BZZT!]', 720, 760, t, toma + .15, 70, -8)
    return draw


def rayos_(fr, x, y, t, r=340, a=40, n=10):
    lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for k in range(n):
        g = t * .8 + k * 2 * math.pi / n
        d.polygon([(x, y), (x + math.cos(g) * r, y + math.sin(g) * r), (x + math.cos(g + .2) * r, y + math.sin(g + .2) * r)], fill=(255, 232, 170, a))
    clip = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); clip.paste(lay.crop((0, 650, R.W, 1210)), (0, 650)); fr.alpha_composite(clip)


# =================================================================== 4 · GRATIS
def v_gratis(s):
    D = s['dur']; sube = s.get('t_sube', .55); arranca = s.get('t_arranca', max(1.0, D * .55))
    def draw(fr, t):
        fondo(fr, bg_calle())
        E.titulo(fr, t, '*GRATIS*', 150, 548)
        q = cl((t - arranca) / max(.6, D - arranca))
        cx = 520 + 760 * q ** 2
        dentro = t >= sube
        tiembla = math.sin(t * 60) * 3 if sube + .15 < t < arranca else 0
        auto(fr, t, cx, 1120 + tiembla, .68, q * 1500, chofer=('feliz', .8) if dentro else None, sirena=dentro)
        if t < sube:                                              # Gus se avienta por la ventana
            u = cl(t / sube)
            gx = _mix(150, 520, u); gy = _mix(G + 20, 1010, u) - 230 * math.sin(math.pi * u)
            sc = .55 * (1 - .55 * u * u)
            GP(fr, gx, gy, sc, emo='feliz', boca=.9, pose='celebra', brazos=1., rot=-70 * u)
        golpe(fr, '[¡ZUUUM!]', 260, 790, t, arranca + .05, 84, -8)
        golpe(fr, '[¡WIU WIU!]', 760, 760, t, sube + .2, 58, 8, arranca)
        if q > 0:
            E.lineas_vel(fr, t, 940, 1130, 8, int(180 * cl(q * 3)))
            for k in range(4):
                u = (t * 2.2 + k * .25) % 1
                R.put(fr, S('nube_polvo', 46), cx - 290 - u * 150, 1100, .6 + u * .7, .6 + u * .7, alpha=(1 - u) * .8, anchor=(69, 46))
        # Flami corre detrás con su dona
        if t > arranca - .1:
            v = cl((t - arranca + .1) / max(.6, D - arranca))
            fx = 90 + 640 * v
            fy = 1195 - abs(math.sin(t * 13)) * 30
            for k in range(3):
                u = (t * 3 + k / 3) % 1
                R.put(fr, S('nube_polvo', 46), fx - 90 - u * 110, 1185, .4 + u * .5, .4 + u * .5, alpha=(1 - u) * .8, anchor=(69, 46))
            E.FL(fr, fx, fy, .46, 'asombro', boca=.9, gafas=0, cuello=.8 + .2 * math.sin(t * 13), ala='senala', rot=-10 + math.sin(t * 13) * 5)
            R.put(fr, rosquilla(), fx + 122, fy - 138 + math.sin(t * 13) * 14, 1, 1, rot=math.sin(t * 9) * 25, anchor=(60, 55))
            R.pop_burbuja(fr, E.bub('¡Mi dona!', 0, 46), fx + 30, fy - 320, t, arranca + .35)
        else:
            FLA(fr, 930, G + 40, .46, emo='feliz', cuello=.3, ala='sostiene', flip=True, sy=.46 * idle(t, 6))
            R.put(fr, rosquilla(), 862, 1055 + math.sin(t * 5) * 6, .9, .9, anchor=(60, 55))
    return draw


# =================================================================== 5 · QUÉDATELA
def v_garaje(s):
    D = s['dur']; para = s.get('t_para', D * .28); pone = s.get('t_mono', D * .52); ok = s.get('t_ok', D * .74)
    def draw(fr, t):
        fondo(fr, bg_garaje())
        E.titulo(fr, t, '*QUÉDATELA*', 130, 548)
        p = eo(cl(t / para))
        sc = .66
        cx = _mix(-330, 440, p)
        auto(fr, t, cx, 1125, sc, p * 900, chofer=('concentrado', 0.) if t < para else None, sirena=t < para)
        golpe(fr, '[¡SCRIII!]', 700, 790, t, para - .15, 70, 8, para + .6)
        techo = (cx + (375 - 390) * sc, 1125 + (60 - 294) * sc)
        if t >= para:
            u = eb(pr(t, para, .3))
            j = cl((t - pone + .3) / .3)
            gx = _mix(150, 200, j)
            GP(fr, gx, G + 30 - 80 * math.sin(math.pi * j), .52 * u, emo='orgullo' if t >= pone else 'concentrado', boca=.5 if t >= pone else 0,
               pose='senala' if t >= pone else 'celebra', brazos=1., mira=(1, 0), sy=.52 * u * idle(t, 7))
            E.poof(fr, 150, 1000, t, para - .05)
            hx, hy = gx + 40, 700
            if t < pone:
                q = eo(cl((t - pone + .4) / .4))
                R.put(fr, mono(), _mix(gx + 60, techo[0], q), _mix(850, techo[1] - 10, q) - 90 * math.sin(math.pi * q), .8 * u, .8 * u, rot=360 * q, anchor=(130, 95))
        if t >= pone:
            q = pr(t, pone, .35)
            k = .95 * (1.6 - .6 * eo(q)) * (1 + .03 * math.sin(t * 8))
            R.put(fr, mono(), techo[0], techo[1] - 26, k, k, rot=math.sin(t * 5) * 4, anchor=(130, 95))
            golpe(fr, '[¡TARÁN!]', 330, 750, t, pone + .1, 76, -8)
            for i, (dx, dy) in enumerate(((-170, -40), (160, -60), (200, 60), (-210, 90))): E.destello(fr, techo[0] + dx, techo[1] + dy, t, i * .23, 1.2)
        # Flami pone palomita
        E.FL(fr, 930, G + 35, .54, 'guino' if t > ok else 'feliz', boca=.4 if t > ok else 0, gafas=0 if t > ok else 1, cuello=.3,
             ala='senala' if t > ok - .2 else 'reposo', flip=True, sy=.54 * idle(t, 6))
        E.sello(fr, t, ok, 770, 760, 1.0)
    return draw


# =================================================================== 6 · CIERRE
def v_cierre(s):
    D = s['dur']
    def draw(fr, t):
        fondo(fr, bg_playa())
        for k, x0 in enumerate((70, 1010)):
            R.put(fr, R.spr('palmera', math.sin(t * 2 + k)), x0, 1050, .5, .5, anchor=(190, 690))
        E.titulo(fr, t, '¿YA LA *VISTE*?', 112, 548)
        # Flami saluda desde atrás
        E.FL(fr, 860, 1040, .48, 'feliz', boca=.6, gafas=1, cuello=.5 + .3 * math.sin(t * 5), ala='saluda' if int(t * 4) % 2 else 'arriba', flip=True, sy=.48 * idle(t, 9))
        R.pop_burbuja(fr, E.bub('¡Adiós!', 0, 46), 810, 750, t, .45)
        # Gus pasa con la sirena
        w = cl(t / D)
        cx = _mix(-200, 760, eo(cl(w * 1.15))) + 380 * cl((w - .85) / .15)
        base = 1165 - abs(math.sin(t * 9)) * 6
        auto(fr, t, cx, base, .68, cx * .9, chofer=('feliz', .8))
        for k in range(3):
            u = (t * 2.4 + k / 3) % 1
            R.put(fr, S('nube_polvo', 46), cx - 280 - u * 130, 1145, .45 + u * .5, .45 + u * .5, alpha=(1 - u) * .7, anchor=(69, 46))
        golpe(fr, '[¡WIU WIU!]', 300, 760, t, .25, 66, -8)
    return draw
