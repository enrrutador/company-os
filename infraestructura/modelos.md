# Modelos a costo $0 — estrategia

## La estrategia en una línea

**Local primero, free tier como complemento, nada pago.** Los modelos open-source corriendo en hardware propio (vía Ollama o vLLM) hacen el trabajo pesado; los free tiers de proveedores cubren picos o capacidades que lo local no da.

## Modelos locales (base del sistema)

Servidores de inferencia open-source:

- **Ollama** — la forma más simple de correr modelos locales: `ollama run` y listo. Ideal para empezar.
- **vLLM** — servidor de alto rendimiento (throughput, batching, API compatible con OpenAI). Para cuando un agente necesita servir muchas requests.

Familias de modelos a considerar (verificar las versiones vigentes al momento de instalar):

- **Qwen** (Alibaba) — buen equilibrio razonamiento/tamaño; suele rendir bien en tareas agénticas y uso de herramientas.
- **Llama** (Meta) — ecosistema amplio, muchas variantes quantizadas.
- Otras familias open-source según el caso (Mistral, Gemma, DeepSeek, etc.).

### Cómo elegir el tamaño según la tarea y el hardware

Regla práctica: **el modelo más chico que resuelva la tarea de forma confiable.**

| Tarea | Tamaño orientativo |
|---|---|
| Clasificación, extracción de datos, respuestas con contexto dado | 3B–8B (rápido, barato en VRAM) |
| Razonamiento medio, redacción, resúmenes | 8B–14B |
| Tareas agénticas con herramientas, multi-paso | 14B–32B (o más, si el hardware lo permite) |
| Razonamiento pesado, planificación compleja | 32B–70B+ (solo si hay GPU con VRAM suficiente) |

Limitantes reales del hardware propio:

- **VRAM de GPU** manda: un modelo 8B quantizado (Q4) necesita ~5–6 GB; un 32B, ~20 GB; un 70B, ~40 GB+.
- **Sin GPU dedicada**: modelos chicos (≤8B) en CPU son usables para tareas acotadas, pero lentos para agentes conversacionales.
- **Quantización** (Q4_K_M y similares): reduce VRAM a costa de una pequeña pérdida de calidad; casi siempre vale la pena.

Medí siempre con *tu* hardware y *tus* tareas: un benchmark de 10 casos reales vale más que cualquier tabla.

## Free tiers como complemento

Los niveles gratuitos de proveedores de modelos sirven para:

- Capacidades que lo local no cubre bien (p. ej. ventanas de contexto muy grandes, ciertos modelos multimodales).
- Picos de demanda que exceden la GPU propia.
- Comparar calidad local vs. proveedor en una tarea concreta.

Sus límites (verificar vigentes en cada proveedor al momento de usar):

- **Cuotas mensuales/diarias** de requests o tokens, que se agotan.
- **Rate limits** que frenan ráfagas.
- **Cambios unilaterales**: el proveedor puede recortar el free tier en cualquier momento. Nada crítico puede depender solo de un free tier.
- **Privacidad**: los datos salen de tu hardware. Nunca enviar datos de clientes o sensibles a un free tier.

El gateway ([LiteLLM proxy](../README.md)) administra las cuotas de los free tiers: techos por key y por agente, para que un loop no queme la cuota mensual en una tarde.

## Contrapartidas honestas

1. **Los modelos locales y free rinden menos que los modelos de punta** en tareas agénticas complejas (planificación larga, uso de herramientas encadenado, razonamiento abstracto). No es una opinión: es el estado del arte en 2026.
2. **El diseño operativo asume esta limitación**: por eso se priorizan **tareas acotadas** — un agente, una función, una tarea medible (ver piloto Reconciler/QA en `../pipeline/`). Los modelos chicos rinden bien cuando el problema está bien delimitado.
3. **Cuándo se justifica un modelo más grande**: cuando el benchmark de la tarea muestra que el modelo chico falla de forma sistemática *y* la tarea ya genera valor medido. Subir de tamaño es una decisión con evidencia, no por defecto.
4. **Cuándo se justificaría un modelo pago**: solo si el valor generado lo paga con margen claro *y* Fabian lo aprueba (regla de [README](README.md)). Hasta entonces, el techo es $0.

## Cómo el gateway enruta entre local y free tier

El LiteLLM proxy self-hosted actúa como único punto de entrada de todos los agentes a los modelos:

1. **El agente nunca llama a un modelo directamente**: llama al proxy con un nombre lógico (p. ej. `agente-qa-rapido`, `agente-reconciler`).
2. **El proxy decide la ruta** según reglas configuradas: por defecto → modelo local (Ollama/vLLM); si el local no responde o la tarea lo requiere → free tier (con cuota).
3. **Fallbacks**: si el free tier devuelve rate limit, el proxy reintenta en local o encola. Nada se pierde por un 429.
4. **Presupuestos**: techos por request, por sesión y por key viven en el proxy, no en el código del agente (principio del diseño operativo).
5. **Observabilidad**: cada llamada queda logueada y se puede ver en Langfuse: qué modelo se usó, cuánto costó (en tokens y en cuota), qué latencia tuvo.

Esto significa que **cambiar de modelo no requiere tocar ningún agente**: se cambia la configuración del proxy y todos los agentes migran. La estrategia de modelos es configuración, no código.
