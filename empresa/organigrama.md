# Organigrama

18 agentes en 7 áreas + Fabian, el único humano. Ningún agente tiene poder sobre otro: **planificador ≠ ejecutor ≠ validador ≠ logger**.

## Fabian (único humano, para siempre)

- **Director de la empresa**: define objetivos, que el Chief of Staff descompone y asigna.
- **Aprueba lo irreversible**: humano *in-the-loop* para dinero, clientes, accesos y deploys (aprobaciones por lote desde el celular).
- **Dueño de todos los agentes**: cada agente tiene identidad propia y permisos mínimos; Fabian es el dueño nombrado de cada uno.
- **Destino final de toda escalación**: soporte, ventas y cualquier caso fuera de guion terminan en él.

## Tabla por área

| Área | Agente | Rol | Ficha |
|---|---|---|---|
| **Coordinación** | Chief of Staff | Recibe objetivos de Fabian, los descompone en tareas, las asigna a cada función y reporta avance. El único que habla con todos. | [chief-of-staff.md](../agentes/coordinacion/chief-of-staff.md) |
| **Ingeniería & Producto** (4) | Builder | Implementa features y fixes. Escribe código, no deploya solo. | [builder.md](../agentes/ingenieria/builder.md) |
| | Reviewer | Revisa el código del Builder: segundo par de ojos. | [reviewer.md](../agentes/ingenieria/reviewer.md) |
| | QA | Corre tests, reporta fallos. Autónomo. | [qa.md](../agentes/ingenieria/qa.md) |
| | Deployer | Deploya solo con aprobación humana (*in-the-loop*). | [deployer.md](../agentes/ingenieria/deployer.md) |
| **Ventas** (4) | Prospector | Investiga cuentas, arma listas. Autónomo. | [prospector.md](../agentes/ventas/prospector.md) |
| | Outreach | Redacta y envía mensajes. *On-the-loop* (revisión antes de enviar en volumen). | [outreach.md](../agentes/ventas/outreach.md) |
| | Qualifier | Califica respuestas, agenda reuniones. Autónomo con reglas claras. | [qualifier.md](../agentes/ventas/qualifier.md) |
| | CRM Keeper | Mantiene el CRM actualizado. Autónomo. | [crm-keeper.md](../agentes/ventas/crm-keeper.md) |
| **Soporte** (3) | L1 Support | Resuelve lo frecuente de forma autónoma dentro de guías. | [l1-support.md](../agentes/soporte/l1-support.md) |
| | Onboarder | Setup del cliente, migración de datos, primera victoria. | [onboarder.md](../agentes/soporte/onboarder.md) |
| | Escalation | Deriva a Fabian ante frustración, temas sensibles o fuera de guion. | [escalation.md](../agentes/soporte/escalation.md) |
| **Marketing & Contenidos** (2) | Content | Redacta posts, docs, newsletters. *On-the-loop* (Fabian revisa antes de publicar). | [content.md](../agentes/marketing/content.md) |
| | Analyst | Mide qué funciona y reporta. Autónomo. | [analyst.md](../agentes/marketing/analyst.md) |
| **Finanzas & Admin** (3) | Biller | Genera facturas electrónicas (ARCA) por cada cobro. *On-the-loop* al inicio. | [biller.md](../agentes/finanzas/biller.md) |
| | Reconciler | Concilia ingresos vs. facturación, alerta inconsistencias. Autónomo. | [reconciler.md](../agentes/finanzas/reconciler.md) |
| | Reporter | P&L mensual y flujo de caja. Autónomo. | [reporter.md](../agentes/finanzas/reporter.md) |
| **Operaciones & IT** (1) | Guardian | Monitorea infra y costo de tokens, alerta anomalías y frena agentes con gasto anormal (kill switch). Autónomo, límites estrictos (solo lectura + freno de emergencia). | [guardian.md](../agentes/operaciones/guardian.md) |

**Total: 18 agentes** + Fabian (único humano).

## Notas de gobierno

- **Autonomía graduada por riesgo**: autónomo (reversible) / on-the-loop (humano revisa post-acción) / in-the-loop (aprobación previa de Fabian para lo irreversible). Dinero real = in-the-loop siempre al principio.
- **Operar con un solo humano**: aprobaciones por lote, modo offline (lo irreversible se encola si Fabian no está), y las fichas de `agentes/` deben minimizar escalaciones con reglas claras.
- Todo agente que hable con personas se identifica como IA (EU AI Act art. 50, exigible desde agosto 2026).
- Las fichas de cada agente (rol, permisos, autonomía, runbook, red-team inicial) viven en `agentes/` — aún por escribir a partir de esta plantilla.

---

*Consistente con el [diseño operativo v1(diseno-operativo-v1.md (2026-10-07).*
