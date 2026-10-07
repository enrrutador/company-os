# Runtime de agentes

El corazón ejecutable de la empresa: convierte las fichas y habilidades del repo
en agentes que realmente corren contra tu proveedor de LLM.

## Arquitectura

```
vos ──▶ ejecutar.py ──▶ nucleo/agente.py ──▶ proxy LiteLLM ──▶ tu proveedor
                        (ficha + SKILL.md        (localhost:4000)
                         = prompt del sistema)
                              │
                              ▼
                       registro/auditoria.jsonl
```

- **Un solo punto de salida a modelos**: el proxy LiteLLM. Cambiar de proveedor
  o modelo no toca código.
- **Cada agente = su ficha + su SKILL.md** del repo. Mejorás el agente editando
  el Markdown, sin programar.
- **Todo queda registrado** en `registro/auditoria.jsonl` (append-only).

## Uso

```bash
# 1. Dependencias
pip install -r requirements.txt

# 2. Proxy levantado (ver infraestructura/litellm/README.md)
# 3. Ejecutar un agente
python3 ejecutar.py conciliador "Revisá estas 5 facturas y marcá inconsistencias: ..."
python3 ejecutar.py contenidos "Dame 3 ideas de post sobre automatización" --modelo empresa-ligero
python3 ejecutar.py gerente-general "Resumí el estado de la empresa en 5 líneas"
```

Los 25 slugs disponibles: `gerente-general`, `arquitecto`, `constructor`, `desarrollador-mobile`,
`ingeniero-datos`, `ingeniero-ml`, `revisor`, `control-de-calidad`, `disenador-ux-ui`,
`ingeniero-seguridad`, `sre`, `responsable-despliegues`, `prospector`, `contacto-inicial`,
`calificador`, `custodio-crm`, `soporte-n1`, `responsable-activacion`,
`escalamiento`, `contenidos`, `analista`, `facturador`, `conciliador`,
`responsable-informes`, `guardian`.

## Modelos por agente

Cada agente tiene un modelo por defecto del proxy:

| Modelo del proxy | Agentes |
|---|---|
| `empresa-razonamiento` | gerente-general, arquitecto, ingeniero-ml, ingeniero-seguridad, revisor, escalamiento, analista, guardian |
| `empresa-base` | constructor, desarrollador-mobile, ingeniero-datos, control-de-calidad, disenador-ux-ui, sre, responsable-despliegues, prospector, contacto-inicial, calificador, responsable-activacion, contenidos, facturador, conciliador, responsable-informes |
| `empresa-ligero` | custodio-crm, soporte-n1 |

Se puede forzar otro con `--modelo`.

## Pruebas

```bash
python3 pruebas/test_e2e_mock.py
```

Levanta un servidor mock compatible con la API de OpenAI y corre un agente
punta a punta sin gastar un centavo: valida el cableado completo
(CLI → prompt → HTTP → respuesta → auditoría).
