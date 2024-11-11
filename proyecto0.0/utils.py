import os
import json
from datetime import datetime
import pygame

class ReproductorMusica:
    @staticmethod
    def iniciar_musica():
        pygame.mixer.init()
        ruta_musica = os.path.join(os.getcwd(), "sonidos", "Bad_Apple.mp3")
        if not os.path.isfile(ruta_musica):
            print(f"Error: el archivo de música no se encuentra en {ruta_musica}")
            return
        pygame.mixer.music.load(ruta_musica)
        pygame.mixer.music.play(-1)  # Repetir indefinidamente

class ReproductorSonidos:
    @staticmethod
    def cargar_sonidos():
        pygame.mixer.init()
        try:
            ReproductorSonidos.sonido_acierto = pygame.mixer.Sound(os.path.join(os.getcwd(), "sonidos", "bien.mp3"))
            ReproductorSonidos.sonido_fallo = pygame.mixer.Sound(os.path.join(os.getcwd(), "sonidos", "fallo.mp3"))
            ReproductorSonidos.sonido_ganar = pygame.mixer.Sound(os.path.join(os.getcwd(), "sonidos", "ganar.mp3"))
            ReproductorSonidos.sonido_menu = pygame.mixer.Sound(os.path.join(os.getcwd(), "sonidos", "menu.mp3"))
            ReproductorSonidos.sonido_salir = pygame.mixer.Sound(os.path.join(os.getcwd(), "sonidos", "salir.mp3"))
        except Exception as e:
            print(f"Error al cargar los sonidos: {e}")

    @staticmethod
    def reproducir_acierto():
        ReproductorSonidos.sonido_acierto.play()

    @staticmethod
    def reproducir_fallo():
        ReproductorSonidos.sonido_fallo.play()
    
    @staticmethod
    def reproducir_ganar():
        ReproductorSonidos.sonido_ganar.play()
        
    @staticmethod
    def reproducir_menu():
        ReproductorSonidos.sonido_menu.play()

    @staticmethod
    def reproducir_salir():
        ReproductorSonidos.sonido_salir.play()    

class Constantes:
    COLOR_FONDO = "#2C3E50"
    COLOR_BOTON_JUGAR = "#3498DB"
    COLOR_BOTON_PUNTUACIONES = "#2ECC71"
    COLOR_BOTON_SALIR = "#E74C3E"
    
    FUENTE_TITULO = ("Helvetica", 36, "bold")
    FUENTE_BOTON = ("Helvetica", 14)
    
    VENTANA_ANCHO = 800
    VENTANA_ALTO = 600

class GestorPuntuaciones:
    def __init__(self, archivo='puntuaciones.json'):
        self.archivo = archivo
        self.puntuaciones = self.cargar_puntuaciones()

    def cargar_puntuaciones(self):
        """Carga las puntuaciones del archivo JSON."""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as f:
                    self.puntuaciones = json.load(f)
            except json.JSONDecodeError:
                print("Error: el archivo de puntuaciones está corrupto.")
                self.puntuaciones = []
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.puntuaciones = []
        else:
            self.puntuaciones = []
        return self.puntuaciones

    def guardar_puntuaciones(self):
        """Guarda las puntuaciones en el archivo JSON."""
        with open(self.archivo, 'w') as f:
            json.dump(self.puntuaciones, f)

    def agregar_puntuacion(self, intentos, tiempo):
        """Agrega una nueva puntuación y mantiene solo las mejores 10."""
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        puntuacion = {
            'intentos': intentos,
            'tiempo': tiempo,
            'fecha': fecha
        }
        
        self.puntuaciones.append(puntuacion)
        # Ordenar por intentos (menor es mejor) y luego por tiempo (menor es mejor)
        self.puntuaciones.sort(key=lambda x: (x['intentos'], x['tiempo']))
        # Mantener solo las mejores 10 puntuaciones
        self.puntuaciones = self.puntuaciones[:10]
        self.guardar_puntuaciones()

    def obtener_mejores_puntuaciones(self):
        """Retorna las mejores puntuaciones ordenadas."""
        return self.puntuaciones
