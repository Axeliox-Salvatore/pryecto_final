import tkinter as tk
from menu import MenuPrincipal

def main():
    root = tk.Tk()
    root.title("Juego de Memoria")

    # Configurar tamaño y posición de la ventana
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)
    root.configure(bg='#2C3E50')

    MenuPrincipal(root)
    root.mainloop()

if __name__ == "__main__":
    main()