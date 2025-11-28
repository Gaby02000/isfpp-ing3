import subprocess
import re
from pathlib import Path
from shutil import which
import sys

# --- CONFIGURACIÓN ---
ROOT_DIR = Path(__file__).resolve().parent
METRICS_DIR = ROOT_DIR / "metrics"
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "web" 


def ensure_metrics_dir():
    METRICS_DIR.mkdir(exist_ok=True)


def run_cmd(cmd, output_name, cwd=None):
    """
    Ejecuta un comando de consola, guarda stdout en metrics/<output_name>
    y muestra un resumen por pantalla.
    """
    out_path = METRICS_DIR / output_name

    print(f"➡ Ejecutando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True if sys.platform == 'win32' else False 
        )
        
        out_path.write_text(result.stdout, encoding="utf-8")

        if result.returncode == 0:
            print(f"✅ OK. Salida guardada en: {out_path.name}")
        else:
            print(f"⚠ El comando terminó con error (código {result.returncode})")
            print(f"   Revisá el archivo {out_path.name} para ver el error.")
        
        return result.returncode

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el comando '{cmd[0]}'. Asegurate de tenerlo instalado.")
        return -1


# ---------------- PARSEADORES ----------------

def parse_backend_totals(path: Path):
    """
    Parsea el bloque de Total que escribe `radon raw -s`.
    """
    if not path.exists():
        return None

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    inside_total = False
    totals = {}

    for line in lines:
        if not inside_total and "Total" in line:
            inside_total = True
            continue

        if inside_total:
            stripped = line.strip()
            if not stripped or stripped.startswith("- Comment Stats"):
                if stripped.startswith("- Comment Stats"):
                    break
                if not stripped: 
                     if totals: break
                     continue

            if ":" not in stripped:
                continue

            parts = stripped.split(":", 1)
            name = parts[0].strip()
            value_part = parts[1].strip()
            
            m = re.search(r"(\d+)", value_part)
            if not m:
                continue

            totals[name] = int(m.group(1))

    return totals or None


def parse_frontend_totals(path: Path):
    """
    Parsea la salida por defecto de `sloc`.
    """
    if not path.exists():
        return None

    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    labels = ["Physical", "Source", "Comment", "Empty", "To Do"]
    totals = {}

    for line in lines:
        stripped = line.strip()
        for label in labels:
            if stripped.startswith(label):
                m = re.search(r"(\d+)", stripped)
                if m:
                    totals[label] = int(m.group(1))

    return totals or None


from typing import Optional

# ---------------- UTILIDADES ----------------

def get_npx_executable() -> Optional[str]:
    """Intenta ubicar npx en el sistema."""
    candidates = ["npx.cmd", "npx"] if sys.platform == "win32" else ["npx"]
    
    for candidate in candidates:
        path = which(candidate)
        if path:
            return candidate 
    return None


# ---------------- MÉTRICAS ----------------

def backend_metrics():
    print("\n== MÉTRICAS BACKEND (Radon) ==")
    
    radon_cmd = ["radon"]
    if not which("radon"):
        # Try to find it in the user bin path if not in PATH
        import sys
        import os
        user_bin = os.path.expanduser("~/Library/Python/3.9/bin/radon")
        if os.path.exists(user_bin):
             radon_cmd = [user_bin]
        else:
             # Try running as module
             radon_cmd = [sys.executable, "-m", "radon"]

    # Radon needs to run on the files. 'backend' dir is valid.
    run_cmd(radon_cmd + ["raw", "-s", "."], "backend_raw.txt", cwd=BACKEND_DIR)
    run_cmd(radon_cmd + ["cc", "-s", "-a", "."], "backend_cc.txt", cwd=BACKEND_DIR)
    run_cmd(radon_cmd + ["mi", "-s", "."], "backend_mi.txt", cwd=BACKEND_DIR)

    backend_raw_path = METRICS_DIR / "backend_raw.txt"
    backend_totals = parse_backend_totals(backend_raw_path)

    if backend_totals:
        print("📊 Resumen Backend:")
        for k, v in backend_totals.items():
            print(f"   • {k}: {v}")
    else:
        print("⚠ No se pudieron leer los totales del backend.")

    return backend_totals


