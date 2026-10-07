# Niveles de autonomía por riesgo

*Fuente de verdad: [Diseño operativo v1(../empresa/diseno-operativo-v1.md · Fecha: 2026-10-07*

Cada agente opera en uno de tres niveles, definidos **por el riesgo de sus acciones, no por su capacidad**. El nivel se asigna en el lanzamiento, se revisa periódicamente y solo se flexibiliza con evidencia (ver "Regla de oro" abajo).

## Nivel 1 — Autónomo

El agente actúa por su cuenta, sin revisión humana. Se reserva para acciones **reversibles**: lecturas, borradores, análisis, cálculos. Todo queda logueado ([auditoria.md](auditoria.md)) para poder revisar después.

**Ejemplos:**

- **QA**: corre la suite de tests y reporta resultados. Si encuentra un fallo, lo registra y avisa; no corrige ni deploya.
- **Prospector**: investiga cuentas y arma listas de prospectos. No contacta a nadie.
- **Qualifier**: califica respuestas según reglas explícitas y agenda reuniones dentro de parámetros pre-aprobados.
- **CRM Keeper**: actualiza el CRM con datos verificados de conversaciones ya ocurridas.
- **Analyst**: mide métricas y produce reportes. No publica ni cambia estrategias.
- **Reconciler**: concilia ingresos vs. facturación. Si detecta una inconsistencia, alerta; no mueve dinero.
- **Reporter**: genera P&L mensual y reportes de flujo de caja a partir de datos ya registrados.

## Nivel 2 — On-the-loop (revisión post-acción)

El agente actúa, pero un humano (Fabian) revisa el resultado. Se usa cuando la acción tiene **consecuencias visibles o difícilmente reversibles**, pero el volumen hace inviable aprobar cada una de antemano. La revisión puede revertir o frenar.

**Ejemplos:**

- **Outreach**: redacta y envía mensajes de prospección. En volumen, Fabian revisa muestras y puede pausar la campaña. El primer envío a un segmento nuevo es in-the-loop hasta validar el guion.
- **Content**: redacta posts, docs y newsletters. Fabian revisa **antes de publicar** (publicar siempre requiere aprobación previa — ver [aprobaciones.md](aprobaciones.md)).
- **L1 Support**: resuelve lo frecuente de forma autónoma **dentro de guías aprobadas**. Todo lo que salga del guion escala (ver [escalación en aprobaciones.md](aprobaciones.md#escalación)).
- **Onboarder**: ejecuta setups y migraciones de datos de clientes siguiendo runbooks aprobados. Errores con datos de clientes escalan.
- **Biller**: genera facturas electrónicas (ARCA) por cada cobro. *On-the-loop al inicio*; pasa a in-the-loop permanente si mueve dinero (ver abajo).
- **Builder**: escribe código, no deploya. El código pasa por Reviewer antes de avanzar.

## Nivel 3 — In-the-loop (aprobación previa obligatoria)

Nada se ejecuta sin la aprobación explícita de Fabian. Reservado para lo **irreversible**: dinero, clientes, accesos y deploys.

**Ejemplos:**

- **Deployer**: despliega a producción **solo con aprobación previa**. Nunca deploya solo.
- **Biller**: cualquier movimiento real de dinero (débito, reembolso, ajuste) requiere aprobación previa. *Dinero real = in-the-loop siempre al principio*, con montos máximos por transacción y por día definidos por Fabian.
- **Guardian**: su operación diaria (monitoreo de infra y costo de tokens) es autónoma **con límites estrictos** (solo lectura + freno de emergencia). Activar el kill switch sobre un agente con gasto anormal es su única acción ejecutiva, y se reporta de inmediato para revisión de Fabian.
- **Reviewer**: su aprobación del código es una compuerta, pero no sustituye la aprobación de Fabian para el deploy. *Planificador ≠ ejecutor ≠ validador.*

**Matriz completa de qué requiere aprobación previa:** ver [aprobaciones.md](aprobaciones.md).

## Regla de oro

> **Máxima restricción al lanzar; más autonomía solo tras ~30 días con tasa de aprobación alta.**

Todo agente nuevo arranca en el nivel más restrictivo que aplique a su función (como mínimo, un nivel más restrictivo que su objetivo). Después de ~30 días de operación, si la tasa de aprobación de sus acciones es alta y sostenida, y los logs no muestran incidentes, se puede subir un nivel. La decisión de flexibilizar la documenta Fabian con la evidencia; nunca es automática.

## Reglas transversales

- **Ningún agente tiene poder sobre otro**: planificador ≠ ejecutor ≠ validador ≠ logger. El Chief of Staff coordina tareas, no aprueba acciones de otros agentes en nombre de Fabian.
- **Longitud máxima de cadena**: todo agente tiene un límite de pasos por tarea (anti-loops) y un presupuesto en el gateway. El presupuesto vive en el gateway, no en el código del agente.
- **Identidad y permisos** determinan lo que *puede* hacer un agente; la autonomía determina lo que puede hacer *sin Fabian*: ver [identidades.md](identidades.md).
- Todo cambio de nivel de autonomía queda registrado en [auditoria.md](auditoria.md) como un cambio de gobernanza.
