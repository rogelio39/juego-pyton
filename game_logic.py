import pygame
import logging
import os

logging.basicConfig(level=logging.DEBUG)

pygame.init()

# Configuración de pantalla
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mi juego')

# Tamaño de los movimientos
movement_distance = 5

#coordenadas iniciales del jugador

# Coordenadas del jugador
player_pos = [100, 500]

# Variable para rastrear si el jugador está en movimiento o no
is_moving = False  


# Colores 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


#se define clase para player
class Player:
    def __init__(self, x, y, image):
        self.pos = [x, y]
        self.image = image  # Cargar la imagen del jugador
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100  # Puntos de vida del jugador

    def draw(self, screen):
        screen.blit(self.image, self.pos)  # Dibujar la imagen del jugador en la posición especificada

#se define direccion
direction = ''

# Obtengo la ruta al directorio actual del script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construyo la ruta completa al archivo players.png
player_png = os.path.join(current_dir, 'assets', 'sprites', 'players', 'players.png')

# Carga de imagenes
player_pygame = pygame.image.load(player_png)

player = Player(100, 500, player_pygame)

# Carga de background y escala al tamaño de la pantalla
background = os.path.join(current_dir, 'assets', 'sprites', 'background', 'middleground.png')
background_image = pygame.image.load(background)
background_image = pygame.transform.scale(background_image, (width, height))



# Variables del ataque
# Variables del ataque
kamehameha_size = 50  # Tamaño del Kamehameha (ancho y altura son iguales para hacerlo cuadrado)
kamehameha_color = BLUE
kamehameha_speed = 5
# kamehameha_rect es un cuadrado con el mismo ancho y altura
kamehameha_rect = pygame.Rect(player.rect.right, player.rect.centery - kamehameha_size // 2, kamehameha_size, kamehameha_size)

kamehameha_active = False


    # Obtener las coordenadas iniciales cuando el jugador comienza a moverse
if not is_moving:
    initial_x, initial_y = player_pos[0], player_pos[1]
    is_moving = True  # Inicia el movimiento al presionar una tecla

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not is_moving:  # Comprueba si el jugador no está en movimiento
                is_moving = True  # Inicia el movimiento al presionar una tecla
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

        # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover el jugador hacia la izquierda
    if keys[pygame.K_LEFT] and player.pos[0] > 0:
        player.pos[0] -= movement_distance

    # Mover el jugador hacia la derecha
    if keys[pygame.K_RIGHT] and player.pos[0] < width - player_pygame.get_width():
        player.pos[0] += movement_distance

            # Verifica si el jugador ha alcanzado la distancia especificada
        if abs(player_pos[0] - initial_x) >= movement_distance or abs(player_pos[1] - initial_y) >= movement_distance:
            is_moving = False  # Detiene el movimiento cuando se alcanza la distancia especificada
    if keys[pygame.K_SPACE]:
            kamehameha_active = True

    # Actualizar posición del Kamehameha
    if kamehameha_active:
        kamehameha_rect.x += kamehameha_speed

        # Desactivar el Kamehameha cuando sale de la pantalla
        if kamehameha_rect.left > width:
            kamehameha_active = False
            kamehameha_rect.x = player.rect.right        

    # Lógica del juego y dibujar pantalla
    screen.fill(WHITE)  # Llenar la pantalla con color blanco

    # Dibujar fondo primero
    screen.blit(background_image, (0, 0))

    # Dibujar jugador encima del fondo
    # screen.blit(player_pygame, player_pos)
    player.draw(screen)
    
    if kamehameha_active:
        pygame.draw.rect(screen, kamehameha_color, kamehameha_rect)



    pygame.display.flip()


pygame.display.quit()