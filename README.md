# 🎮 Juego de Memoria

## 📝 Descripción
Este es un juego de memoria interactivo desarrollado en Python donde los jugadores deben encontrar pares de cartas coincidentes. El juego utiliza imágenes de frutas y ofrece una interfaz gráfica amigable con efectos de sonido para una experiencia más inmersiva.

## 🚀 Características
- Interfaz gráfica intuitiva
- Efectos de sonido para aciertos y fallos
- Sistema de puntuación
- Registro de mejores puntuaciones
- Temporizador de juego
- Contador de intentos

## 📁 Estructura del Proyecto
```
juego-memoria/
│
├── librerias/
│   └── librerias.py     # Script para instalar dependencias
│
├── img/                 # Imágenes de las cartas
│   └── ...              # Archivos de imágenes
│
├── sonidos/             # Efectos de sonido
│   └── ...
│    
├── puntuaciones.json    # Registro de puntuaciones
└── main.py              # Archivo principal del juego
```

## 📋 Requisitos Previos
- Python 3.x
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

## ⚙️ Instalación

### Descargar el Proyecto
1. Abre una terminal
2. Clona el repositorio:
```bash
git clone https://github.com/Axeliox-Salvatore/pryecto_final.git
```
3. Entra al directorio del proyecto:
```bash
cd pryecto_final
```

### Opción 1: Usando el Script de Instalación
1. Abre una terminal
2. Navega hasta la carpeta del proyecto
3. Ejecuta:
```bash
python librerias/librerias.py
```

### Opción 2: Instalación Manual
```bash
pip install Pillow
pip install pygame
```

## 🎮 Cómo Jugar

1. **Iniciar el Juego**
   ```bash
   python main.py
   ```

2. **Menú Principal**
   - **JUGAR**: Inicia una nueva partida
   - **PUNTUACIONES**: Muestra el historial de mejores puntuaciones
   - **SALIR**: Cierra el juego

3. **Reglas del Juego**
   - Haz clic en dos cartas para revelarlas
   - Si las cartas coinciden, permanecerán visibles
   - Si no coinciden, se volverán a ocultar
   - El objetivo es encontrar todos los pares con el menor número de intentos

4. **Puntuación**
   - Al completar el juego, podrás guardar tu puntuación
   - Se registra el tiempo empleado y el número de intentos

## ❗ Solución de Problemas

### Problemas Comunes y Soluciones

1. **Las imágenes no se cargan**
   - Verifica que todas las imágenes estén en la carpeta `img/`
   - Comprueba que los nombres de los archivos coincidan con los esperados
   - Asegúrate de que las imágenes sean archivos válidos

2. **Los sonidos no funcionan**
   - Confirma que los archivos de sonido estén en la carpeta `sonidos/`
   - Verifica que los archivos sean `.mp3` válidos
   - Comprueba que pygame esté correctamente instalado

3. **Error al guardar puntuaciones**
   - Verifica los permisos de escritura en el directorio
   - Comprueba que `puntuaciones.json` sea accesible

### Integrantes:
