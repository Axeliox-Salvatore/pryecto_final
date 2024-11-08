import subprocess
import sys

def instalar_pillow():
    """Instala la librería Pillow usando pip."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
        print("Pillow se ha instalado correctamente.")
    except Exception as e:
        print(f"Ocurrió un error al intentar instalar Pillow: {e}")

if __name__ == "__main__":
    instalar_pillow()
