# Organigrama

18 agentes en 7 áreas + Fabian, el único humano.

## Jerarquía

```
Fabian (único humano, dueño y director)
  │
  │  flujo por defecto de trabajo e información
  ▼
Gerente General (agente directivo)
  │
  ├── Ingeniería & Producto (4): Constructor, Revisor, Control de Calidad, Responsable de Despliegues
  ├── Ventas (4): Prospector, Contacto Inicial, Calificador, Custodio del CRM
  ├── Soporte (3): Soporte Nivel 1, Responsable de Activación, Escalamiento
  ├── Marketing & Contenidos (2): Contenidos, Analista
  ├── Finanzas & Admin (3): Facturador, Conciliador, Responsable de Informes
  └── Operaciones & IT (1): Guardián
```

- **Flujo por defecto**: Fabian define objetivos → el Gerente General los descompone, delega a cada sector, supervisa y reporta. Toda tarea nace asignada por él; todo reporte sube por él.
- **Acceso directo de Fabian**: Fabian puede hablar con cualquier agente cuando quiera — es la excepción, no la norma. El Gerente General lo registra para mantener el mapa de trabajo al día.
- **Separación de funciones**: planificador ≠ ejecutor ≠ validador ≠ logger. Ningún agente ejecuta el trabajo de otro sector ni revoca veredictos ajenos.
- **Excepciones diseñadas** (las únicas dos):
  1. El **Gerente General** tiene autoridad de delegación y supervisión sobre los sectores: asigna tareas, exige avances y reprioriza dentro de los objetivos vigentes. No decide lo estratégico ni mueve dinero.
  2. El **Guardián** tiene el interruptor de emergencia: frena agentes con gasto o comportamiento anormal según umbrales de Fabian, con alerta inmediata.

## Fabian (único humano, para siempre)

- **Director de la empresa**: define objetivos, que el Gerente General descompone y asigna.
- **Aprueba lo irreversible**: humano *in-the-loop* para dinero, clientes, accesos y despliegues (aprobaciones por lote desde el celular).
- **Dueño de todos los agentes**: cada agente tiene identidad propia y permisos mínimos; Fabian es el dueño nombrado de cada uno.
- **Destino final de toda escalación**: soporte, ventas y cualquier caso fuera de guion terminan en él.

## Tabla por área

| Área | Agente | Rol | Ficha |
|---|---|---|---|
| **Dirección** | Gerente General | El directivo después de Fabian: delega tareas a cada sector, supervisa la ejecución y reporta avance. El único que habla con todos. | [gerente-general.md](../agentes/direccion/gerente-general.md) |
| **Ingeniería & Producto** (4) | Constructor | Implementa funcionalidades y correcciones. Escribe código, no despliega solo. | [constructor.md](../agentes/ingenieria/constructor.md) |
| | Revisor | Revisa el código del Constructor: segundo par de ojos. | [revisor.md](../agentes/ingenieria/revisor.md) |
| | Control de Calidad | Corre pruebas, reporta fallos. Autónomo. | [control-de-calidad.md](../agentes/ingenieria/control-de-calidad.md) |
| | Responsable de Despliegues | Despliega solo con aprobación humana (*in-the-loop*). | [responsable-despliegues.md](../agentes/ingenieria/responsable-despliegues.md) |
| **Ventas** (4) | Prospector | Investiga cuentas, arma listas. Autónomo. | [prospector.md](../agentes/ventas/prospector.md) |
| | Contacto Inicial | Redacta y envía mensajes. *On-the-loop* (revisión antes de enviar en volumen). | [contacto-inicial.md](../agentes/ventas/contacto-inicial.md) |
| | Calificador | Califica respuestas, agenda reuniones. Autónomo con reglas claras. | [calificador.md](../agentes/ventas/calificador.md) |
| | Custodio del CRM | Mantiene el CRM actualizado. Autónomo. | [custodio-crm.md](../agentes/ventas/custodio-crm.md) |
| **Soporte** (3) | Soporte Nivel 1 | Resuelve lo frecuente de forma autónoma dentro de guías. | [soporte-n1.md](../agentes/soporte/soporte-n1.md) |
| | Responsable de Activación | Configuración del cliente, migración de datos, primera victoria. | [responsable-activacion.md](../agentes/soporte/responsable-activacion.md) |
| | Escalamiento | Deriva a Fabian ante frustración, temas sensibles o fuera de guion. | [escalamiento.md](../agentes/soporte/escalamiento.md) |
| **Marketing & Contenidos** (2) | Contenidos | Redacta posteos, documentos, newsletters. *On-the-loop* (Fabian revisa antes de publicar). | [contenidos.md](../agentes/marketing/contenidos.md) |
| | Analista | Mide qué funciona y reporta. Autónomo. | [analista.md](../agentes/marketing/analista.md) |
| **Finanzas & Admin** (3) | Facturador | Genera facturas electrónicas (ARCA) por cada cobro. *On-the-loop* al inicio. | [facturador.md](../agentes/finanzas/facturador.md) |
| | Conciliador | Concilia ingresos vs. facturación, alerta inconsistencias. Autónomo. | [conciliador.md](../agentes/finanzas/conciliador.md) |
| | Responsable de Informes | P&L mensual y flujo de caja. Autónomo. | [responsable-informes.md](../agentes/finanzas/responsable-informes.md) |
| **Operaciones & IT** (1) | Guardián | Monitorea infra y costo de tokens, alerta anomalías y frena agentes con gasto anormal (interruptor de emergencia). Autónomo, límites estrictos (solo lectura + freno de emergencia). | [guardian.md](../agentes/operaciones/guardian.md) |

**Total: 18 agentes** + Fabian (único humano).

## Notas de gobierno

- **Autonomía graduada por riesgo**: autónomo (reversible) / on-the-loop (humano revisa post-acción) / in-the-loop (aprobación previa de Fabian para lo irreversible). Dinero real = in-the-loop siempre al principio.
- **Operar con un solo humano**: aprobaciones por lote, modo offline (lo irreversible se encola si Fabian no está), y las fichas de `agentes/` deben minimizar escalaciones con reglas claras.
- Todo agente que hable con personas se identifica como IA (EU AI Act art. 50, exigible desde agosto 2026).
- Las fichas de cada agente (rol, permisos, autonomía, manual operativo, equipo rojo inicial) viven en `agentes/` — aún por escribir a partir de esta plantilla.

---

*Consistente con el [diseño operativo v1](diseno-operativo-v1.md) (2026-10-07).*
