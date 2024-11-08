import tkinter as tk  # Importamos la biblioteca tkinter para la interfaz grafica
from nucleo_juego import MemoriaJuego  # Importamos la clase del juego desde el archivo nucleo_juego

# Creamos la ventana principal
root = tk.Tk()  # Inicializamos la ventana de Tkinter
root.title("Juego de Memoria")  # Asignamos un titulo a la ventana

# Creamos una instancia del juego de memoria con un tablero de 4x4
MemoriaJuego(root, filas=4, columnas=4)  # Iniciamos el juego con una configuracion de 4x4

# Ejecutamos el bucle principal de Tkinter
root.mainloop()  # Mantenemos la ventana abierta hasta que el usuario la cierre
