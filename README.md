# gta6-video

Videos de gta6encyclopedia con voz de ElevenLabs (Adam - Dominant, Firm).

- `videos/lote-N/*.json`: al subir un JSON aquí, GitHub Actions genera su voz en `voz/`.
- `videos/_pendientes/`: JSON que aún no generan voz.
- `tools/tts.py`: genera la voz (corre en Actions, usa el secreto ELEVENLABS_API_KEY).
- `tools/sincronizar.py`: ajusta escenas a la voz, renderiza y pega el audio.
- `plantilla/`: renderizador y assets de marca.
