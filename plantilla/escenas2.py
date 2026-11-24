"""Escenas de caricatura 2 (24-nov-2026): Neza (n_*) y 5 ajustes (a_*). Mudo; los tiempos salen de "dur".
render.py pone en R su propio módulo (put, burbuja, rich, comp...)."""
import math
from PIL import Image, ImageDraw
import caricatura2 as C
import caricatura as K
from caricatura2 import PINK, ORANGE, CREAM, GOLD, CYAN, RED

R = None
_c = {}
G = 1165                                  # piso de los personajes (los subtítulos quedan debajo)


def S(kind, *a):
    k = (kind,) + a
    if k not in _c: _c[k] = getattr(C, kind)(*a)
    return _c[k]


def cl(x, a=0., b=1.): return max(a, min(b, x))
def eo(x): return R.ease_out(x)
def eb(x): return R.ease_back(x)
def pr(t, s, d=.4): return R.prog(t, s, d)
def idle(t, v=6., a=.02): return 1 + a * math.sin(t * v)
def hop(t, v=11., a=16.): return abs(math.sin(t * v)) * a


def FL(fr, x, y, sc=.7, emo='feliz', boca=0., gafas=1, cuello=0., ala='reposo', mira=(0, 0), sudor=0, lente='', rot=0., flip=False, recorte=False, sy=None, alpha=1.):
    im = S('flami2', emo, round(boca * 3) / 3, round(gafas), round(cuello * 3) / 3, ala, (round(mira[0]), round(mira[1])), sudor, lente)
    if recorte: im = im.crop((0, 0, im.width, 450))
    R.put(fr, im, x, y, sc, sy or sc, rot, flip, alpha, anchor=(220, 450 if recorte else 610))


def GU(fr, x, y, sc=.7, emo='nervioso', boca=0., pose='bajos', brazos=0., mira=(0, 0), parp=0., sombrero=None, prenda=None, rot=0., flip=False, recorte=False, sy=None, alpha=1., sudor=None):
    im = S('gus2', emo, round(boca * 3) / 3, pose, round(brazos * 4) / 4, (round(mira[0]), round(mira[1])), round(parp * 2) / 2, sombrero, prenda, sudor, '')
    if recorte: im = im.crop((0, 0, im.width, 430))
    R.put(fr, im, x, y, sc, sy or sc, rot, flip, alpha, anchor=(220, 430 if recorte else 590))


def clip(fr, rect, fn):
    x0, y0, x1, y1 = [int(v) for v in rect]
    tmp = Image.new('RGBA', (max(1, x1 - x0), max(1, y1 - y0)), (0, 0, 0, 0))
    fn(tmp, -x0, -y0)
    R.comp(fr, tmp, x0, y0)


_t = {}
def titulo(fr, t, txt, size=96, y=548, t0=.05):
    k = (txt, size)
    if k not in _t: _t[k] = R.rich(txt, R.F('title', size), R.W - 2 * R.MX)
    R.anim_in(fr, _t[k], R.CX, y, t, t0, 'up')


def tira(fr, im, y_bottom, off, vel):
    w = im.width; x0 = -int((off * vel) % w)
    R.comp(fr, im, x0, int(y_bottom - im.height)); R.comp(fr, im, x0 + w, int(y_bottom - im.height))


def rect(fr, box, col):
    ov = Image.new('RGBA', (box[2] - box[0], box[3] - box[1]), col); R.comp(fr, ov, box[0], box[1])


def bub(txt, cola=0, size=64):
    k = ('b', txt, cola, size)
    if k not in _c: _c[k] = R.burbuja(txt, cola, 560 if size >= 60 else 440, size)
    return _c[k]


def sfx(txt, size=100):
    k = ('s', txt, size)
    if k not in _c: _c[k] = R.sfx(txt, size)
    return _c[k]


def pop(fr, im, x, y, t, t0, dur=.3, rot=0., alpha=1.):
    p = pr(t, t0, dur)
    if p <= 0: return
    sc = .3 + .7 * eb(p)
    R.put(fr, im, x, y, sc, sc, rot, False, cl(p * 3) * alpha, anchor=(im.width / 2, im.height / 2))


def destello(fr, x, y, t, ph=0., r=1.):
    u = (t * 2.2 + ph) % 1
    sc = r * math.sin(math.pi * u)
    if sc > .05: R.put(fr, S('destellos', 34), x, y, sc, sc, u * 90, False, 1., anchor=(39, 39))


def lineas_vel(fr, t, y0, y1, n=9, alpha=150):
    d = ImageDraw.Draw(fr)
    for k in range(n):
        u = (t * 2.6 + k * .37) % 1
        y = y0 + (k * 97 % (y1 - y0))
        x = R.W - u * (R.W + 420)
        d.line([(x, y), (x + 260, y)], fill=(255, 241, 234, alpha), width=7)


# ================================================================== NEZA 1: gancho
def n_hook(s):
    def draw(fr, t):
        titulo(fr, t, 'GTA VI EN *NEZA*', 104, 540)
        bx, by = 540, 905
        sw = 1.0 + .015 * math.sin(t * 6)
        cambio = 1.0
        base = 'isla_leonida' if t < cambio else 'mapa_neza_base'
        im = S(base, 900, 520)
        pe = pr(t, 0, .35)
        R.put(fr, im, bx, by, sw * (.6 + .4 * eb(pe)), sw * (.6 + .4 * eb(pe)), 0, False, cl(pe * 3), anchor=(450, 260))
        ox, oy = bx - 450, by - 260
        if t < cambio:
            for i, (x, y, kind) in enumerate(((180, 380, 'p'), (300, 330, 't'), (390, 290, 't'), (700, 340, 'p'), (790, 420, 'p'), (560, 380, 't'))):
                u = eb(pr(t, .15 + i * .1, .35)) * (1 - eo(pr(t, cambio - .15, .15)))
                if u <= 0: continue
                if kind == 'p': R.put(fr, S('palmera', 0.) if False else R.spr('palmera', 0.), ox + x, oy + y, .3 * u, .3 * u, anchor=(190, 690))
                else: R.put(fr, S('torre_neon', 90, 260, (194, 89, 255)), ox + x, oy + y, .75 * u, .75 * u, anchor=(45, 258))
        else:
            tt = t - cambio
            els = [('bordo', 240, 400), ('a', 640, 360), ('a', 780, 340), ('t', 170, 470), ('t', 380, 470), ('t', 600, 480), ('t', 790, 480)]
            for i, (kind, x, y) in enumerate(els):
                u = eb(pr(tt, .05 + i * .07, .35))
                if u <= 0: continue
                if kind == 'bordo': R.put(fr, S('bordo_strip', 1080, 300).crop((40, 60, 560, 300)), ox + x, oy + y, .9 * u, .9 * u, anchor=(260, 238))
                elif kind == 'a': R.put(fr, S('antena_torre', 300, True), ox + x, oy + y, .8 * u, .8 * u, anchor=(55, 294))
                else: R.put(fr, S('toldo', [(255, 107, 139), (255, 179, 107), (110, 190, 230), (130, 210, 150)][i % 4], (255, 241, 234), 170, 150), ox + x, oy + y, .85 * u, .85 * u, anchor=(85, 144))
            # luz de la antena que parpadea
            if int(t * 4) % 2 == 0:
                for x in (640, 780): R.put(fr, S('destellos', 26), ox + x, oy + 355 - (0 if x == 640 else 20) - 230, .9, .9, anchor=(31, 31))
        # destello del cambio (glitch)
        if cambio - .08 < t < cambio + .3:
            a = 1 - abs(t - (cambio + .05)) / .3
            rect(fr, (0, 300, R.W, 1250), (255, 241, 234, int(150 * cl(a))))
        # personajes
        pf = pr(t, .0, .5)
        FL(fr, 175 + (1 - eo(pf)) * -200, G, .72, 'feliz' if t < cambio + .2 else 'asombro', boca=0 if t < cambio + .2 else 1., gafas=1 if t < cambio + .2 else 0,
           cuello=.3 if t > .5 else 0, ala='senala' if t > .4 else 'reposo', sy=.72 * idle(t, 5))
        gu = pr(t, .1, .45)
        GU(fr, 905 + (1 - eo(gu)) * 220, G, .7, 'feliz' if t < cambio else 'asombro', boca=0 if t < cambio else 1., pose='bajos' if t < cambio else 'orejas', brazos=cl(pr(t, cambio, .25)),
           mira=(-1, 0), flip=True, sy=.7 * idle(t, 14, .03))
        if t > cambio + .15:
            R.pop_burbuja(fr, bub('¿¡Neza!?', 0), 800, G - 420, t, cambio + .15)
    return draw


