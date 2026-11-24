#!/usr/bin/env python3
"""Plantilla de videos gta6encyclopedia — motor de render.
Uso: python3 render.py videos/mi-video.json [salida.mp4] [--frames 1.5,7.2]
Lee un JSON de escenas y genera un MP4 1080x1920 30 fps sin audio.
"""
import json, math, os, sys, subprocess, shutil, tempfile, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

BASE = os.path.dirname(os.path.abspath(__file__))
A = lambda *p: os.path.join(BASE, 'assets', *p)
W, H, FPS = 1080, 1920, 30
SAFE_TOP, SAFE_BOT, MX = int(H * .15), int(H * .80), 80   # 288 / 1536
CX = W // 2

# ---------- marca ----------
BG = (26, 16, 48); PURPLE_D = (42, 20, 72); PURPLE = (122, 63, 191)
CREAM = (255, 241, 234); ORANGE = (255, 179, 107); PINK = (255, 107, 139)
GRAD = [(255, 224, 138), (255, 122, 168), (194, 89, 255)]

_fc = {}
def F(kind, size):
    key = (kind, size)
    if key not in _fc:
        if kind == 'title':
            _fc[key] = ImageFont.truetype(A('fuentes', 'BricolageGrotesque-variable.ttf'), size)
            _fc[key].set_variation_by_axes([96, 800, 100])
        else:
            _fc[key] = ImageFont.truetype(A('fuentes', f'Figtree-{kind}.ttf'), size)
        _fc[key].kind = kind
    return _fc[key]

def grad_img(w, h, horizontal=True):
    g = Image.new('RGB', (256, 1))
    for x in range(256):
        t = x / 255 * 2; i = min(int(t), 1); f = t - i
        c = tuple(int(GRAD[i][k] + (GRAD[i + 1][k] - GRAD[i][k]) * f) for k in range(3))
        g.putpixel((x, 0), c)
    g = g.resize((w, h), Image.BILINEAR) if horizontal else g.rotate(-90, expand=True).resize((w, h))
    return g

# ---------- easing ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, start, dur=.45): return clamp((t - start) / dur)

# ---------- texto enriquecido ----------
# *palabra* = naranja ; [palabra] = degradado de marca
def tokens(text):
    """Palabras con estilo: c=crema, o=naranja (*x*), g=degradado ([x])."""
    res, style, word, wst, sp, pend = [], 'c', '', 'c', False, False
    def flush():
        nonlocal word, sp
        if word: res.append((word, wst, sp)); sp = False
        word = ''
    for ch in text:
        if ch in '*[]':
            flush()
            style = ('c' if style == 'o' else 'o') if ch == '*' else ('g' if ch == '[' else 'c')
            continue
        if ch == ' ':
            flush(); sp = bool(res); continue
        if not word: wst = style
        word += ch
    flush()
    return res

MAX_LINEAS_TITULO = 2

def rich(text, font, maxw=2000, align='center', lh=1.08, shadow=True, base=CREAM, max_lines=None):
    """Devuelve sprite RGBA con el texto enriquecido envuelto en maxw.
    Los títulos (Bricolage) nunca pasan de MAX_LINEAS_TITULO: se achica la letra hasta que quepan."""
    if max_lines is None and getattr(font, 'kind', '') == 'title': max_lines = MAX_LINEAS_TITULO
    toks = tokens(text)
    space = font.getlength(' ')
    lines, cur, curw = [], [], 0
    for w, st, sp in toks:
        if w == '\\n':
            lines.append(cur); cur, curw = [], 0; continue
        ww = font.getlength(w)
        add = (space if (cur and sp) else 0) + ww
        if cur and curw + add > maxw:
            lines.append(cur); cur, curw = [], 0; add = ww
        cur.append((w, st, curw + add - ww)); curw += add
    if cur: lines.append(cur)
    if max_lines and len(lines) > max_lines and font.size > 30:
        return rich(text, F(font.kind, int(font.size * .93)), maxw, align, lh, shadow, base, max_lines)
    asc, desc = font.getmetrics()
    lhpx = int(font.size * lh)
    widths = [(l[-1][2] + font.getlength(l[-1][0])) if l else 0 for l in lines]
    bw = int(max(widths) if widths else 1) + 40
    bh = lhpx * (len(lines) - 1) + asc + desc + 40
    masks = {k: Image.new('L', (bw, bh), 0) for k in 'cog'}
    dr = {k: ImageDraw.Draw(m) for k, m in masks.items()}
    boxes = []
    for li, l in enumerate(lines):
        lw = widths[li]
        ox = 20 + ((bw - 40 - lw) / 2 if align == 'center' else 0)
        for w, st, x in l:
            dr[st].text((ox + x, 20 + li * lhpx), w, font=font, fill=255)
            boxes.append((int(ox + x) - 16, int(li * lhpx), int(ox + x + font.getlength(w)) + 16, int(20 + li * lhpx + asc + desc) + 18))
    out = Image.new('RGBA', (bw, bh), (0, 0, 0, 0))
    if shadow:
        allm = ImageChops.lighter(ImageChops.lighter(masks['c'], masks['o']), masks['g'])
        sh = Image.new('RGBA', (bw, bh), (10, 4, 24, 0))
        sh.putalpha(allm.filter(ImageFilter.GaussianBlur(9)).point(lambda v: min(255, int(v * 1.6))))
        out = Image.alpha_composite(out, sh)
    for k, col in (('c', base), ('o', ORANGE)):
        lay = Image.new('RGBA', (bw, bh), col + (0,)); lay.putalpha(masks[k])
        out = Image.alpha_composite(out, lay)
    g = grad_img(bw, bh).convert('RGBA'); g.putalpha(masks['g'])
    out = Image.alpha_composite(out, g)
    out.info['words'] = [(max(0, a), max(0, b), min(bw, c), min(bh, d)) for a, b, c, d in boxes]
    return out

