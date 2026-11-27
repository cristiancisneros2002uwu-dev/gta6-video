"""Escenas de caricatura 7 (27-nov-2026): el cuarto secreto de Lake Tallaloko (t_*).
Mismo motor y estilo que escenas4/5/6. Todo dibujado, sin logos ni marcas.
Los mapas de las escenas 2 y 4 se cambian desde el JSON ("mapa")."""
import math
from PIL import Image, ImageDraw, ImageFilter
import caricatura2 as C
import escenas2 as E
import escenas4 as B
from caricatura import OUT, SS, GREEN, GREEN_D
from caricatura2 import L2, PINK, PINK_D, PINK_L, ORANGE, CREAM, GOLD, WHITE, CYAN, RED
from escenas4 import mk, S, cl, pr, eo, eb, idle, golpe, sombra, G, FLA

R = None
MADERA = (176, 108, 74); MADERA_D = (130, 76, 56)
BILL = (126, 214, 142); BILL_D = (56, 140, 90)


def _mix(a, b, u): return a + (b - a) * u
def fondo(fr, im, y=1210): R.put(fr, im, 540, y, 1, 1, anchor=(540, im.height))


def mano(x, y, sc, hx, hy, flip=False):
    dx = (hx - 220) * sc
    return x - dx if flip else x + dx, y + (hy - 590) * sc


def luzcapa(fr, fn, blur=0):
    """Capa transparente recortada a la zona de escena (650-1210)."""
    lay = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay))
    if blur: lay = lay.filter(ImageFilter.GaussianBlur(blur))
    clip = Image.new('RGBA', (R.W, R.H), (0, 0, 0, 0)); clip.paste(lay.crop((0, 650, R.W, 1210)), (0, 650)); fr.alpha_composite(clip)


# =================================================================== OBJETOS
def billete():
    def f():
        c = L2(160, 96)
        c.rrect(8, 12, 152, 84, 10, BILL)
        c.rrect(22, 24, 138, 72, 8, (170, 236, 180), ow=3)
        c.elipse(80, 48, 22, 22, BILL, ow=4); c.texto(80, 48, '$', 34, BILL_D)
        for x in (34, 126): c.elipse(x, 48, 6, 6, BILL_D, ow=0)
        return c.fin()
    return mk('tbill', f)


def fajo():
    def f():
        c = L2(180, 130)
        for k in range(4):
            y = 78 - k * 18
            c.rrect(12, y, 168, y + 40, 8, BILL if k % 2 else (150, 226, 164), ow=4)
        c.rrect(70, 20, 112, 120, 6, GOLD, ow=4)
        c.texto(91, 44, '$', 30, BILL_D)
        return c.fin()
    return mk('tfajo', f)


def linterna():
    def f():
        c = L2(170, 70)
        c.rrect(10, 20, 108, 50, 10, (90, 80, 150))
        c.poli([(104, 14), (150, 4), (150, 66), (104, 56)], GOLD)
        c.rrect(42, 12, 66, 24, 5, PINK, ow=3)
        return c.fin()
    return mk('tlint', f)


def computadora():
    """Monitor con el correo. 420x340; la foto se toma de la pantalla."""
    def f():
        c = L2(420, 340)
        c.rrect(170, 268, 250, 316, 6, (120, 110, 160))
        c.rrect(110, 300, 310, 330, 12, (150, 140, 190))
        c.rrect(10, 10, 410, 280, 22, (52, 40, 86))
        c.rrect(30, 30, 390, 258, 10, (240, 244, 255), ow=4)
        c.rrect(30, 30, 390, 80, 10, (90, 140, 230), ow=0)
        c.texto(210, 56, 'CORREO', 30, WHITE)
        c.elipse(66, 112, 20, 20, ORANGE, ow=3); c.texto(66, 112, 'M', 24, WHITE)
        c.texto(98, 112, 'Marcus Fielding', 32, OUT, anchor='lm')
        for y, x1 in ((150, 360), (172, 300)): c.rrect(50, y, x1, y + 10, 5, (180, 186, 214), ow=0)
        c.rrect(64, 192, 356, 248, 12, GOLD, ow=4)
        c.texto(210, 220, 'CÓDIGO  • • • •', 30, OUT)
        return c.fin()
    return mk('tpc', f)


def cartera():
    def f():
        c = L2(220, 160)
        c.rrect(60, 16, 170, 80, 8, BILL, ow=4); c.rrect(84, 6, 190, 70, 8, (150, 226, 164), ow=4)
        c.rrect(16, 44, 200, 146, 20, MADERA)
        c.rrect(16, 44, 200, 78, 16, MADERA_D, ow=4)
        c.rrect(146, 82, 212, 122, 12, MADERA_D, ow=4); c.elipse(164, 102, 9, 9, GOLD, ow=3)
        c.linea([(32, 130), (130, 130)], 4, (220, 160, 110), ow=0)
        return c.fin()
    return mk('tcartera', f)


def cromo(reverso=False):
    """Cromo de un club inventado en dibujo propio. 240x340."""
    def f():
        c = L2(240, 340)
        c.rrect(8, 8, 232, 332, 22, GOLD)
        if reverso:
            c.rrect(26, 26, 214, 314, 14, (122, 63, 191), ow=4)
            c.estrella(120, 170, 62, GOLD, ow=4)
        else:
            c.rrect(24, 24, 216, 316, 14, (255, 150, 180), ow=4)
            c.rrect(24, 190, 216, 316, 14, (90, 60, 150), ow=0)
            c.elipse(120, 106, 54, 54, WHITE, ow=5)
            c.estrella(120, 106, 24, OUT, ow=0, puntas=5)
            for a in range(5):
                g = -math.pi / 2 + a * 2 * math.pi / 5
                c.elipse(120 + math.cos(g) * 44, 106 + math.sin(g) * 44, 9, 9, OUT, ow=0)
            c.texto(120, 214, 'VICE CITY', 32, CREAM)
            c.texto(120, 252, 'CLUB DE', 28, CREAM)
            c.texto(120, 288, 'FÚTBOL', 32, GOLD)
        return c.fin()
    return mk(('tcromo', reverso), f)