# ================================================================== NEZA 2: persecución
def n_persec(s):
    D = s['dur']; sc = .8
    casas = S('casas_neza', 1, 1080, 340, False); bordo = S('bordo_strip', 1080, 300, False)
    def draw(fr, t):
        titulo(fr, t, 'PERSECUCIÓN EN *MEXIBÚS*', 92, 548)
        boost = cl((t - 3.0) / .4) * (1 - cl((t - 5.0) / .6))
        dist = 280 * t + 260 * (cl(t - 3.0, 0, 2.0) ** 1) * 1.0 + 80 * cl(t - 5, 0, 3)
        shx, shy = math.sin(t * 47) * (2 + 3 * boost), math.sin(t * 39) * (2 + 3 * boost)
        lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0))
        tira(lay, bordo, 830, dist, .05)
        tira(lay, casas, 1010, dist, .22)
        for k, xs in enumerate((140, 520, 900)):
            x = (xs - dist * .22) % (R.W + 300) - 150
            R.put(lay, S('antena_torre', 300 + 40 * (k % 2), True), x, 1000, .8, .8, anchor=(55, 280))
        rect(lay, (0, 1008, R.W, 1056), (84, 52, 140, 245))
        for k, xs in enumerate((60, 520, 960, 1380)):
            x = (xs - dist * .6) % (R.W + 500) - 200
            R.put(lay, S('toldo', [(255, 107, 139), (110, 190, 230), (255, 179, 107), (130, 210, 150)][k % 4], (255, 241, 234), 170, 150), x, 1052, .95, .95, anchor=(85, 148))
        rect(lay, (0, 1056, R.W, 1200), (42, 20, 72, 242)); rect(lay, (0, 1056, R.W, 1066), (122, 63, 191, 255))
        d = ImageDraw.Draw(lay)
        for x in range(-140 + int(-dist) % 220, R.W, 220): d.rectangle((x, 1130, x + 110, 1140), fill=(255, 241, 234, 170))
        # tlacuache
        gap = 28 * eo(pr(t, 0, D)) 
        rx = 830 - gap * 3 + (1 - eo(pr(t, 0, 1.2))) * 120
        fase = int(t * 15) % 12
        susto = 'susto'
        R.put(lay, S('tlacuache', fase, susto, -1, 0), rx, 1170 - abs(math.sin(t * 15 * math.pi / 6)) * 10, .62, .62, anchor=(190, 410))
        for k, (dx, dy) in enumerate(((-28, -8), (36, -2), (8, 12))): destello(lay, rx + dx - 20, 1150 + dy, t, k * .33, 1.0)
        if t > 1.6:
            sw_ = math.sin(t * 9) * 8
            R.put(lay, S('etiqueta_precio', '$500'), rx - 40, 1048, .7 * eb(pr(t, 1.6, .3)), .7 * eb(pr(t, 1.6, .3)), rot=sw_, anchor=(10, 12))
        # autobús
        enter = -520 * (1 - eo(pr(t, 0, .9)))
        bx = 324 + enter + (math.sin(t * 6) * 4)
        jump = 0.
        if 5.0 < t < 5.7: jump = -70 * math.sin(math.pi * (t - 5.0) / .7)
        by = 1178 + jump + math.sin(t * 18) * 2.5
        f = lambda cx, cy: (bx + (cx - 500) * sc, by + (cy - 330) * sc)
        inter, body = S('mexibus_capas')
        R.put(lay, inter, bx, by, sc, sc, anchor=(500, 330))
        # Flami al volante
        fx, fy = f(905, 250); x0, y0 = f(846, 56); x1, y1 = f(972, 182)
        emo = 'enojo' if t < 3 else ('feliz' if t < 5 else 'asombro')
        def fl_in(L, ox, oy):
            FL(L, fx + ox, fy + oy, sc * .4, emo, boca=1. if (3.2 < t < 5) else 0., gafas=1, cuello=.2, recorte=True, sy=sc * .4 * (1 + .03 * math.sin(t * 20)))
            R.put(L, S('volante', 34), f(905, 172)[0] + ox, f(905, 172)[1] + oy, sc * 1.2, sc * 1.2, anchor=(39, 39))
        clip(lay, (x0, y0, x1, y1), fl_in)
        R.put(lay, body, bx, by, sc, sc, anchor=(500, 330))
        for cx in (210, 780): R.put(lay, S('rueda', 64), f(cx, 294)[0], f(cx, 294)[1], sc, sc, rot=-(t * 720) % 360, anchor=(70, 70))
        # Gus colgado de la ventana
        gx, gy = f(503, 178); a0, b0 = f(360, -140); a1, b1 = f(650, 178)
        gemo = 'grito' if (1.0 < t < 5 or t > 6) else 'nervioso'
        def gu_in(L, ox, oy):
            GU(L, gx + ox, gy + oy, sc * .44, gemo, boca=.9 if gemo == 'grito' else 0., pose='celebra', brazos=.5 + .5 * math.sin(t * 9), mira=(1, 0),
               rot=-12 + math.sin(t * 12) * 5, recorte=True, sombrero=None)
        clip(lay, (a0, b0, a1, b1), gu_in)
        # polvo y escape
        for k in range(4):
            u = (t * 1.8 + k * .25) % 1
            R.put(lay, S('nube_polvo', 46), f(30, 320)[0] - u * 150, 1160 - u * 50, (.45 + u) * .8, (.45 + u) * .8, alpha=(1 - u) * .8, anchor=(69, 46))
        if boost > 0: lineas_vel(lay, t, 700, 1000, 10, int(170 * boost))
        if 5.0 < t < 5.9: R.put(lay, sfx('[¡BACHE!]', 88), 540, 800, 1, 1, rot=-6, alpha=cl(pr(t, 5.0, .12)) * (1 - pr(t, 5.5, .3)), anchor=(sfx('[¡BACHE!]', 88).width / 2, sfx('[¡BACHE!]', 88).height / 2))
        # burbujas
        sx, sy = 0, 0
        R.pop_burbuja(lay, bub('¡Ahí va el de la riñonera!', 0), gx - 10, gy - 150, t, 1.1, 3.0)
        R.pop_burbuja(lay, bub('¡Sujétate, Gus!', 0), f(905, 40)[0], f(905, 40)[1] - 10, t, 3.3, 5.0)
        R.pop_burbuja(lay, bub('¡Ya casi!', 0), gx - 10, gy - 150, t, 6.2)
        fr.alpha_composite(lay.crop((0, 0, R.W, R.H)), (int(shx), int(shy)) if False else (0, 0)) if False else R.comp(fr, lay, int(shx), int(shy))
    return draw


