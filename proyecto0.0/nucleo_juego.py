import tkinter as tk
import random
import time
import os
import json
from PIL import Image, ImageTk
from datetime import datetime
import math
from sv_ttk import set_theme
from utils import GestorPuntuaciones, ReproductorSonidos


class MemoriaJuego:
    def __init__(self, root, menu_callback, filas, columnas, nivel):
        self.root = root
        set_theme("light")
        
        self.filas = filas
        self.columnas = columnas
        self.nivel = nivel
        self.reiniciar_juego()
        self.menu_callback = menu_callback
        
        ruta_img = os.path.join(os.path.dirname(__file__), "img")
        
        self.imagenes_frutas = []
        nombres_imagenes = ["cerezas.png", "fresa.png", "manzana.png", "naranja.png", 
                            "pera.png", "platano.png", "sandia.png", "uvas.png"]
        
        for nombre in nombres_imagenes:
            ruta_imagen = os.path.join(ruta_img, nombre)
            if os.path.isfile(ruta_imagen):
                self.imagenes_frutas.append(ImageTk.PhotoImage(Image.open(ruta_imagen).resize((64, 64))))
            else:
                print(f"Error: la imagen {ruta_imagen} no se encuentra.")
                return
        
        self.imagen_fondo = self.crear_fondo_gradiente(64, 64)
        
        self.frame_tablero = tk.Frame(self.root, bg='#E0BBE4')
        self.frame_tablero.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.frame_controles = tk.Frame(self.root, bg='#EAB8E4')
        self.frame_controles.pack(fill='x', padx=10, pady=5)
        
        self.label_intentos = tk.Label(
            self.frame_controles,
            text="Intentos: 0",
            font=("Helvetica", 12, "bold"),
            fg='white',
            bg='#EAB8E4'
        )
        self.label_intentos.pack(side=tk.LEFT, padx=10)
        
        self.label_tiempo = tk.Label(
            self.frame_controles,
            text="Tiempo: 0:00",
            font=("Helvetica", 12, "bold"),
            fg='white',
            bg='#EAB8E4'
        )
        self.label_tiempo.pack(side=tk.RIGHT, padx=10)
        
        # Inicializar los sonidos
        ReproductorSonidos.cargar_sonidos()
        
        self.generar_tablero()
        self.actualizar_tiempo()
        self.iniciar_animaciones_idle()

    def reiniciar_juego(self):
        self.pares_encontrados = 0
        self.intentos = 0
        self.cartas = []
        self.seleccionadas = []
        self.tiempo_inicio = time.time()
        self.gestor_puntuaciones = GestorPuntuaciones()
        self.animation_running = False  # Bandera para animaciones

    def calcular_tamano_casillas(self):
        """Calcula el tamaño de las casillas dinámicamente"""
        self.frame_tablero.update_idletasks()
        ancho = self.frame_tablero.winfo_width()
        alto = self.frame_tablero.winfo_height()
        
        ancho_casilla = ancho // self.columnas - 8
        alto_casilla = alto // self.filas - 8
        
        max_tamano = 100
        self.ancho_casilla = min(ancho_casilla, max_tamano)
        self.alto_casilla = min(alto_casilla, max_tamano)

    def crear_fondo_gradiente(self, width, height):
        """Crea un fondo con gradiente para las cartas"""
        image = Image.new('RGBA', (width, height))
        for y in range(height):
            r = int(255 * (1 - y/height))
            g = int(200 * (y/height))
            b = int(255 * (y/height))
            for x in range(width):
                image.putpixel((x, y), (r, g, b, 255))
        return ImageTk.PhotoImage(image)

    def animar_carta_idle(self, boton):
        """Animación suave de flotación para las cartas en estado idle"""
        if not hasattr(boton, 'animation_offset'):
            boton.animation_offset = random.uniform(0, 2 * math.pi)
        
        def update_position():
            if not boton.winfo_exists():
                return
            t = time.time() * 2
            offset = math.sin(t + boton.animation_offset) * 5
            boton.grid_configure(pady=(4 + offset/2, 4 - offset/2))
            self.root.after(50, update_position)
        
        update_position()

    def iniciar_animaciones_idle(self):
        """Inicia las animaciones idle para todas las cartas"""
        for fila in self.cartas:
            for boton in fila:
                self.animar_carta_idle(boton)

    def efecto_presion(self, boton):
        """Efecto de presión al hacer clic en una carta"""
        def scale_down():
            boton.configure(relief='sunken')
            self.root.after(100, scale_up)
        
        def scale_up():
            boton.configure(relief='raised')
        
        scale_down()

    def generar_tablero(self):
        """Genera el tablero de juego con las cartas animadas"""
        num_cartas = self.filas * self.columnas // 2
        if num_cartas > len(self.imagenes_frutas):
            indices_imagenes = list(range(len(self.imagenes_frutas))) * (num_cartas // len(self.imagenes_frutas) + 1)
            random.shuffle(indices_imagenes)
            valores = indices_imagenes[:num_cartas] * 2
        else:
            valores = list(range(num_cartas)) * 2
        random.shuffle(valores)

        self.calcular_tamano_casillas()

        style = {
            'relief': 'flat',
            'borderwidth': 0,
            'highlightthickness': 0,
            'bg': '#E0BBE4'
        }

        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = valores.pop()
                boton = tk.Button(
                    self.frame_tablero,
                    image=self.imagen_fondo,
                    width=self.ancho_casilla,
                    height=self.alto_casilla,
                    command=lambda i=i, j=j: self.seleccionar_carta(i, j),
                    **style
                )
                boton.valor = valor
                boton.imagen = self.imagenes_frutas[valor]
                boton.revelado = False
                boton.bind('<Enter>', lambda e, b=boton: self.hover_enter(b))
                boton.bind('<Leave>', lambda e, b=boton: self.hover_leave(b))
                boton.grid(row=i, column=j, sticky='nsew', padx=4, pady=4)
                fila.append(boton)
            self.cartas.append(fila)

        for i in range(self.filas):
            self.frame_tablero.grid_rowconfigure(i, weight=1)
        for j in range(self.columnas):
            self.frame_tablero.grid_columnconfigure(j, weight=1)

        self.btn_volver = tk.Button(
            self.frame_controles,
            text="Volver al Menú",
            command=self.volver_menu,
            bg='#FF7F7F',
            fg='white',
            font=('Helvetica', 10, 'bold'),
            bd=0,
            cursor='hand2',
            relief='raised',
            highlightthickness=2,
            highlightbackground='#FF69B4',
            highlightcolor='#FF1493'
        )
        self.btn_volver.pack(side=tk.BOTTOM, pady=5)

    def hover_enter(self, boton):
        """Efecto al pasar el mouse por encima"""
        if not boton.revelado and boton.cget('state') != 'disabled':
            boton.configure(bg='#FFB6C1')
            self.root.configure(cursor='hand2')

    def hover_leave(self, boton):
        """Efecto al quitar el mouse de encima"""
        if not boton.revelado and boton.cget('state') != 'disabled':
            boton.configure(bg='#E0BBE4')
            self.root.configure(cursor='')

    def seleccionar_carta(self, i, j):
        """Maneja la selección de una carta con animación"""
        if self.animation_running or len(self.seleccionadas) >= 2:
            return
        
        boton = self.cartas[i][j]
        
        if boton.revelado or len(self.seleccionadas) >= 2:
            return

        self.animation_running = True  # Bloquea la selección de nuevas cartas

        # Efecto de presión
        self.efecto_presion(boton)
        
        # Animación de volteo
        def flip_animation(angle=0):
            if angle <= 90:
                scale = math.cos(math.radians(angle))
                boton.configure(width=int(self.ancho_casilla * scale))
                self.root.after(5, lambda: flip_animation(angle + 10))
            else:
                boton.config(image=boton.imagen)
                def flip_back(angle=90):
                    scale = math.cos(math.radians(angle))
                    boton.configure(width=int(self.ancho_casilla * scale))
                    if angle > 0:
                        self.root.after(5, lambda: flip_back(angle - 10))
                    else:
                        self.animation_running = False  # Desbloquea la selección de nuevas cartas
                        boton.revelado = True
                        self.seleccionadas.append(boton)
                        if len(self.seleccionadas) == 2:
                            self.root.after(1000, self.verificar_pareja)

                flip_back()

        flip_animation()

    def verificar_pareja(self):
        """Verifica si las dos cartas seleccionadas forman una pareja"""
        carta1, carta2 = self.seleccionadas

        def animar_resultado(cartas, es_pareja):
            def scale_effect(scale=1.0, increasing=False):
                if not cartas[0].winfo_exists() or not cartas[1].winfo_exists():
                    return
                for carta in cartas:
                    carta.configure(width=int(self.ancho_casilla * scale),
                                  height=int(self.alto_casilla * scale))
                
                if increasing:
                    if scale < 1.2:
                        self.root.after(20, lambda: scale_effect(scale + 0.02, True))
                    else:
                        self.root.after(20, lambda: scale_effect(1.2, False))
                else:
                    if scale > 1.0:
                        self.root.after(20, lambda: scale_effect(scale - 0.02, False))
                    else:
                        # Aplicar el resultado final
                        if es_pareja:
                            for carta in cartas:
                                carta.config(state="disabled", bg='#A2E8AC')
                            ReproductorSonidos.reproducir_acierto()
                        else:
                            for carta in cartas:
                                carta.config(image=self.imagen_fondo)
                                carta.revelado = False
                            ReproductorSonidos.reproducir_fallo()

            scale_effect(1.0, True)

        if carta1.valor == carta2.valor:
            self.pares_encontrados += 1
            animar_resultado([carta1, carta2], True)
        else:
            animar_resultado([carta1, carta2], False)

        self.seleccionadas = []
        self.intentos += 1
        self.label_intentos.config(text=f"Intentos: {self.intentos}")

        if self.pares_encontrados == (self.filas * self.columnas // 2):
            self.root.after(500, self.mostrar_resultado)

    def mostrar_resultado(self):
        """Muestra la ventana de resultado al finalizar el juego"""
        tiempo_total = int(time.time() - self.tiempo_inicio)
        self.gestor_puntuaciones.agregar_puntuacion(self.nivel, self.intentos, tiempo_total)
        
        ventana_resultado = tk.Toplevel(self.root)
        ventana_resultado.title("¡Juego Terminado!")
        ventana_resultado.geometry("300x200")
        ventana_resultado.configure(bg='#FFD1DC')
        
        # Efecto de aparición gradual
        ventana_resultado.attributes('-alpha', 0.0)
        
        def fade_in(alpha=0.0):
            if alpha < 1.0:
                ventana_resultado.attributes('-alpha', alpha)
                ventana_resultado.after(50, lambda: fade_in(alpha + 0.1))
        
        fade_in()
        
        # Frame con efecto de cristal
        frame_resultado = tk.Frame(
            ventana_resultado,
            bg='#FFD1DC',
            relief='raised',
            borderwidth=3
        )
        frame_resultado.place(relx=0.5, rely=0.5, anchor='center')
        
        mensaje = f"¡Felicitaciones!\n\nIntentos: {self.intentos}\nTiempo: {tiempo_total//60}:{tiempo_total%60:02d}\nNivel: {self.nivel}"
    

        label_resultado = tk.Label(
            frame_resultado,
            text=mensaje,
            font=("Helvetica", 14, "bold"),
            fg='#4A0404',
            bg='#FFD1DC',
            justify=tk.CENTER
        )
        label_resultado = tk.Label(
            frame_resultado,
            text=mensaje,
            font=("Helvetica", 14, "bold"),
            fg='#4A0404',
            bg='#FFD1DC',
            justify=tk.CENTER
        )
        label_resultado.pack(pady=20)
        
        # Botón con efectos
        btn_volver = tk.Button(
            frame_resultado,
            text="Volver al Menú",
            command=lambda: [self.animar_cierre(ventana_resultado), self.volver_menu()],
            bg='#FF7F7F',
            fg='white',
            font=('Helvetica', 12, 'bold'),
            relief='raised',
            borderwidth=3,
            cursor='hand2'
        )
        btn_volver.pack(pady=10)
        
        # Efecto hover para el botón
        btn_volver.bind('<Enter>', 
                        lambda e: btn_volver.configure(bg='#FF69B4', relief='sunken'))
        btn_volver.bind('<Leave>', 
                        lambda e: btn_volver.configure(bg='#FF7F7F', relief='raised'))
        
        # Reproducir sonido de ganar
        ReproductorSonidos.reproducir_ganar()

    def animar_cierre(self, ventana):
        """Animación de cierre para la ventana de resultado"""
        def fade_out(alpha=1.0):
            if alpha > 0:
                ventana.attributes('-alpha', alpha)
                ventana.after(50, lambda: fade_out(alpha - 0.1))
            else:
                ventana.destroy()
        fade_out()

    def actualizar_tiempo(self):
        """Actualiza el tiempo transcurrido con efecto de parpadeo"""
        if not self.label_tiempo.winfo_exists():
            return
        
        tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        
        # Efecto de parpadeo cada minuto
        if segundos == 0:
            self.label_tiempo.configure(fg='#FF69B4')
            self.root.after(500, lambda: self.label_tiempo.configure(fg='white'))
        
        self.label_tiempo.config(text=f"Tiempo: {minutos}:{segundos:02d}")
        if self.pares_encontrados < (self.filas * self.columnas // 2):
            self.root.after(1000, self.actualizar_tiempo)

    def volver_menu(self):
        """Vuelve al menú principal con animación de transición"""
        def fade_out():
            # Crear un Toplevel temporal
            ventana_temporal = tk.Toplevel(self.root)
            ventana_temporal.geometry(self.root.winfo_geometry())
            ventana_temporal.overrideredirect(True)
            ventana_temporal.attributes('-alpha', 1.0)
            
            # Colocar una etiqueta transparente para cubrir el contenido
            etiqueta_cubierta = tk.Label(ventana_temporal, bg='white')
            etiqueta_cubierta.place(x=0, y=0, relwidth=1, relheight=1)
            
            def hide_frames(alpha=1.0):
                if alpha > 0:
                    ventana_temporal.attributes('-alpha', alpha)
                    self.root.after(50, lambda: hide_frames(alpha - 0.1))
                else:
                    ventana_temporal.destroy()
                    self.limpiar_juego()
                    if self.menu_callback:
                        self.menu_callback()
            
            # Ocultar gradualmente el Toplevel temporal
            hide_frames()
        
        fade_out()

    def limpiar_juego(self):
        """Destruye todos los widgets del juego y reinicia el estado"""
        if self.frame_tablero:
            self.frame_tablero.destroy()
        if self.frame_controles:
            self.frame_controles.destroy()
        self.reiniciar_juego()
