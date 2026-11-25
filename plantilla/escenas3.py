"""Escenas de caricatura 3 (25-nov-2026): 5 controles ocultos (c_*), PS5 y Xbox.
Mismo motor y estilo que 5 ajustes (escenas2). render.py pone en R su propio módulo."""
import math
from PIL import Image, ImageDraw
import caricatura2 as C
import escenas2 as E
from caricatura import OUT, SS
from caricatura2 import L2, PINK, ORANGE, CREAM, GOLD, WHITE

R = None
_c = {}
G = E.G
PS_COL = (194, 89, 255)      # PlayStation: lila de la marca
XB_COL = ORANGE              # Xbox: naranja de la marca
DARK = (26, 16, 48)


def S(kind, *a): return E.S(kind, *a)
def cl(x, a=0., b=1.): return max(a, min(b, x))
def pr(t, s, d=.4): return R.prog(t, s, d)
def eo(x): return R.ease_out(x)
def eb(x): return R.ease_back(x)
def idle(t, v=6., a=.02): return 1 + a * math.sin(t * v)
def hop(t, v=11., a=16.): return abs(math.sin(t * v)) * a


def mk(key, fn):
    if key not in _c: _c[key] = fn()
    return _c[key]


# ------------------------------------------------------------------ vestuario de turista
_poncho_orig = C.poncho


def _poncho(c, tipo):
    if tipo != 'turista': return _poncho_orig(c, tipo)
    pts = [(176, 318), (268, 318), (344, 470), (96, 470)]
    c.poli(pts, (255, 107, 139))
    for (fx, fy) in ((150, 430), (210, 360), (262, 410), (300, 455), (196, 450), (238, 335)):
        for k in range(5):
            a = k * math.pi * 2 / 5
            c.elipse(fx + math.cos(a) * 9, fy + math.sin(a) * 9, 8, 8, CREAM, ow=0)
        c.elipse(fx, fy, 5, 5, GOLD, ow=0)
    for (lx, ly) in ((170, 392), (282, 372), (122, 455)):
        c.poli([(lx, ly), (lx + 22, ly - 12), (lx + 30, ly + 4), (lx + 8, ly + 12)], (96, 205, 134), ow=0)
    c.d.line(c.P(pts + [pts[0]]), fill=OUT, width=6 * SS, joint='curve')
    # cámara colgada
    c.linea([(196, 320), (232, 408)], 5, OUT); c.linea([(262, 320), (262, 408)], 5, OUT)
    c.rrect(214, 400, 292, 452, 10, (60, 50, 80), ow=5)
    c.rrect(226, 392, 252, 404, 4, (60, 50, 80), ow=4)
    c.elipse(253, 426, 17, 17, (150, 140, 180), ow=5)
    c.elipse(253, 426, 7, 7, (40, 30, 60), ow=0)


C.poncho = _poncho


def sombrero_turista():
    c = L2(300, 160)
    c.elipse(150, 118, 140, 30, (240, 214, 150))
    c.rrect(80, 46, 220, 118, 30, (240, 214, 150))
    c.rrect(80, 88, 220, 110, 0, (255, 107, 139), ow=4)
    c.elipse(196, 96, 12, 12, GOLD, ow=3)
    return c.fin()


def mapa():
    c = L2(190, 140)
    c.poli([(8, 14), (66, 6), (124, 16), (182, 6), (182, 128), (124, 136), (66, 126), (8, 134)], (250, 236, 200))
    c.linea([(66, 8), (66, 126)], 4, (200, 180, 140)); c.linea([(124, 16), (124, 134)], 4, (200, 180, 140))
    c.curva([(20, 110), (70, 70), (120, 96), (172, 40)], 7, (110, 190, 230), ow=0)
    c.poli([(140, 48), (152, 30), (164, 48), (152, 62)], (255, 84, 84), ow=3)
    c.texto(70, 40, 'MAPA', 28, (42, 20, 72))
    return c.fin().rotate(180)


def banca():
    c = L2(340, 190)
    for x in (50, 290):
        c.rrect(x - 10, 110, x + 10, 186, 4, (60, 40, 90))
    for k in range(3): c.rrect(16, 20 + k * 26, 324, 40 + k * 26, 8, (205, 140, 78))
    c.rrect(10, 100, 330, 124, 8, (205, 140, 78))
    return c.fin()


