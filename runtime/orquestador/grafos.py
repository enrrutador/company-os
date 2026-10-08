"""Grafos LangGraph que implementan las etapas del pipeline.

V1: etapa 3 (Construcción) — la secuencia multi-agente más densa:
  Gerente General (spec) → Arquitecto (diseño) → Diseñador UX/UI
  → Constructor/Mobile/Datos/ML (build) → Revisor → Seguridad
  → Control de Calidad --(rechazo)--> build (reintento, máx 2)
  → SRE (SLOs) → Responsable de Despliegues (frena sin aprobación de Fabian)

Cada nodo ejecuta un agente con el runtime existente y deja su artefacto
en el estado; el siguiente nodo lo recibe como contexto. Todo queda en la
auditoría como ejecuciones individuales.
"""
import operator
import os
from typing import TypedDict, Annotated

from langgraph.graph import StateGraph, END

from nucleo import agente as modulo_agente
from nucleo import cliente as modulo_cliente

MAX_REINTENTOS_QA = 2
MAX_CHARS_ARTEFACTO = 6000


class Estado(TypedDict):
    objetivo: str
    componentes: list
    artefactos: Annotated[dict, operator.or_]
    traza: Annotated[list, operator.add]
    reintentos_qa: int


def _resumen_artefactos(artefactos: dict) -> str:
    if not artefactos:
        return "(sin artefactos previos)"
    partes = []
    for nombre, texto in artefactos.items():
        recorte = texto[:MAX_CHARS_ARTEFACTO]
        if len(texto) > MAX_CHARS_ARTEFACTO:
            recorte += "\n[...recortado...]"
        partes.append(f"--- {nombre} ---\n{recorte}")
    return "\n\n".join(partes)


def _nodo(slug: str, artefacto: str, plantilla: str):
    """Crea un nodo que ejecuta un agente y guarda su artefacto."""
    def fn(state: Estado) -> dict:
        c = modulo_cliente.crear_cliente()
        tarea = plantilla.format(
            objetivo=state["objetivo"],
            artefactos=_resumen_artefactos(state["artefactos"]),
        )
        r = modulo_agente.ejecutar_agente(slug, tarea, c)
        return {
            "artefactos": {artefacto: r["texto"]},
            "traza": [f"{slug}: artefacto '{artefacto}' generado"],
        }
    fn.__name__ = f"nodo_{slug}_{artefacto}"
    return fn


def _nodo_build(state: Estado) -> dict:
    """Ejecuta los builders según los componentes pedidos (constructor por defecto)."""
    c = modulo_cliente.crear_cliente()
    artefactos, traza = {}, []
    for slug in state.get("componentes") or ["constructor"]:
        tarea = (
            f"Objetivo del producto: {state['objetivo']}\n\n"
            f"Artefactos previos:\n{_resumen_artefactos(state['artefactos'])}\n\n"
            "Implementá tu parte según tu rol. Si algo de la especificación o el "
            "diseño es ambiguo, declará el supuesto explícitamente en tu entrega."
        )
        r = modulo_agente.ejecutar_agente(slug, tarea, c)
        artefactos[f"build_{slug}"] = r["texto"]
        traza.append(f"{slug}: build completado")
    return {"artefactos": artefactos, "traza": traza}


def _nodo_despacho_qa(state: Estado) -> str:
    """Borde condicional: si QA rechaza, se reintenta el build (máx 2)."""
    reporte = state["artefactos"].get("reporte_qa", "")
    reintentos = state.get("reintentos_qa") or 0
    if "VEREDICTO: RECHAZADO" in reporte and reintentos < MAX_REINTENTOS_QA:
        return "reintentar"
    return "seguir"


def _nodo_reintento(state: Estado) -> dict:
    return {
        "reintentos_qa": (state.get("reintentos_qa") or 0) + 1,
        "traza": ["control-de-calidad: veredicto RECHAZADO, se reintenta el build"],
    }


