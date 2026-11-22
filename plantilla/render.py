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

    def corner_logo(self, fr):
        fr.alpha_composite(self.logo, (MX - 20, SAFE_TOP + 6))

# ---------- subtítulos ----------
class Subs:
    def __init__(self, text, dur):
        self.f = F('800', 62); self.words = text.split(); self.dur = dur
        maxw = W - 2 * MX - 80; space = self.f.getlength(' ')
        lines, cur, cw = [], [], 0
        for w in self.words:
            ww = self.f.getlength(w)
            if cur and cw + space + ww > maxw: lines.append(cur); cur, cw = [], 0
            cur.append(w); cw += (space if cw else 0) + ww
        if cur: lines.append(cur)
        self.lines = lines; self.lh = 78
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
        place(fr, self.panel, CX, self.y0 + self.box_h / 2 + (1 - a) * 20, a * .92)
        d = ImageDraw.Draw(fr); space = self.f.getlength(' '); k = 0
        for li, l in enumerate(self.lines):
            lw = sum(self.f.getlength(w) for w in l) + space * (len(l) - 1)
            x = CX - lw / 2; y = self.y0 + 22 + li * self.lh + (1 - a) * 20
            for w in l:
                on = t >= self.wt[k]; cur = on and (k + 1 >= len(self.wt) or t < self.wt[k + 1])
                col = ORANGE if cur else (CREAM if on else (170, 150, 190))
                d.text((x, y), w, font=self.f, fill=col + (int(255 * a),))
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
    t1 = rich('Sigue para el' if sig.startswith('#') else 'Sigue para la', F('title', 110), W - 2 * MX)
    t2 = rich(f"[{sig}]", F('title', 200), W - 2 * MX)
    btn = pill('+ Seguir', F('800', 60), fg=BG, padx=60, pady=26)
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
    lg = st.hlogo.resize((860, int(860 * st.hlogo.height / st.hlogo.width)), Image.LANCZOS)
    url = rich('gta6encyclopedia.com', F('title', 70), 1000, base=ORANGE)
    def draw(fr, t):
        p = prog(t, 0, .5)
        place(fr, lg, CX, H / 2 - 50, ease_out(p), .85 + .15 * ease_out(p))
        anim_in(fr, url, CX, H / 2 + 110, t, .25, 'up')
    return draw

SCENES = dict(hook=scene_hook, title=scene_title, map=scene_map, step=scene_step, counter=scene_counter,
              checklist=scene_checklist, total=scene_total, info=scene_info, levels=scene_levels,
              cta=scene_cta, end=scene_end)

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
    lab = (lambda k: f'PARTE {k}') if fmt == 'PARTE' else (lambda k: f'#{k}')
    for s in spec['escenas']:
        if s['tipo'] == 'hook': s['parte'] = lab(n)
        if s['tipo'] == 'cta': s['siguiente'] = lab(n + 1)

def build(spec):
    revisar_texto(spec); numeracion(spec)
    st = Stage(); out = []; T0 = 0
    for i, s in enumerate(spec['escenas']):
        s['_i'] = i
        draw = SCENES[s['tipo']](s, st)
        subs = Subs(s['voz'], s['dur']) if s.get('voz') else None
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
    st.corner_logo(fr)
    if subs: subs.draw(fr, t)
    return fr.convert('RGB')

def render(spec_path, out_path=None, preview=None):
    spec = json.load(open(spec_path, encoding='utf-8'))
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
