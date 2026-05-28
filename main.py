import pygame
import sys

pygame.init()

DIMENSION = 8  
TAMANO_CASILLA = 80 
ANCHO = ALTO = DIMENSION * TAMANO_CASILLA

# --- COLORES BLANCO Y NEGRO ---
COLOR_FONDO_BLANCO = (255, 255, 255)  # Casilla blanca
COLOR_FONDO_NEGRO = (0, 0, 0)          # Casilla negra
COLOR_SELECCION = (50, 150, 255)       # Azul para resaltar selección
COLOR_MENSAJE_FONDO = (40, 40, 40)
COLOR_MENSAJE_TEXTO = (255, 255, 255)

# Colores de fichas
COLOR_FICHA_BLANCA = (255, 255, 255)   
COLOR_FICHA_NEGRA = (0, 0, 0)           


pantalla = pygame.display.set_mode((ANCHO, ALTO + 50))  # Espacio extra para mensajes
pygame.display.set_caption("Ajedrez - Jaque Mate")

# Fuentes
fuente = pygame.font.SysFont("segoeuisymbol", 65)
fuente_mensaje = pygame.font.SysFont("arial", 28)

# --- VARIABLES DEL JUEGO ---
ficha_seleccionada = None  
posicion_seleccionada = None 
turno_actual = 'blanca'  # Empiezan las blancas
mensaje = ""
juego_terminado = False

