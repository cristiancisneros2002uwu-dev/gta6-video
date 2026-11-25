#!/usr/bin/env python3
"""Genera la voz (ElevenLabs, con tiempos por caracter) de cada JSON en videos/lote-*/.

Corre en GitHub Actions. Para cada video sin audio, crea:
  voz/<nombre>.mp3   audio completo
  voz/<nombre>.json  frases con inicio y fin en segundos
Necesita el secreto ELEVENLABS_API_KEY.
"""
import base64, glob, json, os, re, sys, urllib.request, urllib.error
from num2words import num2words

VOICE_ID = os.environ.get("VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Adam - Dominant, Firm
MODEL_ID = os.environ.get("MODEL_ID", "eleven_v3")
RESPALDO = "eleven_multilingual_v2"
PREFIJO = os.environ.get("PREFIJO", "[Mexican Spanish accent] ")
KEY = os.environ.get("ELEVENLABS_API_KEY")
if not KEY:
    sys.exit("Falta el secreto ELEVENLABS_API_KEY")


def hablar(t, idioma="es"):
    """Texto para la voz: GTA VI -> GTA seis, 10.000 -> diez mil, 7.7 -> siete punto siete."""
    if idioma == "en":
        t = re.sub(r"\bGTA\s*(VI|6)\b", "GTA six", t)
        return re.sub(r"\d+", lambda m: num2words(int(m[0]), lang="en"), t)
    t = re.sub(r"\bGTA\s*(VI|6)\b", "GTA seis", t)
    t = re.sub(r"\b(\d+)\.(\d)\b(?!\d)", lambda m: num2words(int(m[1]), lang="es") + " punto " + num2words(int(m[2]), lang="es"), t)
    t = re.sub(r"\d{1,3}(?:[.,]\d{3})+|\d+", lambda m: num2words(int(re.sub(r"[.,]", "", m[0])), lang="es"), t)
    t = re.sub(r"uno (mil|millones)", r"un \1", t).replace("veintiun ", "veintiún ")
    t = t.replace("~", "unos ").replace("$", "")
    return t


def buscar_voz(nombre):
    """Busca una voz de la cuenta por nombre (sin distinguir mayusculas)."""
    pag = None
    for _ in range(20):
        u = "https://api.elevenlabs.io/v2/voices?page_size=100&include_total_count=false" + (f"&next_page_token={pag}" if pag else "")
        with urllib.request.urlopen(urllib.request.Request(u, headers={"xi-api-key": KEY}), timeout=60) as r:
            j = json.load(r)
        for v in j.get("voices", []):
            if nombre.lower() in v["name"].lower():
                print("Voz encontrada:", v["name"], v["voice_id"]); return v["voice_id"]
        pag = j.get("next_page_token")
        if not j.get("has_more"): break
    sys.exit("FALLO: no encuentro la voz " + nombre)


def frases(d):
    return [hablar(s["voz"].strip(), d.get("idioma", "es")) for s in d["escenas"] if s.get("voz", "").strip() and s["tipo"] != "end"]


def tts(texto, modelo=None, idioma="es", prev=None, sig=None):
    modelo = modelo or MODEL_ID
    body = json.dumps({
        "text": texto,
        "model_id": modelo,
        "language_code": idioma,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.0, "speed": 1.0},
        **({"previous_text": prev} if prev else {}), **({"next_text": sig} if sig else {}),
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
        if modelo != RESPALDO and e.code in (400, 422):
            print(f"{modelo} no disponible ({e.code}: {msg[:200]}); uso {RESPALDO}")
            return tts(texto, RESPALDO, idioma)
        sys.exit(f"ElevenLabs {e.code}: {msg}")


def pegar(viejo, meta, cambios, salida):
    """Reemplaza SOLO las frases cambiadas dentro del audio viejo (el resto no se toca ni gasta créditos).
    cambios = {indice: (mp3_nuevo, inicio_nuevo, fin_nuevo)}. Devuelve la lista de frases con tiempos nuevos."""
    import subprocess
    fr = meta["frases"]; n = len(fr)
    c = [0.0] + [(fr[i - 1]["fin"] + fr[i]["inicio"]) / 2 for i in range(1, n)] + [None]
    ins, partes, nuevas, shift = ["-i", viejo], [], [], 0.0
    for i in range(n):
        a, b = c[i], c[i + 1]
        if i in cambios:
            mp3, st, en = cambios[i]
            izq = fr[i]["inicio"] - a
            der = (b - fr[i]["fin"]) if b is not None else 0.35
            ns, ne = max(0.0, st - izq), en + der
            k = len(ins) // 2; ins += ["-i", mp3]
            partes.append(f"[{k}:a]atrim={ns:.3f}:{ne:.3f},asetpts=PTS-STARTPTS[p{i}]")
            nuevas.append({"texto": None, "inicio": round(a + shift + (st - ns), 3), "fin": round(a + shift + (en - ns), 3)})
            if b is not None: shift += (ne - ns) - (b - a)
        else:
            fin_ = f":{b:.3f}" if b is not None else ""
            partes.append(f"[0:a]atrim={a:.3f}{fin_},asetpts=PTS-STARTPTS[p{i}]")
            nuevas.append({"texto": fr[i]["texto"], "inicio": round(fr[i]["inicio"] + shift, 3), "fin": round(fr[i]["fin"] + shift, 3)})
    fc = ";".join(partes) + ";" + "".join(f"[p{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[o]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", fc, "-map", "[o]", "-ar", "44100", "-b:a", "128k", salida], check=True)
    return nuevas


def parchar(f, d, mp3, meta_path):
    """Si el JSON trae "parchar": true y el audio ya existe, genera solo las frases que cambiaron y las pega."""
    meta = json.load(open(meta_path, encoding="utf8"))
    nuevas_t = frases(d)
    if len(nuevas_t) != len(meta["frases"]):
        print(f"{f}: cambió el número de frases; no se puede parchar (quita 'parchar' para regenerar todo)"); return 0
    cambios, gastados = {}, 0
    for i, (t_new, old) in enumerate(zip(nuevas_t, meta["frases"])):
        if t_new == old["texto"]: continue
        prev = nuevas_t[i - 1] if i else None; sig = nuevas_t[i + 1] if i + 1 < len(nuevas_t) else None
        r = tts(t_new, meta.get("modelo", MODEL_ID), d.get("idioma", "es"), prev, sig)
        al = r.get("alignment") or r.get("normalized_alignment")
        tmp = f"/tmp/parche_{i}.mp3"; open(tmp, "wb").write(base64.b64decode(r["audio_base64"]))
        cambios[i] = (tmp, al["character_start_times_seconds"][0], al["character_end_times_seconds"][-1]); gastados += len(t_new)
        print(f"Parche frase {i + 1}: {len(t_new)} caracteres")
    if not cambios: return 0
    out = pegar(mp3, meta, cambios, mp3 + ".nuevo.mp3")
    for i, o in enumerate(out):
        o["texto"] = o["texto"] or nuevas_t[i]
    os.replace(mp3 + ".nuevo.mp3", mp3)
    meta["frases"] = out; meta["caracteres"] = meta.get("caracteres", 0) + gastados
    json.dump(meta, open(meta_path, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    d.pop("parchar", None); json.dump(d, open(f, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    return len(cambios)


hechos = 0
for f in sorted(glob.glob("videos/lote-*/*.json")):
    nombre = os.path.splitext(os.path.basename(f))[0]
    mp3, meta = f"voz/{nombre}.mp3", f"voz/{nombre}.json"
    d = json.load(open(f, encoding="utf8"))
    if os.path.exists(mp3) and os.path.exists(meta):
        if d.get("parchar"):
            VOICE_ID = d.get("voz_id") or VOICE_ID
            hechos += parchar(f, d, mp3, meta)
        continue
    fr = frases(d)
    modelo = d.get("modelo", MODEL_ID)
    VOICE_ID = d.get("voz_id") or (buscar_voz(d["voz_nombre"]) if d.get("voz_nombre") else os.environ.get("VOICE_ID", "pNInz6obpgDQGcFmaJgB"))
    texto, offs = d.get("prefijo", PREFIJO), []
    for p in fr:
        if texto and not texto.endswith(" "):
            texto += " "
        offs.append((len(texto), len(texto) + len(p)))
        texto += p
    print(f"Voz: {nombre} ({len(texto)} caracteres)")
    r = tts(texto, modelo, d.get("idioma", "es"))
    al = r.get("alignment") or r.get("normalized_alignment")
    st, en = al["character_start_times_seconds"], al["character_end_times_seconds"]
    n = len(st)
    out = []
    for p, (a, b) in zip(fr, offs):
        a2, b2 = min(a, n - 1), min(b - 1, n - 1)
        out.append({"texto": p, "inicio": round(st[a2], 3), "fin": round(en[b2], 3)})
    os.makedirs("voz", exist_ok=True)
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    json.dump({"voz_id": VOICE_ID, "modelo": modelo, "caracteres": len(texto), "frases": out},
              open(meta, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    hechos += 1

print(f"Listo: {hechos} audios nuevos")


# ---- Conteo de créditos -> creditos.md ----
import datetime
usados_repo = sum(json.load(open(m, encoding="utf8")).get("caracteres", 0) for m in glob.glob("voz/*.json"))
lineas = ["# Créditos de ElevenLabs", "", f"Actualizado: {datetime.datetime.utcnow():%Y-%m-%d %H:%M} UTC", ""]
try:
    req = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        sub = json.loads(r.read())
    usados, limite = sub["character_count"], sub["character_limit"]
    lineas += [f"- Plan: {sub.get('tier', '?')}",
               f"- Gastados: **{usados:,}** de {limite:,}",
               f"- Quedan: **{limite - usados:,}**",
               f"- Reinicia: {datetime.datetime.utcfromtimestamp(sub['next_character_count_reset_unix']):%Y-%m-%d}"
               if sub.get("next_character_count_reset_unix") else ""]
except Exception as e:
    lineas += [f"- (No pude leer la cuenta: {e})"]
lineas += ["", f"Caracteres en los audios guardados en voz/: {usados_repo:,} ({len(glob.glob('voz/*.mp3'))} audios)",
           "Un video usa ~400 créditos. Las pruebas fuera del repo no aparecen aquí, pero sí en la cuenta."]
open("creditos.md", "w", encoding="utf8").write("\n".join(lineas) + "\n")
print("creditos.md actualizado")
# verificacion de plan 1795360239
# regenerar con licencia 1795360292
