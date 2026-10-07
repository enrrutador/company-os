# Etapas del pipeline (0 a 9)

Detalle operativo de cada etapa. Convención: **quién ejecuta**, **artefacto de handoff obligatorio** (sin entregable no hay pase) y **qué compuerta la cierra** (quién decide).

---

## 0. Sourcing (continuo)

- **Ejecuta:** [Analyst](../agentes/marketing/analyst.md). Autónomo.
- **Qué hace:** escanea mercado, competencia y pedidos de clientes en forma permanente; mantiene un **backlog de tesis priorizado**. El pipeline nunca depende de la inspiración del momento.
- **Artefacto de handoff:** backlog de tesis priorizado (cada entrada: problema, segmento, evidencia inicial).
- **Compuerta:** ninguna; es continuo. El Chief of Staff selecciona qué tesis entra a la etapa 1 según WIP disponible.

## 1. Tesis

- **Ejecutan:** Fabian + [Chief of Staff](../agentes/coordinacion/chief-of-staff.md).
- **Qué pasa:** se formula la hipótesis escrita + criterios de kill + check de WIP. El **Chief of Staff le hace red-team a la hipótesis** antes de gastar un ciclo de validación.
- **Artefacto de handoff:** hipótesis escrita, criterios de kill definidos, check de WIP de Validación aprobado.
- **Compuerta:** implícita de Fabian — si la tesis no sobrevive al red-team o no hay WIP, no pasa.

## 2. Validación

- **Ejecutan:** [Analyst](../agentes/marketing/analyst.md) (research) con entrevistas async por agentes (formularios, landing, chat); Fabian solo cierra 2–3 entrevistas clave.
- **Qué pasa:** se busca evidencia real. **Pricing validado con método** (test en landing/preventa a precio real, no "¿pagarías X?"). La preventa exige infra de cobro lista y promesa explícita (reembolsable).
- **Artefacto de handoff:** evidencia documentada + pricing validado + **mapa de competencia** + **lista de lanzamiento** (entrevistados → CRM como warm leads).
- **Compuerta 1 — decide Fabian:** *se construye o se mata*. SLA 48h; sin decisión, la etapa se pausa sola.

## 3. Construcción

- **Ejecutan:** [Builder](../agentes/ingenieria/builder.md), [Reviewer](../agentes/ingenieria/reviewer.md) (segundo par de ojos; planificador ≠ ejecutor), [QA](../agentes/ingenieria/qa.md) (autónomo). Deploys: solo con aprobación de Fabian vía [Deployer](../agentes/ingenieria/deployer.md).
- **Qué pasa:** spec escrita desde la evidencia → MVP + sales kit (one-pager, demo, pricing) + legales base (términos, privacidad) + checklist: dependencias evaluadas a costo $0, setup de cobro por producto, nombre/marca/dominio.
- **Artefacto de handoff:** MVP funcional + sales kit + legales base + checklist $0/cobro/naming completo.
- **Compuerta:** revisión del Chief of Staff (que lo construido = lo validado); el pase a Dogfooding lo habilita Fabian.

## 4. Dogfooding (uso interno)

- **Ejecutan:** los propios agentes + Fabian como usuario.
- **Qué pasa:** se usa el producto de verdad, con **criterios de salida explícitos**: ¿lo usaríamos nosotros? ¿pasa el umbral?
- **Artefacto de handoff:** resultados del dogfooding contra los criterios de salida (pasa/no pasa, con evidencia).
- **Compuerta 2 — decide Fabian:** el producto pasa el umbral para avanzar al lanzamiento.

## 5. Lanzamiento

- **Ejecutan:** [Chief of Staff](../agentes/coordinacion/chief-of-staff.md) coordina; [Content](../agentes/marketing/content.md) (on-the-loop: Fabian revisa antes de publicar), equipo comercial preparado.
- **Qué pasa:** se sale a vender con posicionamiento, materiales y equipo alineados.
- **Artefacto de handoff:** plan de lanzamiento ejecutado + materiales publicados + equipo comercial listo.
- **Compuerta 3 — decide Fabian:** *aprobación para salir a vender*.

## 6. Comercial

- **Ejecutan:** [Prospector](../agentes/ventas/prospector.md) (listas), [Outreach](../agentes/ventas/outreach.md) (on-the-loop: revisión antes de enviar en volumen), [Qualifier](../agentes/ventas/qualifier.md) (califica y agenda), [CRM Keeper](../agentes/ventas/crm-keeper.md) (CRM actualizado).
- **Qué pasa:** outbound con compliance (opt-out, límites de volumen, Ley 25.326 de datos personales); Qualifier negocia dentro de **matriz pre-aprobada** (descuentos/condiciones); **deal review**: lo vendido = lo que existe.
- **Artefacto de handoff:** contrato (plantilla + firma electrónica) + **primer pago**. Venta concretada = contrato + primer pago, nada menos.
- **Compuerta:** deal review del Chief of Staff — si lo vendido no es lo que existe, no pasa a Onboarding.

## 7. Onboarding & Activación

- **Ejecuta:** [Onboarder](../agentes/soporte/onboarder.md).
- **Qué pasa:** setup del cliente, migración de datos, primera victoria. Vault de credenciales de clientes (mínimo privilegio). Aislamiento de datos: tenancy por producto/cliente; ningún agente cruza datos entre clientes.
- **Artefacto de handoff:** cliente activo = setup completo + primer valor entregado (verificable).
- **Compuerta:** ninguna de Fabian; el criterio es objetivo. **Recién acá la venta está realmente cerrada.**

## 8. Operación

- **Ejecutan:** [L1 Support](../agentes/soporte/l1-support.md), [Biller](../agentes/finanzas/biller.md) (facturación electrónica ARCA), [Reconciler](../agentes/finanzas/reconciler.md) (concilia y alerta), [Reporter](../agentes/finanzas/reporter.md) (P&L por producto), [Guardian](../agentes/operaciones/guardian.md) (monitoreo de infra y costo, kill switch).
- **Qué pasa:** entregan, cobran (dunning automatizado), soportan con SLAs definidos, miden **P&L por producto**.
- **Artefacto de handoff:** P&L por producto al día + SLAs cumplidos (reporte continuo, no un pase único).
- **Compuerta:** revisión periódica de portfolio (ver [portfolio.md](portfolio.md)): lo que no tracciona se mata o se pausa.

## 9. Loops

- **Ejecutan:** [Analyst](../agentes/marketing/analyst.md) (feedback → backlog), equipo comercial (testimonios).
- **Qué pasa:** feedback de clientes → backlog → Construcción (el producto itera); testimonios/casos de éxito → Comercial (go-to-market).
- **Artefacto de handoff:** backlog de producto actualizado + casos de éxito documentados.
- **Compuerta:** ninguna; es el loop permanente que alimenta el sourcing y la construcción.

---

**Ver también:** [reglas.md](reglas.md) · [portfolio.md](portfolio.md) · [README.md](README.md)