# Tablero y piezas
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
    """Dibuja las casillas en blanco y negro"""
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            if (fila + columna) % 2 == 0:
                color = COLOR_FONDO_BLANCO
            else:
                color = COLOR_FONDO_NEGRO
            
            if posicion_seleccionada == (fila, columna):
                color = COLOR_SELECCION

            pygame.draw.rect(pantalla, color, pygame.Rect(columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

def dibujar_fichas():
    """Dibuja las fichas con borde para que se vean bien"""
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            pieza = tablero[fila][columna]
            color_pieza = colores_piezas[fila][columna]
            
            if pieza != '': 
                if color_pieza == 'blanca':
                    color = COLOR_FICHA_BLANCA
                    color_borde = (0, 0, 0) # Borde negro
                else:
                    color = COLOR_FICHA_NEGRA
                    color_borde = (255, 255, 255) # Borde blanco

                # Dibujar borde
                texto_borde = fuente.render(simbolos[pieza], True, color_borde)
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    rect_borde = texto_borde.get_rect(center=(
                        columna * TAMANO_CASILLA + TAMANO_CASILLA//2 + dx, 
                        fila * TAMANO_CASILLA + TAMANO_CASILLA//2 + dy
                    ))
                    pantalla.blit(texto_borde, rect_borde)

                # Dibujar pieza
                texto = fuente.render(simbolos[pieza], True, color)
                rect_texto = texto.get_rect(center=(
                    columna * TAMANO_CASILLA + TAMANO_CASILLA//2, 
                    fila * TAMANO_CASILLA + TAMANO_CASILLA//2
                ))
                pantalla.blit(texto, rect_texto)

def dibujar_mensaje():
    """Muestra mensajes en la parte inferior"""
    rect_fondo = pygame.Rect(0, ALTO, ANCHO, 50)
    pygame.draw.rect(pantalla, COLOR_MENSAJE_FONDO, rect_fondo)
    texto = fuente_mensaje.render(mensaje, True, COLOR_MENSAJE_TEXTO)
    rect_texto = texto.get_rect(center=(ANCHO//2, ALTO + 25))
    pantalla.blit(texto, rect_texto)

def es_movimiento_valido(pieza, inicio_fila, inicio_col, fin_fila, fin_col):
    """Reglas de movimiento de cada pieza"""
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
    """Busca la posición del rey"""
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            if tablero[fila][col] == 'rey' and colores_piezas[fila][col] == color:
                return (fila, col)
    return None

def esta_en_jaque(color):
    """Verifica si el rey está amenazado"""
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
    """Simula el movimiento para ver si deja al rey en jaque"""
    pieza_temp = tablero[fin_fila][fin_col]
    color_temp = colores_piezas[fin_fila][fin_col]

    pieza_origen = tablero[inicio_fila][inicio_col]
    color_origen = colores_piezas[inicio_fila][inicio_col]

    tablero[fin_fila][fin_col] = pieza_origen
    colores_piezas[fin_fila][fin_col] = color_origen
    tablero[inicio_fila][inicio_col] = ''
    colores_piezas[inicio_fila][inicio_col] = ''

    legal = not esta_en_jaque(color_origen)

    # Deshacer simulación
    tablero[inicio_fila][inicio_col] = pieza_origen
    colores_piezas[inicio_fila][inicio_col] = color_origen
    tablero[fin_fila][fin_col] = pieza_temp
    colores_piezas[fin_fila][fin_col] = color_temp

    return legal

def puede_salir_de_jaque(color):
    """Verifica si hay al menos una jugada posible para salir del jaque"""
    # Revisa todas las piezas y todos los movimientos posibles
    for f_ini in range(DIMENSION):
        for c_ini in range(DIMENSION):
            if colores_piezas[f_ini][c_ini] == color:
                for f_fin in range(DIMENSION):
                    for c_fin in range(DIMENSION):
                        if es_movimiento_valido(tablero[f_ini][c_ini], f_ini, c_ini, f_fin, c_fin):
                            if not hay_obstaculo(f_ini, c_ini, f_fin, c_fin):
                                if tablero[f_fin][c_fin] == '' or colores_piezas[f_fin][c_fin] != color:
                                    if es_jugada_legal(f_ini, c_ini, f_fin, c_fin):
                                        return True # Hay una forma de salir
    return False # No hay movimientos legales -> Jaque Mate

def verificar_estado_juego():
    """Comprueba si hay jaque o jaque mate"""
    global mensaje, juego_terminado
    color_actual = turno_actual
    
    if esta_en_jaque(color_actual):
        if puede_salir_de_jaque(color_actual):
            mensaje = "¡Jaque!"
        else:
            # No puede moverse ni defenderse -> JAQUE MATE
            ganador = "blancas" if color_actual == "negra" else "negras"
            mensaje = f"¡Jaque Mate! Ganan las {ganador}."
            juego_terminado = True

def manejar_click(pos_mouse):
    """Gestiona los clics del jugador"""
    global ficha_seleccionada, posicion_seleccionada, turno_actual, mensaje, juego_terminado

    if juego_terminado:
        return

    col = pos_mouse[0] // TAMANO_CASILLA
    fila = pos_mouse[1] // TAMANO_CASILLA

    if ficha_seleccionada is None:
        # Seleccionar ficha
        if tablero[fila][col] != '' and colores_piezas[fila][col] == turno_actual:
            ficha_seleccionada = tablero[fila][col]
            posicion_seleccionada = (fila, col)
            mensaje = f"Seleccionado: {ficha_seleccionada}"
    else:
        # Intentar mover
        fila_ini, col_ini = posicion_seleccionada
        
        if es_movimiento_valido(ficha_seleccionada, fila_ini, col_ini, fila, col):
            if not hay_obstaculo(fila_ini, col_ini, fila, col):
                pieza_destino = tablero[fila][col]
                color_origen = colores_piezas[fila_ini][col_ini]
                color_destino = colores_piezas[fila][col]

                if pieza_destino == '' or color_origen != color_destino:
                    if es_jugada_legal(fila_ini, col_ini, fila, col):
                        # Realizar movimiento
                        if pieza_destino != '':
                            mensaje = f"¡Has comido un/a {pieza_destino}!"
                        else:
                            mensaje = ""

                        tablero[fila][col] = ficha_seleccionada
                        colores_piezas[fila][col] = color_origen
                        tablero[fila_ini][col_ini] = ''
                        colores_piezas[fila_ini][col_ini] = ''

                        # Cambiar turno y verificar jaque/mate
                        turno_actual = 'negra' if turno_actual == 'blanca' else 'blanca'
                        verificar_estado_juego()

        # Reiniciar selección
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