def _nodo_despliegue(state: Estado) -> dict:
    """In-the-loop: sin aprobación explícita de Fabian no se despliega."""
    if os.environ.get("APROBACION_DESPLIEGUE", "").lower() != "si":
        return {
            "artefactos": {
                "despliegue": (
                    "PENDIENTE_APROBACION_FABIAN: el plan de despliegue está listo "
                    "pero no se ejecutó. Fabian debe aprobar (in-the-loop)."
                )
            },
            "traza": ["responsable-despliegues: frenado, pendiente aprobación de Fabian"],
        }
    c = modulo_cliente.crear_cliente()
    tarea = (
        f"Objetivo del producto: {state['objetivo']}\n\n"
        f"Artefactos previos:\n{_resumen_artefactos(state['artefactos'])}\n\n"
        "Fabian APROBÓ el despliegue. Ejecutá el plan de despliegue según tu rol."
    )
    r = modulo_agente.ejecutar_agente("responsable-despliegues", tarea, c)
    return {
        "artefactos": {"despliegue": r["texto"]},
        "traza": ["responsable-despliegues: despliegue ejecutado con aprobación"],
    }


def grafo_construccion():
    """Construye y compila el grafo de la etapa 3."""
    g = StateGraph(Estado)

    g.add_node("spec", _nodo(
        "gerente-general", "especificacion",
        "Objetivo del producto: {objetivo}\n\n"
        "Escribí la especificación funcional completa: qué se construye, para quién, "
        "criterios de aceptación verificables y criterios de salida del uso interno."))
    g.add_node("diseno", _nodo(
        "arquitecto", "diseno",
        "Especificación:\n{artefactos}\n\n"
        "Diseñá la arquitectura (C4) y registrá los ADRs de las decisiones relevantes."))
    g.add_node("ux", _nodo(
        "disenador-ux-ui", "diseno_ux",
        "Especificación y diseño:\n{artefactos}\n\n"
        "Diseñá flujos y pantallas según tu rol. El diseño entra antes del código."))
    g.add_node("build", _nodo_build)
    g.add_node("revision", _nodo(
        "revisor", "revision",
        "Artefactos previos:\n{artefactos}\n\n"
        "Revisá el código entregado en los artefactos build_*. Marcá bloqueantes y "
        "sugerencias. Cerrá con tu veredicto."))
    g.add_node("seguridad", _nodo(
        "ingeniero-seguridad", "revision_seguridad",
        "Artefactos previos:\n{artefactos}\n\n"
        "Revisá la seguridad de lo construido (threat model ligero + OWASP). "
        "Si hay riesgo crítico, declaralo y FRENÁ el flujo con justificación."))
    g.add_node("qa", _nodo(
        "control-de-calidad", "reporte_qa",
        "Artefactos previos:\n{artefactos}\n\n"
        "Probá lo construido y reportá. Cerrá SIEMPRE con una línea exacta: "
        "'VEREDICTO: APROBADO' o 'VEREDICTO: RECHAZADO' (con motivos si rechazás)."))
    g.add_node("reintento", _nodo_reintento)
    g.add_node("sre", _nodo(
        "sre", "slos",
        "Artefactos previos:\n{artefactos}\n\n"
        "Definí los SLOs del producto (disponibilidad, latencia, errores) y la "
        "observabilidad mínima para el lanzamiento."))
    g.add_node("despliegue", _nodo_despliegue)

    g.set_entry_point("spec")
    g.add_edge("spec", "diseno")
    g.add_edge("diseno", "ux")
    g.add_edge("ux", "build")
    g.add_edge("build", "revision")
    g.add_edge("revision", "seguridad")
    g.add_edge("seguridad", "qa")
    g.add_conditional_edges("qa", _nodo_despacho_qa,
                            {"reintentar": "reintento", "seguir": "sre"})
    g.add_edge("reintento", "build")
    g.add_edge("sre", "despliegue")
    g.add_edge("despliegue", END)

    return g.compile()


# Registro de etapas implementadas (extensible: una entrada = un grafo)
ETAPAS = {
    "construccion": ("Etapa 3 — Construcción", grafo_construccion),
}


def ejecutar_etapa(etapa: str, objetivo: str, componentes: list | None = None) -> dict:
    """Ejecuta una etapa del pipeline y devuelve el estado final."""
    if etapa not in ETAPAS:
        raise ValueError(f"Etapa desconocida: {etapa}. Disponibles: {', '.join(ETAPAS)}")
    _, constructor = ETAPAS[etapa]
    grafo = constructor()
    estado_inicial: Estado = {
        "objetivo": objetivo,
        "componentes": componentes or ["constructor"],
        "artefactos": {},
        "traza": [],
        "reintentos_qa": 0,
    }
    return grafo.invoke(estado_inicial)
