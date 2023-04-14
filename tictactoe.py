import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir constantes
ANCHO = 600
ALTO = 600
LINEA_ANCHO = 15
LINEA_COLOR = (23, 145, 135)
CIRCULO_RADIO = 60
CIRCULO_ANCHO = 15
CIRCULO_COLOR = (255, 255, 255)
CRUZ_ANCHO = 25
CRUZ_COLOR = (255, 255, 255)
GREEN = (36, 216, 126)
DARK_GREEN = (28, 166, 97)
RED = (232, 90, 45)
DARK_RED = (188, 72, 35)
BLACK = (0, 0, 0)

ANCHO_BOTON = 1/7*ANCHO
ALTO_BOTON = 1/10*ALTO

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("3 en raya")

# Crear botones
button_si = pygame.Rect((ANCHO- 2 * ANCHO_BOTON)/3, 6/10*ALTO, ANCHO_BOTON, ALTO_BOTON)
button_no = pygame.Rect((ANCHO- 2 * ANCHO_BOTON)/3*2+ANCHO_BOTON, 6/10*ALTO, ANCHO_BOTON, ALTO_BOTON)

# Definir el tablero
tablero = [['', '', ''], ['', '', ''], ['', '', '']]

jugador = 'X'
jugando = True

# Para limpiar el tablero
def limpiarTablero():
    global jugador
    global jugando
    global tablero

    tablero = [['', '', ''], ['', '', ''], ['', '', '']]
    jugador = 'X'
    jugando = True


# Dibujar el tablero
def dibujar_tablero():
    pantalla.fill((0, 0, 0))
    # Líneas horizontales
    pygame.draw.line(pantalla, LINEA_COLOR, (0, 200), (600, 200), LINEA_ANCHO)
    pygame.draw.line(pantalla, LINEA_COLOR, (0, 400), (600, 400), LINEA_ANCHO)
    # Líneas verticales
    pygame.draw.line(pantalla, LINEA_COLOR, (200, 0), (200, 600), LINEA_ANCHO)
    pygame.draw.line(pantalla, LINEA_COLOR, (400, 0), (400, 600), LINEA_ANCHO)
    # Dibujar los círculos y las cruces
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == 'O':
                pygame.draw.circle(pantalla, CIRCULO_COLOR, (columna * 200 + 100, fila * 200 + 100), CIRCULO_RADIO, CIRCULO_ANCHO)
            elif tablero[fila][columna] == 'X':
                pygame.draw.line(pantalla, CRUZ_COLOR, (columna * 200 + 50, fila * 200 + 50), (columna * 200 + 150, fila * 200 + 150), CRUZ_ANCHO)
                pygame.draw.line(pantalla, CRUZ_COLOR, (columna * 200 + 150, fila * 200 + 50), (columna * 200 + 50, fila * 200 + 150), CRUZ_ANCHO)
    pygame.display.update()

# Dibuja un mensjae en el tablero
def dibujar_mensaje(mensaje):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render(mensaje, True, (255, 255, 255))
    x = (ANCHO - texto.get_width()) // 2
    y = (ALTO - texto.get_height()) // 2
    pantalla.blit(texto, (x, y))
    pygame.display.update()

# Dibuja botones y texto de revancha
def dibujar_revancha(mensaje):
    pantalla.fill((0, 0, 0))
    fuente = pygame.font.SysFont(None, 50)
    texto = fuente.render(mensaje, True, (255, 255, 255))
    x = (ANCHO - texto.get_width()) // 2
    y = (ALTO/2 - texto.get_height()) // 2
    pantalla.blit(texto, (x, y))

    font = pygame.font.Font(None, 36)


    text_si = font.render("Sí", True, BLACK)

    pygame.draw.rect(pantalla, GREEN, button_si, 0)
    pygame.draw.rect(pantalla, DARK_GREEN, button_si, 4)
    pantalla.blit(text_si, (button_si.x + ((ANCHO_BOTON - text_si.get_width())/2), button_si.y + ((ALTO_BOTON - text_si.get_height())/2)))


    text_no = font.render("No", True, BLACK)

    pygame.draw.rect(pantalla, RED, button_no, 0)
    pygame.draw.rect(pantalla, DARK_RED, button_no, 4)
    pantalla.blit(text_no, (button_no.x + ((ANCHO_BOTON - text_no.get_width())/2), button_no.y + ((ALTO_BOTON - text_no.get_height())/2)))

    pygame.display.update()

