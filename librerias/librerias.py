import subprocess
import sys

def instalar_librerias():
    """Instala las librerías Pillow y Pygame usando pip."""
    librerias = ['Pillow', 'pygame']
    
    for libreria in librerias:
        try:
            print(f"Instalando {libreria}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', libreria])
            print(f"{libreria} se ha instalado correctamente.")
        except Exception as e:
            print(f"Ocurrió un error al intentar instalar {libreria}: {e}")

if __name__ == "__main__":
    instalar_librerias()