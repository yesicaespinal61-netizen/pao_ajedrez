import pygame
import sys

pygame.init()

DIMENSION = 8  
TAMANO_CASILLA = 80 
ANCHO = ALTO = DIMENSION * TAMANO_CASILLA

# --- COLORES MODIFICADOS: BLANCO Y NEGRO PURO ---
COLOR_FONDO_BLANCO = (255, 255, 255)  # Casilla blanca
COLOR_FONDO_NEGRO = (0, 0, 0)          # Casilla negra
COLOR_SELECCION = (120, 120, 255)     # Azul para resaltar selección (contrasta bien)
COLOR_MENSAJE_FONDO = (40, 40, 40)
COLOR_MENSAJE_TEXTO = (255, 255, 255)

# Colores de fichas
COLOR_FICHA_BLANCA = (255, 255, 255)   
COLOR_FICHA_NEGRA = (0, 0, 0)           


pantalla = pygame.display.set_mode((ANCHO, ALTO + 50))  # Espacio extra para mensajes
pygame.display.set_caption("Ajedrez - Blanco y Negro")

# Fuentes
fuente = pygame.font.SysFont("segoeuisymbol", 65)
fuente_mensaje = pygame.font.SysFont("arial", 30)

# --- VARIABLES PARA EL MOVIMIENTO Y ESTADO ---
ficha_seleccionada = None  
posicion_seleccionada = None 
turno_actual = 'blanca'  # Empiezan las blancas
mensaje = ""
juego_terminado = False