def puerta():
    c = L2(170, 150)
    c.rrect(8, 8, 162, 142, 16, (38, 30, 58), ow=6)
    c.rrect(26, 18, 146, 66, 10, (96, 80, 150), ow=5)
    c.rrect(10, 100, 160, 118, 0, PINK, ow=0)
    c.rrect(10, 110, 160, 118, 0, ORANGE, ow=0)
    c.rrect(110, 78, 146, 90, 5, (170, 170, 190), ow=3)
    return c.fin()


def reloj(ang):
    c = L2(260, 260); m = 130
    c.elipse(m, m, 116, 116, CREAM, ow=8)
    for k in range(12):
        a = k * math.pi / 6
        c.linea([(m + math.cos(a) * 88, m + math.sin(a) * 88), (m + math.cos(a) * 100, m + math.sin(a) * 100)], 7, OUT)
    a = math.radians(ang - 90)
    c.linea([(m, m), (m + math.cos(a) * 84, m + math.sin(a) * 84)], 9, (255, 107, 139))
    c.linea([(m, m), (m + math.cos(a / 12) * 50, m + math.sin(a / 12) * 50)], 11, OUT)
    c.elipse(m, m, 11, 11, OUT, ow=0)
    return c.fin()


# ------------------------------------------------------------------ botones
def chip(tok, col, r=44):
    def f():
        if tok in ('L3', 'R3', 'LS', 'RS'):
            w, h = 132, 2 * r
            c = L2(w + 14, h + 14)
            c.rrect(7, 7, w + 7, h + 7, r, col, ow=6)
            c.texto(w / 2 + 7, h / 2 + 9, tok, 46, DARK)
            return c.fin()
        c = L2(2 * r + 14, 2 * r + 14); m = r + 7
        c.elipse(m, m, r, r, col, ow=6)
        if tok == 'tri':
            pts = [(m, m - 22), (m + 22, m + 15), (m - 22, m + 15)]
            c.d.line(c.P(pts + [pts[0]]), fill=DARK, width=8 * SS, joint='curve')
        elif tok == 'cua':
            c.d.rectangle([(m - 18) * SS, (m - 18) * SS, (m + 18) * SS, (m + 18) * SS], outline=DARK, width=8 * SS)
        elif tok == 'cir':
            c.d.ellipse([(m - 20) * SS, (m - 20) * SS, (m + 20) * SS, (m + 20) * SS], outline=DARK, width=8 * SS)
        else:
            c.texto(m, m + 3, tok, 52, DARK)
        return c.fin()
    return mk(('chip', tok, col, r), f)


def plus():
    return mk('plus', lambda: R.rich('+', R.F('title', 64), 200))


def etiqueta(txt, col):
    return mk(('et', txt, col), lambda: R.pill(txt, R.F('800', 30), fg=DARK, bg=col, gradient=False, padx=20, pady=6))


def combo(fr, t, cx, plat, toks, col, t0, press=()):
    """Etiqueta de consola arriba y botones abajo. press = tiempos en que los botones 'se aprietan'."""
    p = pr(t, t0, .3)
    if p <= 0: return
    a = cl(p * 3); k0 = .5 + .5 * eb(p)
    R.put(fr, etiqueta(plat, col), cx, 650, k0, k0, alpha=a, anchor=(etiqueta(plat, col).width / 2, etiqueta(plat, col).height / 2))
    ims = [plus() if x == '+' else chip(x, col) for x in toks]
    gap = 12
    tw = sum(im.width for im in ims) + gap * (len(ims) - 1)
    x = cx - tw / 2
    k = 1.
    for tp in press:
        q = pr(t, tp, .22)
        if 0 < q < 1: k = 1 - .18 * math.sin(math.pi * q)
    for im in ims:
        kk = k0 * (k if im is not plus() else 1)
        R.put(fr, im, x + im.width / 2, 728, kk, kk, alpha=a, anchor=(im.width / 2, im.height / 2))
        x += im.width + gap


def controles(fr, t, ps, xb, press=()):
    combo(fr, t, 290, 'PS5', ps, PS_COL, .12, press)
    combo(fr, t, 790, 'XBOX', xb, XB_COL, .24, press)
    d = ImageDraw.Draw(fr)
    if t > .2: d.line([(540, 640), (540, 770)], fill=(255, 241, 234, int(120 * cl((t - .2) * 4))), width=4)


