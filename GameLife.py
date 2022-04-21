import pygame
import numpy as np
from time import sleep

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

#Creación de celdas en X y Y
nCx, nCy = 25, 25
#Ancho y alto de las celdas
dimCW = width/nCx
dimCH = height/nCy

#Matriz que genera las celulas (celdas). Viva = 1, Muerta = 0 /Estado de cada celula
gameState = np.zeros((nCx, nCy))

#Aqui se ponen los automatas (conjunto de celulas) para iniciar el juego:
#Ejemplo de autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

#Ejemplo de automata movil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

#Variable que controla el flujo de ejecución del juego con las teclas
pausaExect = False

#Bucles de ejecucion para recorrer los ejes X y Y (vista del tablero)
while True:
    #Realizamos una copia del estado actual del juego
    newGameState = np.copy(gameState)

    #Limpiamos la pantalla en cada iteración
    screen.fill(bg)
    sleep(0.3) #Para observar el cambio del estado de las células en cada iteración

    #Para que cada vez pulsemos una tecla, la ejecución del juego se detenga
    evento = pygame.event.get()
    for ev in evento:
        if ev.type == pygame.KEYDOWN:
            pausaExect = not pausaExect

    #Para cambiar de manera dinamica el estado de las celdas (matar y revivir células)
    mouseClick = pygame.mouse.get_pressed()
    if sum(mouseClick) > 0:
        PosX, PosY = pygame.mouse.get_pos()
        celX, celY = int(np.floor(PosX / dimCW)), int(np.floor(PosY / dimCH))
        newGameState[celX, celY] = not mouseClick[2]

    #Comienza el analisis de las células
    for y in range(0, nCx):
        for x in range(0, nCy):
            if not pausaExect:
                #Para el calculo del número de vecinos cercanos a cada celula
                n_vecinos = gameState[(x-1) % nCx, (y-1) % nCy] + \
                            gameState[(x) % nCx, (y-1) % nCy] + \
                            gameState[(x+1) % nCx, (y-1) % nCy] + \
                            gameState[(x-1) % nCx, (y) % nCy] + \
                            gameState[(x+1) % nCx, (y) % nCy] + \
                            gameState[(x-1) % nCx, (y+1) % nCy] + \
                            gameState[(x) % nCx, (y+1) % nCy] + \
                            gameState[(x+1) % nCx, (y+1) % nCy]

                #Se definen las reglas del juego
                #Primer regla: Una célula muerta (en 0) con exactamente 3 vecinas vivas, revive
                if gameState[x, y] == 0 and n_vecinos == 3:
                    newGameState[x, y] = 1

                #Segunda regla: Una célula viva (en 1) con menos de 2 o más de 3 vecinas vivas, muere
                elif gameState[x, y] == 1 and (n_vecinos < 2 or n_vecinos > 3):
                    newGameState[x, y] = 0

                #Poligono que representa a cada celda a dibujar / célula
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            #Dibujamos cada celda segun el estado de la célula
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)  #célula muerta
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)  #célula viva
    #Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    #Actualizamos la pantalla
    pygame.display.flip()