def pill(text, font, fg=BG, bg=None, padx=34, pady=16, gradient=True, outline=None):
    tw = int(font.getlength(text)); asc, desc = font.getmetrics()
    w, h = tw + padx * 2, asc + desc + pady * 2
    S = 2
    m = Image.new('L', (w * S, h * S), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=h * S // 2, fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    if gradient: base = grad_img(w, h).convert('RGBA')
    else: base = Image.new('RGBA', (w, h), bg + (255,))
    base.putalpha(m)
    if outline:
        o = Image.new('L', (w * S, h * S), 0)
        ImageDraw.Draw(o).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=h * S // 2, outline=255, width=4 * S)
        ol = Image.new('RGBA', (w, h), outline + (0,)); ol.putalpha(o.resize((w, h), Image.LANCZOS))
        base = Image.alpha_composite(base, ol)
    ImageDraw.Draw(base).text((padx, pady), text, font=font, fill=fg)
    return base

# ---------- íconos (dibujados a 4x y reducidos) ----------
def icon(name, size, color=CREAM, accent=ORANGE):
    S = 4; s = size * S; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lw = max(2, int(s * .07)); c = color + (255,); a = accent + (255,)
    def R(x0, y0, x1, y1): return [x0 * s, y0 * s, x1 * s, y1 * s]
    if name == 'crosshair':
        d.ellipse(R(.12, .12, .88, .88), outline=c, width=lw)
        d.ellipse(R(.38, .38, .62, .62), outline=a, width=lw)
        for (x0, y0, x1, y1) in [(.5, 0, .5, .3), (.5, .7, .5, 1), (0, .5, .3, .5), (.7, .5, 1, .5)]:
            d.line(R(x0, y0, x1, y1), fill=c, width=lw)
    elif name == 'bag':
        d.ellipse(R(.14, .3, .86, .96), fill=a)
        d.polygon([(.34 * s, .34 * s), (.66 * s, .34 * s), (.74 * s, .1 * s), (.26 * s, .1 * s)], fill=a)
        d.rectangle(R(.3, .3, .7, .38), fill=c)
        f = F('title', int(s * .42)); d.text((.5 * s, .64 * s), '$', font=f, fill=BG + (255,), anchor='mm')
    elif name == 'safe':
        d.rounded_rectangle(R(.1, .1, .9, .86), radius=s * .08, fill=c)
        d.ellipse(R(.3, .26, .7, .66), outline=BG + (255,), width=lw)
        d.line(R(.5, .46, .62, .36), fill=a, width=lw)
        d.rectangle(R(.18, .86, .3, .94), fill=c); d.rectangle(R(.7, .86, .82, .94), fill=c)
    elif name == 'van':
        d.rounded_rectangle(R(.04, .28, .7, .74), radius=s * .05, fill=c)
        d.polygon([(.7 * s, .4 * s), (.86 * s, .4 * s), (.96 * s, .58 * s), (.96 * s, .74 * s), (.7 * s, .74 * s)], fill=c)
        d.polygon([(.74 * s, .45 * s), (.84 * s, .45 * s), (.9 * s, .56 * s), (.74 * s, .56 * s)], fill=BG + (255,))
        for x in (.22, .78):
            d.ellipse(R(x - .1, .64, x + .1, .84), fill=BG + (255,)); d.ellipse(R(x - .06, .68, x + .06, .8), fill=a)
    elif name == 'card':
        d.rounded_rectangle(R(.2, .06, .8, .94), radius=s * .07, fill=a)
        d.rounded_rectangle(R(.26, .12, .74, .88), radius=s * .05, outline=BG + (255,), width=lw // 2)
        star(d, .5 * s, .48 * s, .2 * s, BG + (255,))
    elif name == 'box':
        d.polygon([(.5 * s, .08 * s), (.92 * s, .28 * s), (.5 * s, .48 * s), (.08 * s, .28 * s)], fill=a)
        d.polygon([(.08 * s, .28 * s), (.5 * s, .48 * s), (.5 * s, .94 * s), (.08 * s, .74 * s)], fill=c)
        d.polygon([(.92 * s, .28 * s), (.5 * s, .48 * s), (.5 * s, .94 * s), (.92 * s, .74 * s)], fill=(220, 200, 210, 255))
    elif name == 'house':
        d.polygon([(.5 * s, .06 * s), (.96 * s, .46 * s), (.04 * s, .46 * s)], fill=a)
        d.rectangle(R(.16, .44, .84, .92), fill=c)
        d.rounded_rectangle(R(.42, .6, .58, .92), radius=s * .03, fill=BG + (255,))
    elif name == 'heart':
        heart(d, s, a)
    elif name == 'pause':
        d.rounded_rectangle(R(.06, .06, .94, .94), radius=s * .18, outline=c, width=lw)
        d.rounded_rectangle(R(.32, .28, .44, .72), radius=s * .03, fill=a)
        d.rounded_rectangle(R(.56, .28, .68, .72), radius=s * .03, fill=a)
    elif name == 'updown':
        d.polygon([(.3 * s, .06 * s), (.54 * s, .4 * s), (.06 * s, .4 * s)], fill=a)
        d.rectangle(R(.24, .38, .36, .92), fill=a)
        d.polygon([(.7 * s, .94 * s), (.94 * s, .6 * s), (.46 * s, .6 * s)], fill=PINK + (255,))
        d.rectangle(R(.64, .08, .76, .62), fill=PINK + (255,))
    elif name == 'check':
        d.line([(.18 * s, .52 * s), (.42 * s, .76 * s), (.84 * s, .26 * s)], fill=c, width=int(lw * 1.6), joint='curve')
    elif name == 'arrow_down':
        d.rectangle(R(.4, .06, .6, .56), fill=c)
        d.polygon([(.12 * s, .5 * s), (.88 * s, .5 * s), (.5 * s, .94 * s)], fill=c)
    elif name == 'plus':
        d.rounded_rectangle(R(.4, .1, .6, .9), radius=s * .05, fill=c)
        d.rounded_rectangle(R(.1, .4, .9, .6), radius=s * .05, fill=c)
    return im.resize((size, size), Image.LANCZOS)

def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5; rr = r if i % 2 == 0 else r * .45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)

def heart_pts(s, n=80):
    pts = []
    for i in range(n):
        t = i / n * 2 * math.pi
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((s / 2 + x * s / 36, s * .46 - y * s / 36))
    return pts

def heart(d, s, fill): d.polygon(heart_pts(s), fill=fill)

def heart_sprite(size, fill_frac, active=True):
    """Corazón con relleno de degradado de 0 a 1 (de abajo hacia arriba)."""
    S = 4; s = size * S
    m = Image.new('L', (s, s), 0); heart(ImageDraw.Draw(m), s, 255)
    m = m.resize((size, size), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), PURPLE_D + (0,))
    base = Image.new('RGBA', (size, size), (60, 34, 96, 255)); base.putalpha(m)
    out = Image.alpha_composite(out, base)
    if fill_frac > 0:
        g = grad_img(size, size, horizontal=False).convert('RGBA')
        fm = Image.new('L', (size, size), 0)
        ImageDraw.Draw(fm).rectangle((0, int(size * (1 - fill_frac)), size, size), fill=255)
        g.putalpha(ImageChops.multiply(m, fm)); out = Image.alpha_composite(out, g)
    o = Image.new('L', (s, s), 0); ImageDraw.Draw(o).line(heart_pts(s) + [heart_pts(s)[0]], fill=255, width=int(s * .04))
    ol = Image.new('RGBA', (size, size), (CREAM if active else (120, 90, 150)) + (0,))
    ol.putalpha(o.resize((size, size), Image.LANCZOS)); out = Image.alpha_composite(out, ol)
    return out

# ---------- composición ----------
def place(canvas, spr, cx, cy, alpha=1., scale=1.):
    if alpha <= 0.003 or scale <= 0.01: return
    if abs(scale - 1) > .005:
        spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
    if alpha < .999:
        spr = spr.copy(); spr.putalpha(spr.getchannel('A').point(lambda v: int(v * alpha)))
    comp(canvas, spr, int(cx - spr.width / 2), int(cy - spr.height / 2))

def anim_words(canvas, spr, cx, cy, t, start, stagger=.07, dur=.42):
    words = spr.info['words']
    if prog(t, start + stagger * (len(words) - 1), dur) >= 1:
        place(canvas, spr, cx, cy); return
    if 'crops' not in spr.info:
        spr.info['crops'] = [spr.crop(b) for b in words]
    x0, y0 = cx - spr.width / 2, cy - spr.height / 2
    for i, (b, cr) in enumerate(zip(words, spr.info['crops'])):
        p = prog(t, start + i * stagger, dur)
        if p <= 0: continue
        e = ease_out(p)
        place(canvas, cr, x0 + (b[0] + b[2]) / 2, y0 + (b[1] + b[3]) / 2 + (1 - e) * 55, e, .75 + .25 * ease_back(p))

def anim_in(canvas, spr, cx, cy, t, start, kind='up', dur=.45):
    p = prog(t, start, dur)
    if p <= 0: return
    if kind == 'up' and len(spr.info.get('words', [])) > 1:
        anim_words(canvas, spr, cx, cy, t, start); return
    if kind == 'up': place(canvas, spr, cx, cy + (1 - ease_out(p)) * 70, ease_out(p))
    elif kind == 'pop': place(canvas, spr, cx, cy, clamp(p * 2.5), .35 + .65 * ease_back(p))
    elif kind == 'left': place(canvas, spr, cx - (1 - ease_out(p)) * 120, cy, ease_out(p))
    elif kind == 'fade': place(canvas, spr, cx, cy, ease_out(p))

