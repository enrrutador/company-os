#!/usr/bin/env python3
"""Dashboard web local de la empresa (Company OS).

Panel visual para manejar y configurar todo sin tocar la terminal:
  - Agentes: ver los 26, buscarlos, asignarles tareas, leer respuestas.
  - Auditoría: quién hizo qué, cuándo, cuántos tokens (filtrable, expandible).
  - Configuración: API key y modelos en formulario, con prueba de conexión
    en vivo contra el proveedor (detecta modelos muertos antes de ejecutar).
  - Empresa: pipeline y productos de un vistazo.

Uso:
    python3 servidor.py [--puerto 8080]

    Abrir en el navegador: http://localhost:8080

Solo biblioteca estándar (sin dependencias nuevas), salvo la importación
perezosa de `openai` al ejecutar o probar modelos. Escucha únicamente en
127.0.0.1: nunca exponer a internet — la configuración incluye secretos.
"""
import argparse
import json
import os
import re
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

RAIZ_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIR_DASHBOARD = os.path.dirname(os.path.abspath(__file__))
RUTA_ENV = os.path.join(RAIZ_REPO, "infraestructura", "litellm", ".env")

sys.path.insert(0, os.path.join(RAIZ_REPO, "runtime"))
from nucleo import agente as modulo_agente  # noqa: E402
# NOTA: `nucleo.cliente` (requiere `openai`) se importa perezoso solo al ejecutar
# o probar modelos, para que el dashboard abra sin dependencias más allá de la
# biblioteca estándar.

CLAVES_ENV = [
    "LLM_API_KEY",
    "MODELO_EMPRESA_BASE",
    "MODELO_EMPRESA_RAZONAMIENTO",
    "MODELO_EMPRESA_LIGERO",
    "LITELLM_BASE_URL",
    "LITELLM_MASTER_KEY",
]
CLAVES_SECRETAS = {"LLM_API_KEY", "LITELLM_MASTER_KEY"}
# Modelos que se prueban en "Probar conexión": (clave de env, etiqueta).
MODELOS_PROBABLES = [
    ("MODELO_EMPRESA_BASE", "base"),
    ("MODELO_EMPRESA_RAZONAMIENTO", "razonamiento"),
    ("MODELO_EMPRESA_LIGERO", "ligero"),
]


