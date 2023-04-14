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

# Crear botones
button_si = pygame.Rect((WIDTH- 2 * BOTTON_WIDTH)/3, 6/10*HEIGHT, BOTTON_WIDTH, BUTTON_HEIGHT)
button_no = pygame.Rect((WIDTH- 2 * BOTTON_WIDTH)/3*2+BOTTON_WIDTH, 6/10*HEIGHT, BOTTON_WIDTH, BUTTON_HEIGHT)

# Definir el tablero
board = [['', '', ''], ['', '', ''], ['', '', '']]

player = 'X'
playing = True

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
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, (255, 255, 255))
    x = (WIDTH - text.get_width()) // 2
    y = (HEIGHT - text.get_height()) // 2
    screen.blit(text, (x, y))
    pygame.display.update()

# Dibuja botones y texto de rematch
def draw_rematch(message):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, (255, 255, 255))
    x = (WIDTH - text.get_width()) // 2
    y = (HEIGHT/2 - text.get_height()) // 2
    screen.blit(text, (x, y))

    font = pygame.font.Font(None, 36)


    text_si = font.render("Sí", True, BLACK)

    pygame.draw.rect(screen, GREEN, button_si, 0)
    pygame.draw.rect(screen, DARK_GREEN, button_si, 4)
    screen.blit(text_si, (button_si.x + ((BOTTON_WIDTH - text_si.get_width())/2), button_si.y + ((BUTTON_HEIGHT - text_si.get_height())/2)))


    text_no = font.render("No", True, BLACK)

    pygame.draw.rect(screen, RED, button_no, 0)
    pygame.draw.rect(screen, DARK_RED, button_no, 4)
    screen.blit(text_no, (button_no.x + ((BOTTON_WIDTH - text_no.get_width())/2), button_no.y + ((BUTTON_HEIGHT - text_no.get_height())/2)))

    pygame.display.update()

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
    # Fin del bucle principal
    pygame.quit()
    sys.exit()

# Ejecutar el juego
mainGame()