# ------------------------------------------------------------------ personajes
def gus(fr, x, sc=.64, turista=True, **k):
    k.setdefault('prenda', 'turista' if turista else None)
    E.GU(fr, x, k.pop('y', G), sc, **k)


def flami(fr, x, sc=.64, **k):
    E.FL(fr, x, k.pop('y', G), sc, flip=True, **k)


def coche(fr, x, y=G, sc=.6, rot=0., anchor=(380, 320), vib=0.):
    R.put(fr, R.spr('coche', 0., 0, 0.), x + vib, y, sc, sc, rot, anchor=anchor)


def sombra(fr, x, y, w, a=90):
    ov = Image.new('RGBA', (int(w), 40), (0, 0, 0, 0))
    ImageDraw.Draw(ov).ellipse((0, 0, int(w) - 1, 39), fill=(20, 10, 40, a))
    R.comp(fr, ov, int(x - w / 2), int(y - 20))


def golpe(fr, txt, x, y, t, t0, size=90, rot=-6):
    p = pr(t, t0, .25)
    if p <= 0: return
    im = E.sfx(txt, size)
    R.put(fr, im, x, y, .4 + .6 * eb(p), .4 + .6 * eb(p), rot + math.sin(t * 12) * 3, alpha=cl(p * 3), anchor=(im.width / 2, im.height / 2))


# ================================================================== GANCHO
def c_hook(s):
    D = s['dur']; sw = max(1.7, D * .46)
    def draw(fr, t):
        if t < sw:
            E.titulo(fr, t, 'JUEGAS COMO *TURISTA*', 100, 548)
            quita = sw * .5
            # Gus de turista peleando con el control
            gx = 330
            gus(fr, gx, .74, emo='nervioso' if t < quita else 'asombro', boca=0 if t < quita else 1., pose='agarra', brazos=1., mira=(0, 1), sy=.74 * idle(t, 14, .03))
            # mapa al revés bajo el brazo
            R.put(fr, mk('mapa', mapa), gx - 120, G - 250, .8, .8, rot=-12 + math.sin(t * 5) * 4, anchor=(95, 70))
            # control que se le resbala
            wob = math.sin(t * 13) * 22
            R.put(fr, S('gamepad'), gx + 125, G - 255 + math.sin(t * 9) * 8, .5, .5, rot=wob + (180 if int(t * 2.5) % 3 == 2 else 0), anchor=(150, 95))
            # sombrero: puesto, y Flami se lo quita
            sx_, sy_ = gx + (240 - 220) * .74, G + (138 - 590) * .74 - 6
            hp = pr(t, quita, .55)
            if hp <= 0:
                R.put(fr, mk('sombrero', sombrero_turista), sx_, sy_, .74, .74, anchor=(150, 118))
            elif hp < 1:
                R.put(fr, mk('sombrero', sombrero_turista), sx_ + 420 * eo(hp), sy_ - 160 * math.sin(math.pi * hp), .74, .74, rot=-hp * 200, alpha=1 - hp * .6, anchor=(150, 118))
            for i in range(2):
                u = pr(t, .35 + i * .25, .3)
                if u > 0: R.put(fr, S('signo', '?', 110, GOLD), gx - 60 + i * 120, 820 + math.sin(t * 4 + i) * 10, eb(u), eb(u), rot=10 - i * 20, anchor=(50, 66))
            # Flami lo mira con los lentes abajo
            fx = 900 - 160 * eo(pr(t, quita - .2, .3))
            flami(fr, fx, .68, emo='enojo' if t < quita else 'guino', gafas=0, boca=0 if t < quita else .4, cuello=.3, ala='senala' if t > quita - .2 else 'cadera', sy=.68 * idle(t, 5))
        else:
            tt = t - sw
            E.titulo(fr, tt, '5 CONTROLES *OCULTOS*', 88, 520)
            R.anim_in(fr, E.pil('PS5', 44, bg=PS_COL), 410, 712, tt, .1, 'pop', .25)
            R.anim_in(fr, E.pil('XBOX', 44, fg=DARK, bg=XB_COL), 640, 712, tt, .2, 'pop', .25)
            for i in range(5):
                u = pr(tt, .25 + i * .1, .3)
                if u > 0: R.put(fr, S('numero', i + 1, 30, ORANGE), 300 + i * 120, 805, eb(u), eb(u), anchor=(34, 34))
            if tt > .5:
                k = 1 + .06 * math.sin(tt * 9)
                im = E.pilg('GUÁRDALO', 56, 40, 16)
                p = pr(tt, .5, .3)
                R.put(fr, im, 615, 905, (.4 + .6 * eb(p)) * k, (.4 + .6 * eb(p)) * k, rot=-4, alpha=cl(p * 3), anchor=(im.width / 2, im.height / 2))
            # Gus ya al volante
            R.put(fr, S('volante', 34), 370, G - 230, 2.6, 2.6, rot=math.sin(tt * 6) * 20, anchor=(39, 39))
            gus(fr, 250, .66, emo='asombro' if tt < .6 else 'feliz', boca=.6, pose='agarra', brazos=1., sy=.66 * idle(t, 10, .03))
            flami(fr, 900, .66, emo='feliz', gafas=1, cuello=.3, ala='arriba', lente='estrella', sy=.66 * idle(t, 6))
        if sw - .08 < t < sw + .22:
            E.rect(fr, (0, 300, R.W, 1250), (255, 241, 234, int(130 * cl(1 - abs(t - sw - .04) / .15))))
    return draw


