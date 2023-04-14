import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir constantes
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

COLOR_LINE = (23, 145, 135)
WHITE = (255, 255, 255)
GREEN = (36, 216, 126)
DARK_GREEN = (28, 166, 97)
RED = (232, 90, 45)
DARK_RED = (188, 72, 35)
BLACK = (0, 0, 0)

BOTTON_WIDTH = 1/7*WIDTH
BUTTON_HEIGHT = 1/10*HEIGHT

# Crear la ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3 en raya")

# Definir el tablero
board = [['', '', ''], ['', '', ''], ['', '', '']]

player = 'X'
playing = True
rematch = True

# Para limpiar el tablero
def cleanBoard():
    global player
    global playing
    global board

    board = [['', '', ''], ['', '', ''], ['', '', '']]
    player = 'X'
    playing = True


# Dibujar el tablero
def draw_board():
    screen.fill((0, 0, 0))
    # Líneas horizontales
    pygame.draw.line(screen, COLOR_LINE, (0, 200), (600, 200), LINE_WIDTH)
    pygame.draw.line(screen, COLOR_LINE, (0, 400), (600, 400), LINE_WIDTH)
    # Líneas verticales
    pygame.draw.line(screen, COLOR_LINE, (200, 0), (200, 600), LINE_WIDTH)
    pygame.draw.line(screen, COLOR_LINE, (400, 0), (400, 600), LINE_WIDTH)
    # Dibujar los círculos y las cruces
    for row in range(3):
        for column in range(3):
            if board[row][column] == 'O':
                pygame.draw.circle(screen, WHITE, (column * 200 + 100, row * 200 + 100), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][column] == 'X':
                pygame.draw.line(screen, WHITE, (column * 200 + 50, row * 200 + 50), (column * 200 + 150, row * 200 + 150), CROSS_WIDTH)
                pygame.draw.line(screen, WHITE, (column * 200 + 150, row * 200 + 50), (column * 200 + 50, row * 200 + 150), CROSS_WIDTH)
    pygame.display.update()

# Dibuja un mensjae en el tablero
def draw_message(message):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, WHITE)
    x = (WIDTH - text.get_width()) // 2
    y = (HEIGHT - text.get_height()) // 2
    screen.blit(text, (x, y))
    pygame.display.update()

def draw_button(message, message_color, x, y, width, height, button_color, border_color=None):

    button = pygame.Rect((x, y, width, height))

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, message_color)

    pygame.draw.rect(screen, button_color, button, 0)

    if border_color is not None:
        pygame.draw.rect(screen, border_color, button, 4)

    screen.blit(text, (button.x + ((width - text.get_width())/2), button.y + ((height - text.get_height())/2)))

    return button

# Dibuja botones y texto de rematch
def draw_rematch(message):

    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, WHITE)
    x = (WIDTH - text.get_width()) // 2
    y = (HEIGHT/2 - text.get_height()) // 2
    screen.blit(text, (x, y))

    # Crear botones
    button_si = draw_button("Sí", BLACK, (WIDTH- 2 * BOTTON_WIDTH)/3, 6/10*HEIGHT, BOTTON_WIDTH, BUTTON_HEIGHT, GREEN, DARK_GREEN)
    button_no = draw_button("No", BLACK, (WIDTH- 2 * BOTTON_WIDTH)/3*2+BOTTON_WIDTH, 6/10*HEIGHT, BOTTON_WIDTH, BUTTON_HEIGHT, RED, DARK_RED)

    pygame.display.update()

    rematch_logic(button_si, button_no)

    

def rematch_logic(button_si, button_no):
    global playing
    global rematch

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # detectar si se hizo clic en el botón
            if button_si.collidepoint(event.pos):
                cleanBoard()
                playing = True
                rematch = False
                break
            elif button_no.collidepoint(event.pos):
                sys.exit()
                break
        elif event.type == pygame.KEYDOWN:
            if event.unicode.lower() == 's':
                cleanBoard()
                playing = True
                rematch = False
                break
            elif event.unicode.lower() == 'n':
                sys.exit()
                break
        elif event.type == pygame.QUIT:
            sys.exit()


# Definir la función para verificar si alguien ganó
def verify_winner(player):
    # Verificar las filas
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True
    # Verificar las columnas
    for column in range(3):
        if board[0][column] == player and board[1][column] == player and board[2][column] == player:
            return True
    # Verificar las diagonales
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

# Definir la función para verificar si hay un empate
def verify_tie():
    for row in range(3):
        for column in range(3):
            if board[row][column] == '':
                return False
    return True


# Definir la función principal del juego
def mainGame():
    global playing
    global player
    global board
    global rematch

    # Bucle principal del juego
    while playing:

        rematch = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                column = position[0] // 200
                row = position[1] // 200
                if board[row][column] == '':
                    board[row][column] = player
                    if player == 'X':
                        player = 'O'
                    else:
                        player = 'X'

            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_r:
                    cleanBoard()
            
        
        draw_board()

        # Verificar si alguien ganó
        for actual_player in ['X', 'O']:
            if verify_winner(actual_player):
                print(actual_player + ' ganó.')
                draw_message(actual_player + ' ganó.')
                playing = False
            elif verify_tie():
                print('Ha habido un empate.')
                draw_message('Ha habido un empate.')
                playing = False
                break
        if not playing:
            pygame.time.wait(1000)
            while rematch:
                draw_rematch('¿Quieres jugar de nuevo?')
    # Fin del bucle principal
    pygame.quit()
    sys.exit()

# Ejecutar el juego
mainGame()
