"""Registro y ejecución de los 18 agentes.

Cada agente se define por su ficha (el QUÉ) + su SKILL.md (el CÓMO).
El prompt del sistema se compone de ambos archivos del repo.
"""
import os

# slug -> (ficha relativa a la raíz del repo, modelo del proxy)
REGISTRO = {
    "gerente-general": ("agentes/direccion/gerente-general.md", "empresa-razonamiento"),
    "constructor": ("agentes/ingenieria/constructor.md", "empresa-base"),
    "revisor": ("agentes/ingenieria/revisor.md", "empresa-razonamiento"),
    "control-de-calidad": ("agentes/ingenieria/control-de-calidad.md", "empresa-base"),
    "responsable-despliegues": ("agentes/ingenieria/responsable-despliegues.md", "empresa-base"),
    "prospector": ("agentes/ventas/prospector.md", "empresa-base"),
    "contacto-inicial": ("agentes/ventas/contacto-inicial.md", "empresa-base"),
    "calificador": ("agentes/ventas/calificador.md", "empresa-base"),
    "custodio-crm": ("agentes/ventas/custodio-crm.md", "empresa-ligero"),
    "soporte-n1": ("agentes/soporte/soporte-n1.md", "empresa-ligero"),
    "responsable-activacion": ("agentes/soporte/responsable-activacion.md", "empresa-base"),
    "escalamiento": ("agentes/soporte/escalamiento.md", "empresa-razonamiento"),
    "contenidos": ("agentes/marketing/contenidos.md", "empresa-base"),
    "analista": ("agentes/marketing/analista.md", "empresa-razonamiento"),
    "facturador": ("agentes/finanzas/facturador.md", "empresa-base"),
    "conciliador": ("agentes/finanzas/conciliador.md", "empresa-base"),
    "responsable-informes": ("agentes/finanzas/responsable-informes.md", "empresa-base"),
    "guardian": ("agentes/operaciones/guardian.md", "empresa-razonamiento"),
}

RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def slugs() -> list:
    return sorted(REGISTRO.keys())


def _leer(rel: str) -> str:
    with open(os.path.join(RAIZ_REPO, rel), encoding="utf-8") as f:
        return f.read()


def prompt_sistema(slug: str) -> str:
    """Compone el prompt del sistema: ficha + habilidad del agente."""
    if slug not in REGISTRO:
        raise ValueError(f"Agente desconocido: {slug}. Opciones: {', '.join(slugs())}")
    ficha_rel, _ = REGISTRO[slug]
    ficha = _leer(ficha_rel)
    try:
        skill = _leer(f"habilidades/{slug}/SKILL.md")
    except FileNotFoundError:
        skill = "(sin SKILL.md)"
    return (
        "Sos un agente de la empresa. Esta es tu ficha de rol:\n\n"
        f"{ficha}\n\n"
        "Y esta es tu habilidad operativa (cómo ejecutar tu trabajo):\n\n"
        f"{skill}\n\n"
        "Respondé en español rioplatense, directo y sin relleno. "
        "Si la tarea excede tus permisos o necesitás aprobación de Fabian, "
        "decilo explícitamente en vez de inventar."
    )


def modelo_para(slug: str) -> str:
    return REGISTRO[slug][1]


def ejecutar_agente(slug: str, tarea: str, cliente, forzar_modelo: str = "") -> dict:
    """Ejecuta un agente contra una tarea. Devuelve dict con respuesta y metadatos."""
    from . import auditoria, cliente as modulo_cliente

    sistema = prompt_sistema(slug)
    modelo = forzar_modelo or modelo_para(slug)
    resultado = modulo_cliente.completar(cliente, modelo, sistema, tarea)
    auditoria.registrar(
        agente=slug,
        modelo=modelo,
        tarea=tarea,
        respuesta=resultado["texto"],
        tokens_entrada=resultado["tokens_entrada"],
        tokens_salida=resultado["tokens_salida"],
    )
    return {"agente": slug, "modelo": modelo, **resultado}