# ================================================================== 1 · MOTOR PRENDIDO
def c_motor(s):
    D = s['dur']
    def draw(fr, t):
        E.titulo(fr, t, '1 · MOTOR *PRENDIDO*', 92, 548)
        controles(fr, t, ['tri', 'tri'], ['Y', 'Y'], press=(.45, .7))
        cx = 600; vib = math.sin(t * 55) * 3
        sombra(fr, cx, G + 4, 430)
        # humito del escape
        for k in range(5):
            u = (t * 1.1 + k * .2) % 1
            R.put(fr, S('nube_polvo', 46), cx - 180 - u * 140, G - 40 - u * 120, .5 + u * .8, .5 + u * .8, alpha=(1 - u) * .85, anchor=(69, 46))
        coche(fr, cx, vib=vib, y=G + abs(math.sin(t * 30)) * 2)
        # notas musicales
        for k in range(4):
            u = (t * .8 + k * .25) % 1
            R.put(fr, S('nota', [PINK, ORANGE, GOLD, (194, 89, 255)][k], k % 2 == 0), cx - 60 + k * 50 + math.sin(u * 7 + k) * 30, 1010 - u * 230, .9, .9, rot=math.sin(u * 6 + k) * 18, alpha=1 - u, anchor=(35, 50))
        # Gus se baja de un salto
        p = pr(t, .75, .55)
        gxx = 520 - 340 * eo(p); gyy = G - 140 * math.sin(math.pi * p) if p < 1 else G
        if p > 0:
            gus(fr, gxx, .6, y=gyy, emo='asombro' if p < 1 else 'feliz', boca=.7, pose='celebra' if p < 1 else 'senala', brazos=1., flip=False, sy=.6 * idle(t, 9, .03), rot=-14 * math.sin(math.pi * p))
            if p >= 1: R.pop_burbuja(fr, E.bub('¡Sigue sonando!', 0, 48), 400, 985, t, .75 + .6)
        flami(fr, 945, .62, emo='feliz', gafas=1, cuello=.35 + .3 * math.sin(t * 8), ala='arriba' if int(t * 3) % 2 else 'reposo', sy=.62 * idle(t, 8, .03))
        E.sello(fr, t, max(1.4, D - .9), 620, 830, .7)
    return draw


