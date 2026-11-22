#!/usr/bin/env python3
"""Genera la voz (ElevenLabs, con tiempos por caracter) de cada JSON en videos/lote-*/.

Corre en GitHub Actions. Para cada video sin audio, crea:
  voz/<nombre>.mp3   audio completo
  voz/<nombre>.json  frases con inicio y fin en segundos
Necesita el secreto ELEVENLABS_API_KEY.
"""
import base64, glob, json, os, sys, urllib.request, urllib.error

VOICE_ID = os.environ.get("VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Adam - Dominant, Firm
MODEL_ID = os.environ.get("MODEL_ID", "eleven_multilingual_v2")
KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("Falta el secreto ELEVENLABS_API_KEY")


def frases(d):
    return [s["voz"].strip() for s in d["escenas"] if s.get("voz", "").strip() and s["tipo"] != "end"]


def tts(texto):
    body = json.dumps({
        "text": texto,
        "model_id": MODEL_ID,
        "language_code": "es",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0},
    }).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:500]
        if e.code == 400 and "language_code" in msg:  # modelo sin language_code: reintenta sin él
            b = json.loads(body); b.pop("language_code")
            req = urllib.request.Request(req.full_url, data=json.dumps(b).encode(), headers=dict(req.headers), method="POST")
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.loads(r.read())
        sys.exit(f"ElevenLabs {e.code}: {msg}")


hechos = 0
for f in sorted(glob.glob("videos/lote-*/*.json")):
    nombre = os.path.splitext(os.path.basename(f))[0]
    mp3, meta = f"voz/{nombre}.mp3", f"voz/{nombre}.json"
    if os.path.exists(mp3) and os.path.exists(meta):
        continue
    d = json.load(open(f, encoding="utf8"))
    fr = frases(d)
    texto, offs = "", []
    for p in fr:
        if texto:
            texto += " "
        offs.append((len(texto), len(texto) + len(p)))
        texto += p
    print(f"Voz: {nombre} ({len(texto)} caracteres)")
    r = tts(texto)
    al = r.get("alignment") or r.get("normalized_alignment")
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    n = len(st)
    out = []
    for p, (a, b) in zip(fr, offs):
        a2, b2 = min(a, n - 1), min(b - 1, n - 1)
        out.append({"texto": p, "inicio": round(st[a2], 3), "fin": round(en[b2], 3)})
    os.makedirs("voz", exist_ok=True)
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump({"voz_id": VOICE_ID, "modelo": MODEL_ID, "caracteres": len(texto), "frases": out},
              open(meta, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    hechos += 1

print(f"Listo: {hechos} audios nuevos")
