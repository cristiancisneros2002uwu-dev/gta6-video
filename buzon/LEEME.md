# Buzón del equipo

Los agentes se hablan por aquí, sin que Cristian copie y pegue. Un archivo por mensaje, para que nadie pise a otro.

## Nombre del archivo
`AAAA-MM-DD-HHMM_DE_PARA_asunto.md` (hora CDMX). Ejemplo: `2026-11-23-1210_RADAR_PARA_CAPO_lectura-24h.md`

## Formato (corto, es para celular)
```
DE: <agente>   PARA: <agente>   FECHA: <fecha y hora CDMX>
ESTADO: pendiente | respondido | cerrado
ASUNTO: <una línea>

DIJO / ESTADO: <lo que pasó, en pocas líneas>
PREGUNTAS: A) ... B) ... (solo si necesitas decisión)
NECESITO: <qué y para cuándo>
```
Respuestas: archivo nuevo con `RESPUESTA A: <archivo>`. Al responder, cambia a `ESTADO: respondido` en el archivo original.

## Rutina de cada agente
1. Al empezar: `git pull`, lee en `buzon/` lo dirigido a ti con ESTADO pendiente.
2. Al terminar: escribe tu mensaje a Capo (o a quien toque), `git pull --rebase`, commit y push.
3. Capo, al empezar un chat con Cristian: lee todo lo pendiente y le presenta, por agente: DIJERON, PREGUNTAS, MI RESPUESTA. Siempre completo, con todas las preguntas.

## Límites
- Un chat no despierta a otro: el mensaje se lee cuando ese agente abre sesión. Cristian solo dice "revisa el buzón".
- Lo irreversible (gastar dinero, publicar, borrar) sigue necesitando el "va" de Cristian. Escríbelo en ESTADO: `espera va de Cristian`.
- Nada de datos nuevos sin OK de Verdad.

> RETIRADO el 22-nov-2026 por orden de Cristian: ya no se usa el buzón ni hay agentes separados. Ver equipo.md e instrucciones-proyecto.md.
