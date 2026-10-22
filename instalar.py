import subprocess
import sys
from pathlib import Path


def instalar_dependencias():
    print("==========================================")
    print("  INSTALADOR AUTOMÁTICO DE DEPENDENCIAS   ")
    print("==========================================")

    # Ruta al archivo de requerimientos
    req_path = Path("config/requirements.txt")

    if not req_path.exists():
        print(f"[!] No se encuentra el archivo de requisitos en: {req_path}")
        return

    print("[*] Verificando e instalando paquetes necesarios...")
    try:
        # Ejecuta pip install usando el mismo intérprete de Python actual
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(req_path)
        ])
        print("\n[+] ¡Listo! Todas las dependencias se han instalado correctamente.")
        print("[*] Ya puedes ejecutar el programa con: python3 main.py")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Hubo un error durante la instalación: {e}")

if __name__ == "__main__":
    instalar_dependencias()