# ================================================================== 2 · VOLTEAR
def c_voltear(s):
    D = s['dur']
    def draw(fr, t):
        E.titulo(fr, t, '2 · *VOLTEA* TU COCHE', 92, 548)
        controles(fr, t, ['L3', '+', 'cua'], ['LS', '+', 'X'], press=(.5,))
        cx = 590
        p = pr(t, .7, .7)
        rot = 180 + 180 * eb(p)
        lift = 150 * math.sin(math.pi * cl(p * 1.2))
        sombra(fr, cx, G + 4, 430 - lift * .8)
        coche(fr, cx, y=G - 95 - lift, rot=rot, anchor=(380, 180))
        if p <= 0:
            for k in range(3):
                u = (t * 1.4 + k * .33) % 1
                R.put(fr, S('nube_polvo', 46), cx - 120 + k * 120, G - 20 - u * 60, .5, .5, alpha=(1 - u) * .6, anchor=(69, 46))
        if p > .9: E.poof(fr, cx, G - 30, t, .7 + .65)
        golpe(fr, '[¡TOING!]', 720, 850, t, .75, 80, 8)
        push = eo(pr(t, .15, .4))
        gus(fr, 175 + 90 * push - 40 * eo(pr(t, .7, .3)), .62, emo='concentrado' if t < .75 else 'feliz', boca=0 if t < .75 else .7,
            pose='empuja' if t < 1.2 else 'celebra', brazos=1., sudor=t < .75, sy=.62 * idle(t, 12, .03), rot=-6 * push * (1 if t < .75 else 0))
        flami(fr, 955, .6, emo='asombro' if t < 1.2 else 'feliz', boca=.8 if t < 1.2 else .3, gafas=1, cuello=.3, ala='abre' if t < 1.2 else 'arriba', sy=.6 * idle(t, 6))
        E.sello(fr, t, max(1.5, D - .9), 540, 850, .75)
    return draw