def frontend_metrics():
    print("\n== MÉTRICAS FRONTEND (sloc) ==")
    
    npx_exec = get_npx_executable()
    if not npx_exec:
        print("❌ No se encontró 'npx'. Asegurate de tener Node.js instalado.")
        return None

    print(f"   Usando: {npx_exec} sloc src")
    
    # Note: sloc output format might vary slightly depending on version, but usually stable.
    run_cmd(
        [npx_exec, "sloc", "src"],
        "frontend_sloc.txt",
        cwd=FRONTEND_DIR,
    )

    frontend_sloc_path = METRICS_DIR / "frontend_sloc.txt"
    frontend_totals = parse_frontend_totals(frontend_sloc_path)

    if frontend_totals:
        print("📊 Resumen Frontend:")
        for k, v in frontend_totals.items():
            print(f"   • {k}: {v}")
    else:
        print("⚠ No se pudieron leer los totales del frontend.")

    return frontend_totals


# ---------------- RESUMEN FINAL ----------------

def write_overall_totals(backend_totals, frontend_totals):
    out_path = METRICS_DIR / "REPORTE_FINAL.txt"
    lines = []

    lines.append("========================================\n")
    lines.append("   REPORTE DE MÉTRICAS DEL PROYECTO\n")
    lines.append("========================================\n\n")

    # --- BACKEND ---
    lines.append("🐍 BACKEND (Python)\n")
    lines.append("-" * 20 + "\n")
    if backend_totals:
        for k, v in backend_totals.items():
            lines.append(f"{k:<15}: {v}\n")
    else:
        lines.append("(No disponible)\n")
    lines.append("\n")

    # --- FRONTEND ---
    lines.append("⚛️ FRONTEND (React/JS)\n")
    lines.append("-" * 20 + "\n")
    if frontend_totals:
        for k, v in frontend_totals.items():
            lines.append(f"{k:<15}: {v}\n")
    else:
        lines.append("(No disponible)\n")
    lines.append("\n")

    # --- TOTALES ---
    lines.append("📊 TOTALES COMBINADOS\n")
    lines.append("-" * 20 + "\n")
    if backend_totals and frontend_totals:
        total_fisicas = backend_totals.get("LOC", 0) + frontend_totals.get("Physical", 0)
        total_logicas = backend_totals.get("SLOC", 0) + frontend_totals.get("Source", 0)
        total_comentarios = (backend_totals.get("Comments", 0) + 
                             frontend_totals.get("Comment", 0))
        total_vacias = backend_totals.get("Blank", 0) + frontend_totals.get("Empty", 0)

        lines.append(f"{'Líneas Totales':<20}: {total_fisicas}\n")
        lines.append(f"{'Código Real':<20}: {total_logicas}\n")
        lines.append(f"{'Comentarios':<20}: {total_comentarios}\n")
        lines.append(f"{'Vacías':<20}: {total_vacias}\n")
    else:
        lines.append("No se pudieron calcular los totales combinados.\n")

    lines.append("\n\n" + "="*40 + "\n")
    lines.append("GLOSARIO DE TÉRMINOS\n")
    lines.append("="*40 + "\n\n")
    
    lines.append("1. LOC / Physical (Líneas Físicas):\n")
    lines.append("   Cuenta cada salto de línea en el archivo. Es el tamaño 'bruto' del archivo.\n\n")
    
    lines.append("2. SLOC / Source (Líneas de Código Fuente):\n")
    lines.append("   Líneas que contienen instrucciones ejecutables. Excluye comentarios y espacios.\n")
    lines.append("   Esta es la métrica más real de 'cuánto trabajo de programación' hubo.\n\n")
    
    lines.append("3. Comments (Comentarios):\n")
    lines.append("   Líneas dedicadas a documentación o explicaciones.\n\n")
    
    lines.append("4. Complexity (CC - Solo Backend):\n")
    lines.append("   Complejidad Ciclomática. Mide cuántos caminos independientes tiene el código (ifs, loops).\n")
    lines.append("   - 1-5: Simple, bajo riesgo.\n")
    lines.append("   - 6-10: Más complejo, riesgo moderado.\n")
    lines.append("   - 11+: Muy complejo, alto riesgo, difícil de testear.\n\n")
    
    lines.append("5. Maintainability Index (MI - Solo Backend):\n")
    lines.append("   Índice de Mantenibilidad (0-100). Cuanto más alto, mejor.\n")
    lines.append("   - > 20: Alta mantenibilidad.\n")

    out_path.write_text("".join(lines), encoding="utf-8")
    print(f"\n📄 Reporte final guardado en: {out_path}")

def main():
    ensure_metrics_dir()
    b_totals = backend_metrics()
    f_totals = frontend_metrics()
    write_overall_totals(b_totals, f_totals)
    print("\n✅ Proceso finalizado.")

if __name__ == "__main__":
    main()