# Definir la función para verificar si alguien ganó
def verificar_ganador(jugador):
    # Verificar las filas
    for fila in range(3):
        if tablero[fila][0] == jugador and tablero[fila][1] == jugador and tablero[fila][2] == jugador:
            return True
    # Verificar las columnas
    for columna in range(3):
        if tablero[0][columna] == jugador and tablero[1][columna] == jugador and tablero[2][columna] == jugador:
            return True
    # Verificar las diagonales
    if tablero[0][0] == jugador and tablero[1][1] == jugador and tablero[2][2] == jugador:
        return True
    if tablero[0][2] == jugador and tablero[1][1] == jugador and tablero[2][0] == jugador:
        return True
    return False

# Definir la función para verificar si hay un empate
def verificar_empate():
    for fila in range(3):
        for columna in range(3):
            if tablero[fila][columna] == '':
                return False
    return True

def mejor_jugada(tablero, jugador):
    mejor_valor = -1000
    mejor_jugada = (-1, -1)
    
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                tablero[i][j] = jugador
                valor = minimax(tablero, jugador)
                tablero[i][j] = " "
                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_jugada = (i, j)
    
    return mejor_jugada

def ganador(tablero, jugador):
    # Comprobamos líneas horizontales
    for i in range(3):
        if tablero[i][0] == jugador and tablero[i][1] == jugador and tablero[i][2] == jugador:
            return True
    
    # Comprobamos líneas verticales
    for j in range(3):
        if tablero[0][j] == jugador and tablero[1][j] == jugador and tablero[2][j] == jugador:
            return True
    
    # Comprobamos diagonales
    if tablero[0][0] == jugador and tablero[1][1] == jugador and tablero[2][2] == jugador:
        return True
    
    if tablero[0][2] == jugador and tablero[1][1] == jugador and tablero[2][0] == jugador:
        return True
    
    return False

def empate(tablero):
    for i in range(3):
        for j in range(3):
            if tablero[i][j] == " ":
                return False
    return not ganador(tablero, "X") and not ganador(tablero, "O")



def minimax(tablero, jugador):
    if ganador(tablero, "X"):
        return -10
    if ganador(tablero, "O"):
        return 10
    if empate(tablero):
        return 0
    
    if jugador == "O":
        mejor_valor = -1000
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = jugador
                    valor = minimax(tablero, "X")
                    tablero[i][j] = " "
                    mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    
    else:
        mejor_valor = 1000
        for i in range(3):
            for j in range(3):
                if tablero[i][j] == " ":
                    tablero[i][j] = jugador
                    valor = minimax(tablero, "O")
                    tablero[i][j] = " "
                    mejor_valor = min(mejor_valor, valor)
        return mejor_valor

# Definir la función principal del juego
def juego():
    global jugando
    global jugador
    global tablero

    # Bucle principal del juego
    while jugando:
        revancha = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicion = pygame.mouse.get_pos()
                columna = posicion[0] // 200
                fila = posicion[1] // 200
                if tablero[fila][columna] == '':
                    tablero[fila][columna] = jugador
                    if jugador == 'X':
                        jugador = 'O'
                    else:
                        jugador = 'X'
                    print(mejor_jugada(tablero, jugador))

            elif evento.type == pygame.KEYDOWN:
                
                if evento.key == pygame.K_r:
                    limpiarTablero()
            
        
        dibujar_tablero()

        # Verificar si alguien ganó
        for jugador_actual in ['X', 'O']:
            if verificar_ganador(jugador_actual):
                print(jugador_actual + ' ganó.')
                dibujar_mensaje(jugador_actual + ' ganó.')
                jugando = False
            elif verificar_empate():
                print('Ha habido un empate.')
                dibujar_mensaje('Ha habido un empate.')
                jugando = False
                break
        if not jugando:
            pygame.time.wait(1000)
            while revancha:
                dibujar_revancha('¿Quieres jugar de nuevo?')
                for evento in pygame.event.get():
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        # detectar si se hizo clic en el botón
                        if button_si.collidepoint(evento.pos):
                            limpiarTablero()
                            jugando = True
                            revancha = False
                            break
                        elif button_no.collidepoint(evento.pos):
                            sys.exit()
                            break
                    elif evento.type == pygame.KEYDOWN:
                        if evento.unicode.lower() == 's':
                            limpiarTablero()
                            jugando = True
                            revancha = False
                            break
                        elif evento.unicode.lower() == 'n':
                            sys.exit()
                            break
                    elif evento.type == pygame.QUIT:
                        sys.exit()
    # Fin del bucle principal
    pygame.quit()
    sys.exit()

# Ejecutar el juego
juego()