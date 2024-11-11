import tkinter as tk
import random
import time
import os
from utils import GestorPuntuaciones, ReproductorSonidos
from PIL import Image, ImageTk 

class MemoriaJuego:
    def __init__(self, root, menu_callback, filas=4, columnas=4):
        self.root = root
        self.filas = filas
        self.columnas = columnas
        self.pares_encontrados = 0
        self.intentos = 0
        self.cartas = []
        self.seleccionadas = []
        self.menu_callback = menu_callback
        self.tiempo_inicio = time.time()
        self.gestor_puntuaciones = GestorPuntuaciones()
        
        # Obtener la ruta absoluta de la carpeta de imágenes
        ruta_img = os.path.join(os.path.dirname(__file__), "img")
        
        # Cargar y redimensionar imágenes de frutas a tamaño fijo (64x64)
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
        
        # Crear una imagen de fondo para los botones
        self.imagen_fondo = ImageTk.PhotoImage(Image.new("RGBA", (64, 64), (0, 0, 0, 0)))
        
        # Crear un frame para contener el tablero
        self.frame_tablero = tk.Frame(self.root, bg='#E0BBE4')
        self.frame_tablero.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Crear un frame separado para los botones de control
        self.frame_controles = tk.Frame(self.root, bg='#EAB8E4')
        self.frame_controles.pack(fill='x', padx=10, pady=5)
        
        # Etiqueta para mostrar los intentos
        self.label_intentos = tk.Label(
            self.frame_controles,
            text="Intentos: 0",
            font=("Helvetica", 12),
            fg='white',
            bg='#EAB8E4'
        )
        self.label_intentos.pack(side=tk.LEFT, padx=10)
        
        # Etiqueta para mostrar el tiempo
        self.label_tiempo = tk.Label(
            self.frame_controles,
            text="Tiempo: 0:00",
            font=("Helvetica", 12),
            fg='white',
            bg='#EAB8E4'
        )
        self.label_tiempo.pack(side=tk.RIGHT, padx=10)
        
        self.generar_tablero()
        self.actualizar_tiempo()

    def actualizar_tiempo(self):
        """Actualiza el tiempo transcurrido"""
        tiempo_transcurrido = int(time.time() - self.tiempo_inicio)
        minutos = tiempo_transcurrido // 60
        segundos = tiempo_transcurrido % 60
        self.label_tiempo.config(text=f"Tiempo: {minutos}:{segundos:02d}")
        if self.pares_encontrados < (self.filas * self.columnas // 2):
            self.root.after(1000, self.actualizar_tiempo)

    def generar_tablero(self):
        """Genera el tablero de juego con las cartas"""
        valores = list(range(len(self.imagenes_frutas))) * 2  # Crear pares
        random.shuffle(valores)

        # Crear el tablero de botones en el frame_tablero
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                valor = valores.pop()
                boton = tk.Button(
                    self.frame_tablero,
                    image=self.imagen_fondo,
                    width=64,
                    height=64,
                    command=lambda i=i, j=j: self.seleccionar_carta(i, j),
                    bg='#FFC0CB'
                )
                boton.valor = valor
                boton.imagen = self.imagenes_frutas[valor]
                boton.revelado = False
                boton.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
                fila.append(boton)
            self.cartas.append(fila)

        # Configurar la cuadrícula para que los botones se expandan
        for i in range(self.filas):
            self.frame_tablero.grid_rowconfigure(i, weight=1)
        for j in range(self.columnas):
            self.frame_tablero.grid_columnconfigure(j, weight=1)

        # Botón para volver al menú en el frame de controles
        self.btn_volver = tk.Button(
            self.frame_controles,
            text="Volver al Menú",
            command=self.volver_menu,
            bg='#FF7F7F',
            fg='white',
            font=('Helvetica', 10),
            bd=0,
            cursor='hand2'
        )
        self.btn_volver.pack(side=tk.BOTTOM, pady=5)

    def seleccionar_carta(self, i, j):
        """Maneja la selección de una carta"""
        boton = self.cartas[i][j]

        if boton.revelado or len(self.seleccionadas) >= 2:
            return

        boton.config(image=boton.imagen)  # Solo muestra la imagen
        boton.revelado = True
        self.seleccionadas.append(boton)

        if len(self.seleccionadas) == 2:
            self.root.after(1000, self.verificar_pareja)

    def verificar_pareja(self):
        """Verifica si las dos cartas seleccionadas forman una pareja"""
        carta1, carta2 = self.seleccionadas

        if carta1.valor == carta2.valor:
            carta1.config(state="disabled", bg='#A2E8AC')  # Color verde claro para cartas emparejadas
            carta2.config(state="disabled", bg='#A2E8AC')
            self.pares_encontrados += 1
            ReproductorSonidos.reproducir_acierto()  # Reproducir sonido de acierto
        else:
            carta1.config(image=self.imagen_fondo)
            carta2.config(image=self.imagen_fondo)
            carta1.revelado = False
            carta2.revelado = False
            ReproductorSonidos.reproducir_fallo()  # Reproducir sonido de fallo

        self.seleccionadas = []
        self.intentos += 1
        self.label_intentos.config(text=f"Intentos: {self.intentos}")

        if self.pares_encontrados == (self.filas * self.columnas // 2):
            self.mostrar_resultado()

    def mostrar_resultado(self):
        """Muestra la ventana de resultado al finalizar el juego"""
        tiempo_total = int(time.time() - self.tiempo_inicio)
        
        # Guardar la puntuación
        self.gestor_puntuaciones.agregar_puntuacion(self.intentos, tiempo_total)
        
        # Mostrar ventana de resultado
        ventana_resultado = tk.Toplevel(self.root)
        ventana_resultado.title("¡Juego Terminado!")
        ventana_resultado.geometry("300x200")
        ventana_resultado.configure(bg='#FFD1DC')
        
        # Mensaje de resultado
        mensaje = f"¡Felicitaciones!\n\nIntentos: {self.intentos}\nTiempo: {tiempo_total//60}:{tiempo_total%60:02d}"
        
        tk.Label(
            ventana_resultado,
            text=mensaje,
            font=("Helvetica", 14),
            fg='black',
            bg='#FFD1DC',
            justify=tk.CENTER
        ).pack(pady=20)
        
        # Botón para volver al menú
        tk.Button(
            ventana_resultado,
            text="Volver al Menú",
            command=lambda: [ventana_resultado.destroy(), self.volver_menu()],
            bg='#FF7F7F',
            fg='white',
            font=('Helvetica', 12)
        ).pack(pady=10)

    def volver_menu(self):
        """Vuelve al menú principal"""
        self.frame_tablero.destroy()
        self.frame_controles.destroy()
        self.cartas = []
        if self.menu_callback:
            self.menu_callback()