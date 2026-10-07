# Restricciones duras

Hay tres restricciones que no se negocian. Todo el diseño de la empresa —organigrama, infra, pipeline— existe para absorberlas.

## 1. Costo total = $0

**Lo que implica:**

- ✅ **Se puede**: todo open-source, self-hosted, modelos locales (Ollama/vLLM: Qwen, Llama) o free tiers. Hardware propio o free tier cloud. LangGraph, MCP, LiteLLM proxy self-hosted, Langfuse self-hosted, bot de aprobaciones propio (Telegram/email).
- ❌ **No se puede**: plataformas enterprise caras, APIs pagas por defecto, servicios de pago sin justificación.
- 💡 **Cómo se absorbe**: el stack entero es OSS y auto-hospedado. Regla explícita: ningún agente incorpora un servicio pago sin que el valor que genera lo justifique **y** Fabian lo apruebe. Con costo $0, el gateway (LiteLLM proxy) controla cuotas de los free tiers y uso de GPU local en vez de controlar gasto en dólares.
- ⚠️ **Contrapartida honesta**: los modelos OSS locales rinden menos que los de punta en tareas agénticas complejas. El diseño lo absorbe priorizando **tareas acotadas donde los modelos chicos rinden bien**, gobernanza mínima viable por agente y máxima restricción al lanzar.

## 2. Un solo humano, para siempre

Fabian es la única persona: sin empleados, socios ni contratistas. Todo human-in-the-loop y toda escalación caen en él.

**Lo que implica:**

- ✅ **Se puede**: aprobaciones en lote (mañana y tarde, desde el celular) en vez de interrupciones constantes; modo offline donde los agentes siguen con lo autónomo y encolan lo irreversible; escalación siempre hacia Fabian con reglas claras que minimicen esas escalaciones.
- ❌ **No se puede**: depender de que Fabian esté disponible en todo momento; delegar aprobaciones irreversibles en nadie (porque no hay nadie); asumir capacidad infinita de atención.
- 💡 **Cómo se absorbe**:
  - **Presupuesto semanal de atención de Fabian**: el pipeline se estrangula a sus horas reales. Es el WIP maestro.
  - **Compuertas con SLA**: Fabian decide en 48h o la etapa se pausa sola.
  - **Runbooks por agente**: los logs y runbooks son la memoria institucional — punto único de fallo documentado para que cualquiera (o un futuro yo) pueda retomar.
  - **Agentes que se identifican como IA** ante personas (EU AI Act art. 50), con el camino al humano siempre existente.

## 3. Bootstrap

La empresa se financia sola: se escala solo cuando un agente o producto paga su propia infra con el valor que genera.

**Lo que implica:**

- ✅ **Se puede**: hosting en hardware propio o free tier cloud; escalar infra cuando el valor generado lo justifique.
- ❌ **No se puede**: comprar capacidad por adelantado; gastar a crédito de un futuro que no existe.
- 💡 **Cómo se absorbe**:
  - **Fase 0 — Piloto**: un agente, una función, una tarea medible (candidatos: Reconciler o QA). Medir el baseline ANTES de automatizar.
  - **Se escala lo que ya funciona y está auditado**: Fase 1 (una función completa) → Fase 2 (multi-función, Chief of Staff coordinando) → Fase 3 (escala por producto).
  - **Regla de oro**: máxima restricción al lanzar; más autonomía solo tras ~30 días con tasa de aprobación alta.
  - El tablero del pipeline (Analyst) mide conversión, cycle time y kill rate: sin métricas, las compuertas son intuición.

---

*Consistente con el [diseño operativo v1(diseno-operativo-v1.md (2026-10-07).*