def reliquia():
    """Cuchillo ceremonial dorado: pieza de museo, sin filo realista. 440x150."""
    def f():
        c = L2(440, 150)
        c.poli([(168, 52), (360, 46), (424, 74), (358, 102), (168, 96)], (255, 208, 80))
        c.linea([(188, 66), (352, 64)], 8, (255, 246, 200), ow=0)
        for x in (210, 250, 290, 330): c.estrella(x, 82, 8, (190, 130, 40), ow=0)
        c.rrect(142, 22, 176, 128, 16, (230, 165, 45))
        c.rrect(48, 54, 144, 96, 14, (122, 63, 191))
        for x in (68, 92, 116): c.linea([(x, 58), (x + 12, 92)], 7, GOLD, ow=0)
        c.elipse(38, 75, 28, 28, (230, 165, 45)); c.elipse(38, 75, 11, 11, PINK, ow=3)
        c.elipse(159, 75, 11, 11, CYAN, ow=3)
        return C.glow(c.fin(), 12, 1.6)
    return mk('treliquia', f)


def cofre_base():
    def f():
        c = L2(280, 160)
        c.rrect(16, 20, 264, 150, 16, MADERA)
        for x in (50, 210): c.rrect(x, 20, x + 22, 150, 4, GOLD, ow=4)
        c.rrect(116, 40, 164, 92, 10, GOLD, ow=4); c.elipse(140, 62, 8, 8, OUT, ow=0)
        return c.fin()
    return mk('tcofre', f)


def cofre_tapa():
    def f():
        c = L2(280, 110)
        c.poli([(16, 102), (16, 56), (46, 20), (234, 20), (264, 56), (264, 102)], MADERA_D)
        for x in (50, 210): c.rrect(x, 20, x + 22, 102, 4, GOLD, ow=4)
        return c.fin()
    return mk('tcofretapa', f)


def vela(fase):
    def f():
        c = L2(90, 190)
        c.rrect(24, 70, 66, 180, 10, CREAM)
        c.linea([(34, 74), (34, 108)], 9, (240, 214, 190), ow=0)
        c.linea([(45, 70), (45, 56)], 5, OUT, ow=0)
        d = (-8, 0, 8)[fase]
        c.poli([(45 + d, 8), (62, 40), (54, 60), (36, 60), (28, 40)], ORANGE, ow=4)
        c.elipse(45 + d * .3, 46, 9, 13, GOLD, ow=0)
        return C.glow(c.fin(), 10, 1.3)
    return mk(('tvela', fase), f)


def proyector():
    def f():
        c = L2(260, 210)
        c.rrect(40, 96, 200, 180, 16, (110, 100, 160))
        c.rrect(196, 114, 246, 160, 8, (70, 60, 110))
        c.elipse(244, 137, 12, 24, CYAN, ow=4)
        for x in (60, 170): c.rrect(x, 178, x + 18, 204, 4, (70, 60, 110), ow=4)
        c.rrect(62, 124, 130, 150, 8, PINK, ow=3)
        return c.fin()
    return mk('tproy', f)


def carrete():
    def f():
        c = L2(110, 110)
        c.elipse(55, 55, 48, 48, (190, 184, 220))
        for k in range(4):
            g = k * math.pi / 2
            c.elipse(55 + math.cos(g) * 25, 55 + math.sin(g) * 25, 12, 12, (60, 46, 96), ow=3)
        c.elipse(55, 55, 7, 7, GOLD, ow=3)
        return c.fin()
    return mk('tcarrete', f)


def guardia():
    """Guardia simpático de espaldas a Gus (mira a la derecha), sin armas, con café. 220x360."""
    def f():
        c = L2(220, 360)
        for x in (66, 118): c.rrect(x, 258, x + 40, 344, 12, (34, 40, 90))
        for x in (66, 118): c.rrect(x, 326, x + 66, 352, 12, (24, 18, 44))
        c.rrect(46, 140, 176, 272, 40, (60, 80, 170))
        c.rrect(60, 238, 164, 260, 6, (30, 26, 60), ow=4)
        c.estrella(142, 178, 16, GOLD, ow=3)
        c.elipse(118, 100, 58, 56, (232, 170, 130))
        c.poli([(54, 70), (74, 26), (150, 20), (176, 58), (212, 66), (204, 80), (60, 82)], (34, 40, 120))
        for x in (132, 162): c.elipse(x, 100, 11, 13, WHITE, ow=3); c.elipse(x + 5, 101, 5, 6, OUT, ow=0)
        c.curva([(120, 132), (148, 148), (176, 130)], 12, (110, 70, 50), ow=0)
        c.curva([(150, 178), (182, 216), (190, 200)], 24, (60, 80, 170), ow=5)
        c.rrect(172, 178, 210, 218, 8, CREAM, ow=4); c.elipse(192, 200, 13, 13, (232, 170, 130), ow=4)
        return c.fin()
    return mk('tguardia', f)


