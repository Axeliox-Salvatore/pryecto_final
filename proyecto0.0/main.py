import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from utils import ReproductorMusica, ReproductorSonidos
import tkinter as tk
from menu import MenuPrincipal

def main():
    # Inicializar la música y los sonidos
    ReproductorMusica.iniciar_musica()
    ReproductorSonidos.cargar_sonidos()

    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Juego de Memoria")

    # Configurar la ventana en pantalla completa
    root.attributes('-fullscreen', True)

    # Configurar el tamaño y la redimensionabilidad de la ventana
    root.resizable(False, False)
    root.configure(bg='#2C3E50')

    # Definir los niveles del juego
    #Agregar niveles
    niveles = {
        1: {'filas': 4, 'columnas': 4, 'cartas': 4},
        2: {'filas': 6, 'columnas': 6, 'cartas': 9},
        3: {'filas': 8, 'columnas': 8, 'cartas': 16}
    }

    # Crear el menú principal y pasar los niveles
    menu = MenuPrincipal(root, niveles)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()