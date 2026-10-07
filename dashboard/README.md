# Dashboard — panel visual de la empresa

El tablero de comando de Fabian: manejar y configurar toda la empresa desde el
navegador, sin tocar la terminal.

## Iniciar

```bash
# Desde la raíz del repo
python3 dashboard/servidor.py

# Abrir: http://localhost:8080
```

Solo usa la biblioteca estándar de Python: no instala nada nuevo.

## Qué incluye

| Pestaña | Qué hace |
|---|---|
| **Agentes** | Los 25 agentes en tarjetas. Clic → escribís la tarea → el agente la ejecuta y ves la respuesta con tokens usados. |
| **Auditoría** | Últimas 50 ejecuciones: quién hizo qué, cuándo, con qué modelo y cuántos tokens. |
| **Configuración** | Tu API key del proveedor y los modelos (base / razonamiento / ligero) en formulario. La key se muestra enmascarada y nunca viaja más allá de tu máquina. |
| **Empresa** | Estado de un vistazo: agentes, etapas del pipeline, productos en portfolio, si el proveedor está conectado. |

## Cómo funciona

```
navegador ──▶ dashboard/servidor.py ──▶ runtime/nucleo ──▶ proxy LiteLLM ──▶ tu proveedor
              (http://localhost:8080)     (agentes + auditoría)   (localhost:4000)
```

El dashboard **no reemplaza** al proxy: los agentes siguen saliendo por LiteLLM.
El dashboard solo les habla y les muestra la configuración del `.env`.

## Seguridad

- Escucha **solo en 127.0.0.1**: accesible únicamente desde tu máquina.
- **Nunca lo expongas a internet** (sin autenticación, la configuración incluye secretos).
- La API key se guarda en `infraestructura/litellm/.env` (ignorado por git) y la
  API del dashboard la devuelve enmascarada.
