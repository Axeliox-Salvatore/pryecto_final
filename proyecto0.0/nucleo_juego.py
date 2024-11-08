import tkinter as tk  # Importamos la biblioteca tkinter para los elementos de interfaz grafica
import random  # Importamos la biblioteca random para mezclar los valores de las cartas

class MemoriaJuego:
    def __init__(self, root, filas=4, columnas=4):
        """
        Inicializa el juego de memoria, creando el tablero y configurando la interfaz inicial
        
        Parametros:
        root: la ventana principal de Tkinter
        filas: numero de filas en el tablero
        columnas: numero de columnas en el tablero
        """
        self.root = root  # Referencia a la ventana principal
        self.filas = filas  # Almacena el numero de filas del tablero
        self.columnas = columnas  # Almacena el numero de columnas del tablero

        # Variables para llevar la cuenta del progreso del juego
        self.pares_encontrados = 0  # Conteo de los pares encontrados
        self.intentos = 0  # Conteo de los intentos realizados
        self.cartas = []  # Almacena los botones que representan las cartas
        self.seleccionadas = []  # Lista de las cartas seleccionadas por el jugador

        # Llamada para generar el tablero del juego
        self.generar_tablero()

    def generar_tablero(self):
        """
        Crea y distribuye los botones en el tablero de juego, asignando valores a cada carta
        """
        # Generamos una lista de pares de valores (ej. [1, 1, 2, 2, ...]) para las cartas
        valores = list(range(1, (self.filas * self.columnas // 2) + 1)) * 2  # Genera pares de valores
        random.shuffle(valores)  # Mezcla los valores de forma aleatoria

        # Creamos el tablero de botones, asignando un valor a cada uno
        for i in range(self.filas):  # Iteramos por cada fila
            fila = []  # Lista temporal para almacenar los botones de la fila
            for j in range(self.columnas):  # Iteramos por cada columna
                valor = valores.pop()  # Extraemos un valor de la lista de valores mezclados
                # Creamos un boton que representa una carta oculta
                boton = tk.Button(self.root, text="?", width=8, height=4,
                                  command=lambda i=i, j=j: self.seleccionar_carta(i, j))
                boton.valor = valor  # Almacenamos el valor de la carta en el boton
                boton.revelado = False  # Indicamos que la carta esta oculta
                boton.grid(row=i, column=j)  # Posicionamos el boton en la ventana
                fila.append(boton)  # Agregamos el boton a la lista de la fila
            self.cartas.append(fila)  # Agregamos la fila completa al tablero de cartas

    def seleccionar_carta(self, i, j):
        """
        Gestiona la seleccion de una carta, rebelandola y verificando si forma una pareja
        
        Parametros:
        - i: indice de la fila de la carta seleccionada
        - j: indice de la columna de la carta seleccionada
        """
        boton = self.cartas[i][j]  # Obtenemos el boton correspondiente a la carta seleccionada

        # Verificamos si la carta ya esta revelada o si hay dos cartas seleccionadas
        if boton.revelado or len(self.seleccionadas) >= 2:
            return  # Si ya esta revelada o hay dos seleccionadas, no hacemos nada

        # Revelamos la carta mostrando su valor y marcandola como revelada
        boton.config(text=str(boton.valor))  # Mostramos el valor de la carta
        boton.revelado = True  # Marcamos la carta como revelada
        self.seleccionadas.append(boton)  # Agregamos la carta a la lista de seleccionadas

        # Si hay dos cartas seleccionadas, verificamos si son una pareja
        if len(self.seleccionadas) == 2:
            self.root.after(1000, self.verificar_pareja)  # Llama a verificar la pareja tras 1 segundo

    def verificar_pareja(self):
        """
        Verifica si las dos cartas seleccionadas forman una pareja si es asi, las desactiva
        si no es asi las vuelve a ocultar
        """
        carta1, carta2 = self.seleccionadas  # Obtenemos las dos cartas seleccionadas

        # Si los valores de las dos cartas coinciden, es una pareja
        if carta1.valor == carta2.valor:
            carta1.config(state="disabled")  # Desactiva la primera carta de la pareja
            carta2.config(state="disabled")  # Desactiva la segunda carta de la pareja
            self.pares_encontrados += 1  # Incrementa el contador de pares encontrados
        else:
            # Si no es una pareja, oculta nuevamente las cartas
            carta1.config(text="?")  # Vuelve a ocultar el valor de la primera carta
            carta2.config(text="?")  # Vuelve a ocultar el valor de la segunda carta
            carta1.revelado = False  # Marca la primera carta como no revelada
            carta2.revelado = False  # Marca la segunda carta como no revelada

        # Resetea la lista de cartas seleccionadas y aumenta el contador de intentos
        self.seleccionadas = []  # Vacia la lista de cartas seleccionadas
        self.intentos += 1  # Incrementa el numero de intentos realizados

        # Si todos los pares fueron encontrados, muestra el resultado
        if self.pares_encontrados == (self.filas * self.columnas // 2):
            self.mostrar_resultado()

    def mostrar_resultado(self):
        """
        Muestra un mensaje indicando el numero de intentos que realizo el jugador para completar el juego
        """
        resultado = f"Juego terminado! Intentos: {self.intentos}"  # Mensaje de resultado
        # Muestra el mensaje en la interfaz
        etiqueta_resultado = tk.Label(self.root, text=resultado, font=("Arial", 14))
        etiqueta_resultado.grid(row=self.filas, column=0, columnspan=self.columnas)  # Posiciona el mensaje en el tablero
