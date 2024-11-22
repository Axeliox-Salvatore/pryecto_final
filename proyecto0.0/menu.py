import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from nucleo_juego import MemoriaJuego
from utils import GestorPuntuaciones, ReproductorSonidos

class MenuPrincipal:
    def __init__(self, root, niveles):
        self.root = root
        self.gestor_puntuaciones = GestorPuntuaciones()
        self.ventana_puntuaciones = None
        self.niveles = niveles
        self.current_theme = 'cute'

        # Configuración general de la ventana
        self.root.geometry("800x600")
        self.root.title("Juego de Memoria")

        # Frame principal del menú
        self.frame_menu = tk.Frame(root, bg=self.get_theme_color('background'))
        self.frame_menu.pack(expand=True, fill='both')

        # Título del menú con animación
        self.titulo = tk.Label(
            self.frame_menu,
            text="✨ JUEGO DE MEMORIA ✨",
            font=("Comic Sans MS", 32, "bold"),
            fg=self.get_theme_color('text'),
            bg=self.get_theme_color('background'),
            pady=40
        )
        self.titulo.pack()
        self.animate_title()

        # Frame para los botones
        self.frame_botones = tk.Frame(self.frame_menu, bg=self.get_theme_color('background'))
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
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            command=self.seleccionar_nivel,
            activebackground=self.get_theme_color('button_active'),
            activeforeground=self.get_theme_color('text_active'),
            **boton_estilo
        )
        self.btn_jugar.pack(pady=15)

        # Botón PUNTUACIONES
        self.btn_puntuaciones = tk.Button(
            self.frame_botones,
            text="PUNTUACIONES",
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            command=self.mostrar_puntuaciones,
            activebackground=self.get_theme_color('button_active'),
            activeforeground=self.get_theme_color('text_active'),
            **boton_estilo
        )
        self.btn_puntuaciones.pack(pady=15)

        # Botón SALIR
        self.btn_salir = tk.Button(
            self.frame_botones,
            text="SALIR",
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            command=self.root.quit,
            activebackground=self.get_theme_color('button_active'),
            activeforeground=self.get_theme_color('text_active'),
            **boton_estilo
        )
        self.btn_salir.pack(pady=15)

        # Botón TOGGLE THEME
        self.btn_toggle_theme = tk.Button(
            self.frame_botones,
            text="☀️",
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            command=self.toggle_theme,
            activebackground=self.get_theme_color('button_active'),
            activeforeground=self.get_theme_color('text_active'),
            **boton_estilo
        )
        self.btn_toggle_theme.pack(pady=15)

        # Efectos de hover para cada botón
        for btn in [self.btn_jugar, self.btn_puntuaciones, self.btn_salir, self.btn_toggle_theme]:
            btn.bind('<Enter>', lambda e, b=btn: self.on_hover(e, b))
            btn.bind('<Leave>', lambda e, b=btn: self.on_leave(e, b))

        # Agregar animaciones de entrada y salida a los botones
        self.btn_jugar.bind('<Button-1>', lambda e: self.animate_button(e, self.btn_jugar))
        self.btn_puntuaciones.bind('<Button-1>', lambda e: self.animate_button(e, self.btn_puntuaciones))
        self.btn_salir.bind('<Button-1>', lambda e: self.animate_button(e, self.btn_salir))
        self.btn_toggle_theme.bind('<Button-1>', lambda e: self.animate_button(e, self.btn_toggle_theme))

    def animate_button(self, event, button):
        button.config(bg=self.get_theme_color('button_hover'))
        button.after(100, lambda: button.config(bg=self.get_theme_color('button')))

    def on_hover(self, event, button):
        button.configure(bg=self.get_theme_color('button_hover'))
        
        # Reproducir el sonido adecuado
        if button == self.btn_salir:
            ReproductorSonidos.reproducir_salir()
        else:
            ReproductorSonidos.reproducir_menu()

    def on_leave(self, event, button):
        button.configure(bg=self.get_theme_color('button'))

    def get_theme_color(self, key):
        if self.current_theme == 'cute':
            theme_colors = {
                'background': '#FFEBE8',
                'text': '#FF6F61',
                'button': '#FFD1DC',
                'button_active': '#FF6F61',
                'button_hover': '#FFF0F5',
                'text_active': 'white'
            }
        else:  # dark theme
            theme_colors = {
                'background': '#2C3E50',
                'text': 'white',
                'button': '#3498DB',
                'button_active': '#2980B9',
                'button_hover': '#3498DB',
                'text_active': 'white'
            }
        return theme_colors[key]

    def toggle_theme(self):
        if self.current_theme == 'cute':
            self.current_theme = 'dark'
            self.btn_toggle_theme.config(text="🌙")
        else:
            self.current_theme = 'cute'
            self.btn_toggle_theme.config(text="☀️")
        self.update_theme()

    def update_theme(self):
        # Actualizar el color de fondo del frame principal
        self.frame_menu.config(bg=self.get_theme_color('background'))
        
        # Actualizar el color de fondo del frame de botones
        self.frame_botones.config(bg=self.get_theme_color('background'))

        # Actualizar el título
        self.titulo.config(bg=self.get_theme_color('background'), fg=self.get_theme_color('text'))

        # Actualizar los botones
        for btn in [self.btn_jugar, self.btn_puntuaciones, self.btn_salir, self.btn_toggle_theme]:
            btn.config(
                bg=self.get_theme_color('button'),
                fg=self.get_theme_color('text'),
                activebackground=self.get_theme_color('button_active'),
                activeforeground=self.get_theme_color('text_active')
            )

        # Actualizar el frame de selección de nivel si existe
        if hasattr(self, 'frame_seleccion_nivel') and self.frame_seleccion_nivel.winfo_exists():
            self.frame_seleccion_nivel.config(bg=self.get_theme_color('background'))
            for widget in self.frame_seleccion_nivel.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=self.get_theme_color('background'), fg=self.get_theme_color('text'))
                elif isinstance(widget, tk.Button):
                    widget.config(
                        bg=self.get_theme_color('button'),
                        fg=self.get_theme_color('text'),
                        activebackground=self.get_theme_color('button_active'),
                        activeforeground=self.get_theme_color('text_active')
                    )

        # Actualizar el frame de juego si existe
        if hasattr(self, 'frame_juego') and self.frame_juego.winfo_exists():
            self.frame_juego.config(bg=self.get_theme_color('background'))
            for widget in self.frame_juego.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=self.get_theme_color('background'), fg=self.get_theme_color('text'))
                elif isinstance(widget, tk.Button):
                    widget.config(
                        bg=self.get_theme_color('button'),
                        fg=self.get_theme_color('text'),
                        activebackground=self.get_theme_color('button_active'),
                        activeforeground=self.get_theme_color('text_active')
                    )

        # Actualizar la ventana de puntuaciones si existe
        if self.ventana_puntuaciones and self.ventana_puntuaciones.winfo_exists():
            self.ventana_puntuaciones.config(bg=self.get_theme_color('background'))
            for widget in self.ventana_puntuaciones.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(bg=self.get_theme_color('background'), fg=self.get_theme_color('text'))
                elif isinstance(widget, tk.Button):
                    widget.config(
                        bg=self.get_theme_color('button'),
                        fg=self.get_theme_color('text'),
                        activebackground=self.get_theme_color('button_active'),
                        activeforeground=self.get_theme_color('text_active')
                    )

    def animate_title(self):
        current_color = self.titulo.cget('fg')
        if current_color == self.get_theme_color('text'):
            new_color = self.get_theme_color('button_hover')
        else:
            new_color = self.get_theme_color('text')
        self.titulo.config(fg=new_color)
        self.root.after(500, self.animate_title)

    def actualizar_tabla_puntuaciones(self, frame_tabla):
        self.gestor_puntuaciones.cargar_puntuaciones()
        for widget in frame_tabla.winfo_children():
            widget.destroy()

        encabezados = ['Posición', 'Nivel', 'Intentos', 'Tiempo', 'Fecha']
        for i, encabezado in enumerate(encabezados):
            tk.Label(
                frame_tabla,
                text=encabezado,
                font=("Comic Sans MS", 12, "bold"),
                fg=self.get_theme_color('text'),
                bg=self.get_theme_color('background'),
                padx=10
            ).grid(row=0, column=i, pady=5, sticky='nsew')

        puntuaciones = self.gestor_puntuaciones.obtener_mejores_puntuaciones()
        
        if not puntuaciones:
            tk.Label(
                frame_tabla,
                text="¡Aún no hay puntuaciones registradas!",
                font=("Comic Sans MS", 12),
                fg=self.get_theme_color('text'),
                bg=self.get_theme_color('background')
            ).grid(row=1, column=0, columnspan=5, pady=20)
        else:
            for i, puntuacion in enumerate(puntuaciones, 1):
                tk.Label(
                    frame_tabla,
                    text=str(i),
                    font=("Comic Sans MS", 12),
                    fg=self.get_theme_color('text'),
                    bg=self.get_theme_color('background')
                ).grid(row=i, column=0, pady=5, sticky='nsew')
                
                tk.Label(
                    frame_tabla,
                    text=str(puntuacion['nivel']),
                    font=("Comic Sans MS", 12),
                    fg=self.get_theme_color('text'),
                    bg=self.get_theme_color('background')
                ).grid(row=i, column=1, pady=5, sticky='nsew')
                
                tk.Label(
                    frame_tabla,
                    text=str(puntuacion['intentos']),
                    font=("Comic Sans MS", 12),
                    fg=self.get_theme_color('text'),
                    bg=self.get_theme_color('background')
                ).grid(row=i, column=2, pady=5, sticky='nsew')
                
                tiempo = puntuacion['tiempo']
                minutos = tiempo // 60
                segundos = tiempo % 60
                tiempo_str = f"{minutos}:{segundos:02d}"
                tk.Label(
                    frame_tabla,
                    text=tiempo_str,
                    font=("Comic Sans MS", 12),
                    fg=self.get_theme_color('text'),
                    bg=self.get_theme_color('background')
                ).grid(row=i, column=3, pady=5, sticky='nsew')
                
                tk.Label(
                    frame_tabla,
                    text=puntuacion['fecha'],
                    font=("Comic Sans MS", 12),
                    fg=self.get_theme_color('text'),
                    bg=self.get_theme_color('background')
                ).grid(row=i, column=4, pady=5, sticky='nsew')

        # Ajustar el peso de las columnas para que se expandan uniformemente
        for i in range(len(encabezados)):
            frame_tabla.grid_columnconfigure(i, weight=1)

    def seleccionar_nivel(self):
        self.frame_menu.pack_forget()
        self.frame_seleccion_nivel = tk.Frame(self.root, bg=self.get_theme_color('background'))
        self.frame_seleccion_nivel.pack(expand=True, fill='both')

        tk.Label(
            self.frame_seleccion_nivel,
            text="Selecciona un Nivel",
            font=("Comic Sans MS", 24, "bold"),
            fg=self.get_theme_color('text'),
            bg=self.get_theme_color('background'),
            pady=40
        ).pack()

        for nivel, config in self.niveles.items():
            btn_nivel = tk.Button(
                self.frame_seleccion_nivel,
                text=f"Nivel {nivel} ({config['filas']}x{config['columnas']})",
                bg=self.get_theme_color('button'),
                fg=self.get_theme_color('text'),
                command=lambda n=nivel: self.iniciar_juego(n),
                activebackground=self.get_theme_color('button_active'),
                activeforeground=self.get_theme_color('text_active'),
                font=("Comic Sans MS", 16, "bold"),
                width=25,
                height=2,
                bd=0,
                relief='flat',
                cursor='hand2'
            )
            btn_nivel.pack(pady=15)

        btn_volver = tk.Button(
            self.frame_seleccion_nivel,
            text="Volver al Menú",
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            command=self.volver_menu,
            activebackground=self.get_theme_color('button_active'),
            activeforeground=self.get_theme_color('text_active'),
            font=("Comic Sans MS", 16, "bold"),
            width=25,
            height=2,
            bd=0,
            relief='flat',
            cursor='hand2'
        )
        btn_volver.pack(pady=15)

    def iniciar_juego(self, nivel):
        self.frame_seleccion_nivel.pack_forget()
        self.frame_juego = tk.Frame(self.root, bg=self.get_theme_color('background'))
        self.frame_juego.pack(expand=True, fill='both')
        juego = MemoriaJuego(self.frame_juego, self.finalizar_juego, self.niveles[nivel]['filas'], self.niveles[nivel]['columnas'], nivel)

    def finalizar_juego(self):
        if self.ventana_puntuaciones and self.ventana_puntuaciones.winfo_exists():
            self.actualizar_tabla_puntuaciones(self.frame_tabla)
        self.volver_menu()

    def volver_menu(self):
        if hasattr(self, 'frame_juego') and self.frame_juego.winfo_exists():
            self.frame_juego.destroy()
        elif hasattr(self, 'frame_seleccion_nivel') and self.frame_seleccion_nivel.winfo_exists():
            self.frame_seleccion_nivel.destroy()
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
        self.ventana_puntuaciones.configure(bg=self.get_theme_color('background'))

        tk.Label(
            self.ventana_puntuaciones,
            text="👑MEJORES PUNTUACIONES👑",
            font=("Comic Sans MS", 20, "bold"),
            fg=self.get_theme_color('text'),
            bg=self.get_theme_color('background')
        ).pack(pady=20)

        self.frame_tabla = tk.Frame(self.ventana_puntuaciones, bg=self.get_theme_color('background'))
        self.frame_tabla.pack(padx=20, pady=10)

        self.actualizar_tabla_puntuaciones(self.frame_tabla)

        tk.Button(
            self.ventana_puntuaciones,
            text="Cerrar",
            command=self.ventana_puntuaciones.destroy,
            bg=self.get_theme_color('button'),
            fg=self.get_theme_color('text'),
            font=("Comic Sans MS", 12),
            width=15,
            cursor='hand2'
        ).pack(pady=20)
