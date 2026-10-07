"""Cliente del proxy LiteLLM.

Los agentes nunca hablan directo con el proveedor: hablan con el proxy local
(http://localhost:4000/v1), que es compatible con la API de OpenAI.
La API key del proveedor vive en el proxy, no acá.
"""
import os

from openai import OpenAI

try:
    import httpx  # noqa: F401
except ImportError:  # entornos con el fork httpx2
    import httpx2 as httpx  # type: ignore[no-redef]


def crear_cliente() -> OpenAI:
    base_url = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000/v1")
    master_key = os.environ.get("LITELLM_MASTER_KEY", "")
    if not master_key:
        raise RuntimeError(
            "Falta LITELLM_MASTER_KEY en el entorno. "
            "Copiá infraestructura/litellm/.env.ejemplo a .env y completalo."
        )
    # El proxy LiteLLM es siempre local: ignorar proxies/variables del entorno
    # (en algunos entornos el no_proxy del sistema rompe el parseo del cliente).
    http_client = httpx.Client(trust_env=False, timeout=120.0)
    return OpenAI(base_url=base_url, api_key=master_key, http_client=http_client)


def completar(cliente: OpenAI, modelo: str, system: str, tarea: str,
             temperature: float = 0.2) -> dict:
    """Una pasada de chat contra el proxy. Devuelve texto + uso de tokens."""
    resp = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": tarea},
        ],
        temperature=temperature,
    )
    eleccion = resp.choices[0].message.content or ""
    uso = resp.usage
    return {
        "texto": eleccion,
        "tokens_entrada": uso.prompt_tokens if uso else None,
        "tokens_salida": uso.completion_tokens if uso else None,
    }
