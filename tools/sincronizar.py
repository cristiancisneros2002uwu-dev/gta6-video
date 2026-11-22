#!/usr/bin/env python3
"""Ajusta las escenas a la voz, renderiza y pega el audio.

Uso: python3 tools/sincronizar.py videos/lote-1/dinero-01.json [salida.mp4]
Lee voz/<nombre>.mp3 y voz/<nombre>.json (frases con inicio/fin).
"""
import json, os, subprocess, sys, tempfile

PREVIO = 0.15   # la escena entra un poco antes de que empiece su frase
COLA = 0.45     # silencio después de la última frase
MIN = 1.2

src = sys.argv[1]
nombre = os.path.splitext(os.path.basename(src))[0]
salida = sys.argv[2] if len(sys.argv) > 2 else f"salida/{nombre}.mp4"
d = json.load(open(src, encoding="utf8"))
fr = json.load(open(f"voz/{nombre}.json", encoding="utf8"))["frases"]

voz = [i for i, s in enumerate(d["escenas"]) if s.get("voz", "").strip() and s["tipo"] != "end"]
if len(voz) != len(fr):
    sys.exit(f"{nombre}: {len(voz)} escenas con voz pero {len(fr)} frases en el audio")

inicios = [0.0] + [max(0.0, fr[k]["inicio"] - PREVIO) for k in range(1, len(fr))]
for k, i in enumerate(voz):
    fin = inicios[k + 1] if k + 1 < len(voz) else fr[-1]["fin"] + COLA
    d["escenas"][i]["dur"] = round(max(MIN, fin - inicios[k]), 3)
for s in d["escenas"]:
    if s["tipo"] == "end":
        s["dur"] = 2.0

os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
tmp = tempfile.mkdtemp()
jt = os.path.join(tmp, nombre + ".json")
json.dump(d, open(jt, "w", encoding="utf8"), ensure_ascii=False)
mudo = os.path.join(tmp, "mudo.mp4")
subprocess.run([sys.executable, "plantilla/render.py", jt, mudo], check=True, cwd=".")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mudo, "-i", f"voz/{nombre}.mp3",
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-af", "apad", "-shortest", salida], check=True)
total = sum(s["dur"] for s in d["escenas"])
print(f"{salida}: {total:.1f} s")
