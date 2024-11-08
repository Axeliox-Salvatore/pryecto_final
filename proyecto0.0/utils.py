import os
import json
from datetime import datetime

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
            except:
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