# ================================================================== NEZA 3: El Escala
def n_escala(s):
    def draw(fr, t):
        rect(fr, (0, 0, R.W, R.H), (14, 8, 34, 120))                         # noche
        titulo(fr, t, 'MISIÓN: EL *ESCALA* UN MARTES', 82, 548)
        d = ImageDraw.Draw(fr)
        for i in range(26):
            x = (i * 211) % R.W; y = 330 + (i * 97) % 300
            a = int(120 + 100 * math.sin(t * 3 + i)); d.ellipse((x - 3, y - 3, x + 3, y + 3), fill=(255, 241, 234, max(0, a)))
        lu = pr(t, 0, .6)
        R.put(fr, S('luna', 74), 190, 780 - 30 * (1 - eo(lu)), 1, 1, alpha=eo(lu), anchor=(84, 84))
        fe = eo(pr(t, 0, .5))
        R.put(fr, S('fachada', 860, 470), 540, 1170, 1, 1, alpha=fe, anchor=(430, 470))
        # letrero con parpadeo
        flick = 1 if (t < .9 or (int(t * 14) % 7) != 3) else 0
        R.put(fr, S('letrero_escala', 0 if flick else 1), 540 + (160 if False else 0), 800, .78 * eb(pr(t, .2, .4)) if t > .2 else 0.01, .78 * eb(pr(t, .2, .4)) if t > .2 else 0.01, anchor=(330 + 0, 100) if False else (S('letrero_escala', 0 if flick else 1).width / 2, S('letrero_escala', 0 if flick else 1).height / 2))
        # fila de compas
        for k in range(6):
            u = eo(pr(t, .3 + k * .1, .35))
            x = 300 + k * 74 + (1 - u) * -240
            scl = .95 + (k % 3) * .04
            R.put(fr, S('compa', k), x, G + 5 - abs(math.sin(t * 5 + k)) * 6, scl, scl, anchor=(75, 320), alpha=u)
        # calendario cae
        cp = pr(t, 1.1, .5)
        if cp > 0:
            R.put(fr, S('calendario', 'MAR'), 905, 960 + (1 - eo(cp)) * -420 + math.sin(t * 5) * 4, .8 * (.8 + .2 * eb(cp)), .8 * (.8 + .2 * eb(cp)), rot=-8 + math.sin(t * 4) * 3, anchor=(135, 155))
        # Flami relajado (derecha) y Gus confundido
        FL(fr, 760, G, .66, 'feliz', boca=0, gafas=1, cuello=.3 + .1 * math.sin(t * 3), ala='sostiene', sy=.66 * idle(t, 4))
        GU(fr, 1020 if False else 960 - 700 * 0 + 0, G, 0.0001) if False else None
        sh = pr(t, .5, .4)
        GU(fr, 110, G, .66, 'confuso', pose='encoge', brazos=eo(pr(t, 1.2, .3)) * (1 if t > 1.2 else 0), mira=(math.sin(t * 3) > 0 and 1 or -1, 0), flip=False, sy=.66 * idle(t, 5, .02))
        for i in range(3):
            u = pr(t, 1.5 + i * .25, .3)
            if u > 0: R.put(fr, S('signo', '?', 120, (255, 224, 138)), 100 + i * 40, 770 - i * 30 - math.sin(t * 4 + i) * 8, eb(u), eb(u), rot=-10 + i * 10, anchor=(54, 72))
    return draw


# ================================================================== NEZA 4: vehículos
def n_vehic(s):
    casas = S('casas_neza', 3, 1080, 340, False)
    def draw(fr, t):
        titulo(fr, t, 'PESEROS · *COMBI TUNEADA*', 92, 548)
        lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0))
        dist = 220 * t
        tira(lay, casas, 1010, dist, .2)
        rect(lay, (0, 1010, R.W, 1056), (84, 52, 140, 245))
        rect(lay, (0, 1056, R.W, 1130), (42, 20, 72, 242))
        rect(lay, (0, 1130, R.W, 1210), (60, 170, 110, 240))               # ciclovía
        d = ImageDraw.Draw(lay)
        for x in range(-100 + int(-dist * 1.2) % 300, R.W, 300):
            d.ellipse((x, 1160, x + 36, 1196), outline=(255, 241, 234, 220), width=5); d.ellipse((x + 70, 1160, x + 106, 1196), outline=(255, 241, 234, 220), width=5)
            d.line([(x + 18, 1178), (x + 52, 1164), (x + 88, 1178)], fill=(255, 241, 234, 220), width=5)
        # pesero al fondo cruzando
        px = -400 + (t / s['dur']) * 1700
        R.put(lay, S('pesero'), px, 1100, .62, .62, anchor=(280, 290))
        for cx in (130, 430): R.put(lay, S('rueda', 44), px + (cx - 280) * .62, 1100 - 40 * .62, .62, .62, rot=-(t * 500) % 360, anchor=(50, 50))
        # combi
        ent = eo(pr(t, .3, .7)); cx0 = 560 + (1 - ent) * 700
        salto = abs(math.sin(t * 6.2)) * 30 * (1 if t > 1.2 else 0)
        cy0 = 1175 - salto
        cs = .98
        f = lambda x, y: (cx0 + (x - 320) * cs, cy0 + (y - 330) * cs)
        col = [PINK, (110, 230, 255), (255, 224, 138)][int(t * 3) % 3]
        R.put(lay, S('neon_suelo', col, 640), cx0, 1190, 1.05, .9, alpha=.85, anchor=(320, 75))
        inter, body = S('combi')
        R.put(lay, inter, cx0, cy0, cs, cs, anchor=(320, 330))
        wx, wy = f(400, 140); x0, y0 = f(330, 78); x1, y1 = f(470, 164)
        def fl_in(L, ox, oy):
            FL(L, wx + ox, wy + 40 + oy + math.sin(t * 12.4) * 7, cs * .4, 'feliz', boca=.5 + .5 * math.sin(t * 12.4), gafas=1, cuello=.4, recorte=True, lente='ondas' if int(t * 4) % 2 else '', rot=math.sin(t * 6.2) * 6)
        clip(lay, (x0, y0, x1, y1), fl_in)
        R.put(lay, body, cx0, cy0, cs, cs, anchor=(320, 330))
        for wxx in (150, 500): R.put(lay, S('rueda', 50), f(wxx, 282)[0], f(wxx, 282)[1] + salto * .0, cs, cs, rot=-(t * 400) % 360, anchor=(56, 56))
        # bocinas sobre el techo + conos que laten
        for k, bxx in enumerate((250, 380)):
            bx_, by_ = f(bxx, 48)
            R.put(lay, S('bocina', 150, 190), bx_, by_, cs * .62, cs * .62, anchor=(75, 190))
            pul = 1 + .16 * max(0, math.sin(t * 12.4 + k))
            R.put(lay, S('cono', 40), bx_, by_ - 190 * .62 * cs * .42, cs * .62 * pul, cs * .62 * pul, anchor=(44, 44))
            R.put(lay, S('cono', 40), bx_, by_ - 190 * .62 * cs * .87 + 0, cs * .62 * .6 * pul, cs * .62 * .6 * pul, anchor=(44, 44))
        # Gus en el techo cambia de cara
        gem = 'grito' if t < 1.9 else ('confuso' if t < 2.9 else 'feliz')
        GU(lay, f(480, 56)[0], f(480, 56)[1], .38, gem, boca=.7 if gem == 'grito' else .3 * (1 if gem == 'feliz' else 0), pose='orejas' if t < 2.9 else 'celebra', brazos=1. if t < 2.9 else .5 + .5 * math.sin(t * 12.4), flip=False, rot=math.sin(t * 6.2) * 6, sy=.38 * (1 + .03 * math.sin(t * 12.4)))
        # notas musicales
        for k in range(6):
            u = (t * .9 + k * .17) % 1
            R.put(lay, S('nota', [PINK, CYAN, GOLD][k % 3]), f(300, 40)[0] - 40 + k * 30 + math.sin(u * 8 + k) * 40, f(300, 40)[1] - 120 - u * 320, .9 - u * .3, .9 - u * .3, rot=math.sin(u * 7 + k) * 20, alpha=1 - u, anchor=(35, 50))
        R.comp(fr, lay, 0, 0)
        R.pop_burbuja(fr, bub('¡Más volumen!', 0), f(300, 40)[0] - 130, 800, t, 3.0) if t > 3.0 else None
    return draw


# ================================================================== NEZA 5: cierre
def n_cierre(s):
    def draw(fr, t):
        titulo(fr, t, '¿QUÉ *COLONIA*?', 108, 540)
        bx, by = 540, 900
        pe = eo(pr(t, 0, .4))
        R.put(fr, S('mapa_neza_base', 900, 520), bx, by, .6 + .4 * pe, .6 + .4 * pe, alpha=pe, anchor=(450, 260))
        pos = [(180, 150), (330, 250), (480, 140), (620, 300), (760, 190), (250, 380), (560, 420), (820, 370)]
        cols = [PINK, ORANGE, (110, 230, 255), (255, 224, 138), (194, 89, 255), PINK, (130, 210, 150), ORANGE]
        for i, (x, y) in enumerate(pos):
            t0 = .35 + i * .3
            u = pr(t, t0, .4)
            if u <= 0: continue
            drop = (1 - eo(u)) * -160
            R.put(fr, S('pin', cols[i], 70), bx - 450 + x, by - 260 + y + drop, eb(u), eb(u), anchor=(35, 90))
            r = pr(t, t0 + .3, .5)
            if 0 < r < 1:
                d = ImageDraw.Draw(fr); rr = 14 + 50 * r; cx, cy = bx - 450 + x, by - 260 + y
                d.ellipse((cx - rr, cy - rr * .5, cx + rr, cy + rr * .5), outline=(255, 241, 234, int(220 * (1 - r))), width=5)
        FL(fr, 175, G, .72, 'feliz', boca=.4, gafas=1, cuello=.3, ala='senala' if t > .3 else 'reposo', sy=.72 * idle(t, 5))
        gem = 'confuso' if t < 1.6 else 'feliz'
        GU(fr, 905, G, .7, gem, boca=0 if gem == 'confuso' else .6, pose='senala' if t > 2.2 else 'cadera', brazos=eo(pr(t, 2.2, .3)) if t > 2.2 else 0.6, flip=True, mira=(-1, 0), sy=.7 * idle(t, 5, .02))
        R.pop_burbuja(fr, bub('¿Qué colonia?', 0), 790, G - 415, t, .5)
        for i in range(2):
            u = pr(t, 1.0 + i * .3, .3)
            if u > 0: R.put(fr, S('signo', '?', 110, (255, 224, 138)), 960 - i * 60, 700 + math.sin(t * 4 + i) * 8, eb(u), eb(u), rot=10 - i * 14, anchor=(50, 66))
    return draw


# ================================================================== 5 AJUSTES
PURP = (122, 63, 191)
COS = dict(sombrero='charro', prenda='mexicano')


def pil(txt, size=44, fg=CREAM, bg=PURP, padx=28, pady=12):
    k = ('pil', txt, size, fg, bg)
    if k not in _c: _c[k] = R.pill(txt, R.F('800', size), fg=fg, bg=bg, gradient=False, padx=padx, pady=pady)
    return _c[k]


def pilg(txt, size=44, padx=30, pady=12):
    k = ('pilg', txt, size)
    if k not in _c: _c[k] = R.pill(txt, R.F('800', size), fg=R.BG, padx=padx, pady=pady)
    return _c[k]


def sello(fr, t, t0, x, y, sc=1.):
    p = pr(t, t0, .3)
    if p <= 0: return
    k = (2.4 - 1.4 * eo(p)) * sc
    R.put(fr, S('palomita', 60), x, y, k, k, rot=-12 * (1 - p), alpha=cl(p * 3), anchor=(65, 65))
    r = pr(t, t0 + .2, .35)
    if 0 < r < 1:
        d = ImageDraw.Draw(fr); rr = 60 * sc + 70 * r
        d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=(255, 241, 234, int(200 * (1 - r))), width=6)


def tablero(fr, t, cy=880, w=820, h=440, tit='AJUSTES', t0=0.):
    p = pr(t, t0, .35)
    R.put(fr, S('panel_menu', w, h, tit), 540, cy, .7 + .3 * eb(p), .7 + .3 * eb(p), alpha=cl(p * 3), anchor=(w / 2, h / 2))


def gusm(fr, x, **k):
    kw = dict(COS); kw.update(k)
    GU(fr, x, G, kw.pop('sc', .66), **kw)


def flm(fr, x, **k):
    FL(fr, x, G, k.pop('sc', .66), flip=True, **k)


def poof(fr, x, y, t, t0):
    u = pr(t, t0, .6)
    if u <= 0 or u >= 1: return
    for k in range(7):
        a = k * math.pi * 2 / 7
        R.put(fr, S('nube_polvo', 46), x + math.cos(a) * 130 * eo(u), y + math.sin(a) * 120 * eo(u), 1.1 * (.5 + u), 1.1 * (.5 + u), alpha=1 - u, anchor=(69, 46))
    destello(fr, x - 70, y - 90, t, 0, 1.4); destello(fr, x + 80, y - 40, t, .4, 1.1)


def a_hook(s):
    def draw(fr, t):
        titulo(fr, t, 'CONFIGURACIÓN DE *GRINGO*', 92, 548)
        cambio = 1.5
        tablero(fr, t, 880, 820, 440, 'AJUSTES · UNIDADES')
        post = t >= cambio
        q = .78 + .04 * math.sin(t * 8) if not post else .55 + .45 * math.exp(-(t - cambio) * 3) * math.cos((t - cambio) * 14) * .6
        if not post: q = eo(pr(t, .3, .6)) * .8 + .02 * math.sin(t * 9)
        pe = eb(pr(t, .2, .4))
        R.put(fr, S('velocimetro', round(q * 20) / 20, 'KM/H' if post else 'MPH'), 540, 1010, .92 * pe, .92 * pe, anchor=(240, 262))
        for k_, (x_, tx) in enumerate(((330, '°F'), (750, '°C'))):
            if (not post and k_ == 0) or (post and k_ == 1): R.anim_in(fr, pilg(tx, 40) if post else pil(tx, 40), x_, 770, t, .4 if not post else cambio + .1, 'pop', .25)
        # personajes
        if not post:
            gusm(fr, 170, sombrero='vaquero', prenda='gringo', emo='confuso', mira=(1, 0), pose='cadera', brazos=.6, sy=.66 * idle(t, 5), sc=.66)
        else:
            gusm(fr, 170, emo='feliz', boca=.6, pose='celebra', brazos=.5 + .5 * math.sin(t * 10), sy=.66 * idle(t, 12, .03))
        fx = 930 + (1 - eo(pr(t, .7, .6))) * 400
        flm(fr, fx, emo='feliz' if not post else 'amor', boca=.4, gafas=1, cuello=.3, ala='arriba' if post else 'sostiene', lente='estrella' if post else '', sy=.66 * idle(t, 5))
        poof(fr, 220, G - 220, t, cambio - .05)
        if cambio - .1 < t < cambio + .2: rect(fr, (0, 300, R.W, 1250), (255, 241, 234, int(120 * (1 - abs(t - cambio - .05) / .15))))
        R.pop_burbuja(fr, bub('¿¡Mph!?', 0, 56), 330, 800, t, .9, cambio - .05)
        R.pop_burbuja(fr, bub('¡Ya soy mexicano!', 0, 52), 340, 800, t, cambio + .25)
    return draw


