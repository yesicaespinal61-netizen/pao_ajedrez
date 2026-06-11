import pygame
import sys
import time

pygame.init()

DIMENSION = 8  
TAMANO_CASILLA = 80 
ANCHO = ALTO = DIMENSION * TAMANO_CASILLA

# --- COLORES ---
COLOR_FONDO_BLANCO = (255, 255, 255)
COLOR_FONDO_NEGRO = (0, 0, 0)
COLOR_SELECCION = (50, 150, 255)
COLOR_MENSAJE_FONDO = (40, 40, 40)
COLOR_MENSAJE_TEXTO = (255, 255, 255)
COLOR_TIEMPO = (255, 215, 0)
COLOR_BOTON = (70, 130, 180)       # Color azul acero
COLOR_BOTON_HOVER = (100, 160, 210) # Color al pasar el mouse
COLOR_BOTON_TEXTO = (255, 255, 255)

# Colores de fichas
COLOR_FICHA_BLANCA = (255, 255, 255)   
COLOR_FICHA_NEGRA = (0, 0, 0)           


pantalla = pygame.display.set_mode((ANCHO, ALTO + 120))  # Más altura para el botón
pygame.display.set_caption("Ajedrez - Jaque Mate")

# Fuentes
fuente = pygame.font.SysFont("segoeuisymbol", 65)
fuente_mensaje = pygame.font.SysFont("arial", 24)
fuente_tiempo = pygame.font.SysFont("arial", 28, bold=True)
fuente_boton = pygame.font.SysFont("arial", 22, bold=True)

# --- VARIABLES DEL JUEGO ---
ficha_seleccionada = None  
posicion_seleccionada = None 
turno_actual = 'blanca'
mensaje = ""
juego_terminado = False

# --- VARIABLES DE TIEMPO ---
TIEMPO_INICIAL = 300  # 5 minutos = 300 segundos
tiempo_blancas = TIEMPO_INICIAL
tiempo_negras = TIEMPO_INICIAL
ultimo_tiempo = time.time()
tiempo_agotado = False

