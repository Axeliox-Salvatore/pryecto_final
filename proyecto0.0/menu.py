import tkinter as tk
from nucleo_juego import MemoriaJuego
from utils import GestorPuntuaciones, ReproductorSonidos

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.gestor_puntuaciones = GestorPuntuaciones()
        self.ventana_puntuaciones = None

        # Frame principal del menú
        self.frame_menu = tk.Frame(root, bg='#FFEBE8')
        self.frame_menu.pack(expand=True, fill='both')

        # Título del menú
        self.titulo = tk.Label(
            self.frame_menu,
            text="✨ JUEGO DE MEMORIA ✨",
            font=("Comic Sans MS", 32, "bold"),
            fg='#FF6F61',
            bg='#FFEBE8',
            pady=40
        )
        self.titulo.pack()

        # Frame para los botones
        self.frame_botones = tk.Frame(self.frame_menu, bg='#FFEBE8')
        self.frame_botones.pack(expand=True)

        # Estilo común para botones
        boton_estilo = {
            'font': ('Comic Sans MS', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bd': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }

        # Botón JUGAR
        self.btn_jugar = tk.Button(
            self.frame_botones,
            text="JUGAR",
            bg='#FFD1DC',
            fg='black',
            command=self.iniciar_juego,
            activebackground='#FF6F61',
            activeforeground='white',
            **boton_estilo
        )
        self.btn_jugar.pack(pady=15)

        # Botón PUNTUACIONES
        self.btn_puntuaciones = tk.Button(
            self.frame_botones,
            text="PUNTUACIONES",
            bg='#C1E1C1',
            fg='black',
            command=self.mostrar_puntuaciones,
            activebackground='#66CDAA',
            activeforeground='white',
            **boton_estilo
        )
        self.btn_puntuaciones.pack(pady=15)

        # Botón SALIR
        self.btn_salir = tk.Button(
            self.frame_botones,
            text="SALIR",
            bg='#FFB6B9',
            fg='black',
            command=self.root.quit,
            activebackground='#FF6F61',
            activeforeground='white',
            **boton_estilo
        )
        self.btn_salir.pack(pady=15)

        # Efectos de hover para cada botón
        for btn in [self.btn_jugar, self.btn_puntuaciones, self.btn_salir]:
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(e, b))
            btn.bind('<Leave>', lambda e, b=btn: self.on_leave(e, b))

    def on_hover(self, event, button):
        button.configure(bg='#FFF0F5')
        
        # Reproducir el sonido adecuado
        if button == self.btn_salir:
            ReproductorSonidos.reproducir_salir()
        else:
            ReproductorSonidos.reproducir_menu()

    def on_leave(self, event, button):
        colors = {'JUGAR': '#FFD1DC', 'PUNTUACIONES': '#C1E1C1', 'SALIR': '#FFB6B9'}
        button.configure(bg=colors[button.cget('text')])

    def actualizar_tabla_puntuaciones(self, frame_tabla):
        self.gestor_puntuaciones.cargar_puntuaciones()
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        encabezados = ['Posición', 'Intentos', 'Tiempo', 'Fecha']
        for i, encabezado in enumerate(encabezados):
            tk.Label(
                frame_tabla,
                text=encabezado,
                font=("Comic Sans MS", 12, "bold"),
                fg='black',
                bg='#FFEBE8',
                padx=10
            ).grid(row=0, column=i, pady=5)

        puntuaciones = self.gestor_puntuaciones.obtener_mejores_puntuaciones()
        
        if not puntuaciones:
            tk.Label(
                frame_tabla,
                text="¡Aún no hay puntuaciones registradas!",
                font=("Comic Sans MS", 12),
                fg='black',
                bg='#FFEBE8'
            ).grid(row=1, column=0, columnspan=4, pady=20)
        else:
            for i, puntuacion in enumerate(puntuaciones, 1):
                tk.Label(
                    frame_tabla,
                    text=str(i),
                    font=("Comic Sans MS", 12),
                    fg='black',
                    bg='#FFEBE8'
                ).grid(row=i, column=0, pady=5)
                
                tk.Label(
                    frame_tabla,
                    text=str(puntuacion['intentos']),
                    font=("Comic Sans MS", 12),
                    fg='black',
                    bg='#FFEBE8'
                ).grid(row=i, column=1, pady=5)
                
                tiempo = puntuacion['tiempo']
                minutos = tiempo // 60
                segundos = tiempo % 60
                tiempo_str = f"{minutos}:{segundos:02d}"
                tk.Label(
                    frame_tabla,
                    text=tiempo_str,
                    font=("Comic Sans MS", 12),
                    fg='black',
                    bg='#FFEBE8'
                ).grid(row=i, column=2, pady=5)
                
                tk.Label(
                    frame_tabla,
                    text=puntuacion['fecha'],
                    font=("Comic Sans MS", 12),
                    fg='black',
                    bg='#FFEBE8'
                ).grid(row=i, column=3, pady=5)

    def iniciar_juego(self):
        self.frame_menu.pack_forget()
        self.frame_juego = tk.Frame(self.root, bg='#FFEBE8')
        self.frame_juego.pack(expand=True, fill='both')
        juego = MemoriaJuego(self.frame_juego, self.finalizar_juego)

    def finalizar_juego(self):
        if self.ventana_puntuaciones and self.ventana_puntuaciones.winfo_exists():
            self.actualizar_tabla_puntuaciones(self.frame_tabla)
        self.volver_menu()

    def volver_menu(self):
        if hasattr(self, 'frame_juego'):
            self.frame_juego.destroy()
        self.frame_menu.pack(expand=True, fill='both')
        self.gestor_puntuaciones.cargar_puntuaciones()

    def mostrar_puntuaciones(self):
        self.gestor_puntuaciones.cargar_puntuaciones()

        if self.ventana_puntuaciones and self.ventana_puntuaciones.winfo_exists():
            self.actualizar_tabla_puntuaciones(self.frame_tabla)
            self.ventana_puntuaciones.lift()
            self.ventana_puntuaciones.focus_force()
            return

        self.ventana_puntuaciones = tk.Toplevel(self.root)
        self.ventana_puntuaciones.title("Puntuaciones")
        self.ventana_puntuaciones.geometry("500x400")
        self.ventana_puntuaciones.configure(bg='#FFEBE8')

        tk.Label(
            self.ventana_puntuaciones,
            text="👑MEJORES PUNTUACIONES👑",
            font=("Comic Sans MS", 20, "bold"),
            fg='#FF6F61',
            bg='#FFEBE8'
        ).pack(pady=20)

        self.frame_tabla = tk.Frame(self.ventana_puntuaciones, bg='#FFEBE8')
        self.frame_tabla.pack(padx=20, pady=10)

        self.actualizar_tabla_puntuaciones(self.frame_tabla)

        tk.Button(
            self.ventana_puntuaciones,
            text="Cerrar",
            command=self.ventana_puntuaciones.destroy,
            bg='#FFB6B9',
            fg='black',
            font=("Comic Sans MS", 12),
            width=15,
            cursor='hand2'
        ).pack(pady=20)