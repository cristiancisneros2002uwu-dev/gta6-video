# Plantilla de videos — gta6encyclopedia

Motor que convierte un JSON de escenas en un MP4 vertical 1080x1920, 30 fps, sin audio, con las reglas de marca.

## Uso
    pip install pillow
    python3 render.py videos/dinero-01-nave-delincuentes.json salida.mp4
    python3 render.py videos/x.json prev.mp4 --frames 1.5,10   # solo fotogramas PNG de revisión

Requiere ffmpeg. Fuentes, logos y fondo van en assets/.

## Encabezado del JSON
    "serie": "Dinero", "numero": 1, "formato": "PARTE"   (o "#" para Errores, Datos curiosos, etc.)
El render pone "PARTE N" grande al inicio y "Sigue para la PARTE N+1" en la escena cta.

## Escenas (campo "tipo")
- hook: serie, texto (pregunta/promesa); "PARTE N" / "#N" se llena solo
- title: icono, kicker, texto
- map: texto, referencia, destino, zona (mapa dibujado, ilustrativo)
- step: paso, icono, texto
- counter: icono, texto, desde, hasta, prefijo, sufijo, nota
- checklist: titulo, items[{icono, texto}]
- total: texto, desde, hasta, prefijo, chips[{icono, texto}]
- info: icono, texto, nota
- levels: nivel (0 = presentación), nombre, desc, texto
- cta: se llena solo con "Sigue para la PARTE N+1" (o "Sigue para el #N+1")
- end: cierre de 2 s con logo horizontal + gta6encyclopedia.com

Todas llevan "dur" (segundos) y "voz" (frase del guion = subtítulo sincronizado).
Marcado de texto: *palabra* = naranja #FFB36B · [palabra] = degradado de marca.
Íconos: crosshair, bag, safe, van, card, box, house, heart, pause, updown, check, arrow_down, plus.

## Marca fija
Fondo atardecer-leonida oscurecido con #1A1030 al 60 %, títulos Bricolage Grotesque 800 crema #FFF1EA,
texto Figtree, ícono arriba a la izquierda dentro del margen seguro, zona segura 15 % arriba / 20 % abajo.

## Reglas de texto
- El subtítulo es solo la frase de "voz". El texto grande de la escena debe decir algo distinto (no repetir la voz).
- Animación automática: entrada palabra por palabra, zoom suave continuo, destello cada ~2 s,
  barrido con el degradado de marca entre escenas y salida deslizando a la izquierda.
- Evita la flecha "→" (Figtree no la tiene); usa "·".
- Ningún título pasa de 2 líneas: si no cabe, la letra se achica sola. Aun así, escribe títulos cortos.

## Regla permanente: numeración de series
- Toda serie sigue su orden: Parte 1, 2, 3... (o #1, #2, #3...). Nunca se salta ni se repite un número.
- Antes de crear cada video, revisa serie.md y usa el número de "Siguientes" de esa serie.
- Al entregar, agrega el video a la tabla de serie.md y sube en 1 el número de "Siguientes".
- La escena cta de todo video de serie dice en grande "Sigue para la PARTE N+1" (o "#N+1"), antes del cierre con logo.

## Regla permanente: palabras que TikTok e Instagram suelen limitar
No uses en textos, voz ni subtítulos: droga, sexo, desnudo, matar, sangre ni armas de fuego explícitas
(pistola, rifle, escopeta). Alternativas: "mercancía", "relación cercana", "eliminar", "armas".
render.py revisa el JSON antes de renderizar y se detiene si encuentra alguna (lista PROHIBIDAS).