# ================================================================== 3 · CÁMARA LENTA
def c_lenta(s):
    D = s['dur']
    def draw(fr, t):
        E.titulo(fr, t, '3 · *CÁMARA LENTA*', 96, 548)
        controles(fr, t, ['L3', '+', 'R3'], ['LS', '+', 'RS'], press=(.3,))
        sl = pr(t, .35, .35)
        if sl > 0: E.rect(fr, (0, 790, R.W, 1250), (122, 63, 191, int(70 * sl)))
        ang = 40 + 300 * t if t < .35 else 40 + 300 * .35 + 25 * (t - .35)
        rk = eb(pr(t, .2, .35))
        R.put(fr, reloj_c(int(ang) // 3 * 3), 830, 940, .75 * rk, .75 * rk, anchor=(130, 130))
        # Gus cayendo en cámara lenta (con estela)
        fall = cl((t - .3) / max(.8, D - .6))
        y0 = G - 150
        for g in (3, 2, 1, 0):
            u = cl(fall - g * .06)
            yy = y0 + (G - y0) * u; rr = -40 + 30 * u
            gus(fr, 480, .52, y=yy, emo='asombro', boca=1., pose='orejas', brazos=1., rot=rr, alpha=1. if g == 0 else .18)
        golpe(fr, '[LEEENTO...]', 250, 1000, t, .5, 60, -4)
        flami(fr, 960, .58, emo='asombro', boca=.6, gafas=0, cuello=.2, ala='abre', sy=.58)
        E.sello(fr, t, max(1.6, D - .9), 540, 850, .75)
    return draw


def reloj_c(a):
    return mk(('reloj', a), lambda: reloj(a))


# ================================================================== 4 · SENTARTE
def c_sentar(s):
    D = s['dur']
    def draw(fr, t):
        E.titulo(fr, t, '4 · *SIÉNTATE*', 100, 548)
        sit = min(1.1, D * .45)
        controles(fr, t, ['cir'], ['B'], press=(sit - .15,))
        bx = 600
        R.put(fr, mk('banca', banca), bx, G + 6, .95, .95, anchor=(170, 186))
        if t < sit:
            w = eo(pr(t, 0, sit))
            gus(fr, 130 + (bx - 40 - 130) * w, .6, y=G - hop(t, 12, 14), emo='feliz', boca=.3, pose='bajos', sy=.6 * idle(t, 12, .03))
        else:
            q = eb(pr(t, sit, .3))
            gus(fr, bx - 30, .6, y=G - 70 - 20 * (1 - q), emo='feliz', boca=.6, pose='cadera', brazos=1., recorte=True, sy=.6 * (1 - .06 * math.sin(math.pi * pr(t, sit, .25))))
            R.pop_burbuja(fr, E.bub('¡Ahhh!', 0, 50), bx - 40, G - 345, t, sit + .2)
        flami(fr, 950, .62, emo='feliz', gafas=1, cuello=.3, ala='senala' if t > sit else 'reposo', sy=.62 * idle(t, 5))
        E.sello(fr, t, max(1.4, D - .9), 840, 860, .7)
    return draw


# ================================================================== 5 · PORTAZO
def c_portazo(s):
    D = s['dur']
    def draw(fr, t):
        E.titulo(fr, t, '5 · *PORTAZO*', 100, 548)
        controles(fr, t, ['cua'], ['X'], press=(.55,))
        cx = 470; sc = .6
        sombra(fr, cx, G + 4, 430)
        hit = .7
        # Gus adentro (se le ve la cabeza) hasta que sale volando
        if t < hit:
            gus(fr, cx + 10, .45, y=G - 70, emo='nervioso', recorte=True)
        coche(fr, cx, sc=sc, vib=math.sin(t * 60) * 4 if hit < t < hit + .3 else 0)
        # puerta: cerrada en el coche y luego abierta de golpe
        dx, dy = cx + (330 - 380) * sc, G + (215 - 320) * sc
        if t < hit:
            R.put(fr, mk('puerta', puerta), dx, dy, sc, sc, anchor=(85, 75))
        else:
            p = eo(pr(t, hit, .18))
            R.put(fr, mk('puerta', puerta), dx + 150 * p, dy + 10 * p, sc * (1 - .55 * p), sc, rot=-8 * p, anchor=(85, 75))
            golpe(fr, '[¡PUM!]', 610, 905, t, hit, 100, 6)
            f = pr(t, hit, .9)
            if f < 1:
                gus(fr, cx - 420 * eo(f), .6, y=G - 60 - 330 * math.sin(math.pi * f), emo='grito', boca=1., pose='orejas', brazos=1., rot=f * 360)
            else:
                gus(fr, 110, .6, y=G, emo='nervioso', boca=.3, pose='encoge', brazos=1., sy=.6 * idle(t, 14, .03))
                R.put(fr, K_estrellas(t), 120, G - 420, 1., 1., anchor=(110, 45))
        flami(fr, 870 - 60 * eo(pr(t, hit - .25, .2)), .62, emo='guino' if t > hit else 'feliz', boca=.4, gafas=1, cuello=.3, ala='senala' if t > hit - .25 else 'reposo', sy=.62 * idle(t, 5))
        R.anim_in(fr, E.pil('EN EL COCHE', 36, bg=(74, 38, 120)), 540, 815, t, .4, 'pop', .25)
        E.sello(fr, t, max(1.4, D - .8), 905, 835, .6)
    return draw


def K_estrellas(t):
    import caricatura as K
    return K.estrellas_mareo(t)


# ================================================================== CIERRE
def c_cierre(s):
    nombres = (('MOTOR PRENDIDO', ['tri', 'tri']), ('VOLTEAR', ['L3', 'cua']), ('CÁMARA LENTA', ['L3', 'R3']), ('SENTARTE', ['cir']), ('PORTAZO', ['cua']))
    def draw(fr, t):
        E.titulo(fr, t, '¿CUÁL NO *CONOCÍAS*?', 84, 540)
        for i, (n, _) in enumerate(nombres):
            u = eo(pr(t, .1 + i * .12, .3))
            if u <= 0: continue
            y = 680 + i * 74; xo = (1 - u) * 400
            R.put(fr, S('numero', i + 1, 26, ORANGE), 440 + xo, y, 1, 1, alpha=u, anchor=(30, 30))
            im = E.pil(n, 34, bg=(74, 38, 120))
            R.put(fr, im, 482 + xo, y, 1, 1, alpha=u, anchor=(0, im.height / 2))
            E.sello(fr, t, .9 + i * .3, 482 + im.width + 36, y, .4)
        gus(fr, 160, .6, turista=False, emo='feliz', boca=.6, pose='celebra' if int(t * 2.5) % 2 else 'saluda', brazos=.8, sy=.6 * idle(t, 9, .03))
        # el disfraz sale volando
        p = pr(t, 0, .6)
        if p < 1:
            R.put(fr, mk('sombrero', sombrero_turista), 170 - 200 * p, G - 420 - 200 * math.sin(math.pi * p), .6, .6, rot=-300 * p, alpha=1 - p, anchor=(150, 118))
        flami(fr, 960, .6, emo='feliz', gafas=1, cuello=.3, ala='senala', sy=.6 * idle(t, 5))
        R.pop_burbuja(fr, mk('bcierre', lambda: R.burbuja('¿Cuál no conocías?', 0, 240, 46)), 230, G - 380, t, .6)
    return draw
