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
| **Agentes** | Los 26 agentes en tarjetas, con buscador. Clic → se abre un **chat** con el agente: múltiples mensajes con historial (Enter para enviar, Shift+Enter para salto de línea), **selector de modelo** en la caja de mensajería (por defecto usa el del agente; elegís Base/Razonamiento/Ligero y viaja con cada mensaje), indicador de "escribiendo", respuestas con formato (títulos, listas, tablas, código) y botón Cancelar. En la tarjeta del Gerente General hay además **Orquestar**: delega a especialistas y consolida la respuesta (la traza de delegaciones queda colapsada, clic para verla; respeta el modelo elegido para todas las llamadas). |
| **Auditoría** | Últimas 50 ejecuciones: quién hizo qué, cuándo, con qué modelo y cuántos tokens. Filtrable por agente; clic en un evento para ver tarea y respuesta completas. |
| **Configuración** | Tu API key del proveedor y los modelos (base / razonamiento / ligero) en formulario. La key se muestra enmascarada y nunca viaja más allá de tu máquina. **Probar conexión** verifica en vivo que cada modelo configurado responde (detecta modelos retirados, p. ej. HTTP 410, antes de ejecutar). |
| **Empresa** | Estado de un vistazo: agentes, etapas del pipeline, productos en portfolio, si el proveedor está conectado. |

## Cómo funciona

```
navegador ──▶ dashboard/servidor.py ──▶ runtime/nucleo ──▶ proxy LiteLLM ──▶ tu proveedor
              (http://localhost:8080)     (agentes + auditoría)   (localhost:4000)
```

El dashboard **no reemplaza** al proxy: los agentes siguen saliendo por LiteLLM.
El dashboard solo les habla y les muestra la configuración del `.env`.

**Precedencia de configuración:** lo que guardás en la pestaña Configuración
(archivo `infraestructura/litellm/.env`) rige de inmediato para las próximas
ejecuciones y es lo que muestran las tarjetas. Las variables de entorno del
proceso que el archivo no menciona (p. ej. los secretos de Kaggle) se respetan
tal cual.

## Seguridad

- Escucha **solo en 127.0.0.1**: accesible únicamente desde tu máquina.
- **Nunca lo expongas a internet** (sin autenticación, la configuración incluye secretos).
- La API key se guarda en `infraestructura/litellm/.env` (ignorado por git) y la
  API del dashboard la devuelve enmascarada.