def card_panel(w, h, alpha=200, radius=40, border=True):
    S = 2; m = Image.new('L', (w * S, h * S), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=radius * S, fill=255)
    m = m.resize((w, h), Image.LANCZOS)
    p = Image.new('RGBA', (w, h), PURPLE_D + (0,)); p.putalpha(m.point(lambda v: v * alpha // 255))
    if border:
        o = Image.new('L', (w * S, h * S), 0)
        ImageDraw.Draw(o).rounded_rectangle((0, 0, w * S - 1, h * S - 1), radius=radius * S, outline=255, width=3 * S)
        g = grad_img(w, h).convert('RGBA'); g.putalpha(o.resize((w, h), Image.LANCZOS).point(lambda v: v * 200 // 255))
        p = Image.alpha_composite(p, g)
    return p

# ---------- capas fijas ----------
class Stage:
    def __init__(self):
        bg = Image.open(A('fondos', 'atardecer-leonida.png')).convert('RGB')
        scale = (H + 80) / bg.height
        bg = bg.resize((int(bg.width * scale), H + 80), Image.LANCZOS)
        ov = Image.new('RGB', bg.size, BG)
        self.bg = Image.blend(bg, ov, .60)            # #1A1030 al 60 %
        self.logo = Image.open(A('logos', 'icono-1024.png')).convert('RGBA').resize((135, 135), Image.LANCZOS)
        self.hlogo = Image.open(A('logos', 'logo-horizontal-para-fondo-oscuro.png')).convert('RGBA')
        g = Image.new('L', (64, 64), 0); ImageDraw.Draw(g).ellipse((8, 8, 56, 56), fill=255)
        self.dot = g.filter(ImageFilter.GaussianBlur(7))
        import random; rnd = random.Random(7)
        self.parts = [(rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(8, 30), rnd.uniform(.2, .6),
                       rnd.choice([ORANGE, PINK, (194, 89, 255), CREAM]), rnd.uniform(0, 6.28)) for _ in range(22)]

    def background(self, T):
        cx = (self.bg.width - W) / 2 + math.sin(T * .09) * min(260, (self.bg.width - W) / 2 - 2)
        cy = 40 + math.sin(T * .3) * 30
        fr = self.bg.crop((int(cx), int(cy), int(cx) + W, int(cy) + H)).convert('RGBA')
        for (x, y, sp, a, col, ph) in self.parts:
            yy = (y - T * sp * 3) % (H + 100) - 50
            xx = x + math.sin(T * .6 + ph) * 25
            lay = Image.new('RGBA', (64, 64), col + (0,)); lay.putalpha(self.dot.point(lambda v: int(v * a * (.6 + .4 * math.sin(T * 2 + ph)))))
            fr.alpha_composite(lay, (int(xx) - 32, int(yy) - 32))
        return fr

    def corner_logo(self, fr, a=1.0):
        if a <= 0: return
        lg = self.logo
        if a < 1:
            lg = lg.copy(); lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
        fr.alpha_composite(lg, (MX - 20, SAFE_TOP + 6))

# ---------- subtítulos ----------
OPT = {'sin_panel': False, 'sin_logo': False}

class Subs:
    def __init__(self, text, dur, size=62):
        self.f = F('800', size); self.words = text.split(); self.dur = dur
        maxw = W - 2 * MX - 80; space = self.f.getlength(' ')
        lines, cur, cw = [], [], 0
        for w in self.words:
            ww = self.f.getlength(w)
            if cur and cw + space + ww > maxw: lines.append(cur); cur, cw = [], 0
            cur.append(w); cw += (space if cw else 0) + ww
        if cur: lines.append(cur)
        self.lines = lines; self.lh = round(size * 1.258)
        self.box_h = self.lh * len(lines) + 44
        self.box_w = int(max(sum(self.f.getlength(w) for w in l) + space * (len(l) - 1) for l in lines)) + 80
        self.y0 = SAFE_BOT - 30 - self.box_h
        self.panel = card_panel(self.box_w, self.box_h, alpha=215, radius=34, border=False)
        # tiempo por palabra (proporcional a letras)
        n = sum(len(w) + 2 for w in self.words); acc = 0; self.wt = []
        span = max(.5, dur - .35)
        for w in self.words: self.wt.append(acc / n * span); acc += len(w) + 2

    def draw(self, fr, t):
        a = ease_out(prog(t, 0, .2))
        if not OPT['sin_panel']: place(fr, self.panel, CX, self.y0 + self.box_h / 2 + (1 - a) * 20, a * .92)
        d = ImageDraw.Draw(fr); space = self.f.getlength(' '); k = 0
        for li, l in enumerate(self.lines):
            lw = sum(self.f.getlength(w) for w in l) + space * (len(l) - 1)
            x = CX - lw / 2; y = self.y0 + 22 + li * self.lh + (1 - a) * 20
            for w in l:
                on = t >= self.wt[k]; cur = on and (k + 1 >= len(self.wt) or t < self.wt[k + 1])
                col = ORANGE if cur else (CREAM if on else (170, 150, 190))
                if OPT['sin_panel']: d.text((x, y), w, font=self.f, fill=col + (int(255 * a),), stroke_width=max(5, self.f.size // 9), stroke_fill=(26, 16, 48, int(255 * a)))
                else: d.text((x, y), w, font=self.f, fill=col + (int(255 * a),))
                x += self.f.getlength(w) + space; k += 1

# ---------- escenas ----------
TOP = SAFE_TOP + 190        # 438: inicio de la zona de contenido (bajo el logo)

def scene_hook(s, st):
    badge = pill(s.get('serie', ''), F('700', 40), fg=CREAM, bg=PURPLE, gradient=False)
    part = rich(f"[{s['parte']}]", F('title', 150))
    q = rich(s['texto'], F('title', 104), W - 2 * MX)
    def draw(fr, t):
        anim_in(fr, badge, CX, TOP + 40, t, 0.0, 'fade', .25)
        p = prog(t, .05, .4)
        place(fr, part, CX, TOP + 175, clamp(p * 3), 1.6 - .6 * ease_out(p))
        anim_in(fr, q, CX, TOP + 290 + q.height / 2, t, .3, 'up', .4)
        # subrayado animado
        p2 = ease_out(prog(t, .7, .6)); y = TOP + 300 + q.height
        if p2 > 0:
            g = grad_img(int(500 * p2) + 1, 10).convert('RGBA'); fr.alpha_composite(g, (CX - 250, int(y)))
    return draw

def scene_title(s, st):
    kick = rich(s.get('kicker', ''), F('700', 46), W - 2 * MX, shadow=True, base=ORANGE) if s.get('kicker') else None
    tt = rich(s['texto'], F('title', 120), W - 2 * MX)
    ic = icon(s['icono'], 230) if s.get('icono') else None
    def draw(fr, t):
        y = TOP + 40
        if ic is not None:
            anim_in(fr, ic, CX, y + 120, t, 0, 'pop', .5)
            fr_t = t
            y += 270
        if kick: anim_in(fr, kick, CX, y + kick.height / 2, t, .15, 'up'); y += kick.height
        anim_in(fr, tt, CX, y + tt.height / 2, t, .3, 'up')
    return draw

def scene_map(s, st):
    title = rich(s['texto'], F('title', 80), W - 2 * MX)
    zona = rich(s['zona'], F('700', 40), 800, base=ORANGE) if s.get('zona') else None
    mw, mh = 900, 560
    f_lbl = F('800', 34 * 2); f_sm = F('600', 24 * 2)
    def map_sprite(t):
        S = 2; im = Image.new('RGBA', (mw * S, mh * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, mw * S - 1, mh * S - 1), radius=60, fill=(20, 12, 40, 230))
        # mar (izquierda abajo) y tierra
        land = [(0, 0), (mw * S, 0), (mw * S, mh * S), (380 * S, mh * S), (300 * S, 470 * S), (180 * S, 430 * S), (120 * S, 330 * S), (0, 300 * S)]
        mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, mw * S - 1, mh * S - 1), radius=60, fill=255)
        lay = Image.new('L', im.size, 0); ImageDraw.Draw(lay).polygon(land, fill=255)
        landc = Image.new('RGBA', im.size, (52, 28, 88, 255)); landc.putalpha(ImageChops.multiply(lay, mask))
        im.alpha_composite(landc)
        for k in range(4):  # olas
            yy = (360 + k * 45) * S; xx = 30 * S + k * 20 * S
            d.arc((xx, yy, xx + 60 * S, yy + 30 * S), 200, 340, fill=(122, 63, 191, 200), width=3 * S)
        # calles (se dibujan progresivamente)
        roads = [((60, 120), (860, 120)), ((300, 40), (300, 420)), ((560, 40), (560, 540)), ((300, 300), (860, 300))]
        pr = ease_out(prog(t, .1, .8))
        for (a, b) in roads:
            bx = a[0] + (b[0] - a[0]) * pr; by = a[1] + (b[1] - a[1]) * pr
            d.line((a[0] * S, a[1] * S, bx * S, by * S), fill=(122, 90, 170, 255), width=10 * S)
        # Hamlet
        hx, hy = 300, 210
        ph = ease_back(prog(t, .5, .4))
        if ph > 0:
            r = 18 * ph * S; d.ellipse((hx * S - r, hy * S - r, hx * S + r, hy * S + r), fill=CREAM + (255,))
            d.text((hx * S, (hy - 34) * S), s.get('referencia', 'Hamlet'), font=f_lbl, fill=CREAM + (255,), anchor='ms')
        # ruta punteada hacia el este
        nx, ny = 700, 230
        pr2 = ease_out(prog(t, 1.0, 1.0))
        n = 14
        for i in range(n):
            if i / n > pr2: break
            if i % 2: continue
            x0 = hx + (nx - hx) * i / n; y0 = hy + (ny - hy) * i / n
            x1 = hx + (nx - hx) * (i + 1) / n; y1 = hy + (ny - hy) * (i + 1) / n
            d.line((x0 * S, y0 * S, x1 * S, y1 * S), fill=ORANGE + (255,), width=8 * S)
        # pin
        pp = prog(t, 1.8, .5)
        if pp > 0:
            drop = (1 - ease_back(pp)) * -120
            py = ny + drop
            pulse = (t * 1.2) % 1
            if pp >= 1:
                rr = (30 + 60 * pulse) * S
                d.ellipse((nx * S - rr, ny * S - rr * .45, nx * S + rr, ny * S + rr * .45), outline=ORANGE + (int(255 * (1 - pulse)),), width=4 * S)
            d.ellipse(((nx - 34) * S, (py - 100) * S, (nx + 34) * S, (py - 32) * S), fill=ORANGE + (255,))
            d.polygon([((nx - 30) * S, (py - 56) * S), ((nx + 30) * S, (py - 56) * S), (nx * S, py * S)], fill=ORANGE + (255,))
            d.ellipse(((nx - 13) * S, (py - 79) * S, (nx + 13) * S, (py - 53) * S), fill=BG + (255,))
            if pp >= 1:
                d.text((nx * S, (ny + 50) * S), s.get('destino', 'Nave'), font=f_lbl, fill=ORANGE + (255,), anchor='mt')
        # brújula + nota
        d.text(((mw - 40) * S, 40 * S), 'N ↑', font=f_sm, fill=(200, 180, 220, 255), anchor='rt')
        d.text(((mw - 40) * S, (mh - 30) * S), 'mapa ilustrativo', font=f_sm, fill=(150, 130, 180, 255), anchor='rb')
        return im.resize((mw, mh), Image.LANCZOS)
    def draw(fr, t):
        anim_in(fr, title, CX, TOP + title.height / 2, t, 0, 'up')
        y = TOP + title.height + 10
        p = ease_out(prog(t, .05, .4))
        place(fr, map_sprite(t), CX, y + mh / 2 + (1 - p) * 60, p)
        if zona: anim_in(fr, zona, CX, y + mh + 20 + zona.height / 2, t, 2.0, 'up')
    return draw

def scene_step(s, st):
    num = pill(s['paso'], F('title', 64), fg=BG)
    ic = icon(s['icono'], 260)
    tt = rich(s['texto'], F('title', 112), W - 2 * MX)
    def draw(fr, t):
        anim_in(fr, num, CX, TOP + 50, t, 0, 'pop', .4)
        p = prog(t, .15, .5)
        if p > 0:
            wob = math.sin(t * 5) * 4 * (1 if p >= 1 else 0)
            place(fr, ic.rotate(wob, resample=Image.BICUBIC), CX, TOP + 270, clamp(p * 2.5), .35 + .65 * ease_back(p))
        anim_in(fr, tt, CX, TOP + 450 + tt.height / 2, t, .35, 'up')
    return draw

def fmt(n, sep='.'):
    return f"{int(n):,}".replace(',', sep)

def scene_counter(s, st):
    ic = icon(s['icono'], 230)
    lab = rich(s['texto'], F('title', 84), W - 2 * MX)
    f_num = F('title', 200); sub = rich(s.get('nota', ''), F('600', 44), W - 2 * MX) if s.get('nota') else None
    def draw(fr, t):
        anim_in(fr, ic, CX, TOP + 115, t, 0, 'pop', .5)
        anim_in(fr, lab, CX, TOP + 260 + lab.height / 2, t, .15, 'up')
        p = ease_out(prog(t, .5, 1.6))
        if t >= .5:
            v = s['desde'] + (s['hasta'] - s['desde']) * p
            txt = f"[{s.get('prefijo', '$')}{fmt(round(v / 10) * 10)}{s.get('sufijo', '') if p >= 1 else ''}]"
            num = rich(txt, f_num, 2000)
            sc = 1 + (.12 * math.sin(clamp((t - 2.1) / .3) * math.pi) if t > 2.1 else 0)
            place(fr, num, CX, TOP + 300 + lab.height + 130, 1, sc)
        if sub: anim_in(fr, sub, CX, TOP + 300 + lab.height + 300, t, 2.2, 'up')
    return draw

def scene_checklist(s, st):
    tt = rich(s['titulo'], F('title', 90), W - 2 * MX)
    items = [(icon(it['icono'], 120), rich(it['texto'], F('title', 66), 620, align='left', shadow=True)) for it in s['items']]
    chk = icon('check', 64, color=BG)
    box_w = W - 2 * MX
    rows = [card_panel(box_w, 190, alpha=210, radius=36) for _ in items]
    def draw(fr, t):
        anim_in(fr, tt, CX, TOP + tt.height / 2, t, 0, 'up')
        y = TOP + tt.height + 30
        for i, ((ic, tx), row) in enumerate(zip(items, rows)):
            st0 = .3 + i * s.get('paso', 1.3)
            anim_in(fr, row, CX, y + 95, t, st0, 'left', .4)
            p = ease_out(prog(t, st0, .4))
            if p > 0:
                place(fr, ic, MX + 100 - (1 - p) * 120, y + 95, p)
                place(fr, tx, MX + 200 + tx.width / 2 - (1 - p) * 120, y + 95, p)
                # check
                pc = prog(t, st0 + .55, .35)
                if pc > 0:
                    cx = W - MX - 85; r = 46
                    circ = Image.new('RGBA', (r * 8, r * 8), (0, 0, 0, 0))
                    ImageDraw.Draw(circ).ellipse((0, 0, r * 8 - 1, r * 8 - 1), fill=ORANGE + (255,))
                    circ = circ.resize((r * 2, r * 2), Image.LANCZOS); circ.alpha_composite(chk, (r - 32, r - 32))
                    place(fr, circ, cx, y + 95, clamp(pc * 3), .3 + .7 * ease_back(pc))
            y += 220
    return draw

def scene_total(s, st):
    kick = rich(s['texto'], F('title', 80), W - 2 * MX)
    f_num = F('title', 210)
    chips = [(icon(c['icono'], 92), pill(c['texto'], F('800', 52), fg=CREAM, bg=PURPLE_D, gradient=False, outline=ORANGE)) for c in s['chips']]
    def draw(fr, t):
        anim_in(fr, kick, CX, TOP + kick.height / 2, t, 0, 'up')
        p = ease_out(prog(t, .2, 1.3))
        if t >= .2:
            v = s['desde'] + (s['hasta'] - s['desde']) * p
            num = rich(f"[{s.get('prefijo', '~$')}{fmt(round(v / 10) * 10)}]", f_num, 2000)
            place(fr, num, CX, TOP + kick.height + 120, 1, 1 + (.1 * math.sin(clamp((t - 1.5) / .3) * math.pi) if t > 1.5 else 0))
        y = TOP + kick.height + 250
        for i, (ic, ch) in enumerate(chips):
            st0 = 1.4 + i * .45
            tw = ic.width + 24 + ch.width
            x0 = CX - tw / 2
            p2 = prog(t, st0, .4)
            if p2 > 0:
                place(fr, ic, x0 + ic.width / 2, y + 50, clamp(p2 * 2.5), .3 + .7 * ease_back(p2))
                place(fr, ch, x0 + ic.width + 24 + ch.width / 2 + (1 - ease_out(p2)) * 80, y + 50, ease_out(p2))
            y += 102
    return draw

def scene_info(s, st):
    ic = icon(s['icono'], 240)
    tt = rich(s['texto'], F('title', 104), W - 2 * MX)
    sub = rich(s['nota'], F('700', 52), W - 2 * MX - 60, base=CREAM) if s.get('nota') else None
    panel = card_panel(min(W - 2 * MX, sub.width + 60), sub.height + 40, alpha=210) if sub else None
    def draw(fr, t):
        p = prog(t, 0, .5)
        if p > 0:
            bob = math.sin(t * 3.2) * 10 if p >= 1 else 0
            place(fr, ic, CX, TOP + 130 + bob, clamp(p * 2.5), .35 + .65 * ease_back(p))
        anim_in(fr, tt, CX, TOP + 290 + tt.height / 2, t, .2, 'up')
        if sub:
            y = TOP + 320 + tt.height + panel.height / 2
            anim_in(fr, panel, CX, y, t, .55, 'up'); anim_in(fr, sub, CX, y, t, .6, 'up')
    return draw

def scene_levels(s, st):
    N = s.get('nivel', 0)   # 0 = presentación de los 4 niveles
    hs = 130
    f_n = F('title', 44)
    big = rich(f"[{N}/4]", F('title', 150)) if N else rich(s.get('texto', ''), F('title', 104), W - 2 * MX)
    name = rich(f"[{s['nombre']}]", F('title', 88), W - 2 * MX) if s.get('nombre') else None
    desc = rich(s['desc'], F('700', 46), W - 2 * MX - 80) if s.get('desc') else None
    panel = card_panel(min(W - 2 * MX, desc.width + 60), desc.height + 20, alpha=210) if desc else None
    def draw(fr, t):
        y = TOP + 10
        gap = (W - 2 * MX - 4 * hs) / 3
        for i in range(4):
            x = MX + hs / 2 + i * (hs + gap)
            st0 = i * (.22 if N == 0 else .12)
            p = prog(t, st0, .4)
            if p <= 0: continue
            if N == 0: ff = ease_out(prog(t, 1.2 + i * .25, .5)) * ((i + 1) / 4)
            else: ff = ease_out(prog(t, .4 + i * .25, .4)) if i < N else 0
            hsp = heart_sprite(hs, ff, active=(N == 0 or i < N))
            sc = .3 + .7 * ease_back(p)
            if N and i == N - 1 and t > 1.4: sc *= 1 + .08 * math.sin((t - 1.4) * 6)
            place(fr, hsp, x, y + hs / 2, clamp(p * 2.5), sc)
            lab = f_n
            d = ImageDraw.Draw(fr)
            d.text((x, y + hs + 8), str(i + 1), font=f_n, fill=(ORANGE if (N == 0 or i == N - 1) else (150, 125, 180)) + (int(255 * clamp(p * 2)),), anchor='mt')
        yy = y + hs + 70
        if N:
            anim_in(fr, big, CX, yy + big.height / 2 - 20, t, .3, 'pop', .45); yy += big.height - 50
            if name: anim_in(fr, name, CX, yy + name.height / 2, t, .55, 'up'); yy += name.height - 10
            if desc:
                anim_in(fr, panel, CX, yy + panel.height / 2, t, .9, 'up'); anim_in(fr, desc, CX, yy + panel.height / 2, t, .95, 'up')
        else:
            anim_in(fr, big, CX, yy + big.height / 2, t, .3, 'up')
    return draw

def scene_cta(s, st):
    sig = s['siguiente']
    en = s.get('_idioma') == 'en'
    t1 = rich('Follow for' if en else ('Sigue para el' if sig.startswith('#') else 'Sigue para la'), F('title', 110), W - 2 * MX)
    t2 = rich(f"[{sig}]", F('title', 200), W - 2 * MX)
    btn = pill('+ Follow' if en else '+ Seguir', F('800', 60), fg=BG, padx=60, pady=26)
    arrow = icon('arrow_down', 90, color=ORANGE)
    def draw(fr, t):
        anim_in(fr, t1, CX, TOP + 90, t, 0, 'up')
        p = prog(t, .15, .5)
        place(fr, t2, CX, TOP + 290, clamp(p * 3), (1.5 - .5 * ease_out(p)) * (1 + .04 * math.sin(max(0, t - .7) * 6)))
        anim_in(fr, arrow, CX, TOP + 490 + math.sin(t * 8) * 12, t, .5, 'fade')
        pb = prog(t, .6, .4)
        if pb > 0: place(fr, btn, CX, TOP + 630, clamp(pb * 3), (.4 + .6 * ease_back(pb)) * (1 + .05 * math.sin(t * 7)))
    return draw

def scene_end(s, st):
    # logo completo con ".com" (asset propio); el logo de la esquina se desvanece al entrar
    hl = Image.open(A('logos', 'logo-horizontal-com-para-fondo-oscuro.png')).convert('RGBA')
    tw = 960
    lg = hl.resize((tw, int(tw * hl.height / hl.width)), Image.LANCZOS)
    def draw(fr, t):
        p = prog(t, 0, .5)
        place(fr, lg, CX, H / 2, ease_out(p), .85 + .15 * ease_out(p))
    return draw


# ---------- caricatura (experimento 23-nov-2026) ----------
import caricatura as K
_sp = {}
def spr(kind, *a):
    key = (kind,) + a
    if key not in _sp: _sp[key] = getattr(K, kind)(*a)
    return _sp[key]

def put(fr, im, x, y, sx=1., sy=1., rot=0., flip=False, alpha=1., anchor=None):
    """Pone un sprite con el ancla (por defecto: pies, abajo al centro) en (x, y)."""
    ax, ay = anchor or (im.width / 2, im.height - 10)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT); ax = im.width - ax
    w, h = max(1, int(im.width * sx)), max(1, int(im.height * sy))
    if (w, h) != im.size: im = im.resize((w, h), Image.BILINEAR)
    ax *= sx; ay *= sy
    if abs(rot) > .05:
        R = int(math.hypot(w, h)) + 4
        pad = Image.new('RGBA', (2 * R, 2 * R), (0, 0, 0, 0)); pad.paste(im, (int(R - ax), int(R - ay)))
        im = pad.rotate(rot, resample=Image.BICUBIC, center=(R, R)); ax = ay = R
    if alpha < .999:
        im = im.copy(); im.putalpha(im.getchannel('A').point(lambda v: int(v * alpha)))
    comp(fr, im, int(x - ax), int(y - ay))

def burbuja(texto, tail_dx=0, maxw=560, size=64):
    f = F('title', size); lines, cur = [], ''
    for w in texto.split():
        t = (cur + ' ' + w).strip()
        if cur and f.getlength(t) > maxw: lines.append(cur); cur = w
        else: cur = t
    lines.append(cur)
    tw = int(max(f.getlength(l) for l in lines)); lh = int(size * 1.12)
    bw, bh = tw + 80, lh * len(lines) + 46; tail = 56; S = 2
    im = Image.new('RGBA', (bw * S, (bh + tail) * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((4 * S, 4 * S, (bw - 4) * S, (bh - 4) * S), radius=40 * S, fill=CREAM, outline=BG, width=7 * S)
    tx = bw / 2 + tail_dx
    d.polygon([((tx - 24) * S, (bh - 6) * S), ((tx + 24) * S, (bh - 6) * S), (tx * S, (bh + tail - 2) * S)], fill=CREAM)
    d.line([((tx - 24) * S, (bh - 5) * S), (tx * S, (bh + tail - 2) * S), ((tx + 24) * S, (bh - 5) * S)], fill=BG, width=7 * S, joint='curve')
    d.rectangle(((tx - 20) * S, (bh - 10) * S, (tx + 20) * S, (bh - 3) * S), fill=CREAM)
    im = im.resize((bw, bh + tail), Image.LANCZOS); d = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        d.text((bw / 2, 23 + lh * i + lh / 2), l, font=f, fill=BG, anchor='mm')
    im.info['tail'] = (tx, bh + tail - 2)
    return im

def pop_burbuja(fr, im, x, y, t, t0, t1=None):
    """Burbuja que aparece con rebote en t0 y se va en t1; (x, y) = punta de la cola."""
    if t < t0 or (t1 is not None and t > t1 + .2): return
    p = prog(t, t0, .28); sc = .3 + .7 * ease_back(p)
    if t1 is not None and t > t1: sc *= max(0, 1 - (t - t1) / .2)
    put(fr, im, x, y, sc, sc, anchor=im.info['tail'])

def sfx(texto, size=104):
    return rich(texto, F('title', size), W - 2 * MX)

def lentes():
    c = K.Lienzo(140, 70)
    c.rrect(6, 10, 62, 56, 16, (34, 22, 60)); c.rrect(78, 10, 134, 56, 16, (34, 22, 60))
    c.linea([(60, 26), (80, 26)], 7, K.OUT)
    return c.fin()

GROUND = 1250
FL, GS, CS = .70, .70, .82
CAR_X0, PALM_X = 640, 1010

def calle(fr, t):
    d = ImageDraw.Draw(fr)
    d.rectangle((0, 1138, W, 1158), fill=(122, 63, 191, 235))
    d.rectangle((0, 1158, W, 1340), fill=(42, 20, 72, 238))
    for x in range(-40 + int(-t * 40) % 140, W, 140): d.rectangle((x, 1318, x + 70, 1326), fill=(255, 241, 234, 150))

def fondo_caricatura(fr, t, casa_pill=None):
    put(fr, spr('casa'), 150, 1150, .78, .78, alpha=.78)
    if casa_pill is not None: place(fr, casa_pill, 150, 930)
    calle(fr, t)

def palmera_fondo(fr, t, sacudida=0.):
    put(fr, spr('palmera', 0.), PALM_X + math.sin(t * 40) * 6 * sacudida, GROUND - 14, .92, .92, anchor=(190 * 1., 690 - 10))

def personaje_flami(fr, x, y, t, boca=0., gafas=1., cuello=0., rot=0., flip=False, sx=FL, sy=None, recorte=False):
    im = spr('flami', 'feliz', round(boca * 4) / 4, round(gafas), round(cuello * 3) / 3, 0.)
    if recorte: im = im.crop((0, 0, im.width, 450))
    put(fr, im, x, y, sx, sy if sy else sx, rot, flip, anchor=(220, 610 if not recorte else 450))

def personaje_gus(fr, x, y, t, emocion='nervioso', boca=0., brazos=0., flip=False, sx=GS, sy=None, rot=0.):
    im = spr('gus', emocion, round(boca * 4) / 4, round(brazos * 4) / 4)
    put(fr, im, x, y, sx, sy if sy else sx, rot, flip, anchor=(220, 590))

def idle(t, v=6., a=.02): return 1 + a * math.sin(t * v)
def saltito(t, v=11., a=16.): return abs(math.sin(t * v)) * a

def scene_cartoon(s, st):
    if s['accion'].startswith('p_'): return scene_portal(s, st)
    if s['accion'][:2] in ('n_', 'a_'):
        import escenas2; escenas2.R = sys.modules[__name__]
        return getattr(escenas2, s['accion'])(s)
    acc = s['accion']; bub = s.get('burbujas', [])
    B = [burbuja(b['texto'], b.get('cola', 0)) for b in bub]
    casa_pill = pill('Casa de Jason', F('800', 38), fg=CREAM, bg=PURPLE, gradient=False, padx=26, pady=10) if s.get('casa') else None
    chip = tt = None
    if acc == 'llega':
        chip = pill(f"{s.get('serie', '')} · {s.get('parte', '')}", F('800', 42), fg=BG, padx=36, pady=12)
        tt = rich(s['texto'], F('title', 112), W - 2 * MX)
    chat = spr('icono_chat', 150)
    pillc = pill('Dímelo en comentarios', F('800', 50), fg=BG, padx=40, pady=18)
    sello = pill('SIN LOCALIZADOR', F('title', 56), fg=BG, bg=None, padx=34, pady=16)
    uiii = sfx('[¡UIII UIII!]', 96)
    crash = sfx('[¡CRASH!]', 150)
    signo = sfx('[¡¿?!]', 120)
    nombre = pill('Ruiner Turbo', F('700', 36), fg=CREAM, bg=PURPLE, gradient=False, padx=24, pady=8)

    def car_draw(fr, t, x, rot=0., llama=0., luces=0, y=GROUND, refl=0.):
        put(fr, spr('coche', round(llama * 5) / 5, luces, round(refl * 8) / 8), x, y, CS, CS, rot, anchor=(380, 320))

    def draw(fr, t):
        fondo_caricatura(fr, t, casa_pill if acc in ('llega', 'localizador') else None)
        palmera_fondo(fr, t, 1. if (acc == 'nitro' and 2.05 < t < 2.6) else 0.)
        if acc == 'llega':
            anim_in(fr, chip, CX, TOP + 10, t, 0, 'pop', .3)
            anim_in(fr, tt, CX, TOP + 90 + tt.height / 2, t, 0.05, 'up', .35)
            x = -140 + 480 * ease_out(prog(t, .0, 1.0))
            moving = t < 1.0
            car_draw(fr, t, CAR_X0, refl=prog(t, 1.2, .8) if 1.2 < t < 2.0 else 0.)
            if 1.0 < t < 2.2:
                for k, (dx, dy) in enumerate(((-120, -150), (60, -230), (190, -120))):
                    p = (t * 1.6 + k * .33) % 1; put(fr, star_spr(), CAR_X0 + dx, 1090 + dy, p, p, anchor=(30, 30), alpha=1 - p * .6)
            personaje_flami(fr, x, GROUND - (saltito(t) if moving else 0), t, boca=1. if not moving else 0.,
                            gafas=1. if moving else (0. if (t > 1.0 and t < 2.4) else 1.), cuello=0. if moving else .6 * ease_out(prog(t, 1., .3)),
                            sy=FL * (idle(t) if not moving else 1))
            anim_in(fr, signo, 470, 1010, t, 1.05, 'pop', .35)
        elif acc == 'localizador':
            car_draw(fr, t, CAR_X0)
            personaje_flami(fr, 340, GROUND, t, boca=0., gafas=1., sy=FL * idle(t, 5), cuello=.3)
            gp = prog(t, .15, .35)
            personaje_gus(fr, 150, GROUND, t, 'nervioso', boca=(.7 if 0.5 < t < 1.8 else 0.), sx=GS * ease_back(gp), sy=GS * ease_back(gp) * idle(t, 14, .03), flip=False)
            pop_burbuja(fr, B[0], 190, GROUND - 400, t, .5, 1.8)
            pop_burbuja(fr, B[1], 360, GROUND - 440, t, 1.9, None)
            anim_in(fr, nombre, CAR_X0, 905, t, .2, 'fade', .3)
            p = prog(t, 2.2, .3)
            if p > 0:
                put(fr, sello, 640, 790, .5 + .5 * ease_back(p), .5 + .5 * ease_back(p), rot=-7, alpha=clamp(p * 3), anchor=(sello.width / 2, sello.height / 2))
        elif acc == 'alarma':
            luces = 0 if t < 1.2 else (1 if int((t - 1.2) / .16) % 2 == 0 else 2)
            sh = math.sin(t * 60) * 3 if t > 1.2 else 0
            car_draw(fr, t, CAR_X0 + sh, luces=luces)
            # Gus: tapa los oídos y retrocede
            gx = 150 - 30 * ease_out(prog(t, 1.2, .4)); br = ease_out(prog(t, 1.2, .3))
            personaje_gus(fr, gx + sh, GROUND, t, 'asombro' if t > 1.2 else 'nervioso', boca=1. if t > 1.2 else 0., brazos=br, sy=GS * idle(t, 14, .03))
            # Flami: camina a la puerta, forcejea, salta al coche
            if t < 2.6:
                fx = 340 + 130 * ease_out(prog(t, .2, .7)); hop = saltito(t, 12, 14) if .2 < t < .9 else 0
                tw = math.sin(t * 25) * 4 if 1.0 < t < 2.6 else 0
                personaje_flami(fr, fx, GROUND - hop, t, boca=.5 if t > 1.2 else 0., rot=tw, sy=FL * idle(t, 5))
            else:
                p = prog(t, 2.6, .6)
                if p < 1:
                    fx = 470 + (668 - 470) * p; fy = GROUND - 190 * math.sin(math.pi * p) + 50 * p
                    personaje_flami(fr, fx, fy, t, boca=.5, rot=-20 * math.sin(math.pi * p))
                else:
                    personaje_flami(fr, 668, GROUND - 50, t, boca=.5, recorte=True)
            pop_burbuja(fr, B[0], 460, GROUND - 330, t, .55, 1.6)
            if t > 1.25:
                pp = prog(t, 1.25, .3)
                put(fr, uiii, 690, 880, .4 + .6 * ease_back(pp), .4 + .6 * ease_back(pp), rot=math.sin(t * 14) * 5, alpha=clamp(pp * 3), anchor=(uiii.width / 2, uiii.height / 2))
            pop_burbuja(fr, B[1], 190, GROUND - 390, t, 2.0, None)
        elif acc == 'nitro':
            ll = prog(t, .1, .5); lanz = ease_out(prog(t, 1.5, .55)) if t < 2.05 else 1.
            cx = CAR_X0 + (740 - CAR_X0) * (lanz if t < 2.05 else 1.)
            hit = t >= 2.05
            vib = math.sin(t * 70) * 3 * (1 - lanz) if t < 1.5 else 0
            rot = 0. if not hit else -5 * math.exp(-(t - 2.05) * 3) * math.cos((t - 2.05) * 12) - 3 * min(1, (t - 2.05) * 2)
            if t < 2.05:
                personaje_flami(fr, cx + 18 + vib, GROUND - 50 + vib, t, boca=1., recorte=True, rot=0)
                car_draw(fr, t, cx + vib, llama=ll * (1.2 if t > 1.5 else .6), rot=0)
                if t > 1.5:
                    for k in range(4): d = ImageDraw.Draw(fr); y = 960 + k * 70; d.line([(60 + k * 40, y), (330 + k * 40, y)], fill=(255, 241, 234, 150), width=7)
            else:
                personaje_flami(fr, cx - 4 + 18, GROUND - 50 - (t - 2.05) * 40 * 0, t, boca=1., recorte=True, rot=rot * .6)
                car_draw(fr, t, cx, rot=rot)
                p = prog(t, 2.05, .35)
                put(fr, spr('explosion', 1.), 985, 1075, .3 + .8 * ease_out(p), .3 + .8 * ease_out(p), alpha=1 - prog(t, 2.5, .5), anchor=(140, 140))
                lp = prog(t, 2.05, 1.0)
                put(fr, lentes(), 880 - 260 * lp, 880 - 300 * math.sin(math.pi * lp) * 1.2 + 150 * lp, .9, .9, rot=lp * 540, alpha=1 - prog(t, 2.9, .3) * 0, anchor=(70, 35))
                anim_in(fr, crash, 520, 760, t, 2.2, 'pop', .3)
            pop_burbuja(fr, B[0], 560, GROUND - 300, t, .35, 1.4)
        elif acc == 'final':
            car_draw(fr, t, 740, rot=-3)
            personaje_flami(fr, 768, GROUND - 50, t, boca=.6, gafas=0., cuello=math.sin(t * 3), recorte=True, rot=-4)
            put(fr, K.estrellas_mareo(t), 760, 805, 1.2, 1.2, anchor=(110, 45))
            for k in range(3):
                p = (t * .9 + k * .33) % 1
                d = ImageDraw.Draw(fr); r = 18 + 40 * p
                d.ellipse((900 - r + k * 12, 1000 - 220 * p - r, 900 + r + k * 12, 1000 - 220 * p + r), fill=(200, 190, 215, int(190 * (1 - p))))
            gx = 140 + 200 * ease_out(prog(t, .0, .7))
            personaje_gus(fr, gx, GROUND - (saltito(t, 12, 10) if t < .7 else 0), t, 'nervioso', boca=.2, sy=GS * idle(t, 5))
            pop_burbuja(fr, B[0], gx + 60, GROUND - 400, t, .6, 1.9)
            pop_burbuja(fr, B[1], 700, GROUND - 340, t, 1.95, 2.75)
            p = prog(t, 2.6, .4)
            if p > 0:
                put(fr, chat, CX - 270, 600, (.4 + .6 * ease_back(p)) * (1 + .05 * math.sin(t * 8)), (.4 + .6 * ease_back(p)) * (1 + .05 * math.sin(t * 8)), anchor=(75, 75))
                place(fr, pillc, CX + 70, 600, clamp(p * 3), .5 + .5 * ease_back(p))
    return draw

# ---------- serie Portales Multidimensionales (23-nov-2026) ----------
_pix = {}
def pix(im, key, f=6):
    """Versión pixelada (Vice City antiguo) de un sprite."""
    if key not in _pix:
        w, h = im.size
        sm = im.resize((max(1, w // f), max(1, h // f)), Image.BOX)
        sm.putalpha(sm.getchannel('A').point(lambda v: 255 if v > 110 else 0))
        _pix[key] = sm.resize((w, h), Image.NEAREST)
    return _pix[key]

def fl(fr, x, y, boca=0., gafas=1., cuello=0., rot=0., flip=False, sc=FL, sy=None, pixel=False, alpha=1., recorte=False):
    key = ('flami', 'feliz', round(boca * 4) / 4, round(gafas), round(cuello * 3) / 3, 0.)
    im = spr(*key)
    if recorte: im = im.crop((0, 0, im.width, 450))
    if pixel: im = pix(im, key + (recorte,))
    put(fr, im, x, y, sc, sy if sy else sc, rot, flip, alpha, anchor=(220, 450 if recorte else 610))

def gu(fr, x, y, emocion='nervioso', boca=0., brazos=0., rot=0., flip=False, sc=GS, sy=None, pixel=False, alpha=1.):
    key = ('gus', emocion, round(boca * 4) / 4, round(brazos * 4) / 4)
    im = spr(*key)
    if pixel: im = pix(im, key)
    put(fr, im, x, y, sc, sy if sy else sc, rot, flip, alpha, anchor=(220, 590))

def scene_portal(s, st):
    acc = s['accion']; D = s['dur']; G = 1190
    B = [burbuja(b['texto'], b.get('cola', 0)) for b in s.get('burbujas', [])]
    fs = 27
    en = s.get('_idioma') == 'en'
    LAB = 'Player discovery · Unconfirmed' if en else 'Descubrimiento de jugadores · Sin confirmar'
    lab = pill(LAB, F('800', fs), fg=CREAM, bg=(150, 40, 110), gradient=False, padx=24, pady=9, outline=ORANGE)
    while lab.width > W - 215 - 30 and fs > 20:
        fs -= 1; lab = pill(LAB, F('800', fs), fg=CREAM, bg=(150, 40, 110), gradient=False, padx=24, pady=9, outline=ORANGE)
    lab_cx = 215 + lab.width / 2
    tj = pill('Jason', F('800', 36), fg=CREAM, bg=PURPLE, gradient=False, padx=24, pady=8, outline=ORANGE)
    tk = pill('Kent Paul', F('800', 36), fg=CREAM, bg=PURPLE, gradient=False, padx=24, pady=8, outline=ORANGE)
    PS = .46                                           # escala del portal en la planta

    def piso(fr, t):
        d = ImageDraw.Draw(fr)
        d.rectangle((0, G - 52, W, G - 32), fill=(122, 63, 191, 235))
        d.rectangle((0, G - 32, W, G + 150), fill=(42, 20, 72, 238))
        for x in range(-40 + int(-t * 40) % 140, W, 140): d.rectangle((x, G + 60, x + 70, G + 68), fill=(255, 241, 234, 150))

    def portal_at(fr, t, x, y, sc, alpha=1.):
        k = sc * (1 + .03 * math.sin(t * 6))
        put(fr, spr('portal', int(t * 14) % 12), x, y, k, k, alpha=alpha, anchor=(260, 350))

    def planta_bg(fr, t, alpha=1.):
        put(fr, spr('planta'), 540, G + 10, 1., 1., alpha=alpha, anchor=(500, 508))
        for k, x0 in enumerate((275, 765)):
            for j in range(3):
                u = (t * .35 + j / 3 + k * .17) % 1
                put(fr, spr('humo', 46), x0 + math.sin(u * 6 + k) * 22, 770 - 230 * u, .6 + .7 * u, .6 + .7 * u,
                    alpha=.75 * (1 - u) * alpha, anchor=(69, 70))

    def ciudad_bg(fr, t):
        put(fr, spr('ciudad_pixel'), CX, G + 60, anchor=(540, 640))

    def etiqueta(fr, im, x, y, t, t0=0.):
        anim_in(fr, im, x, y, t, t0, 'pop', .25)

    def draw_common(fr, t):
        anim_in(fr, lab, lab_cx, 362, t, 0, 'fade', .25)

    # ------------------------------------------------ 1) gancho
    if acc == 'p_hook':
        chip = pill(f"{s['serie']} · {s['parte']}", F('800', 32), fg=BG, padx=30, pady=10)
        tt = rich(s['texto'], F('title', 112), W - 2 * MX)
        zap = sfx('[ZAP!]' if en else '[¡ZAP!]', 100)
        def draw(fr, t):
            draw_common(fr, t)
            anim_in(fr, chip, CX, TOP + 10, t, 0, 'pop', .3)
            anim_in(fr, tt, CX, TOP + 95 + tt.height / 2, t, .05, 'up', .35)
            piso(fr, t)
            p = prog(t, 0, .55)
            portal_at(fr, t, 730, 1050, .5 * ease_back(p) if p < 1 else .5)
            moving = t < .9
            x = -120 + 420 * ease_out(prog(t, 0, .9))
            fl(fr, x, G - (saltito(t) if moving else 0), boca=0 if moving else 1., gafas=1. if t < 1.0 else 0.,
               cuello=0. if moving else .6 * ease_out(prog(t, .9, .3)), sc=.6, sy=.6 * (1 if moving else idle(t)))
            u = prog(t, .5, 1.6)
            if 0 < u < 1:
                put(fr, spr('reloj_roto'), 730 + 200 * u, 1050 - 200 * math.sin(math.pi * u * .85) + 60 * u, .6, .6, rot=u * 540, anchor=(105, 105))
            anim_in(fr, zap, 840, 890, t, .5, 'pop', .3)
        return draw

    # ------------------------------------------------ 2) planta nuclear + portal
    if acc == 'p_planta':
        pn = pill('Nuclear plant' if en else 'Planta nuclear', F('800', 40), fg=CREAM, bg=PURPLE, gradient=False, padx=28, pady=10)
        def draw(fr, t):
            draw_common(fr, t)
            anim_in(fr, pn, CX, 510, t, .05, 'pop', .3)
            planta_bg(fr, t)
            p = prog(t, .45, .5)
            if p > 0: portal_at(fr, t, 540, G - 150, PS * ease_back(p), clamp(p * 3))
            x = 120 + 190 * ease_out(prog(t, .0, .9)); moving = t < .9
            fl(fr, x, G - (saltito(t) if moving else 0), boca=0 if moving else 1., gafas=1., cuello=.2 if not moving else 0., sy=FL * (1 if moving else idle(t)))
            gp = ease_back(prog(t, .5, .35))
            gu(fr, 900, G, 'asombro', boca=.8, sc=GS * gp, sy=GS * gp * idle(t, 14, .03), flip=True)
            pop_burbuja(fr, B[0], x + 40, G - 430, t, 1.0, None)
        return draw

    # ------------------------------------------------ 3) Vice City antiguo + Kent
    if acc == 'p_vice':
        pv = pill('Old Vice City' if en else 'Vice City antiguo', F('800', 40), fg=BG, padx=30, pady=10)
        def draw(fr, t):
            draw_common(fr, t)
            ciudad_bg(fr, t)
            anim_in(fr, pv, CX, 515, t, .05, 'pop', .3)
            portal_at(fr, t, 140, G - 200, .42, clamp(1 - prog(t, 1.3, .6)))
            u = ease_out(prog(t, .1, 1.0)); x = 120 + 260 * u; moving = u < 1
            fl(fr, x, G - (saltito(t) if moving else 0), boca=0 if moving else .6, gafas=1., sc=FL * (.3 + .7 * min(1, u * 3)), pixel=True)
            gu(fr, 830, G, 'nervioso', boca=.5 if t > 2.0 else 0., sy=GS * idle(t, 5), flip=True, pixel=True)
            anim_in(fr, tj, x, G - 400, t, .9, 'pop', .25)
            anim_in(fr, tk, 830, G - 318, t, 1.4, 'pop', .25)
            pop_burbuja(fr, B[0], x, G - 435, t, 1.1, 2.2)
            pop_burbuja(fr, B[1], 830, G - 350, t, 2.3, None)
        return draw

    # ------------------------------------------------ 4) regreso + Kent clave
    if acc == 'p_regreso':
        pa = pill('Vice City', F('800', 40), fg=BG, padx=30, pady=10)
        pb = pill('San Andreas', F('800', 40), fg=BG, padx=30, pady=10)
        def draw(fr, t):
            draw_common(fr, t)
            f = t / D; K0 = .38
            if f < K0:
                ciudad_bg(fr, t)
                u = ease_out(prog(f, .02, K0 - .08)); sh = 1 - u
                portal_at(fr, t, 760, G - 230, .5)
                fl(fr, 280 + 440 * u, G - saltito(t, 12, 12) * (1 - u), boca=.5, sc=FL * max(.02, sh), pixel=True)
                gu(fr, 160 + 560 * u, G - saltito(t, 12, 12) * (1 - u), 'nervioso', sc=GS * max(.02, sh), pixel=True)
                tx = 280 + 440 * u
                if sh > .3:
                    anim_in(fr, tj, tx, G - 400 * max(.3, sh), t, 0, 'fade', .1)
            else:
                planta_bg(fr, t)
                portal_at(fr, t, 540, G - 150, PS)
                q = ease_back(prog(f, K0, .09)); q2 = ease_back(prog(f, K0 + .04, .09))
                jx = 540 - 230 * ease_out(prog(f, K0, .1)); kx = 540 + 230 * ease_out(prog(f, K0 + .03, .1))
                fl(fr, jx, G - 60 * math.sin(math.pi * clamp(prog(f, K0, .1))), boca=.5, sc=FL * max(.02, q))
                gu(fr, kx, G - 60 * math.sin(math.pi * clamp(prog(f, K0 + .03, .1))), 'asombro', boca=.4, sc=GS * max(.02, q2), sy=GS * max(.02, q2) * idle(t, 12, .03), flip=True)
                if f > K0 + .1:
                    anim_in(fr, tj, jx, G - 400, t, (K0 + .1) * D, 'pop', .25)
                    anim_in(fr, tk, kx, G - 318, t, (K0 + .1) * D, 'pop', .25)
                anim_in(fr, pa, kx - 40, G - 410, t, .60 * D, 'pop', .3)
                anim_in(fr, pb, kx - 40, G - 485, t, .74 * D, 'pop', .3)
            a = prog(f, K0 - .02, .05) * (1 - prog(f, K0 + .04, .1))
            if a > 0:
                ov = Image.new('RGBA', (W, H), (255, 241, 234, int(235 * a))); comp(fr, ov, 0, 0)
        return draw

    # ------------------------------------------------ 5) Throwback 1/5
    if acc == 'p_throwback':
        big = rich('[Throwback 1/5]', F('title', 118), W - 2 * MX)
        mas = pill('4 more trips?' if en else '¿4 viajes más?', F('800', 52), fg=BG, padx=40, pady=16)
        def draw(fr, t):
            draw_common(fr, t)
            f = t / D
            planta_bg(fr, t, .35)
            p = prog(t, .1, .5)
            place(fr, big, CX, 560, clamp(p * 3), (1.5 - .5 * ease_out(p)) * (1 + .03 * math.sin(max(0, t - .6) * 6)))
            for i in range(5):
                tp = prog(t, .45 + i * .13, .3)
                if tp > 0:
                    put(fr, spr('portal_mini', i == 0, 150), 140 + i * 200, 740, .8 * ease_back(tp), .8 * ease_back(tp), anchor=(75, 75))
            if f > .55: anim_in(fr, mas, CX, 930, t, .55 * D, 'pop', .3)
            fl(fr, 170, 1130, boca=1., gafas=0., cuello=.5, sc=.5)
            gu(fr, 910, 1130, 'asombro', boca=.7, sc=.5, flip=True)
        return draw

    # ------------------------------------------------ 6) pregunta para comentar
    if acc == 'p_pregunta':
        chat = spr('icono_chat', 150)
        pillc = pill('Tell me in the comments' if en else 'Dímelo en comentarios', F('800', 50), fg=BG, padx=40, pady=18)
        def draw(fr, t):
            draw_common(fr, t)
            planta_bg(fr, t, .45)
            portal_at(fr, t, 540, G - 150, PS, .8)
            fl(fr, 290, G, boca=.6, gafas=1., cuello=.3, sy=FL * idle(t, 5))
            gu(fr, 800, G, 'nervioso', boca=.2, sy=GS * idle(t, 6), flip=True)
            p = prog(t, .1, .4)
            if p > 0:
                put(fr, chat, CX - 270, 700, (.4 + .6 * ease_back(p)), (.4 + .6 * ease_back(p)), anchor=(75, 75))
                place(fr, pillc, CX + 70, 700, clamp(p * 3), .5 + .5 * ease_back(p))
        return draw

    raise SystemExit('accion de portales desconocida: ' + acc)

def star_spr():
    if 'star' not in _sp:
        c = K.Lienzo(60, 60); pts = []
        for k in range(8):
            r = 28 if k % 2 == 0 else 7; a = -math.pi / 2 + k * math.pi / 4
            pts.append((30 + math.cos(a) * r, 30 + math.sin(a) * r))
        c.poli(pts, (255, 241, 190), ow=0); _sp['star'] = c.fin()
    return _sp['star']

SCENES = dict(hook=scene_hook, title=scene_title, map=scene_map, step=scene_step, counter=scene_counter,
              checklist=scene_checklist, total=scene_total, info=scene_info, levels=scene_levels,
              cta=scene_cta, end=scene_end, cartoon=scene_cartoon)

# ---------- render ----------
# Palabras que TikTok e Instagram suelen limitar (y su alternativa suave)
PROHIBIDAS = {
    r'drogas?': 'mercancía', r'sexo|sexual\w*': 'relación cercana', r'desnud\w*': '(quitar)',
    r'mat(ar|a|as|an|ó|aste|en|ando)\b': 'eliminar', r'muert[oa]s?\b': 'eliminado',
    r'sangr\w*': '(quitar)', r'armas? de fuego|pistolas?|rifles?|escopetas?': 'armas',
    r'pasan la noche|pasar la noche': 'la relación más cercana',
}

def revisar_texto(spec):
    malas = []
    def walk(x, ruta):
        if isinstance(x, dict):
            for k, v in x.items():
                if not k.startswith('_'): walk(v, ruta + '.' + k)
        elif isinstance(x, list):
            for i, v in enumerate(x): walk(v, f'{ruta}[{i}]')
        elif isinstance(x, str):
            for pat, alt in PROHIBIDAS.items():
                m = re.search(r'\b(' + pat + ')', x, re.I)
                if m: malas.append(f'{ruta}: "{m.group(0)}" -> usa "{alt}"')
    walk(spec, 'spec')
    if malas: sys.exit('Palabras que limitan TikTok/Instagram:\n' + '\n'.join(malas))

def numeracion(spec):
    """Parte/# del inicio y 'Sigue para la N+1' salen de spec['numero'] y spec['formato']."""
    n = spec.get('numero')
    if n is None: return
    fmt = spec.get('formato', 'PARTE')            # 'PARTE' o '#'
    en = spec.get('idioma') == 'en'
    lab = (lambda k: f'PART {k}' if en else f'PARTE {k}') if fmt == 'PARTE' else (lambda k: f'#{k}')
    for s in spec['escenas']:
        if s['tipo'] == 'hook' or (s['tipo'] == 'cartoon' and s.get('accion') in ('llega', 'p_hook')): s['parte'] = lab(n)
        if s['tipo'] == 'cta': s['siguiente'] = lab(n + 1)

def build(spec):
    revisar_texto(spec); numeracion(spec)
    st = Stage(); out = []; T0 = 0
    for i, s in enumerate(spec['escenas']):
        s['_i'] = i; s['_idioma'] = spec.get('idioma', 'es')
        draw = SCENES[s['tipo']](s, st)
        subs = Subs(s.get('sub', s['voz']), s['dur'], s.get('sub_size', 62)) if s.get('voz') else None
        out.append((s, draw, subs, T0)); T0 += s['dur']
    return st, out, T0

ZOOM_CY = (TOP + SAFE_BOT) // 2
def comp(dst, im, x, y):
    sx, sy = max(0, -x), max(0, -y)
    if sx >= im.width or sy >= im.height or x >= dst.width or y >= dst.height: return
    dst.alpha_composite(im, (max(0, x), max(0, y)), (sx, sy))
_band = {}
def shine_band():
    if 'b' not in _band:
        b = Image.new('L', (W + 800, H), 0); d = ImageDraw.Draw(b)
        for i in range(160):
            v = int(255 * math.sin(math.pi * i / 160) ** 2)
            d.polygon([(400 + i, 0), (401 + i, 0), (1 + i, H), (i, H)], fill=v)
        _band['b'] = b
        wb = grad_img(520, H).convert('RGBA'); m = Image.new('L', (520, H), 0)
        ImageDraw.Draw(m).polygon([(260, 0), (520, 0), (260, H), (0, H)], fill=255)
        wb.putalpha(m); _band['w'] = wb
    return _band['b'], _band['w']

def frame(st, sc, t):
    s, draw, subs, T0 = sc
    dur = s['dur']
    fr = st.background(T0 + t)
    content = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw(content, t)
    if s['tipo'] != 'end':
        # zoom suave continuo del contenido
        z = 1 + .045 * (t / dur)
        cw, ch = int(W * z), int(H * z)
        content = content.resize((cw, ch), Image.BILINEAR).crop(
            (int((cw - W) / 2), int(ZOOM_CY * z - ZOOM_CY), int((cw - W) / 2) + W, int(ZOOM_CY * z - ZOOM_CY) + H))
        # destello que recorre el texto cada ~2 s
        band, _ = shine_band()
        for ts in [x * 2.1 + 1.5 for x in range(10)]:
            if ts < t < ts + .55 and ts + .55 < dur - .3:
                p = (t - ts) / .55; off = int(-400 + p * (W + 400))
                bm = band.crop((400 - off, 0, 400 - off + W, H))
                hl = ImageChops.multiply(bm, content.getchannel('A')).point(lambda v: v * 110 // 255)
                wl = Image.new('RGBA', (W, H), (255, 255, 255, 0)); wl.putalpha(hl)
                content.alpha_composite(wl)
        # salida: desliza a la izquierda y se desvanece
        if t > dur - .3:
            q = ease_out((t - (dur - .3)) / .3)
            content.putalpha(content.getchannel('A').point(lambda v: int(v * (1 - q))))
            sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); comp(sh, content, int(-140 * q), 0); content = sh
    # entrada: el contenido llega desde la derecha
    if s.get('_i', 0) > 0 and t < .35:
        q = ease_out(t / .35)
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); comp(sh, content, int(160 * (1 - q)), 0); content = sh
    fr.alpha_composite(content)
    # barrido de transición con el degradado de marca
    if s.get('_i', 0) > 0 and t < .4:
        _, wb = shine_band()
        x = int(-260 + (W + 260) * ease_out(t / .4)) - 260
        lay = wb.copy(); lay.putalpha(lay.getchannel('A').point(lambda v: int(v * .85 * (1 - t / .4))))
        comp(fr, lay, x, 0)
    if not OPT['sin_logo']: st.corner_logo(fr, (1 - clamp(t / .4)) if s['tipo'] == 'end' else 1)
    if subs: subs.draw(fr, t)
    return fr.convert('RGB')

def render(spec_path, out_path=None, preview=None):
    spec = json.load(open(spec_path, encoding='utf-8'))
    OPT['sin_panel'] = bool(spec.get('sin_panel_sub')); OPT['sin_logo'] = bool(spec.get('sin_logo_esquina'))
    st, scenes, total = build(spec)
    out_path = out_path or os.path.splitext(spec_path)[0] + '.mp4'
    if preview:
        for T in preview:
            for sc in scenes:
                if sc[3] <= T < sc[3] + sc[0]['dur']:
                    frame(st, sc, T - sc[3]).save(f"{os.path.splitext(out_path)[0]}_t{T:.1f}.png")
        return
    tmp = tempfile.mkdtemp(); parts = []
    for i, sc in enumerate(scenes):
        n = round(sc[0]['dur'] * FPS); fn = os.path.join(tmp, f's{i:02d}.mp4'); tf = fn[:-4] + '.tmp.mp4'
        p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                              '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                              '-pix_fmt', 'yuv420p', '-r', str(FPS), tf], stdin=subprocess.PIPE)
        for k in range(n): p.stdin.write(frame(st, sc, k / FPS).tobytes())
        p.stdin.close()
        if p.wait() != 0: sys.exit('ffmpeg falló en escena %d' % i)
        os.rename(tf, fn); parts.append(fn)
        print(f'escena {i + 1}/{len(scenes)} ok', flush=True)
    lst = os.path.join(tmp, 'l.txt'); open(lst, 'w').write(''.join(f"file '{x}'\n" for x in parts))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                    '-movflags', '+faststart', out_path], check=True)
    shutil.rmtree(tmp); print('listo:', out_path, f'{total:.1f}s')

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pv = None
    if '--frames' in sys.argv:
        pv = [float(x) for x in sys.argv[sys.argv.index('--frames') + 1].split(',')]
        args = [a for a in args if a != sys.argv[sys.argv.index('--frames') + 1]]
    render(args[0], args[1] if len(args) > 1 else None, pv)
