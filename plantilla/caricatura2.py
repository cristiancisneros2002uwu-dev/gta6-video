"""Caricatura 2 (24-nov-2026): personajes con más caras/poses y objetos para Neza y 5 ajustes.
Todo dibujado con código (sin imágenes externas). Usa el Lienzo de caricatura.py."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import caricatura as K
from caricatura import OUT, CREAM, ORANGE, PINK, PINK_L, PINK_D, GREEN, GREEN_D, BELLY, SS

BASE = os.path.dirname(os.path.abspath(__file__))
PURPLE = (122, 63, 191); PURPLE_D = (42, 20, 72); PURPLE_M = (74, 38, 120)
GOLD = (255, 224, 138); RED = (255, 84, 84); CYAN = (110, 230, 255); WHITE = (255, 255, 255)
_f = {}


def fuente(kind, size):
    k = (kind, size)
    if k not in _f:
        if kind == 'title':
            f = ImageFont.truetype(os.path.join(BASE, 'assets', 'fuentes', 'BricolageGrotesque-variable.ttf'), size)
            f.set_variation_by_axes([96, 800, 100])
        else:
            f = ImageFont.truetype(os.path.join(BASE, 'assets', 'fuentes', f'Figtree-{kind}.ttf'), size)
        _f[k] = f
    return _f[k]


class L2(K.Lienzo):
    def hueco(self, x0, y0, x1, y1, r):
        """Borra (transparente) un rectángulo redondeado: ventanas por las que se ve lo de atrás."""
        self.d.rounded_rectangle([x0 * SS, y0 * SS, x1 * SS, y1 * SS], radius=r * SS, fill=(0, 0, 0, 0))

    def afilada(self, pts, r0, r1, fill, ow=5, n=44, punta=None):
        """Trazo que se adelgaza de r0 a r1 (alas, hojas). punta=(color, desde 0..1)."""
        def bez(t):
            q = list(pts)
            while len(q) > 1: q = [((1 - t) * a[0] + t * b[0], (1 - t) * a[1] + t * b[1]) for a, b in zip(q, q[1:])]
            return q[0]
        path = [bez(i / n) for i in range(n + 1)]
        for outline in (True, False):
            for i, (x, y) in enumerate(path):
                u = i / n; r = r0 + (r1 - r0) * u
                col = OUT if outline else (punta[0] if punta and u >= punta[1] else fill)
                rr = r + (ow if outline else 0)
                self.d.ellipse([(x - rr) * SS, (y - rr) * SS, (x + rr) * SS, (y + rr) * SS], fill=col)

    def texto(self, x, y, txt, size, fill, kind='title', anchor='mm'):
        self.d.text((x * SS, y * SS), txt, font=fuente(kind, size * SS), fill=fill, anchor=anchor)

    def corazon(self, cx, cy, s, fill, ow=0):
        pts = []
        for i in range(40):
            t = i / 40 * 2 * math.pi
            x = 16 * math.sin(t) ** 3
            y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
            pts.append((cx + x * s / 32, cy - y * s / 32))
        self.poli(pts, fill, ow=ow)

    def estrella(self, cx, cy, r, fill, ow=0, puntas=5):
        pts = []
        for k in range(puntas * 2):
            rr = r if k % 2 == 0 else r * .45; a = -math.pi / 2 + k * math.pi / puntas
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        self.poli(pts, fill, ow=ow)

    def segmento(self, cx, cy, r, ang, cubre, fill, linea=True):
        """Párpado: parte del círculo (cx,cy,r) que queda de un lado de una recta (ang = lado que se cubre)."""
        d = r * (1 - 2 * cubre)          # cubre 0 = nada, 1 = todo
        if cubre <= 0: return
        a0 = math.radians(ang)
        al = math.acos(max(-1, min(1, d / r)))
        pts = [(cx + math.cos(a0 + al * (2 * i / 20 - 1)) * r, cy + math.sin(a0 + al * (2 * i / 20 - 1)) * r) for i in range(21)]
        self.poli(pts, fill, ow=0)
        if linea: self.d.line(self.P([pts[0], pts[-1]]), fill=OUT, width=5 * SS)


def glow(im, radio=14, fuerza=1.6):
    """Resplandor suave detrás de un sprite (neón)."""
    pad = radio * 3
    base = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); base.paste(im, (pad, pad))
    g = base.filter(ImageFilter.GaussianBlur(radio))
    g.putalpha(g.getchannel('A').point(lambda v: min(255, int(v * fuerza))))
    out = Image.alpha_composite(g, base)
    return out


# =============================================================== FLAMI 2
ALAS = {'reposo': (118, 408), 'arriba': (118, 196), 'senala': (428, 346), 'sostiene': (352, 410),
        'cadera': (150, 420), 'abre': (70, 250), 'saluda': (178, 150)}


def flami2(emo='feliz', boca=0., gafas=1., cuello=0., ala='reposo', mira=(0, 0), sudor=0, lente='', lentes_y=None):
    """Sprite 440x620 anclado en los pies (220, 610). Mira a la derecha.
    emo: feliz, enojo, asombro, triste, amor, guino, mareo. ala: nombre o (x, y) de la punta."""
    c = L2(440, 620)
    for px in (190, 250):
        c.linea([(px, 420), (px - 6, 520), (px + 4, 600)], 11, PINK_D, ow=4)
        c.poli([(px - 6, 603), (px + 44, 603), (px + 30, 586), (px + 2, 590)], ORANGE, ow=4)
    c.poli([(95, 330), (45, 365), (70, 395), (125, 392)], PINK_D)
    c.elipse(215, 360, 118, 82, PINK)
    c.elipse(190, 368, 66, 44, PINK_L)
    c.poli([(125, 378), (100, 410), (160, 405)], PINK_D, ow=4)
    sw = cuello * 14
    hx, hy = 288 + sw, 128
    c.curva([(270, 320), (215 - sw, 250), (330 + sw, 200), (hx, hy + 30)], 38, PINK, ow=6)
    c.elipse(hx, hy, 56, 52, PINK)
    ab = min(1., boca) * 14
    c.poli([(hx + 40, hy - 12), (hx + 128, hy + 14 - ab * .2), (hx + 112, hy + 40 + ab), (hx + 38, hy + 34)], ORANGE)
    c.poli([(hx + 104, hy + 6), (hx + 128, hy + 14 - ab * .2), (hx + 112, hy + 40 + ab), (hx + 96, hy + 30)], OUT, ow=0)
    if boca > .1:
        c.elipse(hx + 78, hy + 26 + ab * .3, 14 * boca + 6, 10 * boca + 4, OUT, ow=0)
    # sonrisa / mejilla
    c.elipse(hx + 18, hy + 30, 11, 7, PINK_L, ow=0)
    if emo in ('feliz', 'amor', 'guino'):
        c.elipse(hx + 8, hy + 30, 13, 8, (255, 130, 160), ow=0)
    ey = hy - 8
    mx, my = mira
    if gafas < .5:        # ojos al descubierto
        gran = 1.18 if emo == 'asombro' else 1.
        for k, ex in enumerate((hx + 6, hx + 44)):
            if emo in ('feliz', 'guino') and not (emo == 'guino' and k == 0):
                c.d.arc([(ex - 16) * SS, (ey - 8) * SS, (ex + 16) * SS, (ey + 22) * SS], 200, 340, fill=OUT, width=7 * SS)
            elif emo == 'mareo':
                c.elipse(ex, ey, 17, 19, CREAM, ow=4)
                c.linea([(ex - 9, ey - 9), (ex + 9, ey + 9)], 5, OUT); c.linea([(ex + 9, ey - 9), (ex - 9, ey + 9)], 5, OUT)
            elif emo == 'amor':
                c.elipse(ex, ey, 17, 19, CREAM, ow=4); c.corazon(ex, ey, 22, PINK, ow=0)
            else:
                c.elipse(ex, ey, 17 * gran, 19 * gran, CREAM, ow=4)
                c.elipse(ex + 3 + mx * 5, ey + 2 + my * 5, 7 if emo != 'asombro' else 4.5, 8 if emo != 'asombro' else 5.5, OUT, ow=0)
                if emo == 'enojo': c.segmento(ex, ey, 17, -90 + (25 if k == 0 else -25), .45, PINK)
        by = ey - 34
        if emo in ('enojo',):
            c.linea([(hx - 12, by - 8), (hx + 22, by + 8)], 7, OUT); c.linea([(hx + 66, by - 8), (hx + 32, by + 8)], 7, OUT)
        elif emo in ('triste', 'mareo'):
            c.linea([(hx - 12, by + 8), (hx + 22, by - 8)], 7, OUT); c.linea([(hx + 66, by + 8), (hx + 32, by - 8)], 7, OUT)
        elif emo == 'asombro':
            c.linea([(hx - 10, by - 10), (hx + 22, by - 14)], 7, OUT); c.linea([(hx + 64, by - 10), (hx + 32, by - 14)], 7, OUT)
    gy = ey - 58 * (1 - gafas) if lentes_y is None else ey + lentes_y      # lentes_y: lentes bajados sobre el pico
    for (x0, x1) in ((hx - 14, hx + 26), (hx + 28, hx + 68)):
        c.rrect(x0, gy - 16, x1, gy + 22, 14, (34, 22, 60), ow=5)
    c.linea([(hx + 24, gy - 6), (hx + 30, gy - 6)], 6, OUT)
    # brillo o dibujo en las lentes
    for k, (x0, x1) in enumerate(((hx - 14, hx + 26), (hx + 28, hx + 68))):
        cx = (x0 + x1) / 2
        if lente == 'corazon': c.corazon(cx, gy + 2, 30, PINK, ow=0)
        elif lente == 'estrella': c.estrella(cx, gy + 3, 15, GOLD)
        elif lente == 'dolar': c.texto(cx, gy + 3, '$', 34, (110, 230, 150), kind='800')
        elif lente == 'espiral':
            pts = [(cx + math.cos(i * .5) * (2 + i * .8), gy + 3 + math.sin(i * .5) * (2 + i * .8)) for i in range(26)]
            c.linea(pts, 3, CYAN)
        elif lente == 'ondas':
            c.linea([(cx - 12, gy + 6), (cx - 4, gy - 2), (cx + 4, gy + 8), (cx + 12, gy)], 4, CYAN)
        else:
            c.linea([(x0 + 4, gy - 8), (x0 + 18, gy - 12)], 5, WHITE)
    if gafas >= .5:       # cejas sobre las lentes
        by = gy - 30
        if emo == 'enojo':
            c.linea([(hx - 14, by - 6), (hx + 24, by + 8)], 8, OUT); c.linea([(hx + 70, by - 6), (hx + 32, by + 8)], 8, OUT)
        elif emo in ('triste', 'mareo'):
            c.linea([(hx - 14, by + 8), (hx + 24, by - 6)], 8, OUT); c.linea([(hx + 70, by + 8), (hx + 32, by - 6)], 8, OUT)
        elif emo == 'asombro':
            c.curva([(hx - 14, by - 4), (hx + 4, by - 28), (hx + 24, by - 10)], 8, OUT, ow=0)
            c.curva([(hx + 70, by - 4), (hx + 52, by - 28), (hx + 32, by - 10)], 8, OUT, ow=0)
        elif emo in ('feliz', 'amor', 'guino'):
            c.curva([(hx - 12, by + 2), (hx + 6, by - 12), (hx + 24, by + 2)], 7, OUT, ow=0)
            c.curva([(hx + 68, by + 2), (hx + 50, by - 12), (hx + 32, by + 2)], 7, OUT, ow=0)
    if sudor:
        c.poli([(hx - 40, hy - 40), (hx - 52, hy - 8), (hx - 40, hy + 2), (hx - 28, hy - 8)], (150, 210, 255), ow=4)
    # ala (al frente)
    tip = ALAS.get(ala, ala) if not isinstance(ala, tuple) else ala
    S = (222, 338)
    if ala == 'senala': ctrl = (340, 372)
    elif ala in ('arriba', 'saluda'): ctrl = (120, 330)
    elif ala == 'sostiene': ctrl = (310, 420)
    elif ala == 'abre': ctrl = (110, 320)
    else: ctrl = ((S[0] + tip[0]) / 2 - 20, (S[1] + tip[1]) / 2 + 36)
    if isinstance(ala, tuple): ctrl = ((S[0] + tip[0]) / 2 - 24, (S[1] + tip[1]) / 2 + 22)
    c.afilada([S, ctrl, tip], 28, 9, PINK_D, ow=5, punta=((70, 40, 100), .8))
    return c.fin()


# =============================================================== GUS 2
POSES = {'bajos': ((322, 476), (126, 476)), 'orejas': ((276, 286), (172, 286)), 'encoge': ((384, 392), (80, 392)),
         'senala': ((430, 352), (126, 476)), 'celebra': ((338, 196), (112, 196)), 'agarra': ((392, 424), (300, 440)),
         'cadera': ((332, 436), (108, 436)), 'saluda': ((356, 226), (126, 476)), 'empuja': ((410, 410), (330, 430)),
         'pecho': ((290, 380), (170, 380))}


def _lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def sombrero_vaquero(c, cx, cy):
    tan = (205, 140, 78); tan_d = (160, 98, 52)
    c.poli([(cx - 128, cy + 6), (cx - 100, cy + 24), (cx - 50, cy + 30), (cx + 50, cy + 30), (cx + 100, cy + 24), (cx + 128, cy + 6),
            (cx + 118, cy - 14), (cx + 70, cy - 2), (cx - 70, cy - 2), (cx - 118, cy - 14)], tan_d)
    c.poli([(cx - 66, cy), (cx - 58, cy - 66), (cx - 30, cy - 82), (cx - 6, cy - 66), (cx + 6, cy - 66), (cx + 30, cy - 82), (cx + 58, cy - 66), (cx + 66, cy)], tan)
    c.rrect(cx - 66, cy - 22, cx + 66, cy - 2, 6, (34, 40, 120), ow=5)
    for k in range(5): c.estrella(cx - 48 + k * 24, cy - 12, 7, CREAM)


def sombrero_charro(c, cx, cy):
    neg = (46, 30, 78); oro = (255, 200, 90)
    c.poli([(cx - 150, cy - 18), (cx - 120, cy + 20), (cx - 40, cy + 30), (cx + 40, cy + 30), (cx + 120, cy + 20), (cx + 150, cy - 18),
            (cx + 100, cy - 2), (cx - 100, cy - 2)], neg)
    c.poli([(cx - 70, cy), (cx - 54, cy - 70), (cx - 24, cy - 112), (cx + 24, cy - 112), (cx + 54, cy - 70), (cx + 70, cy)], neg)
    c.rrect(cx - 70, cy - 26, cx + 70, cy - 4, 6, oro, ow=5)
    for k in range(7): c.elipse(cx - 54 + k * 18, cy - 15, 5, 5, (255, 107, 139), ow=0)
    c.elipse(cx, cy - 114, 12, 12, oro, ow=4)
    c.linea([(cx - 130, cy + 14), (cx + 130, cy + 14)], 5, oro)


def poncho(c, tipo):
    if tipo == 'gringo':
        pts = [(176, 318), (268, 318), (344, 470), (96, 470)]
        c.poli(pts, WHITE)
        for k in range(4):
            y0 = 360 + k * 30
            c.poli([(176 - (y0 - 318) * .12 - 1, y0), (268 + (y0 - 318) * .5, y0), (268 + (y0 - 318) * .5 + 6, y0 + 15), (176 - (y0 - 318) * .12 - 6, y0 + 15)], (220, 60, 70), ow=0)
        c.poli([(176, 318), (240, 318), (232, 390), (160, 390)], (34, 40, 120), ow=0)
        for i in range(2):
            for j in range(2): c.estrella(184 + j * 24 + i * 6, 336 + i * 22, 7, WHITE)
        c.poli(pts, None, ow=6) if False else c.d.line(c.P(pts + [pts[0]]), fill=OUT, width=6 * SS, joint='curve')
    elif tipo == 'mexicano':
        pts = [(176, 318), (268, 318), (344, 470), (96, 470)]
        cols = [(255, 107, 139), (255, 179, 107), (194, 89, 255), (255, 241, 234), (110, 230, 255)]
        c.poli(pts, (42, 20, 72))
        for k, col in enumerate(cols):
            y0 = 334 + k * 26
            xl = 176 - (y0 - 318) * .46; xr = 268 + (y0 - 318) * .5
            c.poli([(xl, y0), (xr, y0), (xr + 4, y0 + 13), (xl - 4, y0 + 13)], col, ow=0)
        c.d.line(c.P(pts + [pts[0]]), fill=OUT, width=6 * SS, joint='curve')
        for x in range(104, 340, 22): c.linea([(x, 470), (x - 2, 486)], 5, (255, 200, 90))


def gus2(emo='nervioso', boca=0., pose='bajos', brazos=0., mira=(0, 0), parp=0., sombrero=None, prenda=None, sudor=None, extra=''):
    """Sprite 440x600 anclado en los pies (220, 590). Mira a la derecha.
    emo: nervioso, asombro, feliz, confuso, enojo, triste, orgullo, concentrado, amor, grito."""
    c = L2(440, 600)
    big = 1.22 if emo in ('asombro', 'grito') else 1.
    pn, pf = _lerp(POSES['bajos'][0], POSES[pose][0], brazos), _lerp(POSES['bajos'][1], POSES[pose][1], brazos)

    def brazo(sh, hand, lado, dedo=False):
        mid = ((sh[0] + hand[0]) / 2, (sh[1] + hand[1]) / 2)
        el = (mid[0] + 34 * lado, mid[1] + 24)
        c.curva([sh, el, hand], 30, GREEN, ow=5)
        c.elipse(hand[0], hand[1], 21, 21, GREEN, ow=5)
        if dedo: c.linea([(hand[0] + 6, hand[1] - 4), (hand[0] + 46, hand[1] - 10)], 13, GREEN, ow=4)
    brazo((160, 376), pf, -1)                         # brazo lejano (detrás del cuerpo)
    c.poli([(120, 470), (30, 520), (20, 560), (110, 540), (150, 520)], GREEN_D)
    for px in (190, 260):
        c.rrect(px - 24, 520, px + 24, 592, 16, GREEN_D)
        c.rrect(px - 28, 572, px + 42, 596, 12, GREEN_D)
    c.elipse(220, 400, 104, 140, GREEN)
    c.elipse(238, 420, 66, 100, BELLY, ow=0)
    for i in range(4):
        y = 300 + i * 52
        c.poli([(122 + i * 3, y - 18), (92 + i * 2, y + 6), (124 + i * 3, y + 28)], GREEN_D, ow=4)
    if prenda: poncho(c, prenda)
    brazo((300, 380), pn, 1, dedo=(pose == 'senala' and brazos > .5))
    # cabeza + hocico
    c.elipse(228, 250, 100, 74, GREEN)
    c.rrect(230, 232, 410, 300, 32, GREEN)
    c.elipse(380, 246, 7, 6, OUT, ow=0)
    # boca
    A = 6 + boca * 46
    forma = {'feliz': 'sonrisa', 'orgullo': 'media', 'triste': 'triste', 'confuso': 'ondas', 'nervioso': 'ondas', 'amor': 'sonrisa',
             'enojo': 'dientes', 'concentrado': 'lengua', 'asombro': 'abierta', 'grito': 'abierta'}.get(emo, 'recta')
    if boca > .12 or forma in ('abierta', 'dientes'):
        if forma == 'dientes': A = max(A, 22)
        if forma == 'abierta': A = max(A, 36)
        c.rrect(238, 286, 408, 300 + A + 12, 18, GREEN)
        c.poli([(250, 296), (398, 296), (386, 296 + A), (262, 296 + A)], (120, 30, 60), ow=4)
        if A > 24: c.elipse(326, 296 + A - 9, 38, 11, (255, 120, 150), ow=0)
        for tx in (258, 310, 362): c.poli([(tx, 296), (tx + 16, 296), (tx + 8, 311)], CREAM, ow=3)
    else:
        if forma == 'recta': pts = [(250, 288), (400, 288)]
        elif forma == 'ondas': pts = [(250, 288), (272, 295), (296, 286), (320, 295), (344, 286), (368, 295), (400, 288)]
        elif forma == 'sonrisa': pts = [(250, 280), (310, 304), (372, 300), (404, 270)]
        elif forma == 'media': pts = [(250, 292), (330, 292), (376, 284), (404, 268)]
        elif forma == 'triste': pts = [(250, 296), (324, 278), (402, 298)]
        elif forma == 'lengua':
            pts = [(250, 288), (400, 288)]
            c.rrect(330, 284, 384, 316, 14, (255, 120, 150), ow=5)
        else: pts = [(250, 288), (400, 288)]
        c.curva(pts, 8, OUT, ow=0) if forma in ('sonrisa', 'media', 'triste') else c.linea(pts, 8, OUT)
        for tx in (258, 310, 362):
            c.poli([(tx, 300 + (4 if forma in ('triste',) else 0)), (tx + 16, 300), (tx + 8, 313)], CREAM, ow=3) if forma == 'recta' and False else None
    # ojos
    for k, ex in enumerate((236, 306)):
        r = 33 * big
        c.elipse(ex, 190, r, r + 2 * big, CREAM)
        px, py = ex + 8 + mira[0] * 12, 194 + mira[1] * 12
        if emo == 'amor': c.corazon(px, py, 34, PINK, ow=0)
        else:
            c.elipse(px, py, 11 * big if emo != 'asombro' else 7, 12 * big if emo != 'asombro' else 8, OUT, ow=0)
            c.elipse(px - 3, py - 4, 3.4, 3.4, WHITE, ow=0)
        # párpados
        if emo == 'enojo': c.segmento(ex, 190, r, -90 + (28 if k == 0 else -28), .42, GREEN)
        elif emo == 'triste': c.segmento(ex, 190, r, -90 + (-24 if k == 0 else 24), .38, GREEN)
        elif emo in ('feliz', 'amor'): c.segmento(ex, 190, r, 90, .30, GREEN)
        elif emo == 'orgullo': c.segmento(ex, 190, r, -90, .42, GREEN)
        elif emo == 'concentrado': c.segmento(ex, 190, r, -90 + (14 if k == 0 else -14), .30, GREEN)
        elif emo == 'confuso' and k == 1: c.segmento(ex, 190, r, -90, .28, GREEN)
        if parp > 0: c.segmento(ex, 190, r, -90, min(1., parp), GREEN)
    # cejas
    def ceja(a, b): c.linea([a, b], 9, OUT)
    if emo in ('nervioso', 'triste'):
        ceja((204, 154), (252, 134)); ceja((340, 154), (292, 134))
    elif emo in ('asombro', 'grito'):
        c.curva([(202, 130), (226, 104), (256, 126)], 9, OUT, ow=0); c.curva([(340, 130), (316, 104), (286, 126)], 9, OUT, ow=0)
    elif emo == 'enojo':
        ceja((200, 130), (254, 156)); ceja((344, 130), (290, 156))
    elif emo in ('feliz', 'amor'):
        c.curva([(204, 142), (228, 124), (254, 140)], 9, OUT, ow=0); c.curva([(340, 142), (316, 124), (288, 140)], 9, OUT, ow=0)
    elif emo == 'confuso':
        c.curva([(204, 140), (228, 116), (254, 134)], 9, OUT, ow=0); ceja((290, 150), (340, 144))
    elif emo == 'concentrado':
        ceja((204, 152), (254, 142)); ceja((338, 152), (290, 142))
    else:
        ceja((206, 150), (254, 146)); ceja((338, 150), (290, 146))
    sudor = (emo in ('nervioso', 'grito')) if sudor is None else sudor
    if sudor:
        c.poli([(176, 124), (162, 156), (176, 166), (190, 156)], (150, 210, 255), ow=4)
    if emo == 'triste': c.poli([(262, 224), (254, 246), (262, 254), (270, 246)], (150, 210, 255), ow=3)
    if sombrero == 'vaquero': sombrero_vaquero(c, 240, 138)
    elif sombrero == 'charro': sombrero_charro(c, 240, 130)
    return c.fin()


# =============================================================== NEZA: ESCENARIO
def _rnd(seed):
    import random
    return random.Random(seed)


def casas_neza(seed=1, w=1080, h=340, noche=False):
    """Franja repetible de casas de Neza: colores vivos, tinacos, antenas, ropa tendida. Se dibuja de lado a lado sin cortes."""
    r = _rnd(seed); c = L2(w, h)
    cols = [(255, 107, 139), (255, 179, 107), (110, 190, 230), (150, 120, 220), (130, 210, 150), (255, 224, 138)]
    if noche: cols = [(120, 50, 110), (150, 80, 70), (60, 90, 140), (80, 60, 140), (60, 120, 90), (140, 120, 70)]
    x = 6
    while x < w - 70:
        bw = r.randint(96, 150); bh = r.randint(120, 250)
        if x + bw > w - 6: bw = w - 6 - x
        if bw < 70: break
        col = r.choice(cols)
        top = h - 8 - bh
        c.rrect(x, top, x + bw, h - 8, 6, col)
        c.rrect(x - 4, top - 10, x + bw + 4, top + 6, 3, tuple(max(0, v - 50) for v in col))       # losa
        for j in range(r.randint(1, 2)):
            for i in range(max(1, (bw - 30) // 44)):
                wx, wy = x + 16 + i * 44, top + 28 + j * 70
                if wy + 40 < h - 40:
                    lit = noche and r.random() < .6
                    c.rrect(wx, wy, wx + 30, wy + 42, 4, GOLD if lit else (60, 40, 100), ow=4)
        if h - 8 - bh > 6:
            # varillas
            if r.random() < .6:
                for k in range(3): c.linea([(x + 12 + k * 14, top - 8), (x + 12 + k * 14, top - 34)], 5, (150, 120, 120), ow=0)
            # tinaco
            if r.random() < .8:
                tx = x + bw - 40
                c.elipse(tx, top - 26, 26, 30, (36, 36, 60) if r.random() < .5 else (70, 90, 150), ow=5)
                c.rrect(tx - 14, top - 8, tx + 14, top + 2, 2, (60, 60, 80), ow=3)
            # antena de TV / parabólica
            if r.random() < .5:
                ax = x + 26
                c.linea([(ax, top - 6), (ax, top - 50)], 5, (190, 190, 210))
                c.linea([(ax - 20, top - 44), (ax + 20, top - 44)], 5, (190, 190, 210)); c.linea([(ax - 14, top - 32), (ax + 14, top - 32)], 5, (190, 190, 210))
        x += bw + r.randint(2, 10)
    return c.fin()


def bordo_strip(w=1080, h=300, noche=False):
    """Bordo de Xochiaca: lomas verdes lejanas con camino, antena y banderines (repetible)."""
    c = L2(w, h)
    verde = (70, 120, 120) if not noche else (34, 60, 84)
    claro = (96, 158, 140) if not noche else (44, 78, 100)
    pts = [(0, h)]
    for i in range(0, w + 1, 20):
        pts.append((i, h - 120 - 80 * math.sin(i / w * 2 * math.pi * 2 - .6) - 30 * math.sin(i / w * 2 * math.pi * 6)))
    pts.append((w, h))
    c.poli(pts, verde, ow=0)
    pts2 = [(0, h)] + [(i, y + 34) for i, y in pts[1:-1]] + [(w, h)]
    c.poli(pts2, claro, ow=0)
    # camino en zigzag
    top = pts[len(pts) // 4]
    c.linea([(250, h - 10), (300, h - 70), (230, h - 120), (300, h - 170)], 9, (230, 200, 160) if not noche else (110, 100, 130))
    # antena en la cima
    px, py = pts[len(pts) // 4][0], pts[len(pts) // 4][1]
    c.linea([(px, py + 6), (px, py - 50)], 5, (200, 200, 220))
    c.elipse(px, py - 54, 6, 6, RED, ow=0)
    return c.fin()


def antena_torre(h=300, rojo=True):
    c = L2(110, h)
    c.poli([(55, 8), (96, h - 6), (14, h - 6)], None, ow=0) if False else None
    for k in range(7):
        y0 = 20 + k * (h - 40) / 7; y1 = y0 + (h - 40) / 7
        w0 = 6 + (y0 / h) * 36; w1 = 6 + (y1 / h) * 36
        c.linea([(55 - w0, y0), (55 + w1, y1)], 5, (200, 196, 225), ow=2)
        c.linea([(55 + w0, y0), (55 - w1, y1)], 5, (200, 196, 225), ow=2)
        c.linea([(55 - w1, y1), (55 + w1, y1)], 5, (200, 196, 225), ow=2)
    c.linea([(55 - 6, 14), (14, h - 6)], 6, (170, 166, 205), ow=2); c.linea([(55 + 6, 14), (96, h - 6)], 6, (170, 166, 205), ow=2)
    c.elipse(55, 10, 9, 9, RED if rojo else (120, 40, 50), ow=3)
    return c.fin()


def toldo(col=(255, 107, 139), col2=CREAM, w=170, h=150):
    """Puesto de tianguis: toldo de rayas y mesa con mercancía de colores."""
    c = L2(w, h)
    c.linea([(14, 36), (14, h - 6)], 7, (150, 120, 120), ow=2); c.linea([(w - 14, 36), (w - 14, h - 6)], 7, (150, 120, 120), ow=2)
    n = 6; sw = (w - 16) / n
    for i in range(n):
        x0 = 8 + i * sw
        c.poli([(x0, 40), (x0 + sw, 40), (x0 + sw - 2, 8), (x0 + 6, 8)] if False else [(x0, 44), (x0 + sw, 44), (x0 + sw - 4, 10), (x0 + 4, 10)], col if i % 2 == 0 else col2, ow=3)
        c.d.pieslice([x0 * SS, (36) * SS, (x0 + sw) * SS, (60) * SS], 0, 180, fill=col if i % 2 == 0 else col2, outline=OUT, width=3 * SS)
    c.rrect(20, h - 52, w - 20, h - 36, 4, (150, 100, 70), ow=4)
    r = _rnd(int(col[0] + col[1]))
    for i in range(7):
        c.elipse(32 + i * 18, h - 62, 9, 9, r.choice([(255, 107, 139), GOLD, (130, 210, 150), CYAN, ORANGE]), ow=3)
    return c.fin()


def pin(col=PINK, w=70):
    c = L2(w, int(w * 1.3))
    cx, cy, r = w / 2, w * .46, w * .40
    c.poli([(cx - r * .85, cy + r * .5), (cx, w * 1.26), (cx + r * .85, cy + r * .5)], col)
    c.elipse(cx, cy, r, r, col)
    c.elipse(cx, cy, r * .38, r * .38, CREAM, ow=3)
    return c.fin()


def torre_neon(w=90, h=260, col=(194, 89, 255)):
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 4, 8, (34, 20, 68))
    r = _rnd(w + h)
    for j in range(h // 34):
        for i in range(max(1, (w - 24) // 22)):
            if r.random() < .7: c.rrect(14 + i * 22, 20 + j * 34, 26 + i * 22, 38 + j * 34, 3, r.choice([col, PINK, GOLD, CYAN]), ow=0)
    c.linea([(w / 2, 6), (w / 2, -4)], 5, OUT)
    return c.fin()


def mapa_panel(w=900, h=520, tono=0):
    """Tablero de mapa: panel oscuro con cuadrícula y borde de la marca."""
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 6, 40, (30, 16, 58), ow=7)
    for x in range(60, w - 40, 60): c.linea([(x, 24), (x, h - 24)], 2, (70, 44, 120))
    for y in range(60, h - 30, 60): c.linea([(24, y), (w - 24, y)], 2, (70, 44, 120))
    return c.fin()


def isla_leonida(w=900, h=520):
    """Costa tipo Leonida: agua rosa-azul, tierra morada, playa y rutas de neón."""
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 6, 40, (46, 70, 150), ow=7)
    c.poli([(6 + 40, 6), (w - 46, 6), (w - 6, 46), (w - 6, 190), (640, 230), (560, 330), (430, 300), (300, 360), (190, 330), (120, 430), (60, h - 6), (46, h - 6), (6, h - 46), (6, 46)], (130, 74, 190), ow=0)
    c.poli([(40, 120), (180, 80), (330, 110), (470, 70), (610, 130), (760, 90), (880, 150), (860, 300), (620, 250), (560, 350), (420, 322), (300, 380), (190, 350), (130, 440), (50, 470)], (160, 100, 215), ow=0)
    c.linea([(60, 440), (190, 340), (310, 372), (430, 312), (560, 342)], 7, (255, 224, 138))
    c.linea([(100, 200), (330, 180), (520, 160), (780, 190)], 8, PINK)
    c.rrect(6, 6, w - 6, h - 6, 40, None, ow=7) if False else c.d.rounded_rectangle([6 * SS, 6 * SS, (w - 6) * SS, (h - 6) * SS], radius=40 * SS, outline=OUT, width=7 * SS)
    return c.fin()


def mapa_neza_base(w=900, h=520):
    """Neza: plano de colonias (manzanas), canal, avenida y bordo."""
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 6, 40, (84, 70, 120), ow=7)
    c.rrect(26, 26, w - 26, h - 26, 30, (60, 46, 100), ow=0)
    r = _rnd(5)
    for i in range(7):
        for j in range(4):
            x0, y0 = 54 + i * 118, 60 + j * 104
            c.rrect(x0, y0, x0 + 96, y0 + 82, 8, r.choice([(110, 80, 160), (96, 70, 150), (126, 90, 170), (255, 179, 107, 255)] if False else [(110, 80, 160), (96, 70, 150), (126, 90, 170)]), ow=0)
    c.linea([(30, 410), (270, 330), (520, 360), (870, 250)], 22, (70, 150, 190))          # canal
    c.linea([(30, 410), (270, 330), (520, 360), (870, 250)], 6, (170, 220, 240))
    c.linea([(40, 140), (860, 170)], 16, (255, 224, 138)); c.linea([(40, 140), (860, 170)], 4, (255, 179, 107))
    c.d.rounded_rectangle([6 * SS, 6 * SS, (w - 6) * SS, (h - 6) * SS], radius=40 * SS, outline=OUT, width=7 * SS)
    return c.fin()


# =============================================================== NEZA: MEXIBÚS
def mexibus_capas():
    """(interior, carrocería con ventanas huecas). Sprite 1000x340; el piso queda en y=330."""
    W_, H_ = 1000, 340
    vent = [(58, 168), (188, 298), (318, 428), (448, 558), (578, 688), (708, 818)]
    ci = L2(W_, H_)
    ci.rrect(40, 50, 980, 200, 20, (60, 34, 100), ow=0)
    for x0, x1 in vent[:-1]:
        ci.rrect(x0 + 8, 132, x1 - 8, 200, 10, (96, 60, 150), ow=0)        # respaldos
        ci.linea([((x0 + x1) / 2, 60), ((x0 + x1) / 2, 100)], 6, (200, 190, 230))   # agarraderas
    c = L2(W_, H_)
    c.rrect(20, 38, 980, 296, 46, (255, 128, 56))
    c.rrect(20, 214, 980, 296, 36, (226, 58, 70), ow=0)
    c.rrect(26, 200, 974, 216, 0, CREAM, ow=0)
    c.rrect(20, 38, 980, 296, 46, None, ow=0) if False else c.d.rounded_rectangle([20 * SS, 38 * SS, 980 * SS, 296 * SS], radius=46 * SS, outline=OUT, width=6 * SS)
    c.rrect(150, 18, 820, 44, 12, (210, 210, 228))                      # aire acondicionado
    for x0, x1 in vent: c.hueco(x0, 66, x1, 178, 14)
    c.hueco(846, 56, 972, 182, 22)                                       # parabrisas
    for x0, x1 in vent: c.d.rounded_rectangle([x0 * SS, 66 * SS, x1 * SS, 178 * SS], radius=14 * SS, outline=OUT, width=5 * SS)
    c.d.rounded_rectangle([846 * SS, 56 * SS, 972 * SS, 182 * SS], radius=22 * SS, outline=OUT, width=5 * SS)
    c.rrect(560, 70, 580, 290, 4, (255, 128, 56), ow=0)
    for x in (303, 433, 563): c.linea([(x, 186), (x, 296)], 5, OUT)      # puertas
    c.texto(500, 252, 'MEXIBÚS', 50, CREAM, kind='title')
    c.elipse(962, 236, 12, 16, GOLD, ow=4); c.elipse(38, 236, 9, 14, RED, ow=4)
    for cx in (210, 780):
        c.elipse(cx, 294, 78, 78, (24, 16, 40), ow=0)
        c.rrect(cx - 80, 294, cx + 80, 340, 0, (0, 0, 0, 0), ow=0)
    return ci.fin(), c.fin()


def rueda(r=64):
    c = L2(2 * r + 12, 2 * r + 12); m = r + 6
    c.elipse(m, m, r, r, (24, 18, 40), ow=6)
    c.elipse(m, m, r * .58, r * .58, (200, 198, 220), ow=4)
    for k in range(5):
        a = k * 2 * math.pi / 5
        c.linea([(m, m), (m + math.cos(a) * r * .52, m + math.sin(a) * r * .52)], 7, (110, 100, 150))
    c.elipse(m, m, r * .14, r * .14, OUT, ow=0)
    return c.fin()


def volante(r=34):
    c = L2(2 * r + 10, 2 * r + 10); m = r + 5
    c.elipse(m, m, r, r * .55, None, ow=0) if False else None
    c.d.ellipse([(m - r) * SS, (m - r * .6) * SS, (m + r) * SS, (m + r * .6) * SS], outline=OUT, width=12 * SS)
    c.d.ellipse([(m - r) * SS, (m - r * .6) * SS, (m + r) * SS, (m + r * .6) * SS], outline=(120, 110, 150), width=6 * SS)
    return c.fin()


# =============================================================== NEZA: TLACUACHE CORREDOR
GRIS = (196, 192, 210); GRIS_C = (238, 234, 246); ROSA_T = (255, 160, 182)


def tlacuache(fase=0, emo='susto', mira=-1, tenis=0):
    """Tlacuache corriendo hacia la derecha con riñonera y tenis brillantes. 12 fases. Sprite 400x420, pies en y=410."""
    c = L2(400, 420); ph = fase / 12 * 2 * math.pi
    hip = [(150, 316), (178, 316)]
    def pierna(h, ph_, lejos):
        fx = h[0] + math.sin(ph_) * 62; fy = 404 - max(0, -math.cos(ph_)) * 56
        kx = (h[0] + fx) / 2 + 18; ky = (h[1] + fy) / 2 - 6
        col = (150, 146, 170) if lejos else GRIS
        c.curva([h, (kx, ky), (fx, fy)], 24, col, ow=5)
        # tenis
        c.poli([(fx - 20, fy - 4), (fx + 26, fy - 4), (fx + 44, fy + 8), (fx + 44, fy + 14), (fx - 22, fy + 14)], CREAM if not lejos else (220, 216, 230))
        c.poli([(fx - 20, fy + 8), (fx + 44, fy + 8), (fx + 44, fy + 14), (fx - 22, fy + 14)], GOLD, ow=0)
        c.linea([(fx + 8, fy - 3), (fx + 24, fy + 4)], 4, GOLD)
        return fx, fy
    pierna(hip[0], ph + math.pi, True)
    # brazo lejano
    ax = 170 + math.sin(ph) * 40
    c.curva([(168, 220), (ax + 6, 262), (ax + 20, 290)], 20, (150, 146, 170), ow=4)
    # cola rosa
    c.curva([(96, 270), (40, 262), (22, 318), (54, 342)], 14, ROSA_T, ow=4)
    # cuerpo
    c.elipse(150, 250, 74, 90, GRIS)
    c.elipse(168, 262, 44, 62, GRIS_C, ow=0)
    # riñonera
    c.linea([(84, 280), (214, 292)], 16, (40, 28, 70), ow=0)
    c.rrect(176, 268, 232, 316, 14, (255, 200, 90), ow=5)
    c.linea([(184, 286), (224, 286)], 4, OUT)
    c.elipse(206, 300, 5, 5, OUT, ow=0)
    pierna(hip[1], ph, False)
    ax2 = 170 - math.sin(ph) * 40
    c.curva([(176, 220), (ax2 + 10, 256), (ax2 + 28, 280)], 22, GRIS, ow=5)
    c.elipse(ax2 + 28, 282, 13, 13, ROSA_T, ow=4)
    # cabeza
    c.elipse(190, 112, 22, 22, ROSA_T)                      # orejas
    c.elipse(222, 112, 22, 22, ROSA_T)
    c.poli([(176, 160), (214, 82), (276, 112), (356, 164), (276, 190), (206, 196)], GRIS_C)
    c.elipse(358, 164, 11, 11, (60, 30, 70), ow=3)
    # ojo
    c.elipse(256, 138, 20, 22, CREAM, ow=4)
    c.elipse(256 + 7 * mira, 140, 8, 9, OUT, ow=0)
    if emo == 'susto':
        c.linea([(232, 104), (276, 120)], 7, OUT)
        c.poli([(210, 100), (200, 76), (220, 86)], (150, 210, 255), ow=3)
    elif emo == 'burla':
        c.linea([(232, 114), (276, 110)], 7, OUT)
    c.linea([(300, 180), (338, 178)], 5, OUT)
    return c.fin()


def etiqueta_precio(txt='$500'):
    c = L2(190, 100)
    c.linea([(8, 12), (40, 40)], 4, CREAM)
    c.rrect(34, 24, 184, 88, 14, CREAM)
    c.elipse(46, 38, 5, 5, OUT, ow=0)
    c.texto(112, 58, txt, 48, OUT, kind='title')
    return c.fin()


def destellos(r=40):
    c = L2(2 * r + 10, 2 * r + 10)
    m = r + 5
    c.poli([(m, m - r), (m + r * .18, m - r * .18), (m + r, m), (m + r * .18, m + r * .18), (m, m + r), (m - r * .18, m + r * .18), (m - r, m), (m - r * .18, m - r * .18)], (255, 250, 210), ow=0)
    return c.fin()


def nube_polvo(r=46):
    c = L2(r * 3, r * 2)
    for dx, dy, rr in ((0, 0, r * .8), (r * .8, -r * .1, r * .6), (-r * .8, r * .1, r * .6), (r * .3, r * .3, r * .55)):
        c.elipse(r * 1.5 + dx, r + dy, rr, rr, (232, 220, 244), ow=0)
    return c.fin()


# =============================================================== NEZA: ESCALA (noche)
def compa(var=0):
    """Siluetas de compas (150x330) con detalles de color; miran a la derecha, hacia la puerta."""
    gorra = [PINK, CYAN, GOLD, (130, 210, 150), ORANGE][var % 5]
    chamarra = [(70, 44, 120), (52, 34, 96), (96, 54, 130), (44, 52, 110), (80, 40, 90)][var % 5]
    c = L2(150, 330); skin = (58, 36, 96)
    c.rrect(46, 230, 72, 320, 10, (40, 26, 76)); c.rrect(80, 230, 106, 320, 10, (40, 26, 76))
    c.rrect(30, 110, 124, 252, 34, chamarra)
    c.linea([(76, 120), (76, 250)], 4, (30, 18, 60))
    c.elipse(78, 70, 38, 40, skin)
    if var % 5 in (0, 2): c.poli([(38, 58), (50, 24), (112, 24), (120, 58), (150, 66), (116, 74), (40, 74)], gorra)      # gorra con visera
    elif var % 5 == 1: c.poli([(36, 66), (46, 20), (112, 18), (122, 66), (110, 50), (50, 50)], chamarra)               # capucha
    elif var % 5 == 3: c.rrect(44, 54, 112, 70, 8, (20, 12, 44)); c.linea([(52, 62), (104, 62)], 3, CYAN)               # lentes
    else: c.poli([(42, 50), (60, 14), (96, 10), (114, 50)], (30, 18, 60))                                              # pelo
    for ex in (68, 92): c.elipse(ex, 74, 6, 7, CREAM, ow=0); c.elipse(ex + 2, 75, 3, 3.5, OUT, ow=0)
    if var % 5 in (2, 4): c.curva([(52, 118), (76, 160), (100, 118)], 6, GOLD, ow=2)                                     # cadena
    c.linea([(28, 120), (14, 200)], 24, chamarra, ow=4); c.linea([(126, 120), (138, 190)], 24, chamarra, ow=4)
    return c.fin()


def fachada(w=860, h=470):
    c = L2(w, h)
    c.rrect(10, 10, w - 10, h, 12, (46, 24, 84))
    for y in range(40, h, 36):
        c.linea([(14, y), (w - 14, y)], 2, (70, 40, 112))
        for x in range(30 + (y // 36 % 2) * 30, w - 20, 60): c.linea([(x, y), (x, y + 36)], 2, (70, 40, 112))
    c.rrect(560, 150, 700, h, 10, (255, 140, 160), ow=6)             # puerta iluminada
    c.rrect(574, 164, 686, h, 8, (255, 214, 190), ow=0)
    c.poli([(540, 130), (720, 130), (740, 160), (520, 160)], PINK_D)
    for i in range(6): c.poli([(520 + i * 37, 160), (557 + i * 37, 160), (554 + i * 37, 130), (523 + i * 37, 130)], CREAM if i % 2 else PINK_D, ow=3)
    for x in (70, 210, 340):
        c.rrect(x, 190, x + 100, 300, 10, (255, 179, 107), ow=6); c.linea([(x + 50, 190), (x + 50, 300)], 4, OUT)
    return c.fin()


def letrero_escala(apagado=0):
    c = L2(660, 200)
    col = PINK if not apagado else (150, 70, 110)
    c.d.rounded_rectangle([10 * SS, 10 * SS, 650 * SS, 190 * SS], radius=36 * SS, fill=(24, 12, 44), outline=col, width=9 * SS)
    c.d.rounded_rectangle([26 * SS, 26 * SS, 634 * SS, 174 * SS], radius=26 * SS, outline=(110, 230, 255) if not apagado else (70, 110, 130), width=4 * SS)
    c.texto(330, 102, 'EL ESCALA', 92, (255, 235, 245) if not apagado else (170, 130, 160), kind='title')
    im = c.fin()
    return glow(im, 18, 1.5) if not apagado else im


def calendario(txt='MAR'):
    c = L2(270, 310)
    c.rrect(10, 30, 260, 300, 22, CREAM)
    c.rrect(10, 30, 260, 120, 22, (226, 58, 70)); c.rrect(10, 80, 260, 120, 0, (226, 58, 70), ow=0)
    c.d.line(c.P([(10, 120), (260, 120)]), fill=OUT, width=6 * SS)
    c.texto(135, 208, txt, 100, OUT, kind='title')
    for x in (70, 200): c.linea([(x, 8), (x, 52)], 14, (200, 198, 220), ow=3)
    c.texto(135, 262, '21:00', 38, (120, 90, 150), kind='800')
    return c.fin()


def luna(r=74):
    c = L2(2 * r + 20, 2 * r + 20); m = r + 10
    c.elipse(m, m, r, r, (255, 246, 210))
    for dx, dy, rr in ((-.3, -.2, .22), (.3, .15, .28), (-.1, .45, .14)): c.elipse(m + dx * r, m + dy * r, rr * r, rr * r, (232, 220, 180), ow=4)
    return glow(c.fin(), 22, 1.2)


def signo(txt='?', size=120, col=GOLD):
    c = L2(int(size * .9), int(size * 1.2))
    c.texto(c.w / 2, c.h / 2, txt, size, col, kind='title')
    out = c.fin()
    return out


# =============================================================== NEZA: VEHÍCULOS
def combi():
    """(interior, carrocería). 640x340, ruedas apoyadas en y=330. Ventana del conductor hueca en (330,78)-(470,164)."""
    ci = L2(640, 340)
    ci.rrect(300, 70, 590, 175, 14, (70, 40, 110), ow=0)
    c = L2(640, 340)
    c.poli([(28, 268), (24, 98), (46, 64), (480, 58), (556, 72), (584, 164), (614, 178), (628, 268)], (150, 70, 220))
    c.poli([(28, 214), (628, 214), (628, 236), (28, 236)], PINK, ow=0)
    c.poli([(28, 228), (628, 228), (628, 242), (28, 242)], CYAN, ow=0)
    c.poli([(28, 262), (628, 262), (628, 268), (28, 268)], (120, 50, 190), ow=0)
    for x0, x1 in ((64, 184), (198, 318)): c.rrect(x0, 82, x1, 164, 12, (96, 70, 170), ow=5)
    c.hueco(334, 82, 468, 164, 12); c.d.rounded_rectangle([334 * SS, 82 * SS, 468 * SS, 164 * SS], radius=12 * SS, outline=OUT, width=5 * SS)
    c.poli([(486, 76), (548, 86), (570, 164), (486, 164)], (96, 70, 170), ow=5)
    c.linea([(326, 70), (326, 214)], 5, OUT)
    c.rrect(590, 236, 640, 262, 8, (220, 220, 236), ow=5)
    c.elipse(604, 196, 14, 18, GOLD, ow=4); c.elipse(40, 200, 9, 14, RED, ow=4)
    # alerón y rack
    c.poli([(24, 62), (24, 34), (150, 26), (150, 40), (60, 60)], (60, 30, 110))
    c.linea([(60, 60), (60, 44)], 6, OUT)
    for x in (230, 400): c.linea([(x, 58), (x, 48)], 6, (220, 220, 236))
    c.linea([(210, 48), (440, 48)], 6, (220, 220, 236), ow=3)
    return ci.fin(), c.fin()


def pesero():
    c = L2(560, 300)
    c.rrect(26, 50, 548, 252, 26, (240, 240, 252))
    c.rrect(26, 158, 548, 190, 0, (60, 200, 120), ow=0)
    c.d.rounded_rectangle([26 * SS, 50 * SS, 548 * SS, 252 * SS], radius=26 * SS, outline=OUT, width=6 * SS)
    r = _rnd(3)
    for i in range(5):
        x0 = 54 + i * 90
        c.rrect(x0, 70, x0 + 74, 142, 10, (96, 70, 170), ow=5)
        c.elipse(x0 + 38, 118, 14, 14, tuple(r.choice([(255, 179, 107), (255, 107, 139), (130, 210, 150)])), ow=3)
    c.poli([(484, 70), (536, 80), (544, 150), (484, 150)], (96, 70, 170), ow=5)
    c.rrect(430, 22, 540, 50, 8, (30, 20, 50), ow=4); c.texto(485, 37, 'RUTA 42', 22, GOLD, kind='800')
    c.elipse(536, 214, 11, 15, GOLD, ow=4)
    c.linea([(40, 214), (500, 214)], 5, OUT)
    return c.fin()


def bocina(w=150, h=190):
    c = L2(w, h)
    c.rrect(8, 8, w - 8, h - 8, 14, (30, 22, 54))
    c.elipse(w / 2, 56, 30, 30, (56, 44, 96), ow=5); c.elipse(w / 2, 56, 12, 12, (150, 140, 190), ow=3)
    c.elipse(w / 2, 128, 46, 46, (56, 44, 96), ow=5)
    return c.fin()


def cono(r=40):
    c = L2(2 * r + 8, 2 * r + 8); m = r + 4
    c.elipse(m, m, r, r, (120, 40, 80), ow=5); c.elipse(m, m, r * .55, r * .55, (200, 80, 120), ow=3); c.elipse(m, m, r * .2, r * .2, (240, 200, 210), ow=0)
    return c.fin()


def nota(col=PINK, doble=False):
    c = L2(70, 100)
    c.linea([(44, 14), (44, 70)], 8, col, ow=3)
    c.elipse(30, 74, 16, 12, col, ow=4)
    c.poli([(44, 12), (68, 30), (44, 38)], col, ow=3)
    return c.fin()


def neon_suelo(col=PINK, w=640):
    c = Image.new('RGBA', (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([20, 60, w - 20, 130], fill=col + (255,))
    c = c.filter(ImageFilter.GaussianBlur(26))
    c.putalpha(c.getchannel('A').point(lambda v: min(255, int(v * 1.5))))
    return c


# =============================================================== AJUSTES (menú del juego)
def panel_menu(w=820, h=440, titulo='AJUSTES'):
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 6, 36, (30, 16, 58), ow=7)
    c.rrect(6, 6, w - 6, 70, 36, (74, 38, 120), ow=0); c.rrect(6, 40, w - 6, 70, 0, (74, 38, 120), ow=0)
    c.d.line(c.P([(6, 70), (w - 6, 70)]), fill=OUT, width=5 * SS)
    c.texto(40, 40, titulo, 34, CREAM, kind='title', anchor='lm')
    for i in range(3): c.elipse(w - 50 - i * 34, 40, 9, 9, (PINK, ORANGE, GOLD)[i], ow=0)
    c.d.rounded_rectangle([6 * SS, 6 * SS, (w - 6) * SS, (h - 6) * SS], radius=36 * SS, outline=OUT, width=7 * SS)
    return c.fin()


def palomita(r=60):
    c = L2(2 * r + 10, 2 * r + 10); m = r + 5
    c.elipse(m, m, r, r, (96, 205, 134), ow=7)
    c.linea([(m - r * .45, m + r * .02), (m - r * .1, m + r * .38), (m + r * .5, m - r * .35)], int(r * .22), WHITE, ow=0)
    return c.fin()


def velocimetro(q=0., unit='MPH'):
    c = L2(480, 330); cx, cy, r = 240, 262, 205
    c.d.pieslice([(cx - r) * SS, (cy - r) * SS, (cx + r) * SS, (cy + r) * SS], 180, 360, fill=(46, 26, 88), outline=OUT, width=7 * SS)
    for i in range(21):
        a = math.radians(180 + i * 9); long = i % 5 == 0
        r1, r0 = r - 16, r - (46 if long else 30)
        col = RED if i >= 17 else (CREAM if long else (170, 150, 200))
        c.linea([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)], 8 if long else 5, col)
    a = math.radians(180 + q * 180)
    c.linea([(cx, cy), (cx + math.cos(a) * (r - 60), cy + math.sin(a) * (r - 60))], 12, GOLD, ow=4)
    c.elipse(cx, cy, 20, 20, ORANGE, ow=5)
    c.texto(cx, cy - 74, unit, 56, CREAM, kind='title')
    return c.fin()


def interruptor(p=0.):
    c = L2(300, 150)
    col = tuple(int(a + (b - a) * p) for a, b in zip((86, 62, 130), (96, 205, 134)))
    c.rrect(8, 20, 292, 130, 55, col, ow=7)
    kx = 75 + 150 * p
    c.elipse(kx, 75, 46, 46, CREAM, ow=7)
    return c.fin()


def reticula(k=0.):
    """k=0: mira complicada (anillos, marcas, cruz). k=1: solo un punto."""
    c = L2(340, 340); m = 170; f = 1 - k
    if f > .02:
        a = int(255 * f)
        for rr, w in ((140 * (1 - .5 * k), 9), (84 * (1 - .5 * k), 6)):
            c.d.ellipse([(m - rr) * SS, (m - rr) * SS, (m + rr) * SS, (m + rr) * SS], outline=CREAM + (a,), width=int(w * SS))
        for ang in range(0, 360, 45):
            t_ = math.radians(ang); r0, r1 = 100 * (1 - .5 * k), 160 * (1 - .5 * k)
            c.d.line([((m + math.cos(t_) * r0) * SS, (m + math.sin(t_) * r0) * SS), ((m + math.cos(t_) * r1) * SS, (m + math.sin(t_) * r1) * SS)], fill=(PINK if ang % 90 else ORANGE) + (a,), width=int(8 * SS))
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.d.line([((m + dx * 22) * SS, (m + dy * 22) * SS), ((m + dx * 70) * SS, (m + dy * 70) * SS)], fill=GOLD + (a,), width=int(6 * SS))
    rd = 7 + 9 * k
    c.elipse(m, m, rd, rd, RED if k < .5 else (255, 107, 139), ow=3 if k > .4 else 0)
    return c.fin()


def campana(w=220):
    c = L2(w, w)
    m = w / 2
    c.poli([(m - 70, w - 70), (m - 56, 80), (m - 20, 36), (m + 20, 36), (m + 56, 80), (m + 70, w - 70)], GOLD)
    c.rrect(m - 84, w - 80, m + 84, w - 56, 12, GOLD)
    c.elipse(m, 30, 14, 14, GOLD, ow=5); c.elipse(m, w - 40, 22, 20, ORANGE, ow=5)
    c.linea([(m - 38, 96), (m - 44, 150)], 8, (255, 250, 210))
    return c.fin()


def badge_rojo(txt='1', r=34):
    c = L2(2 * r + 8, 2 * r + 8); c.elipse(r + 4, r + 4, r, r, RED, ow=5); c.texto(r + 4, r + 5, txt, int(r * 1.3), WHITE, kind='title')
    return c.fin()


def toast(w=620, h=120, txt='¡Objetivo cumplido!', f=0.):
    c = L2(w, h)
    c.rrect(6, 6, w - 6, h - 6, 28, (46, 26, 88), ow=6)
    c.estrella(64, h / 2, 28, GOLD, ow=4)
    c.texto(110, 44, txt, 34, CREAM, kind='title', anchor='lm')
    c.rrect(110, 74, w - 40, 94, 10, (30, 16, 58), ow=4)
    if f > 0: c.rrect(110, 74, 110 + (w - 150) * f, 94, 10, (96, 205, 134), ow=0)
    return c.fin()


def barra_subs(txt='Vamos por el botín.', mision=True):
    c = L2(700, 130)
    c.rrect(6, 6, 694, 124, 24, (10, 6, 24), ow=5)
    c.texto(350, 66, txt, 40, CREAM, kind='800')
    if mision:
        c.rrect(30, 14, 160, 44, 12, ORANGE, ow=4); c.texto(95, 29, 'MISIÓN', 22, OUT, kind='800')
    return c.fin()


def candado_ui(ang=0., abierto=0., sweet=60., r=150):
    """Minijuego de ganzúa: anillo con zona verde y una ganzúa que gira."""
    c = L2(2 * r + 40, 2 * r + 40); m = r + 20
    c.elipse(m, m, r, r, (30, 16, 58), ow=8)
    c.d.arc([(m - r + 14) * SS, (m - r + 14) * SS, (m + r - 14) * SS, (m + r - 14) * SS], sweet - 14, sweet + 14, fill=(96, 205, 134), width=int(18 * SS))
    for k_ in range(0, 360, 30):
        t_ = math.radians(k_); c.linea([(m + math.cos(t_) * (r - 40), m + math.sin(t_) * (r - 40)), (m + math.cos(t_) * (r - 28), m + math.sin(t_) * (r - 28))], 5, (170, 150, 200))
    a = math.radians(ang)
    c.linea([(m, m), (m + math.cos(a) * (r - 26), m + math.sin(a) * (r - 26))], 10, GOLD, ow=4)
    c.elipse(m, m, 34, 34, (200, 198, 220) if not abierto else (96, 205, 134), ow=6)
    c.rrect(m - 7, m - 4, m + 7, m + 22, 3, OUT, ow=0); c.elipse(m, m - 6, 8, 8, OUT, ow=0)
    return c.fin()


def cables(chispa=0.):
    c = L2(300, 300)
    c.curva([(10, 80), (110, 40), (150, 140)], 12, RED, ow=4); c.curva([(10, 220), (110, 260), (150, 160)], 12, (80, 150, 255), ow=4)
    c.rrect(150, 130, 190, 170, 8, (200, 198, 220), ow=4)
    c.rrect(190, 70, 290, 230, 18, (44, 30, 80), ow=6)
    c.texto(240, 150, 'ON', 44, GOLD if chispa > 0 else (120, 100, 160), kind='title')
    if chispa > 0:
        for k_ in range(7):
            a_ = k_ * 0.9 + chispa * 3; rr = 20 + 36 * chispa
            c.linea([(150, 150), (150 + math.cos(a_) * rr, 150 + math.sin(a_) * rr)], 6, (255, 250, 190))
    return c.fin()


def icono_ajuste(k=1, tam=150):
    c = L2(tam, tam); m = tam / 2
    c.elipse(m, m, m - 6, m - 6, (74, 38, 120), ow=6)
    if k == 1:
        c.d.pieslice([(m - 46) * SS, (m - 36) * SS, (m + 46) * SS, (m + 56) * SS], 180, 360, fill=(46, 26, 88), outline=CREAM, width=4 * SS)
        c.linea([(m, m + 12), (m + 28, m - 20)], 7, GOLD)
    elif k == 2:
        c.d.ellipse([(m - 40) * SS, (m - 40) * SS, (m + 40) * SS, (m + 40) * SS], outline=CREAM, width=5 * SS)
        c.elipse(m, m, 9, 9, PINK, ow=0)
    elif k == 3:
        c.poli([(m - 30, m + 22), (m - 22, m - 12), (m, m - 34), (m + 22, m - 12), (m + 30, m + 22)], GOLD, ow=4); c.elipse(m, m + 32, 9, 8, ORANGE, ow=3)
    elif k == 4:
        c.rrect(m - 48, m - 22, m + 48, m + 24, 10, (10, 6, 24), ow=4); c.linea([(m - 34, m), (m + 34, m)], 6, CREAM); c.linea([(m - 20, m + 12), (m + 20, m + 12)], 5, CREAM)
    else:
        c.rrect(m - 28, m - 4, m + 28, m + 40, 8, GOLD, ow=5); c.d.arc([(m - 20) * SS, (m - 40) * SS, (m + 20) * SS, (m + 8) * SS], 180, 360, fill=OUT, width=7 * SS)
    return c.fin()


def numero(n, r=34, col=ORANGE):
    c = L2(2 * r + 8, 2 * r + 8); c.elipse(r + 4, r + 4, r, r, col, ow=5); c.texto(r + 4, r + 5, str(n), int(r * 1.35), OUT, kind='title')
    return c.fin()


def gamepad():
    c = L2(300, 190)
    c.poli([(40, 40), (260, 40), (292, 140), (260, 178), (222, 120), (78, 120), (40, 178), (8, 140)], (70, 50, 120))
    c.elipse(96, 82, 24, 24, (40, 28, 80), ow=4); c.elipse(204, 108, 24, 24, (40, 28, 80), ow=4)
    c.linea([(70, 60), (70, 60)], 1, OUT)
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)): c.rrect(150 - 12 + dx * 0, 60 - 12, 150 + 12, 60 + 12, 3, (40, 28, 80), ow=0) if False else None
    for dx, dy, col in ((0, -22, PINK), (0, 22, CYAN), (-22, 0, GOLD), (22, 0, (130, 210, 150))): c.elipse(240 + dx * .5 if False else 232 + dx, 78 + dy, 9, 9, col, ow=3)
    return c.fin()
