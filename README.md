# 🍎 Vista Previa 🍎

![Juego de Memoria Demo](https://s11.gifyu.com/images/SGblI.gif)

### 🎮 ¡Pon a prueba tu memoria en este emocionante juego! 🧠✨

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Activo-success.svg)](https://github.com/Axeliox-Salvatore/pryecto_final)

## 📝 Descripción

Este es un juego de memoria interactivo desarrollado en Python donde los jugadores deben encontrar pares de cartas coincidentes. El juego utiliza imágenes de frutas para un interesante desafío visual y ofrece una interfaz gráfica amigable con efectos de sonido para una experiencia más inmersiva.

## 🚀 Características

| Característica | Descripción |
|----------------|-------------|
| 🎨 **Interfaz Gráfica Intuitiva** | Diseño amigable para jugar desde ordenador |
| 🔊 **Efectos de Sonido** | Sonidos para aciertos y fallos que aumentan la inmersión |
| 🏆 **Sistema de Puntuación** | Registra tus tiempos y intentos en cada partida |
| 📊 **Registro de Mejores Puntuaciones** | Mantiene y muestra las mejores puntuaciones |
| ⏱️ **Temporizador de Juego** | Controla el tiempo transcurrido en cada partida |
| 🔢 **Contador de Intentos** | Monitorea el número de intentos realizados |

## 📁 Estructura del Proyecto

```plaintext
juego-memoria/
├── 📂 librerias/
│   └── 📜 librerias.py     # Script para instalar dependencias
│
├── 📂 img/                 # Imágenes de las cartas
│   └── 🖼️ ...              # Archivos de imágenes
│
├── 📂 sonidos/             # Efectos de sonido
│   └── 🔊 ...              # Archivos de audio
│    
├── 📊 puntuaciones.json    # Registro de puntuaciones
└── 🎮 main.py              # Archivo principal del juego
```

## 📋 Requisitos Previos

| Requisito | Versión |
|-----------|---------|
| ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) | 3.x o superior |
| ![pip](https://img.shields.io/badge/pip-Latest-orange.svg) | Última versión |
| ![Git](https://img.shields.io/badge/Git-Latest-f05032.svg) | Última versión |

## ⚙️ Instalación

### 1️⃣ Descargar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/Axeliox-Salvatore/pryecto_final.git

# Entrar al directorio
cd pryecto_final
```

### 2️⃣ Instalar Dependencias

```bash
# Usando el script de instalación
python librerias/librerias.py
```

## 🎮 Cómo Jugar

### 🕹️ Controles Principales

| Acción | Descripción |
|--------|-------------|
| 🖱️ Clic | Revelar carta |
| 🌓 Tema | Cambiar tema (☀️/🌙) |

### 📊 Niveles de Dificultad

| Nivel | Tablero | Dificultad |
|-------|----------|------------|
| 1️⃣ | 4x4 | Principiante |
| 2️⃣ | 6x6 | Intermedio |
| 3️⃣ | 8x8 | Avanzado |

## ❗ Solución de Problemas

### 📷 Las imágenes no se cargan
- ✅ Verifica que todas las imágenes estén en la carpeta `img/`
- ✅ Comprueba que los nombres de los archivos coincidan
- ✅ Asegúrate de que las imágenes sean archivos válidos

### 🔊 Los sonidos no funcionan
- ✅ Confirma que los archivos de sonido estén en `sonidos/`
- ✅ Verifica que los archivos sean `.mp3` válidos
- ✅ Comprueba que pygame esté instalado correctamente

### 💾 Error al guardar puntuaciones
- ✅ Verifica los permisos de escritura
- ✅ Comprueba que `puntuaciones.json` sea accesible

## 🌟 ¡Diviértete jugando! 🌟

![Logo](https://avatars.githubusercontent.com/u/85382972?v=4)
