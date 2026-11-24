#!/usr/bin/env python3
"""Miniatura (portada) 1080x1920: un fotograma de la escena 1 sin subtítulos.
Uso: python3 tools/miniatura.py videos/lote-5/x.json salida/x.png [segundos]"""
import json, sys
sys.path.insert(0, 'plantilla')
import render as R
spec = json.load(open(sys.argv[1], encoding='utf8'))
st, scenes, total = R.build(spec)
s, draw, subs, T0 = scenes[0]
R.frame(st, (s, draw, None, T0), float(sys.argv[3]) if len(sys.argv) > 3 else 1.8).save(sys.argv[2])