# Definimos todas las piezas y su posición inicial
tablero = [
    ['torre', 'caballo', 'alfil', 'reina', 'rey', 'alfil', 'caballo', 'torre'],
    ['peon', 'peon', 'peon', 'peon', 'peon', 'peon', 'peon', 'peon'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['peon', 'peon', 'peon', 'peon', 'peon', 'peon', 'peon', 'peon'],
    ['torre', 'caballo', 'alfil', 'reina', 'rey', 'alfil', 'caballo', 'torre']
]

# Definimos el color de cada pieza en el tablero
colores_piezas = [
    ['negra', 'negra', 'negra', 'negra', 'negra', 'negra', 'negra', 'negra'],
    ['negra', 'negra', 'negra', 'negra', 'negra', 'negra', 'negra', 'negra'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca'],
    ['blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca', 'blanca']
]

simbolos = {
    'rey': '♚',
    'reina': '♛',
    'alfil': '♝',
    'caballo': '♞',
    'torre': '♜',
    'peon': '♟'
}

def dibujar_tablero():
    """Dibuja las casillas del tablero en blanco y negro"""
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            # Alternancia estricta blanco y negro
            if (fila + columna) % 2 == 0:
                color = COLOR_FONDO_BLANCO
            else:
                color = COLOR_FONDO_NEGRO
            
            if posicion_seleccionada == (fila, columna):
                color = COLOR_SELECCION

            pygame.draw.rect(pantalla, color, pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

def dibujar_fichas():
    """Dibuja las fichas, con borde para que se vean sobre fondo del mismo color"""
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            pieza = tablero[fila][columna]
            color_pieza = colores_piezas[fila][columna]
            
            if pieza != '': 
                if color_pieza == 'blanca':
                    color = COLOR_FICHA_BLANCA
                    # Borde negro para fichas blancas (se vean en casillas blancas)
                    color_borde = (0, 0, 0)
                else:
                    color = COLOR_FICHA_NEGRA
                    # Borde blanco para fichas negras (se vean en casillas negras)
                    color_borde = (255, 255, 255)

                # Dibujamos primero el borde (desplazado 1 píxel)
                texto_borde = fuente.render(simbolos[pieza], True, color_borde)
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    rect_borde = texto_borde.get_rect(center=(
                        columna * TAMANO_CASILLA + TAMANO_CASILLA//2 + dx, 
                        fila * TAMANO_CASILLA + TAMANO_CASILLA//2 + dy
                    ))
                    pantalla.blit(texto_borde, rect_borde)

                # Dibujamos la pieza encima
                texto = fuente.render(simbolos[pieza], True, color)
                rect_texto = texto.get_rect(center=(
                    columna * TAMANO_CASILLA + TAMANO_CASILLA//2, 
                    fila * TAMANO_CASILLA + TAMANO_CASILLA//2
                ))
                pantalla.blit(texto, rect_texto)

def dibujar_mensaje():
    """Muestra mensajes de estado en la parte inferior"""
    rect_fondo = pygame.Rect(0, ALTO, ANCHO, 50)
    pygame.draw.rect(pantalla, COLOR_MENSAJE_FONDO, rect_fondo)
    texto = fuente_mensaje.render(mensaje, True, COLOR_MENSAJE_TEXTO)
    rect_texto = texto.get_rect(center=(ANCHO//2, ALTO + 25))
    pantalla.blit(texto, rect_texto)

def es_movimiento_valido(pieza, inicio_fila, inicio_col, fin_fila, fin_col):
    """Comprueba si el movimiento sigue las reglas básicas de cada pieza"""
    df = fin_fila - inicio_fila
    dc = fin_col - inicio_col

    if df == 0 and dc == 0:
        return False

    if pieza == 'peon':
        pieza_destino = tablero[fin_fila][fin_col]
        if colores_piezas[inicio_fila][inicio_col] == 'negra':
            if df == 1 and dc == 0 and pieza_destino == '': 
                return True
            if inicio_fila == 1 and df == 2 and dc == 0 and pieza_destino == '' and tablero[inicio_fila+1][inicio_col] == '': 
                return True
            if df == 1 and abs(dc) == 1 and pieza_destino != '' and colores_piezas[fin_fila][fin_col] == 'blanca':
                return True
        else: 
            if df == -1 and dc == 0 and pieza_destino == '': 
                return True
            if inicio_fila == 6 and df == -2 and dc == 0 and pieza_destino == '' and tablero[inicio_fila-1][inicio_col] == '': 
                return True
            if df == -1 and abs(dc) == 1 and pieza_destino != '' and colores_piezas[fin_fila][fin_col] == 'negra':
                return True

    elif pieza == 'torre':
        if df == 0 or dc == 0:
            return True

    elif pieza == 'caballo':
        if (abs(df), abs(dc)) in [(2,1), (1,2)]:
            return True

    elif pieza == 'alfil':
        if abs(df) == abs(dc):
            return True

    elif pieza == 'reina':
        if df == 0 or dc == 0 or abs(df) == abs(dc):
            return True

    elif pieza == 'rey':
        if abs(df) <= 1 and abs(dc) <= 1:
            return True

    return False

def hay_obstaculo(inicio_fila, inicio_col, fin_fila, fin_col):
    """Verifica si hay piezas en el camino"""
    df = fin_fila - inicio_fila
    dc = fin_col - inicio_col

    if tablero[inicio_fila][inicio_col] == 'caballo':
        return False

    paso_fila = 0 if df == 0 else df // abs(df)
    paso_col = 0 if dc == 0 else dc // abs(dc)

    f, c = inicio_fila + paso_fila, inicio_col + paso_col
    while (f, c) != (fin_fila, fin_col):
        if tablero[f][c] != '':
            return True 
        f += paso_fila
        c += paso_col

    return False

def encontrar_rey(color):
    """Busca la posición del rey de un color"""
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            if tablero[fila][col] == 'rey' and colores_piezas[fila][col] == color:
                return (fila, col)
    return None

def esta_en_jaque(color):
    """Verifica si el rey de este color está en jaque"""
    rey_fila, rey_col = encontrar_rey(color)
    color_enemigo = 'negra' if color == 'blanca' else 'blanca'

    for f in range(DIMENSION):
        for c in range(DIMENSION):
            if colores_piezas[f][c] == color_enemigo:
                if es_movimiento_valido(tablero[f][c], f, c, rey_fila, rey_col):
                    if not hay_obstaculo(f, c, rey_fila, rey_col):
                        return True
    return False

def es_jugada_legal(inicio_fila, inicio_col, fin_fila, fin_col):
    """Verifica que la jugada no deje al rey en jaque"""
    pieza_temp = tablero[fin_fila][fin_col]
    color_temp = colores_piezas[fin_fila][fin_col]

    pieza_origen = tablero[inicio_fila][inicio_col]
    color_origen = colores_piezas[inicio_fila][inicio_col]

    tablero[fin_fila][fin_col] = pieza_origen
    colores_piezas[fin_fila][fin_col] = color_origen
    tablero[inicio_fila][inicio_col] = ''
    colores_piezas[inicio_fila][inicio_col] = ''

    legal = not esta_en_jaque(color_origen)

    tablero[inicio_fila][inicio_col] = pieza_origen
    colores_piezas[inicio_fila][inicio_col] = color_origen
    tablero[fin_fila][fin_col] = pieza_temp
    colores_piezas[fin_fila][fin_col] = color_temp

    return legal

def hay_rey(color):
    """Comprueba si existe el rey de un color"""
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            if tablero[fila][col] == 'rey' and colores_piezas[fila][col] == color:
                return True
    return False

def manejar_click(pos_mouse):
    """Gestiona lo que pasa al hacer clic en el tablero"""
    global ficha_seleccionada, posicion_seleccionada, turno_actual, mensaje, juego_terminado

    if juego_terminado:
        return

    col = pos_mouse[0] // TAMANO_CASILLA
    fila = pos_mouse[1] // TAMANO_CASILLA

    if ficha_seleccionada is None:
        if tablero[fila][col] != '' and colores_piezas[fila][col] == turno_actual:
            ficha_seleccionada = tablero[fila][col]
            posicion_seleccionada = (fila, col)
            mensaje = f"Seleccionado: {ficha_seleccionada}"
    else:
        fila_ini, col_ini = posicion_seleccionada
        
        if es_movimiento_valido(ficha_seleccionada, fila_ini, col_ini, fila, col):
            if not hay_obstaculo(fila_ini, col_ini, fila, col):
                pieza_destino = tablero[fila][col]
                color_origen = colores_piezas[fila_ini][col_ini]
                color_destino = colores_piezas[fila][col]

                if pieza_destino == '' or color_origen != color_destino:
                    if es_jugada_legal(fila_ini, col_ini, fila, col):
                        if pieza_destino != '':
                            mensaje = f"¡Has comido un/a {pieza_destino}!"
                        else:
                            mensaje = ""

                        tablero[fila][col] = ficha_seleccionada
                        colores_piezas[fila][col] = color_origen
                        tablero[fila_ini][col_ini] = ''
                        colores_piezas[fila_ini][col_ini] = ''

                        # Verificar si se comió al rey
                        if not hay_rey('negra'):
                            mensaje = "¡Ganan las BLANCAS! Fin del juego."
                            juego_terminado = True
                        elif not hay_rey('blanca'):
                            mensaje = "¡Ganan las NEGRAS! Fin del juego."
                            juego_terminado = True
                        else:
                            turno_actual = 'negra' if turno_actual == 'blanca' else 'blanca'

        ficha_seleccionada = None
        posicion_seleccionada = None


# Bucle principal
ejecutando = True
while ejecutando:
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1: 
                manejar_click(evento.pos)

    pantalla.fill((0,0,0))
    dibujar_tablero()
    dibujar_fichas()
    dibujar_mensaje()
    
    pygame.display.flip()

pygame.quit()
sys.exit()        