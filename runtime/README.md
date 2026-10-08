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

## Orquestador multi-agente (LangGraph)

El pipeline como código ejecutable: `orquestador/` implementa las etapas como
grafos LangGraph que encadenan agentes, pasando artefactos de uno al siguiente.

```bash
# Etapa 3 (Construcción): spec → diseño → UX → build → revisión → seguridad
# → QA → (reintento si QA rechaza, máx 2) → SRE → despliegue
python3 ejecutar_pipeline.py construccion --objetivo "App de lista de tareas"
python3 ejecutar_pipeline.py construccion --objetivo "..." --componentes constructor,ingeniero-datos
```

- **Borde condicional real**: si Control de Calidad cierra con `VEREDICTO: RECHAZADO`,
  el grafo vuelve al build automáticamente (máximo 2 reintentos).
- **In-the-loop**: el despliegue frena con `PENDIENTE_APROBACION_FABIAN` salvo que
  se exporte `APROBACION_DESPLIEGUE=si`. Lo irreversible lo aprueba Fabian, siempre.
- **Artefactos encadenados**: cada nodo recibe los artefactos previos como contexto
  (recortados a 6000 caracteres para cuidar el contexto).
- Nuevas etapas se agregan en `orquestador/grafos.py` (diccionario `ETAPAS`).

```bash
python3 pruebas/test_orquestador_mock.py   # grafo completo contra mock
```

## Modo empresa (pipeline punta a punta)

Un objetivo en lenguaje natural, y el Gerente General orquesta las etapas:

```bash
python3 ejecutar_pipeline.py producto --objetivo "Tu objetivo en lenguaje natural"
```

Flujo: **tesis** (etapa 1: el GG escribe la tesis, el equipo rojo la ataca,
veredicto SEGUIR/MATAR) → **validación** (etapa 2: investigación, landing,
cobro de preventa, veredicto VALIDADO/DESCARTADO) → **construcción**
(etapa 3) → **comercial** (etapa 6: ICP, outreach, criterios, plan comercial).

Cada etapa puede matar el producto: si la tesis da MATAR o la validación da
DESCARTADO, el grafo se detiene ahí y lo reporta (no se construye nada).

```bash
python3 pruebas/test_producto_mock.py   # camino feliz + kill en tesis, contra mock
```

## Probar sin computadora (Kaggle)

El runtime corre en la máquina virtual gratuita de Kaggle, sin proxy LiteLLM:
apunta directo a tu proveedor con estas variables:

```bash
export LITELLM_BASE_URL="https://api.openai.com/v1"   # o tu proveedor OpenAI-compatible
export LITELLM_MASTER_KEY="tu-key"
export MODELO_EMPRESA_BASE="gpt-4o-mini"
export MODELO_EMPRESA_RAZONAMIENTO="gpt-4o"           # o el que elijas
export MODELO_EMPRESA_LIGERO="gpt-4o-mini"
```

`runtime/kaggle/probar-modo-empresa.ipynb` es el notebook listo: lo subís a
Kaggle (*New Notebook → Upload*), cargás dos secretos (*Add-ons → Secrets*:
`GITHUB_TOKEN` con acceso al repo y `LLM_API_KEY`), editás proveedor/modelos
y corrés las celdas en orden: dependencias → clon → smoke test de un agente →
modo empresa → auditoría. En Kaggle se usa el CLI (el dashboard no expone
puertos públicos).