# =================================================================== FONDOS
def bg_boveda():
    """Escena 1: cuarto oscuro con puertas y baúles."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (34, 18, 70), ow=0)
        for j in range(7):
            for i in range(8):
                c.rrect(i * 150 - (75 if j % 2 else 0), j * 62 + 6, i * 150 + 140 - (75 if j % 2 else 0), j * 62 + 60, 8, (48, 28, 92) if (i + j) % 3 else (58, 34, 104), ow=3)
        c.rrect(-10, 440, 1090, 560, 0, (60, 36, 70), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        for x in range(0, 1100, 160): c.linea([(x, 446), (x - 40, 556)], 4, (84, 52, 94), ow=0)
        return c.fin()
    return mk('t1', f)


def bg_tienda():
    """Escena 2b: costado de la tienda con la puerta de empleados."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (120, 190, 236), ow=0)
        c.rrect(30, 70, 1050, 440, 12, (255, 214, 150), ow=6)
        c.rrect(16, 54, 1064, 150, 14, (214, 50, 100), ow=6)
        c.texto(290, 102, 'POPPERS', 66, CREAM)
        for x in range(30, 1040, 92): c.poli([(x, 150), (x + 92, 150), (x + 76, 190), (x + 16, 190)], PINK if (x // 92) % 2 else CREAM, ow=4)
        c.rrect(70, 224, 450, 400, 10, (110, 190, 220), ow=6)
        for y in (290, 356):
            c.rrect(84, y, 436, y + 10, 3, WHITE, ow=3)
            for k in range(9): c.rrect(96 + k * 38, y - 36, 120 + k * 38, y, 5, (PINK, GOLD, (130, 220, 150), (194, 89, 255))[k % 4], ow=3)
        c.rrect(668, 196, 920, 262, 12, (52, 40, 100), ow=5)
        c.texto(794, 229, 'EMPLEADOS', 38, GOLD)
        c.rrect(694, 272, 894, 440, 6, (24, 14, 46), ow=6)
        c.rrect(-10, 440, 1090, 560, 0, (90, 76, 120), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        return c.fin()
    return mk('t2', f)


def hoja_emp():
    def f():
        c = L2(212, 180)
        c.rrect(6, 6, 206, 174, 6, (90, 130, 210))
        c.rrect(40, 26, 172, 70, 8, (150, 200, 240), ow=4)
        c.elipse(176, 104, 11, 11, GOLD, ow=4)
        return c.fin()
    return mk('thojae', f)


def bg_oficina():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (84, 120, 160), ow=0)
        for x in range(0, 1080, 130): c.linea([(x, 0), (x, 440)], 4, (96, 136, 178), ow=0)
        for (x, y) in ((40, 40), (180, 40)):
            c.rrect(x, y, x + 110, y + 130, 8, CREAM, ow=5)
            for k in range(4): c.rrect(x + 18, y + 24 + k * 24, x + 92, y + 34 + k * 24, 4, (190, 180, 210), ow=0)
        for k, col in enumerate((PINK, GOLD, CYAN)):
            c.rrect(880, 60 + k * 90, 1060, 80 + k * 90, 4, MADERA, ow=4)
            for j in range(3): c.rrect(892 + j * 54, 14 + k * 90, 936 + j * 54, 60 + k * 90, 6, col, ow=4)
        c.rrect(-10, 440, 1090, 560, 0, (56, 44, 90), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        return c.fin()
    return mk('t3', f)


def mesa(w=380):
    def f():
        c = L2(w, 170)
        for x in (36, w - 66): c.rrect(x, 30, x + 30, 164, 6, MADERA_D)
        c.rrect(8, 10, w - 8, 48, 10, MADERA)
        return c.fin()
    return mk(('tmesa', w), f)


def bg_lago():
    """Escena 4: lago al fondo (norte) y la casa."""
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 240, 0, (120, 188, 236), ow=0)
        for x, r in ((80, 130), (320, 100), (980, 150), (780, 90)): c.elipse(x, 232, r, r * .55, (74, 150, 120), ow=4)
        c.rrect(-10, 220, 1090, 380, 0, (62, 130, 200), ow=0)
        for k in range(18): c.linea([((k * 197) % 1030, 240 + (k * 31) % 120), ((k * 197) % 1030 + 56, 240 + (k * 31) % 120)], 5, (190, 232, 255), ow=0)
        c.rrect(-10, 370, 1090, 560, 0, (96, 176, 110), ow=0)
        c.linea([(-10, 370), (1090, 370)], 7, OUT)
        c.rrect(300, 190, 760, 450, 12, (244, 226, 250), ow=6)
        c.poli([(270, 205), (530, 70), (790, 205)], (190, 60, 110), ow=6)
        for x in (340, 470, 640):
            c.rrect(x, 232, x + 84, 308, 8, (110, 190, 220), ow=5); c.linea([(x + 42, 232), (x + 42, 308)], 4, OUT)
        return c.fin()
    return mk('t4', f)


def muro():
    def f():
        c = L2(520, 200)
        c.rrect(8, 30, 512, 192, 8, (200, 130, 100))
        for j in range(4):
            for i in range(7):
                x = 14 + i * 76 - (38 if j % 2 else 0)
                c.rrect(max(14, x), 40 + j * 38, min(506, x + 68), 70 + j * 38, 5, (216, 150, 116) if (i + j) % 2 else (188, 118, 92), ow=3)
        c.rrect(0, 14, 520, 42, 8, (236, 214, 190))
        return c.fin()
    return mk('tmuro', f)


def bg_sala():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (236, 196, 160), ow=0)
        for x in range(0, 1080, 110): c.rrect(x, 0, x + 40, 440, 0, (226, 182, 150), ow=0)
        c.rrect(400, 50, 680, 220, 14, (110, 190, 220), ow=6); c.linea([(540, 50), (540, 220)], 5, OUT)
        c.rrect(420, 160, 660, 214, 4, (62, 130, 200), ow=0)
        c.rrect(60, 80, 220, 200, 10, GOLD, ow=5); c.rrect(76, 96, 204, 184, 6, PINK_L, ow=3)
        c.rrect(280, 250, 800, 420, 50, (122, 63, 191), ow=6)
        c.rrect(250, 330, 330, 450, 30, (142, 80, 214), ow=6); c.rrect(750, 330, 830, 450, 30, (142, 80, 214), ow=6)
        c.rrect(320, 350, 760, 440, 26, (156, 96, 226), ow=5)
        c.rrect(950, 120, 1060, 440, 8, MADERA, ow=5)
        for y in (200, 280, 360): c.rrect(960, y, 1050, y + 12, 3, MADERA_D, ow=3)
        c.rrect(-10, 440, 1090, 560, 0, (110, 70, 90), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        c.elipse(540, 505, 430, 46, (214, 60, 110), ow=5)
        return c.fin()
    return mk('t5', f)


def bg_pasillo():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (72, 56, 128), ow=0)
        for x in range(0, 1080, 100): c.rrect(x, 0, x + 44, 440, 0, (82, 64, 142), ow=0)
        c.rrect(-10, 440, 1090, 560, 0, MADERA_D, ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        for x in range(0, 1080, 150): c.linea([(x, 446), (x - 30, 556)], 4, (96, 56, 48), ow=0)
        return c.fin()
    return mk('t6', f)


def bg_secreto():
    def f():
        c = L2(1080, 560)
        c.rrect(-10, 0, 1090, 440, 0, (26, 12, 52), ow=0)
        for x in range(0, 1080, 135): c.rrect(x, 0, x + 66, 440, 0, (34, 16, 64), ow=0)
        c.rrect(600, 40, 1030, 280, 14, (232, 228, 244), ow=7)
        c.poli([(-10, 0), (170, 0), (80, 150), (60, 440), (-10, 440)], (150, 30, 80), ow=6)
        c.rrect(-10, 440, 1090, 560, 0, (48, 26, 62), ow=0)
        c.linea([(-10, 440), (1090, 440)], 7, OUT)
        return c.fin()
    return mk('t7', f)


# =================================================================== MAPAS
def mapa_wb():
    """940x560: bahía, calles y manzanas (dibujo propio)."""
    def f():
        c = L2(940, 560)
        c.rrect(6, 6, 934, 554, 40, (60, 140, 205), ow=7)
        tierra = [(30, 30), (700, 30), (660, 140), (760, 230), (640, 330), (700, 430), (560, 530), (30, 530)]
        c.poli(tierra, (238, 222, 180))
        for x in range(60, 560, 108):
            for y in range(70, 480, 96):
                c.rrect(x, y, x + 84, y + 68, 10, ((150, 205, 160), (190, 150, 220), (168, 134, 214))[(x // 108 + y // 96) % 3], ow=3)
        for x in range(152, 580, 108): c.linea([(x, 40), (x, 520)], 10, WHITE, ow=0)
        for y in range(154, 480, 96): c.linea([(40, y), (610, y)], 10, WHITE, ow=0)
        for (x, y) in ((790, 120), (840, 420), (780, 500)): c.elipse(x, y, 44, 28, (150, 205, 160), ow=4)
        c.d.rounded_rectangle([6 * SS, 6 * SS, 934 * SS, 554 * SS], radius=40 * SS, outline=OUT, width=7 * SS)
        return c.fin()
    return mk('tmapa', f)


def tienda_icono():
    def f():
        c = L2(150, 120)
        c.rrect(16, 46, 134, 112, 8, (255, 214, 150))
        c.rrect(8, 22, 142, 54, 8, (214, 50, 100))
        c.rrect(58, 74, 92, 112, 4, (52, 40, 100), ow=4)
        for x in (26, 102): c.rrect(x, 68, x + 22, 92, 4, CYAN, ow=3)
        return c.fin()
    return mk('ttienda', f)


def minimapa(lago, casa, etiqueta):
    """380x250: lago al norte y la casa abajo."""
    def f():
        c = L2(380, 250)
        c.rrect(6, 6, 374, 244, 26, (150, 205, 160), ow=6)
        x0, y0, x1, y1 = lago
        c.rrect(x0, y0, x1, y1, min(x1 - x0, y1 - y0) / 2 - 2, (62, 130, 200), ow=5)
        c.texto((x0 + x1) / 2, (y0 + y1) / 2, etiqueta, 27, WHITE)
        c.linea([(24, 216), (356, 216)], 9, WHITE, ow=0)
        hx, hy = casa
        c.rrect(hx - 22, hy - 8, hx + 22, hy + 26, 5, CREAM, ow=4)
        c.poli([(hx - 30, hy - 4), (hx, hy - 30), (hx + 30, hy - 4)], PINK, ow=4)
        c.texto(344, 158, 'N', 28, OUT)
        c.poli([(344, 112), (362, 140), (326, 140)], OUT, ow=0)
        return c.fin()
    return mk(('tmini', tuple(lago), tuple(casa), etiqueta), f)


# =================================================================== 1 · GANCHO
def t_hook(s):
    D = s['dur']
    def draw(fr, t):
        fondo(fr, bg_boveda())
        E.titulo(fr, t, '¿*$70,000* ESCONDIDOS?', 100, 548, .0)
        gx, gy, sc = 250, G + 20, .64
        mx, my = mano(gx, gy, sc, 430, 352)
        ang = -.18 + math.sin(t * 3.2) * .22
        def haz(d):
            x0, y0 = mx + 80, my - 6
            d.polygon([(x0, y0), (x0 + math.cos(ang - .22) * 900, y0 + math.sin(ang - .22) * 900), (x0 + math.cos(ang + .22) * 900, y0 + math.sin(ang + .22) * 900)], fill=(255, 236, 160, 85))
        luzcapa(fr, haz, 5)
        for k in range(14):                                      # billetes volando
            u = (t * .55 + k * .173) % 1
            x = 420 + (k * 131) % 520 + math.sin(t * 4 + k) * 34
            y = 1190 - u * 520
            q = eb(pr(t, .05 + (k % 5) * .07, .3))
            if q > 0:
                k_ = (.55 + (k % 3) * .16) * q
                R.put(fr, billete(), x, y, k_, k_ * (.5 + .5 * abs(math.cos(t * 5 + k))), rot=math.sin(t * 3 + k) * 35, alpha=min(1, (1 - u) * 3), anchor=(80, 48))
        paso = t < D * .45
        E.GU(fr, gx, gy, sc, 'concentrado' if t < .55 else ('asombro' if paso else 'amor'), boca=0 if t < .55 else .8, pose='senala', brazos=1., mira=(1, 0), sy=sc * idle(t, 8, .025))
        R.put(fr, linterna(), mx, my - 4, .85, .85, rot=-math.degrees(ang), anchor=(60, 35))
        if t < D * .45:
            E.FL(fr, 900, G + 30, .56, 'feliz', gafas=1, cuello=.3, ala='cadera', flip=True, sy=.56 * idle(t, 5))
        else:
            q = pr(t, D * .45, .3)
            FLA(fr, 900, G + 30, .56 * (1 + .1 * math.sin(math.pi * q)), emo='asombro', boca=.6, cuello=.4 + .6 * eo(q), ala='senala', mira=(-1, 0))
            golpe(fr, '[¿EH?]', 830, 710, t, D * .45, 70, 8)
        for i, (x, y) in enumerate(((620, 720), (760, 900), (520, 840))): E.destello(fr, x, y, t, i * .33, 1.2)
    return draw


# =================================================================== 2 · MAPA Y PUERTA
def t_poppers(s):
    D = s['dur']; corte = s.get('t_puerta', D * .46)
    cfg = s.get('mapa', {})
    zona = cfg.get('zona', 'WATSON BAY'); pin = cfg.get('pin', [370, 300]); et = cfg.get('etiqueta', [300, 62])
    ep = cfg.get('etiqueta_pin', 'POPPERS'); ruta = cfg.get('ruta', [[90, 470], [250, 360]])
    MX0, MY0 = 540 - 470, 930 - 280
    def draw(fr, t):
        E.titulo(fr, t, '*POPPERS* · WATSON BAY', 82, 548)
        if t < corte:
            pe = eo(pr(t, 0, .3))
            R.put(fr, mapa_wb(), 540, 930, .8 + .2 * pe, .8 + .2 * pe, alpha=cl(pe * 2), anchor=(470, 280))
            if pe < 1: return
            d = ImageDraw.Draw(fr)
            for k in range(8):
                x = MX0 + 740 + (k * 37) % 150; y = MY0 + 180 + (k * 61 + t * 36) % 200
                d.arc((x - 16, y - 6, x + 16, y + 10), 200, 340, fill=(200, 235, 255, 255), width=4)
            R.anim_in(fr, E.pil(zona, 42, bg=(74, 38, 120)), MX0 + et[0], MY0 + et[1], t, .2, 'pop', .25)
            px, py = MX0 + pin[0], MY0 + pin[1]
            u = pr(t, .35, .35)
            if u > 0:
                for j in (0, .5):
                    r = (t + j) % 1.0
                    d.ellipse((px - 60 - 70 * r, py + 20 - 24 - 34 * r, px + 60 + 70 * r, py + 20 + 24 + 34 * r), outline=(255, 60, 90, int(255 * (1 - r))), width=8)
                R.put(fr, tienda_icono(), px, py + 40, eb(u), eb(u), anchor=(75, 112))
                R.put(fr, S('pin', PINK, 70), px, py - 76 + (1 - eo(u)) * -190 - abs(math.sin(t * 6)) * 14, 1.2 * eb(u), 1.2 * eb(u), anchor=(35, 90))
                R.anim_in(fr, E.pilg(ep, 36, 22, 8), px, py + 80, t, .55, 'pop', .25)
            (ax, ay), (bx, by) = ruta
            w = eo(cl((t - .4) / max(.4, corte - .6)))
            gx, gy = MX0 + _mix(ax, bx, w), MY0 + _mix(ay, by, w) + 90
            E.GU(fr, gx, gy - abs(math.sin(t * 11)) * 18, .3, 'feliz', boca=.5, pose='celebra', brazos=1.)
        else:
            q = t - corte; L = max(.8, D - corte)
            fondo(fr, bg_tienda())
            ab = eo(pr(t, corte + L * .22, .35))
            top = 1210 - 560 + 272
            R.put(fr, hoja_emp(), 694, top - 4, 1 - .84 * ab, .98, anchor=(6, 6))
            w = eo(cl((q - .1) / (L * .62)))
            entra = eo(cl((q - L * .66) / (L * .26)))
            gx = _mix(150, 780, w); gsc = .5 * (1 - .3 * entra)
            gy = G + 10 - abs(math.sin(t * 9)) * 30 * (1 - entra) - 62 * entra
            sombra(fr, gx, min(G + 14, gy + 8), 170)
            E.GU(fr, gx, gy, gsc, 'concentrado' if w < .9 else ('nervioso' if entra < .5 else 'feliz'), boca=0, pose='pecho', brazos=1., mira=(1, 0), rot=math.sin(t * 9) * 7 * (1 - entra), alpha=1 - cl((entra - .6) / .4))
            R.pop_burbuja(fr, E.bub('Shhh...', 0, 46), max(200, gx - 40), 850, t, corte + .15, corte + L * .62)
            E.FL(fr, 975, G + 30, .46, 'feliz' if entra < .5 else 'guino', gafas=0, cuello=.3 + .2 * math.sin(t * 6), ala='senala', flip=True, sy=.46 * idle(t, 7))
            E.poof(fr, 540, 930, t, corte - .02)
    return draw


# =================================================================== 3 · DINERO Y FOTO
def t_foto(s):
    D = s['dur']; guarda = s.get('t_guarda', .5); foto = s.get('t_foto', D * .68)
    def draw(fr, t):
        fondo(fr, bg_oficina())
        E.titulo(fr, t, 'FOTO AL *CÓDIGO*', 108, 548)
        R.put(fr, mesa(360), 250, 1180, 1, 1, anchor=(180, 164))
        R.put(fr, mesa(470), 700, 1180, 1, 1, anchor=(235, 164))
        ent = eb(pr(t, .1, .35))
        R.put(fr, computadora(), 700, 1042, 1.02 * ent, 1.02 * ent, rot=math.sin(t * 2) * .8, anchor=(210, 330))
        gx, gy, sc = 130, G + 30, .54
        mx, my = mano(gx, gy, sc, 392, 424)
        quedan = 0
        for k in range(3):
            t0 = guarda + k * .38
            q = eo(cl((t - t0) / .34))
            x0, y0 = 340 - k * 14, 1000 - k * 44
            if q < 1:
                x = _mix(x0, gx + 20, q); y = _mix(y0, gy - 130, q) - 150 * math.sin(math.pi * q)
                R.put(fr, fajo(), x, y, .82 * (1 - .5 * q), .82 * (1 - .5 * q), rot=300 * q, anchor=(90, 70))
        listo = t > guarda + 1.2
        E.GU(fr, gx, gy, sc, 'amor' if t < guarda else ('feliz' if not listo else 'orgullo'), boca=.6, pose='agarra' if not listo else 'cadera', brazos=1., mira=(1, 0), sy=sc * idle(t, 12 if not listo else 6, .03))
        for k in range(3): golpe(fr, '[¡FSH!]', 230 + k * 40, 760 + k * 26, t, guarda + k * .38 + .22, 52, -10 + k * 9, guarda + k * .38 + .55)
        # Flami toma la foto
        fx = 960
        disparo = t >= foto
        E.FL(fr, fx, G + 35, .5, 'guino' if disparo else 'feliz', boca=.4 if disparo else 0, gafas=0, cuello=.6 if not disparo else .3, ala='sostiene', flip=True, mira=(1, 0), sy=.5 * idle(t, 6))
        R.put(fr, B.camara_foto(), 868, 1020 + math.sin(t * 5) * 6, .78, .78, rot=-6, anchor=(B.camara_foto().width / 2, B.camara_foto().height / 2))
        if disparo:
            q = t - foto
            if q < .3:
                luzcapa(fr, lambda d: d.rectangle((0, 650, 1080, 1210), fill=(255, 255, 255, int(235 * (1 - q / .3)))))
                R.put(fr, B.flash(), 840, 985, 2.2, 2.2, anchor=(B.flash().width / 2, B.flash().height / 2))
            golpe(fr, '[¡CLIC!]', 880, 770, t, foto, 76, 8)
            p = eb(pr(t, foto + .2, .35))
            if p > 0:                                             # la foto instantánea
                im = mk('tpolar', lambda: _polaroid())
                R.put(fr, im, 520, 800 + math.sin(t * 5) * 8, .78 * p, .78 * p, rot=-9 + math.sin(t * 3) * 3, anchor=(im.width / 2, im.height / 2))
                E.sello(fr, t, foto + .45, 650, 720, .8)
    return draw


def _polaroid():
    im = Image.new('RGBA', (390, 330), (0, 0, 0, 0))
    d = ImageDraw.Draw(im); d.rounded_rectangle((3, 3, 386, 326), 16, fill=(255, 252, 246, 255), outline=OUT + (255,), width=6)
    p = computadora().crop((30, 30, 390, 260)).resize((344, 220))
    im.alpha_composite(p, (23, 22))
    return im


# =================================================================== 4 · MURO TRASERO
def t_muro(s):
    D = s['dur']; sube = s.get('t_sube', D * .45)
    cfg = s.get('mapa', {})
    lago = cfg.get('lago', [50, 24, 304, 112]); casa = cfg.get('casa', [180, 172]); et = cfg.get('etiqueta', 'TALLALOKO')
    def draw(fr, t):
        fondo(fr, bg_lago())
        E.titulo(fr, t, 'POR *ATRÁS*', 140, 548)
        # guardia mira al otro lado
        sombra(fr, 930, G + 26, 170)
        R.put(fr, guardia(), 925, G + 30, .8, .8 * idle(t, 3, .015), rot=math.sin(t * 1.6) * 2.5, anchor=(110, 352))
        for k in range(2):
            u = (t * .8 + k * .5) % 1
            R.put(fr, S('nota', GOLD if k else PINK, False), 990 + u * 40, 890 - u * 150, .8, .8, rot=math.sin(t * 5 + k) * 20, alpha=math.sin(math.pi * u), anchor=(40, 60))
        # Gus trepa el muro
        gsc = .46
        u = eo(cl((t - .25) / max(.4, sube - .25)))
        v = cl((t - sube) / max(.8, D - sube - .35))
        if t < sube:
            gx = _mix(80, 370, u); gy = G + 40 - abs(math.sin(t * 9)) * 30
            emo, pose = 'concentrado', 'pecho'
        else:
            gx = 370 + 90 * v; gy = G + 40 - 200 * eo(cl(v / .7)) - abs(math.sin(t * 13)) * 12 * (v < .7)
            emo, pose = ('nervioso', 'celebra') if v < .7 else ('feliz', 'saluda')
        pared = lambda: R.put(fr, muro(), 400, G + 44, 1.04, .94, anchor=(260, 192))
        if t < sube:
            pared(); E.GU(fr, gx, gy, .5, emo, pose=pose, brazos=1., mira=(1, 0), rot=math.sin(t * 9) * 6)
        elif v < .7:                                              # trepando, por delante del muro
            pared(); E.GU(fr, gx, gy, .5, emo, boca=.5, pose=pose, brazos=1., mira=(1, 0), rot=math.sin(t * 13) * 12)
        else:                                                     # ya cruzó: se asoma detrás del muro
            k = eo(cl((v - .7) / .3))
            E.GU(fr, 460, G - 160 + 105 * k, .5, emo, boca=.7, pose=pose, brazos=1., rot=math.sin(t * 6) * 5); pared()
        golpe(fr, '[¡HOP!]', 170, 930, t, sube + .1, 66, -10, sube + .9)
        # mini mapa: el lago queda al norte
        p = eb(pr(t, .3, .35))
        if p > 0:
            R.put(fr, minimapa(lago, casa, et), 240, 765, p, p, rot=-3 + math.sin(t * 2) * 1.2, anchor=(190, 125))
        # Flami vigila volando
        E.FL(fr, 850 + math.sin(t * 2) * 30, 840 + math.sin(t * 5) * 18, .26, 'feliz', gafas=0 if t > sube else 1, cuello=.7, ala='arriba' if int(t * 7) % 2 else 'abre', mira=(-1, 0), flip=True)
        R.pop_burbuja(fr, E.bub('¡Ahora!', 0, 40), 640, 750, t, sube - .35, sube + .7)
    return draw


# =================================================================== 5 · LA SALA
def t_sala(s):
    D = s['dur']; c1 = s.get('t_cartera', D * .22); c2 = s.get('t_cromo', D * .56)
    def draw(fr, t):
        fondo(fr, bg_sala())
        E.titulo(fr, t, 'REVISA LA *SALA*', 108, 548)
        gsc = .62
        gx = 170 + 70 * eo(cl(t / c1))
        emo = 'concentrado' if t < c1 else ('feliz' if t < c2 else 'asombro')
        E.GU(fr, gx, G + 30, gsc, emo, boca=.6 if t > c1 else 0, pose='agarra' if t < c2 else 'senala', brazos=1., mira=(1, 0), sy=gsc * idle(t, 9, .025))
        q = eb(pr(t, c1, .35))
        if t < c1:
            for k in range(3):
                R.put(fr, S('signo', '?', 90, GOLD), 450 + k * 150, 900 + math.sin(t * 7 + k * 2) * 26, .7, .7, rot=math.sin(t * 5 + k) * 15, anchor=(50, 66))
        if q > 0:
            x = _mix(500, 390, eo(pr(t, c2 - .2, .35))); y = _mix(1060, 1030, q) - 180 * math.sin(math.pi * cl((t - c1) / .45))
            R.put(fr, cartera(), x, y, q, q, rot=math.sin(t * 6) * 8, anchor=(110, 95))
            golpe(fr, '[¡CARTERA!]', 330, 750, t, c1 + .1, 60, -8, c2 - .05)
        p = eb(pr(t, c2, .35))
        if p > 0:
            cx, cy = 660, 905 + math.sin(t * 4) * 10
            B_rayos(fr, cx, cy, t)
            giro = math.cos(2 * math.pi * cl((t - c2 - .2) / .6))           # una vuelta y queda de frente
            R.put(fr, cromo(giro < 0), cx, cy, max(.06, abs(giro)) * 1.35 * p, 1.35 * p, rot=math.sin(t * 3) * 4, anchor=(120, 170))
            for i, (dx, dy) in enumerate(((-170, -140), (170, -100), (150, 150), (-160, 120))): E.destello(fr, cx + dx, cy + dy, t, i * .27, 1.2)
        E.FL(fr, 950, G + 30, .5, 'feliz' if t < c2 else 'amor', boca=.4 if t > c2 else 0, gafas=1 if t < c2 else 0, cuello=.4, ala='cadera' if t < c2 else 'arriba', flip=True, sy=.5 * idle(t, 6 if t < c2 else 12))
    return draw


def B_rayos(fr, x, y, t, r=330, a=44, n=10):
    def f(d):
        for k in range(n):
            g = t * .8 + k * 2 * math.pi / n
            d.polygon([(x, y), (x + math.cos(g) * r, y + math.sin(g) * r), (x + math.cos(g + .2) * r, y + math.sin(g + .2) * r)], fill=(255, 232, 170, a))
    luzcapa(fr, f)


# =================================================================== 6 · EL TECLADO
def teclado(lit):
    """420x540. lit = tecla encendida ('' ninguna)."""
    def f():
        c = L2(420, 540)
        c.rrect(8, 8, 412, 532, 40, (150, 140, 190))
        for i, n in enumerate('123456789*0#'):
            x = 40 + (i % 3) * 118; y = 44 + (i // 3) * 118
            on = n == lit
            c.rrect(x, y, x + 104, y + 100, 22, GOLD if on else (52, 40, 86))
            c.texto(x + 52, y + 50, n, 62, OUT if on else CREAM)
        return c.fin()
    return mk(('tteclado', lit), f)


def pantalla(txt, ok):
    def f():
        c = L2(420, 130)
        c.rrect(8, 8, 412, 122, 26, (26, 60, 50) if ok else (20, 36, 62))
        for i in range(4):
            x = 66 + i * 96
            if i < len(txt): c.texto(x, 66, txt[i], 84, (150, 255, 180) if ok else CYAN)
            else: c.rrect(x - 26, 88, x + 26, 98, 4, (90, 130, 170), ow=0)
        return c.fin()
    return mk(('tpant', txt, ok), f)


def t_teclado(s):
    D = s['dur']; ts = s.get('t_teclas', [D * .30, D * .45, D * .59, D * .73]); abre = s.get('t_abre', ts[-1] + .28)
    def draw(fr, t):
        fondo(fr, bg_pasillo())
        E.titulo(fr, t, '*7304*', 150, 540)
        # puerta secreta
        ab = eo(pr(t, abre, .4))
        def hueco(d):
            d.rounded_rectangle((700, 710, 1010, 1150), 16, fill=(20, 8, 40, 255), outline=OUT + (255,), width=8)
            if ab > 0:
                d.rounded_rectangle((716, 726, 994, 1140), 10, fill=(255, 190, 110, int(150 * ab)))
        luzcapa(fr, hueco)
        R.put(fr, mk('tpuerta', _puerta), 700, 1150, 1 - .86 * ab, 1, anchor=(6, 446))
        n = sum(t >= x for x in ts)
        lit = ''
        for k, x in enumerate(ts):
            if x <= t < x + .26: lit = '7304'[k]
        p = eb(pr(t, 0, .35))
        R.put(fr, pantalla('7304'[:n], n == 4 and t >= abre), 370, 700, .82 * p, .82 * p, anchor=(210, 65))
        R.put(fr, teclado(lit), 370, 965 , .76 * p, .76 * p, anchor=(210, 270))
        if lit:
            i = '123456789*0#'.index(lit)
            kx = 370 + (92 + (i % 3) * 118 - 210) * .76; ky = 965 + (94 + (i // 3) * 118 - 270) * .76
            E.destello(fr, kx + 34, ky - 30, t, .2, 1.4)
        E.GU(fr, 110, G + 40, .48, 'concentrado' if n < 4 else ('asombro' if t > abre else 'feliz'), boca=.7 if t > abre else 0, pose='senala' if t < abre else 'orejas', brazos=1., mira=(1, 0), sy=.42 * idle(t, 8))
        if t < abre:
            E.FL(fr, 620, G + 45, .46, 'feliz', gafas=1, cuello=.3 + .3 * math.sin(t * 5), ala='senala', flip=False, sy=.46 * idle(t, 6))
        else:
            FLA(fr, 620, G + 45, .46, emo='asombro', cuello=.8, ala='abre', mira=(-1, 0), flip=False)
            golpe(fr, '[¡CRIIIC!]', 840, 700, t, abre + .05, 66, 8)
    return draw


def _puerta():
    c = L2(322, 452)
    c.rrect(6, 6, 316, 446, 14, MADERA)
    for y0 in (40, 240): c.rrect(44, y0, 278, y0 + 168, 12, MADERA_D, ow=4)
    c.elipse(272, 226, 15, 15, GOLD, ow=4)
    return c.fin()


# =================================================================== 7 · EL CUARTO
def t_cuarto(s):
    D = s['dur']; abre = s.get('t_cofre', D * .24); pregunta = s.get('t_pregunta', D * .5)
    def draw(fr, t):
        fondo(fr, bg_secreto())
        E.titulo(fr, t, '¿TE *ATREVES*?', 130, 548)
        # haz del proyector y película en la pantalla
        parp = 1 - .18 * (int(t * 12) % 3 == 0)
        luzcapa(fr, lambda d: d.polygon([(372, 806), (615, 700), (615, 920), (372, 836)], fill=(220, 240, 255, int(110 * parp))), 3)
        def peli(L, ox, oy):
            ImageDraw.Draw(L).rectangle((0, 0, L.width, L.height), fill=(150, 190, 230, int(150 * parp)))
            x = 720 + math.sin(t * 2.2) * 80 + ox
            E.FL(L, x, 925 + oy - abs(math.sin(t * 8)) * 24, .3, 'feliz', gafas=1, cuello=.5 + .5 * math.sin(t * 8), ala='arriba' if int(t * 6) % 2 else 'abre')
            d = ImageDraw.Draw(L)
            for k in range(3):
                y = (t * 260 + k * 90) % L.height
                d.line([(0, y), (L.width, y)], fill=(255, 255, 255, 120), width=3)
        E.clip(fr, (616, 702, 956, 924), peli)
        R.put(fr, mesa(260), 250, 1000, .82, .82, anchor=(130, 164))
        R.put(fr, proyector(), 270, 886, .92, .92, anchor=(120, 204))
        for k, (x, r) in enumerate(((215, 0), (318, 1))):
            R.put(fr, carrete(), x, 766, .82, .82, rot=-(t * 220 + r * 40) % 360, anchor=(55, 55))
        # velas
        for k, (x, y, sc) in enumerate(((34, 1195, .72), (292, 1100, .55), (1044, 1185, .9), (884, 1205, .62))):
            luzcapa(fr, lambda d: d.ellipse((x - 90, y - 200, x + 90, y - 30), fill=(255, 170, 80, 55 + int(25 * math.sin(t * 11 + k)))), 24)
            R.put(fr, vela((int(t * 9) + k) % 3), x, y, sc, sc, anchor=(45, 180))
        # la caja se abre con billetes
        cx, cy = 745, 1170
        q = eo(pr(t, abre, .35))
        tapa_y = cy - 106 - 112 * q
        tiemblo = math.sin(t * 50) * 3 if abre - .35 < t < abre else 0
        if q > 0:
            luzcapa(fr, lambda d: d.polygon([(cx - 104, cy - 112), (cx - 170, cy - 330), (cx + 170, cy - 330), (cx + 104, cy - 112)], fill=(255, 224, 138, int(95 * q))), 10)
        R.put(fr, cofre_tapa(), cx + tiemblo, tapa_y, .92, .92 * (1 - .22 * q), anchor=(140, 102))
        if q > 0:
            for k in range(5):
                R.put(fr, fajo(), cx - 72 + k * 36, cy - 108 - (k % 2) * 20 * q, .56 * q, .56 * q, rot=(k - 2) * 9, anchor=(90, 90))
            for k in range(8):
                u = ((t - abre) * .8 + k * .13) % 1
                R.put(fr, billete(), cx + (k - 3.5) * 36 + math.sin(t * 4 + k) * 20, cy - 150 - u * 190 * q, .5, .5 * (.5 + .5 * abs(math.cos(t * 5 + k))), rot=math.sin(t * 3 + k) * 40, alpha=min(1, (1 - u) * 2.5) * q, anchor=(80, 48))
        R.put(fr, cofre_base(), cx, cy, .92, .92, anchor=(140, 150))
        golpe(fr, '[¡TAC!]', 590, 990, t, abre, 56, -8, abre + .8)
        # reliquia dorada en el piso
        B_rayos(fr, 450, 1150, t, 190, 40, 9)
        R.put(fr, reliquia(), 450, 1178 + math.sin(t * 4) * 3, .74, .74, rot=-5, anchor=(reliquia().width / 2, reliquia().height / 2 + 20))
        for i, (dx, dy) in enumerate(((-110, -40), (100, -50), (10, -70))): E.destello(fr, 450 + dx, 1170 + dy, t, i * .31, 1.1)
        # Gus tiembla y Flami sonríe
        tiembla = math.sin(t * 55) * 6
        E.GU(fr, 140 + tiembla, G - 5, .48, 'nervioso' if t < pregunta else 'grito', boca=.2 if t < pregunta else .8, pose='pecho' if t < pregunta else 'orejas', brazos=1., mira=(1, 0), sudor=True, rot=tiembla * .5)
        for k in range(3):
            if int(t * 8) % 2:
                ImageDraw.Draw(fr).arc((26 - k * 4, 920 + k * 48, 66 - k * 4, 984 + k * 48), 100, 260, fill=(255, 241, 234, 220), width=6)
        E.FL(fr, 965, 1105, .44, 'guino' if t > pregunta else 'feliz', boca=.5 if t > pregunta else .2, gafas=0, cuello=.4 + .3 * math.sin(t * 3), ala='saluda' if t > pregunta else 'cadera', flip=True, sy=.44 * idle(t, 6))
    return draw
