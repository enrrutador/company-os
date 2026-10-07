# Auditoría y logs

*Fuente de verdad: [Diseño operativo v1(../empresa/diseno-operativo-v1.md · Fecha: 2026-10-07*

Principio: **todo queda registrado. Sin log, no existe.** La empresa responde por lo que hagan sus agentes; los logs son la prueba.

## Qué se loguea de cada acción

Cada acción de cada agente registra, como mínimo:

- **Timestamp**: fecha y hora exacta de la acción.
- **Agente**: qué identidad no-humana actuó ([identidades.md](identidades.md)).
- **Acción**: qué hizo, en términos verificables (no solo "procesó datos").
- **Resumen de inputs**: con qué información trabajó, resumida (no el contenido crudo completo).
- **Datos accedidos**: qué leyó y qué escribió (qué sistemas, qué registros).
- **Estado de aprobación**: autónomo / on-the-loop (revisado por Fabian: sí/no, cuándo) / in-the-loop (aprobado por Fabian: sí/no, cuándo, con qué alcance).
- **Resultado**: éxito, fallo, escalación; y a qué derivó (siguiente acción, ticket, cola de aprobación).

## Log append-only e inmutable

- El log es **append-only**: se agrega, nunca se edita ni se borra. Una corrección se registra como una nueva entrada que referencia a la anterior.
- Ningún agente puede modificar ni eliminar entradas del log, ni siquiera las propias. Escribir en el log y ejecutar acciones son permisos separados (logger ≠ ejecutor).
- Si un agente factura o mueve dinero: facturación electrónica ARCA desde el día uno, todo trazable contra el log.

## Retención y redacción de PII

- **Redactar PII antes de loguear**: los datos personales (nombres, emails, teléfonos, documentos, datos de pago) se redactan o se reemplazan por referencias antes de entrar al log. El log dice *qué tipo de dato* se usó, no el dato.
- Los secretos y credenciales nunca aparecen en texto plano: solo referencias al vault ([identidades.md](identidades.md)).
- **Retención**: los logs se conservan por el plazo que exija la normativa aplicable (fiscal, protección de datos) y por el tiempo que la operación necesite para investigar incidentes. Definir los plazos concretos con asesoría legal antes del primer cliente; documentarlos acá cuando existan.
- Riesgo conocido: fuga de datos en logs y prompt injection / tool poisoning → la redacción de PII y el uso de MCP solo de fuentes confiables son mitigaciones obligatorias, no opcionales.

## Tenancy: aislamiento por producto y por cliente

- **Ningún agente cruza datos entre clientes.** Cada producto y cada cliente opera en su propio tenant lógico: sus datos, sus credenciales, sus logs.
- El CRM, el vault y los logs están particionados por tenant. Una consulta de un agente solo ve el tenant para el que está autorizado en esa tarea.
- El aislamiento se verifica en el red-team inicial de cada agente y en revisiones periódicas: intentar acceder a datos de otro tenant debe fallar y debe quedar registrado el intento.

## Los logs como memoria institucional

Fabian es el único humano: si él no está, la empresa sigue operando con agentes. Los logs son la **memoria institucional** que permite retomar, investigar y aprender:

- **Runbooks por agente**: documentan cómo opera cada agente, sus límites y sus procedimientos de contingencia. Son el punto único de fallo declarado: si algo le pasa a Fabian, cualquiera (o un futuro él) retoma desde los runbooks + los logs.
- Los reportes del Analyst y del Reporter se construyen sobre los logs, no sobre memoria de agentes.
- Revisión periódica: los logs alimentan la revisión de niveles de autonomía ([autonomia.md](autonomia.md) — regla de oro de los ~30 días) y la detección de patrones anómalos (Guardian).