# ---------------------------------------------------------------- .env
def leer_env() -> dict:
    valores = {}
    if os.path.exists(RUTA_ENV):
        with open(RUTA_ENV, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                k, v = linea.split("=", 1)
                valores[k.strip()] = v.strip()
    return valores


def escribir_env(nuevos: dict) -> None:
    """Actualiza solo las claves recibidas, preservando comentarios y orden."""
    lineas = []
    vistas = set()
    if os.path.exists(RUTA_ENV):
        with open(RUTA_ENV, encoding="utf-8") as f:
            lineas = f.readlines()
    salida = []
    for linea in lineas:
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", linea.strip())
        if m and m.group(1) in nuevos:
            salida.append(f"{m.group(1)}={nuevos[m.group(1)]}\n")
            vistas.add(m.group(1))
        else:
            salida.append(linea)
    for k, v in nuevos.items():
        if k not in vistas:
            salida.append(f"{k}={v}\n")
    os.makedirs(os.path.dirname(RUTA_ENV), exist_ok=True)
    tmp = RUTA_ENV + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.writelines(salida)
    os.replace(tmp, RUTA_ENV)


def aplicar_env() -> dict:
    """Aplica el .env del dashboard sobre el entorno del proceso.

    El archivo es la fuente de verdad de lo que se configuró en la pestaña
    Configuración: lo que se guarda ahí es lo que se usa al ejecutar.
    Las claves que el archivo no trae (p. ej. en Kaggle, donde los secretos
    viven como variables de entorno) se dejan intactas.
    """
    valores = leer_env()
    for k, v in valores.items():
        if k in CLAVES_ENV:
            os.environ[k] = v
    return valores


def config_publica() -> dict:
    aplicar_env()
    valores = {k: os.environ.get(k, "") for k in CLAVES_ENV}
    pub = {}
    for k in CLAVES_ENV:
        v = valores.get(k, "")
        if k in CLAVES_SECRETAS:
            pub[k] = {"configurada": bool(v), "ultimos4": v[-4:] if len(v) >= 4 else ""}
        else:
            pub[k] = v
    return pub


# ---------------------------------------------------------------- datos
def info_agentes() -> list:
    aplicar_env()
    datos = []
    for slug in modulo_agente.slugs():
        ficha_rel, modelo = modulo_agente.REGISTRO[slug]
        try:
            with open(os.path.join(RAIZ_REPO, ficha_rel), encoding="utf-8") as f:
                lineas = f.read().splitlines()
            nombre = lineas[0].lstrip("# ").strip() if lineas else slug
            area = ""
            for ln in lineas[1:8]:
                m = re.match(r"\*\*Área\*\*:\s*(.+)", ln)
                if m:
                    area = m.group(1).strip()
                    break
        except OSError:
            nombre, area = slug, ""
        datos.append({"slug": slug, "nombre": nombre, "area": area, "modelo": modelo,
                      "modelo_efectivo": modulo_agente._resolver_modelo(modelo)})
    return datos


def leer_auditoria(limite: int = 50, agente: str = "") -> dict:
    from nucleo import auditoria
    eventos = []
    try:
        with open(auditoria.ARCHIVO, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    try:
                        eventos.append(json.loads(linea))
                    except json.JSONDecodeError:
                        continue
    except FileNotFoundError:
        pass
    total = len(eventos)
    if agente:
        eventos = [e for e in eventos if e.get("agente") == agente]
    tokens = sum((e.get("tokens_entrada") or 0) + (e.get("tokens_salida") or 0)
                 for e in eventos)
    return {
        "total": total,
        "filtrados": len(eventos),
        "tokens": tokens,
        "eventos": eventos[-limite:][::-1],
    }


def estado_empresa() -> dict:
    aplicar_env()
    etapas = []
    try:
        with open(os.path.join(RAIZ_REPO, "pipeline", "etapas.md"), encoding="utf-8") as f:
            for linea in f:
                m = re.match(r"##\s+(\d+)\.\s+(.+)", linea)
                if m:
                    etapas.append({"n": int(m.group(1)), "nombre": m.group(2).strip()})
    except OSError:
        pass
    productos = []
    dir_prod = os.path.join(RAIZ_REPO, "productos")
    try:
        for fn in sorted(os.listdir(dir_prod)):
            if fn.endswith(".md") and fn != "README.md":
                productos.append(fn[:-3])
    except OSError:
        pass
    return {
        "agentes": len(modulo_agente.slugs()),
        "etapas": etapas,
        "productos": productos,
        "proxy_configurado": bool(os.environ.get("LITELLM_MASTER_KEY")),
    }


def probar_modelos() -> dict:
    """Prueba en vivo cada modelo configurado contra el proveedor.

    Devuelve por modelo: ok True/False, latencia en ms o mensaje de error.
    Detecta modelos muertos/retirados (p. ej. HTTP 410) antes de ejecutar.
    """
    aplicar_env()
    try:
        from nucleo import cliente as modulo_cliente
    except ImportError:
        raise RuntimeError(
            "Falta el paquete 'openai': instalá dependencias con "
            "`pip install -r runtime/requirements.txt`."
        )
    c = modulo_cliente.crear_cliente()
    try:
        publicados = [m.id for m in c.models.list(timeout=30)]
    except Exception:  # noqa: BLE001 - no es fatal para la prueba
        publicados = []
    resultados = []
    for clave, etiqueta in MODELOS_PROBABLES:
        modelo = os.environ.get(clave, "")
        if not modelo:
            resultados.append({"clave": clave, "etiqueta": etiqueta, "modelo": "",
                               "ok": False, "error": "no configurado"})
            continue
        t0 = time.monotonic()
        try:
            r = c.chat.completions.create(
                model=modelo,
                messages=[{"role": "user",
                           "content": "Responde con una sola palabra: ok"}],
                max_tokens=16,
                temperature=0,
                timeout=45,
            )
            texto = (r.choices[0].message.content or "").strip()
            ms = int((time.monotonic() - t0) * 1000)
            if texto:
                resultados.append({"clave": clave, "etiqueta": etiqueta,
                                   "modelo": modelo, "ok": True,
                                   "latencia_ms": ms,
                                   "en_catalogo": (modelo in publicados) if publicados else None})
            else:
                resultados.append({"clave": clave, "etiqueta": etiqueta,
                                   "modelo": modelo, "ok": False,
                                   "error": "el modelo respondió vacío"})
        except Exception as e:  # noqa: BLE001 - se reporta en el resultado
            resultados.append({"clave": clave, "etiqueta": etiqueta,
                               "modelo": modelo, "ok": False,
                               "error": str(e)[:220]})
    return {"modelos_publicados": len(publicados), "resultados": resultados}


# ---------------------------------------------------------------- servidor
class Manejador(BaseHTTPRequestHandler):
    server_version = "CompanyOS/1.0"

    def _json(self, obj, codigo=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _html(self):
        with open(os.path.join(DIR_DASHBOARD, "index.html"), "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _cuerpo(self) -> dict:
        largo = int(self.headers.get("Content-Length", 0) or 0)
        if not largo:
            return {}
        try:
            return json.loads(self.rfile.read(largo) or b"{}")
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def _entero(qs, clave, defecto, minimo=1, maximo=200):
        try:
            v = int(qs.get(clave, [str(defecto)])[0])
        except (ValueError, TypeError):
            v = defecto
        return max(minimo, min(maximo, v))

    def do_GET(self):  # noqa: N802
        ruta = urlparse(self.path)
        if ruta.path in ("/", "/index.html"):
            self._html()
        elif ruta.path == "/api/agentes":
            self._json(info_agentes())
        elif ruta.path == "/api/auditoria":
            qs = parse_qs(ruta.query)
            limite = self._entero(qs, "limite", 50)
            agente = (qs.get("agente", [""])[0] or "").strip()
            if agente and agente not in modulo_agente.slugs():
                self._json({"ok": False, "error": "agente desconocido"}, 400)
                return
            self._json(leer_auditoria(limite, agente))
        elif ruta.path == "/api/config":
            self._json(config_publica())
        elif ruta.path == "/api/empresa":
            self._json(estado_empresa())
        elif ruta.path == "/api/modelos":
            # Modelos por nivel ya resueltos (para el selector del chat).
            aplicar_env()
            self._json({
                "base": modulo_agente._resolver_modelo("empresa-base"),
                "razonamiento": modulo_agente._resolver_modelo("empresa-razonamiento"),
                "ligero": modulo_agente._resolver_modelo("empresa-ligero"),
            })
        else:
            self._json({"ok": False, "error": "no encontrado"}, 404)

    def do_POST(self):  # noqa: N802
        ruta = urlparse(self.path)
        if ruta.path == "/api/ejecutar":
            cuerpo = self._cuerpo()
            slug = cuerpo.get("slug", "")
            tarea = cuerpo.get("tarea", "")
            if not slug or not tarea:
                self._json({"ok": False, "error": "faltan slug o tarea"}, 400)
                return
            if slug not in modulo_agente.slugs():
                self._json({"ok": False, "error": "agente desconocido"}, 400)
                return
            try:
                aplicar_env()
                try:
                    from nucleo import cliente as modulo_cliente
                except ImportError:
                    raise RuntimeError(
                        "Falta el paquete 'openai': instalá dependencias con "
                        "`pip install -r runtime/requirements.txt`."
                    )
                c = modulo_cliente.crear_cliente()
                historial = cuerpo.get("historial", [])
                if not isinstance(historial, list):
                    historial = []
                r = modulo_agente.ejecutar_agente(
                    slug, tarea, c, forzar_modelo=cuerpo.get("modelo", ""),
                    historial=historial)
                self._json({"ok": True, "agente": r["agente"], "modelo": r["modelo"],
                            "texto": r["texto"],
                            "tokens_entrada": r["tokens_entrada"],
                            "tokens_salida": r["tokens_salida"]})
            except Exception as e:  # noqa: BLE001 - se reporta al dashboard
                self._json({"ok": False, "error": str(e)})
        elif ruta.path == "/api/orquestar":
            # El Gerente General planifica, delega a especialistas y consolida.
            cuerpo = self._cuerpo()
            tarea = cuerpo.get("tarea", "")
            if not tarea:
                self._json({"ok": False, "error": "falta tarea"}, 400)
                return
            try:
                aplicar_env()
                try:
                    from nucleo import cliente as modulo_cliente
                    from nucleo import delegacion as modulo_delegacion
                except ImportError:
                    raise RuntimeError(
                        "Falta el paquete 'openai': instalá dependencias con "
                        "`pip install -r runtime/requirements.txt`."
                    )
                c = modulo_cliente.crear_cliente()
                modelo = cuerpo.get("modelo", "")
                r = modulo_delegacion.orquestar(tarea, c, forzar_modelo=modelo)
                self._json({"ok": True, **r})
            except Exception as e:  # noqa: BLE001 - se reporta al dashboard
                self._json({"ok": False, "error": str(e)})
        elif ruta.path == "/api/probar":
            try:
                r = probar_modelos()
                self._json({"ok": True, **r})
            except Exception as e:  # noqa: BLE001 - se reporta al dashboard
                self._json({"ok": False, "error": str(e)})
        elif ruta.path == "/api/config":
            cuerpo = self._cuerpo()
            nuevos = {}
            for k in CLAVES_ENV:
                if k in cuerpo and isinstance(cuerpo[k], str):
                    v = cuerpo[k].strip()
                    # clave secreta vacía = conservar la actual
                    if k in CLAVES_SECRETAS and not v:
                        continue
                    nuevos[k] = v
            escribir_env(nuevos)
            self._json({"ok": True, "config": config_publica()})
        else:
            self._json({"ok": False, "error": "no encontrado"}, 404)

    def log_message(self, *args):  # noqa: N802
        pass


def main() -> int:
    ap = argparse.ArgumentParser(description="Dashboard web local de la empresa.")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("DASHBOARD_PORT", "8080")))
    args = ap.parse_args()
    servidor = ThreadingHTTPServer(("127.0.0.1", args.puerto), Manejador)
    print(f"Dashboard en http://localhost:{args.puerto}  (Ctrl+C para detener)")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