def a_lista(s):
    nombres = ('UNIDADES', 'RETÍCULA', 'AVISOS', 'SUBTÍTULOS', 'MINIJUEGOS')
    def draw(fr, t):
        titulo(fr, t, '5 AJUSTES · PS5 · *GUÁRDALO*', 80, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · PS5')
        pg = eb(pr(t, .05, .4))
        R.put(fr, S('gamepad'), 540, 735, .42 * pg, .42 * pg, rot=math.sin(t * 8) * 6, anchor=(150, 95))
        for i, n in enumerate(nombres):
            u = eo(pr(t, .1 + i * .12, .3))
            if u <= 0: continue
            y = 800 + i * 62; xo = (1 - u) * 400
            R.put(fr, S('numero', i + 1, 24, ORANGE), 345 + xo, y, 1, 1, alpha=u, anchor=(28, 28))
            R.put(fr, pil(n, 36, bg=(74, 38, 120)), 540 + xo, y, 1, 1, alpha=u, anchor=(pil(n, 36, bg=(74, 38, 120)).width / 2, 28))
            R.put(fr, S('icono_ajuste', i + 1, 150), 715 + xo, y, .45, .45, alpha=u, anchor=(75, 75))
        if t > .9:
            R.anim_in(fr, pilg('GUÁRDALO', 40), 540, 1128, t, .9, 'pop', .3)
        gusm(fr, 150, emo='feliz', boca=.7, pose='celebra', brazos=.5 + .5 * math.sin(t * 11), sy=.66 * idle(t, 12, .03))
        flm(fr, 930, emo='amor', gafas=1, lente='estrella', cuello=.3, ala='arriba', sy=.66 * idle(t, 6))
    return draw


def a_uni(s):
    def draw(fr, t):
        titulo(fr, t, '1 · UNIDADES: *MÉTRICO*', 84, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · UNIDADES')
        p = eo(pr(t, .45, .4)); done = p > .98
        R.put(fr, pil('MPH · °F', 44, bg=(150, 70, 110)), 545, 765, 1 - .1 * p, 1 - .1 * p, alpha=1 - .6 * p, anchor=(pil('MPH · °F', 44, bg=(150, 70, 110)).width / 2, 28))
        gp = pilg('KM/H · °C', 44)
        R.put(fr, gp, 545, 835, .85 + .2 * eb(pr(t, .8, .3)) * (1 if t > .8 else 0), .85 + .2 * eb(pr(t, .8, .3)) * (1 if t > .8 else 0), alpha=.45 + .55 * p, anchor=(gp.width / 2, 28))
        R.put(fr, S('interruptor', round(p * 8) / 8), 580, 960, 1, 1, anchor=(150, 75))
        gx = 150 + 130 * eo(pr(t, 0, .4))
        gusm(fr, gx, emo='concentrado' if t < .9 else 'feliz', boca=0 if t < .9 else .6, pose='empuja', brazos=eo(pr(t, .25, .25)), sy=.66 * idle(t, 8))
        flm(fr, 930, emo='feliz', ala='sostiene' if t > 1.0 else 'reposo', lente='', cuello=.3, sy=.66 * idle(t, 5))
        sello(fr, t, 1.1, 735, 905, .8)
    return draw


def a_retic(s):
    def draw(fr, t):
        titulo(fr, t, '2 · RETÍCULA: *PUNTO*', 90, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · MIRA')
        k = eo(pr(t, .4, .6))
        pop_ = 1 + (.25 * math.sin(math.pi * pr(t, .95, .3)) if t > .95 else 0)
        R.put(fr, S('reticula', round(k * 12) / 12), 560, 890, 1.0 * pop_, 1.0 * pop_, rot=(1 - k) * 90, anchor=(170, 170))
        gx = 150 + 90 * eo(pr(t, 0, .4))
        gusm(fr, gx, emo='concentrado' if t < .9 else 'orgullo', pose='senala', brazos=eo(pr(t, .2, .3)), sy=.66 * idle(t, 8))
        flm(fr, 930, emo='feliz', ala='sostiene' if t > 1.1 else 'reposo', cuello=.3, sy=.66 * idle(t, 5))
        sello(fr, t, 1.2, 735, 770, .8)
    return draw


def a_aviso(s):
    def draw(fr, t):
        titulo(fr, t, '3 · AVISOS DE PROGRESO', 90, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · AVISOS')
        pe = eb(pr(t, .1, .35))
        sac = math.sin((t - .45) * 28) * 22 * math.exp(-(t - .45) * 2.5) if t > .45 else 0
        R.put(fr, S('campana', 220), 470, 960, .95 * pe, .95 * pe, rot=sac, anchor=(110, 24))
        R.put(fr, S('badge_rojo', '1', 34), 545, 880, eb(pr(t, .5, .3)), eb(pr(t, .5, .3)), anchor=(38, 38))
        f = cl((t - .6) / .7)
        x = 590 + (1 - eo(pr(t, .5, .35))) * 500
        R.put(fr, S('toast', 620, 120, '¡Objetivo cumplido!', round(f * 10) / 10), x, 790, .56, .56, anchor=(310, 60))
        gusm(fr, 150, emo='feliz' if t > .45 else 'asombro', boca=.6 if t > .45 else 1., pose='senala', brazos=eo(pr(t, .1, .3)), sy=.66 * idle(t, 9))
        flm(fr, 930, emo='feliz', ala='sostiene' if t > 1.1 else 'reposo', cuello=.3, sy=.66 * idle(t, 5))
        sello(fr, t, 1.2, 700, 950, .8)
    return draw


def a_subs(s):
    def draw(fr, t):
        titulo(fr, t, '4 · SUBTÍTULOS: SOLO *MISIONES*', 78, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · SUBTÍTULOS')
        R.put(fr, S('barra_subs', 'Vamos por el botín.', True), 560, 775, .62, .62, alpha=.5 + .5 * eo(pr(t, .25, .3)), anchor=(350, 65))
        opts = ('SIEMPRE', 'SOLO MISIONES', 'NUNCA'); xs = (545, 545, 545); ys = (850, 915, 980)
        sel = 0 if t < .75 else 1
        for i, (o, x_) in enumerate(zip(opts, xs)):
            y_ = ys[i]
            im = pilg(o, 32, 22, 10) if (i == sel) else pil(o, 32, bg=(74, 38, 120), padx=22, pady=10)
            k_ = 1 + (.12 * math.sin(math.pi * pr(t, .75, .3)) if i == 1 else 0)
            R.put(fr, im, x_, y_, k_, k_, anchor=(im.width / 2, im.height / 2))
        mx = 230 + 310 * eo(pr(t, .35, .4))
        gusm(fr, 150 + 60 * eo(pr(t, 0, .4)), emo='concentrado' if t < .8 else 'feliz', boca=0 if t < .8 else .5, pose='empuja', brazos=eo(pr(t, .2, .25)), sy=.66 * idle(t, 8))
        flm(fr, 930, emo='feliz', ala='sostiene' if t > 1.1 else 'reposo', cuello=.3, sy=.66 * idle(t, 5))
        sello(fr, t, 1.15, 735, 1040, .8)
    return draw


def a_mini(s):
    D = s['dur']
    def draw(fr, t):
        titulo(fr, t, '5 · INTERFAZ DE *MINIJUEGOS*', 80, 548)
        tablero(fr, t, 880, 820, 440, 'AJUSTES · MINIJUEGOS')
        ang = (-90 + 300 * eo(pr(t, .3, 1.8))) if t < 2.2 else 62
        abierto = 1 if t > 2.25 else 0
        sweet = 62
        R.put(fr, S('candado_ui', round(ang / 4) * 4, abierto, sweet, 150), 450, 900, .68, .68, anchor=(170, 170))
        if t > 2.25:
            R.anim_in(fr, sfx('[¡CLIC!]', 70), 450, 765, t, 2.25, 'pop', .25)
        pw = eb(pr(t, .4, .4)); ch = 0 if t < 2.7 else .5 + .5 * math.sin((t - 2.7) * 14)
        R.put(fr, S('cables', round(ch * 4) / 4 if t > 2.7 else 0), 690, 900, .62 * pw, .62 * pw, anchor=(150, 150))
        if t > 2.7: R.anim_in(fr, sfx('[¡ZAP!]', 60), 700, 785, t, 2.7, 'pop', .2)
        R.put(fr, S('icono_ajuste', 5, 150), 330, 760, .5, .5, anchor=(75, 75)) if False else None
        gusm(fr, 150, emo='concentrado' if t < 2.3 else 'feliz', boca=0 if t < 2.3 else .6, pose='agarra', brazos=eo(pr(t, .2, .4)), mira=(1, 0), sy=.66 * idle(t, 8))
        flm(fr, 930, emo='feliz', ala='sostiene' if t > 2.8 else 'reposo', cuello=.3, sy=.66 * idle(t, 5))
        sello(fr, t, 3.0, 580, 1050, .9)
    return draw


def a_cierre(s):
    def draw(fr, t):
        titulo(fr, t, '¿CUÁL *PRIMERO*?', 110, 540)
        for i in range(5):
            x = 330 + i * 112
            u = pr(t, .25 + i * .22, .4)
            if u <= 0: continue
            dy = (1 - eo(u)) * -200 - abs(math.sin(t * 5 + i * .8)) * 10
            R.put(fr, S('icono_ajuste', i + 1, 150), x, 880 + dy, .68 * eb(u), .68 * eb(u), anchor=(75, 75))
            R.put(fr, S('numero', i + 1, 20, ORANGE), x + 34, 835 + dy, eb(u), eb(u), anchor=(24, 24))
        gusm(fr, 150, emo='feliz', boca=.5, pose='celebra' if int(t * 2) % 2 else 'saluda', brazos=.7, sy=.66 * idle(t, 8, .025), sc=.66)
        flm(fr, 930, emo='guino', gafas=0, ala='senala', cuello=.3, sy=.66 * idle(t, 5))
        R.pop_burbuja(fr, bub('¿Cuál cambias primero?', 0, 54), 280, 800, t, .8)
        for i in range(2):
            u = pr(t, 1.4 + i * .3, .3)
            if u > 0: R.put(fr, S('signo', '?', 110, (255, 224, 138)), 700 + i * 90, 1010 - i * 30 + math.sin(t * 4 + i) * 8, eb(u), eb(u), rot=8 - i * 16, anchor=(50, 66))
    return draw
