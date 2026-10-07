# Productos — portfolio

## El portfolio está intencionalmente vacío

Ningún producto nace por decreto. **Todos los productos entran por el [pipeline](../pipeline/)**: sourcing → tesis → validación → construcción → dogfooding → lanzamiento → comercial → operación. Sin artefacto en cada handoff, no hay pase; sin pasar las compuertas de Fabian, no hay producto.

Esta carpeta se llena sola a medida que el pipeline produce: cada producto que sobrevive a la validación obtiene su ficha acá.

## Cómo nacería el primer producto

1. El Analyst mantiene el backlog de tesis (sourcing continuo).
2. Fabian + Chief of Staff eligen una tesis y le hacen red-team.
3. Se valida con evidencia real (pricing testeado a precio real, no encuestas de intención).
4. *Compuerta 1 — Fabian: se construye o se mata.*
5. Recién entonces se crea `productos/<slug>.md` con la estructura de abajo, en estado `en-construccion`.

Nada de lo anterior se saltea "porque la idea es buena". Las ideas son baratas; la validación es el filtro.

## Reglas de kill

Ver [pipeline/portfolio.md](../pipeline/portfolio.md): los productos compiten entre sí por capacidad de agentes y atención de Fabian. Lo que no tracciona se mata o se pausa. El pipeline crea productos, pero también los mata — con agentes baratos, el riesgo es el cementerio de productos zombies. Cada ficha indica sus **dependencias con otros productos** (la tesis los conecta: matar uno puede romper otro).

## Estructura de cada ficha (`productos/<slug>.md`)

```markdown
# <Nombre del producto>

- **Slug:** <slug>
- **Estado en el pipeline:** en-construccion | dogfooding | lanzamiento | comercial | operacion | pausado | sunset
- **Problema:** ¿qué dolor resuelve, para quién?
- **Cliente objetivo:** segmento concreto, no "todo el mundo".
- **Pricing:** modelo y precio validado (con método, no estimado).
- **P&L:** ingresos, costos (infra a $0 + atención de Fabian), margen. Actualiza el Reporter.
- **Dependencias con otros productos:** qué MCP consume, qué MCP expone, qué se rompe si este producto muere.
- **Criterios de kill:** umbrales explícitos (tracción, ingresos, fecha de revisión).
- **Notas:** decisiones, aprendizajes, links a artefactos del pipeline.
```

Reglas de la ficha:

- **Una ficha por producto**, nombre de archivo = slug en minúsculas con guiones.
- El **estado** siempre refleja la etapa real del pipeline, no la aspiracional.
- El **P&L** se actualiza cada mes (lo genera el Reporter, lo revisa Fabian).
- Las **dependencias** se mantienen al día: es el mapa que hace real la tesis de productos interconectados.
- Un producto en `sunset` conserva su ficha con el plan de migración y cierre hasta que el último cliente esté resuelto.
