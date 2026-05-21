import pygame
import sys

pygame.init()

DIMENSION = 8  
TAMANO_CASILLA = 80 
ANCHO = ALTO = DIMENSION * TAMANO_CASILLA

COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)


pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tablero Blanco y Negro")

ejecutando = True
while ejecutando:
    
   
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    for fila in range(DIMENSION):
        for columna in range(DIMENSION):

            if (fila + columna) % 2 == 0:
                color = COLOR_BLANCO
            else:
                color = COLOR_NEGRO
            
           
            pygame.draw.rect(pantalla, color, pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

 
    pygame.display.flip()

pygame.quit()
sys.exit()