# --- DATOS DEL BOTÓN DE REINICIO ---
boton_reinicio = pygame.Rect(ANCHO//2 - 80, ALTO + 75, 160, 35)
mostrar_boton = False

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

def reiniciar_juego():
    """Devuelve todo al estado inicial"""
    global ficha_seleccionada, posicion_seleccionada, turno_actual, mensaje
    global juego_terminado, tiempo_blancas, tiempo_negras, ultimo_tiempo
    global tiempo_agotado, mostrar_boton, tablero, colores_piezas

    # Reiniciar variables de estado
    ficha_seleccionada = None  
    posicion_seleccionada = None 
    turno_actual = 'blanca'
    mensaje = ""
    juego_terminado = False
    tiempo_agotado = False
    mostrar_boton = False

    # Reiniciar tiempos
    tiempo_blancas = TIEMPO_INICIAL
    tiempo_negras = TIEMPO_INICIAL
    ultimo_tiempo = time.time()

    # Reiniciar tablero
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

def dibujar_tablero():
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
    for fila in range(DIMENSION):
        for columna in range(DIMENSION):
            pieza = tablero[fila][columna]
            color_pieza = colores_piezas[fila][columna]
            
            if pieza != '': 
                if color_pieza == 'blanca':
                    color = COLOR_FICHA_BLANCA
                    color_borde = (0, 0, 0)
                else:
                    color = COLOR_FICHA_NEGRA
                    color_borde = (255, 255, 255)

                texto_borde = fuente.render(simbolos[pieza], True, color_borde)
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    rect_borde = texto_borde.get_rect(center=(
                        columna * TAMANO_CASILLA + TAMANO_CASILLA//2 + dx, 
                        fila * TAMANO_CASILLA + TAMANO_CASILLA//2 + dy
                    ))
                    pantalla.blit(texto_borde, rect_borde)

                texto = fuente.render(simbolos[pieza], True, color)
                rect_texto = texto.get_rect(center=(
                    columna * TAMANO_CASILLA + TAMANO_CASILLA//2, 
                    fila * TAMANO_CASILLA + TAMANO_CASILLA//2
                ))
                pantalla.blit(texto, rect_texto)

def dibujar_mensaje():
    rect_fondo = pygame.Rect(0, ALTO, ANCHO, 120)
    pygame.draw.rect(pantalla, COLOR_MENSAJE_FONDO, rect_fondo)
    
    # Mensaje principal
    texto = fuente_mensaje.render(mensaje, True, COLOR_MENSAJE_TEXTO)
    rect_texto = texto.get_rect(center=(ANCHO//2, ALTO + 20))
    pantalla.blit(texto, rect_texto)

    def formato_tiempo(segundos):
        m = int(segundos // 60)
        s = int(segundos % 60)
        return f"{m:02d}:{s:02d}"

    # Tiempo blancas
    texto_t_blancas = fuente_tiempo.render(f"Blancas: {formato_tiempo(tiempo_blancas)}", True, COLOR_TIEMPO if turno_actual == 'blanca' else COLOR_MENSAJE_TEXTO)
    pantalla.blit(texto_t_blancas, (20, ALTO + 45))

    # Tiempo negras
    texto_t_negras = fuente_tiempo.render(f"Negras: {formato_tiempo(tiempo_negras)}", True, COLOR_TIEMPO if turno_actual == 'negra' else COLOR_MENSAJE_TEXTO)
    rect_n = texto_t_negras.get_rect(right=ANCHO - 20)
    pantalla.blit(texto_t_negras, (rect_n.x, ALTO + 45))

    # Dibujar botón si corresponde
    if mostrar_boton:
        # Cambiar color si el mouse está encima
        pos_mouse = pygame.mouse.get_pos()
        color_boton_actual = COLOR_BOTON_HOVER if boton_reinicio.collidepoint(pos_mouse) else COLOR_BOTON
        
        pygame.draw.rect(pantalla, color_boton_actual, boton_reinicio, border_radius=8)
        texto_boton = fuente_boton.render("Reiniciar partida", True, COLOR_BOTON_TEXTO)
        rect_texto_boton = texto_boton.get_rect(center=boton_reinicio.center)
        pantalla.blit(texto_boton, rect_texto_boton)

def actualizar_tiempo():
    global tiempo_blancas, tiempo_negras, ultimo_tiempo, juego_terminado, mensaje, tiempo_agotado, mostrar_boton
    
    if juego_terminado or tiempo_agotado:
        return

    tiempo_actual_seg = time.time()
    paso = tiempo_actual_seg - ultimo_tiempo
    ultimo_tiempo = tiempo_actual_seg

    if turno_actual == 'blanca':
        tiempo_blancas -= paso
        if tiempo_blancas <= 0:
            tiempo_blancas = 0
            juego_terminado = True
            tiempo_agotado = True
            mensaje = "¡Tiempo agotado! Ganan las negras."
            mostrar_boton = True # Mostrar botón al finalizar
    else:
        tiempo_negras -= paso
        if tiempo_negras <= 0:
            tiempo_negras = 0
            juego_terminado = True
            tiempo_agotado = True
            mensaje = "¡Tiempo agotado! Ganan las blancas."
            mostrar_boton = True # Mostrar botón al finalizar

def es_movimiento_valido(pieza, inicio_fila, inicio_col, fin_fila, fin_col):
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
    for fila in range(DIMENSION):
        for col in range(DIMENSION):
            if tablero[fila][col] == 'rey' and colores_piezas[fila][col] == color:
                return (fila, col)
    return None

def esta_en_jaque(color):
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

def puede_salir_de_jaque(color):
    for f_ini in range(DIMENSION):
        for c_ini in range(DIMENSION):
            if colores_piezas[f_ini][c_ini] == color:
                for f_fin in range(DIMENSION):
                    for c_fin in range(DIMENSION):
                        if es_movimiento_valido(tablero[f_ini][c_ini], f_ini, c_ini, f_fin, c_fin):
                            if not hay_obstaculo(f_ini, c_ini, f_fin, c_fin):
                                if tablero[f_fin][c_fin] == '' or colores_piezas[f_fin][c_fin] != color:
                                    if es_jugada_legal(f_ini, c_ini, f_fin, c_fin):
                                        return True
    return False

def verificar_estado_juego():
    global mensaje, juego_terminado, mostrar_boton
    color_actual = turno_actual
    
    if esta_en_jaque(color_actual):
        if puede_salir_de_jaque(color_actual):
            mensaje = "¡Jaque!"
        else:
            ganador = "blancas" if color_actual == "negra" else "negras"
            mensaje = f"¡Jaque Mate! Ganan las {ganador}."
            juego_terminado = True
            mostrar_boton = True # Mostrar botón al haber jaque mate

def manejar_click(pos_mouse):
    global ficha_seleccionada, posicion_seleccionada, turno_actual, mensaje, juego_terminado, ultimo_tiempo

    # Verificar si se hizo clic en el botón de reinicio
    if mostrar_boton and boton_reinicio.collidepoint(pos_mouse):
        reiniciar_juego()
        return

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

                        turno_actual = 'negra' if turno_actual == 'blanca' else 'blanca'
                        ultimo_tiempo = time.time()
                        verificar_estado_juego()

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

    actualizar_tiempo()

    pantalla.fill((0,0,0))
    dibujar_tablero()
    dibujar_fichas()
    dibujar_mensaje()
    
    pygame.display.flip()

pygame.quit()
sys.exit()