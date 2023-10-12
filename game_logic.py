import pygame
import logging
import os
import random
import sys

# Establece el directorio de trabajo al directorio del script actual
os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.DEBUG)

pygame.init()

# Configuración de pantalla
width, height = 1000, 750
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Mi juego')

# Obtén la ruta al directorio del script actual
script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


# Construyo la ruta completa al archivo players.png
start_png = os.path.join(script_dir, 'assets', 'sprites', 'menu', 'press-enter-text.png')
press_start_image = pygame.image.load(start_png)
press_start_image = pygame.transform.scale(press_start_image, (width, height))

has_ganado_jpg = os.path.join(script_dir, 'assets', 'sprites', 'messages', 'has_ganado.jpg')
has_perdido_png = os.path.join(script_dir, 'assets', 'sprites', 'messages', 'has_perdido.png')

has_ganado_image = pygame.image.load(has_ganado_jpg)
has_perdido_image = pygame.image.load(has_perdido_png)


# Tamaño de los movimientos
movement_distance = 5
# Variable para rastrear si el jugador está en movimiento o no
is_moving = False  


# Colores 
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


#se define clase para players
class Player:
    def __init__(self, x, y, health, image):
        self.pos = [x, y]
        self.image = image  # Cargar la imagen del jugador
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = health  # Puntos de vida del jugador

    def draw(self, screen):
        screen.blit(self.image, self.pos)  # Dibujar la imagen del jugador en la posición especificada
    def recibir_dano(self, cantidad_dano):
        self.health -= cantidad_dano

    def esta_vivo(self):
        return self.health > 0 
    
class Enemigo:
    def __init__(self, x, y, health, image):
        self.pos = [x, y]
        self.image = image  # Cargar la imagen del jugador
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = health  # Puntos de vida del jugador

    def draw(self, screen):
        screen.blit(self.image, self.pos)  # Dibujar la imagen del jugador en la posición especificada
    def recibir_dano(self, cantidad_dano):
        self.health -= cantidad_dano

    def esta_vivo(self):
        return self.health > 0  
    

# Definición de constantes
TIEMPO_ENTRE_BOLAS_DE_ENERGIA = 60  

#se define direccion
direction = ''


# Construyo la ruta completa al archivo players.png
player_png = os.path.join(script_dir, 'assets', 'sprites', 'players', 'players.png')


# Construyo la ruta completa al archivo enemies.png
enemies_png = os.path.join(script_dir, 'assets', 'sprites', 'enemies', 'enemies.png')

# Carga de imagenes
player_pygame = pygame.image.load(player_png)

# Carga de imagenes
enemies_pygame = pygame.image.load(enemies_png)
player = Player(100, 500, 100, player_pygame)

enemy = Enemigo(700, 500, 100, enemies_pygame)


# Construyo la ruta completa al archivo de musica
music_mp3 = os.path.join(script_dir, 'assets', 'sounds', 'heroic.mp3')
#carga de musica
pygame.mixer.music.load(music_mp3)
pygame.mixer.music.play(-1)

class BolaEnergia:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocidad = 3  # Velocidad de movimiento de la bola de energía

    def mover(self):
        self.rect.x -= self.velocidad  # Mover la bola de energía hacia la izquierda

    def dibujar(self, screen):
        pygame.draw.rect(screen, RED, self.rect)  # Dibujar la bola de energía en la pantalla

lista_de_bolas_de_energia = []  # Lista para almacenar las bolas de energía del enemigo

tiempo_para_crear_nueva_bola_de_energia = TIEMPO_ENTRE_BOLAS_DE_ENERGIA

bola_energia = None

# Función para verificar la colisión del Kamehameha con el enemigo
def colision_kamehameha_enemigo(enemigo_rect, kamehameha_rect):
    return enemigo_rect.colliderect(kamehameha_rect)

# Función para verificar la colisión de la bola de energía del enemigo con el jugador
def colision_bola_energia_jugador(player_rect, bola_energia_rect):
    return player_rect.colliderect(bola_energia_rect)

# Carga de background y escala al tamaño de la pantalla
background = os.path.join(script_dir, 'assets', 'sprites', 'background', 'middleground.png')
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
    initial_x, initial_y = player.pos[0], player.pos[1]
    is_moving = True  # Inicia el movimiento al presionar una tecla

# Variable para rastrear si el juego ha comenzado o no
juego_iniciado = False

# Bucle principal
running = True
running = True
juego_iniciado = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not juego_iniciado:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    juego_iniciado = True  # Comienza el juego cuando se presiona Enter
                    
            else:
                # Resto del código para manejar eventos mientras el juego está en curso
                if not is_moving:
                    is_moving = True
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

    if not juego_iniciado:
        screen.blit(press_start_image, ((width - press_start_image.get_width()) // 2, (height - press_start_image.get_height()) // 2))
    else :
            # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()

        # Mover el jugador hacia la izquierda
        if keys[pygame.K_LEFT] and player.pos[0] > 0:
            player.pos[0] -= movement_distance

        # Mover el jugador hacia la derecha
        if keys[pygame.K_RIGHT] and player.pos[0] < width - player_pygame.get_width():
            player.pos[0] += movement_distance

                # Verifica si el jugador ha alcanzado la distancia especificada
            if abs(player.pos[0] - initial_x) >= movement_distance or abs(player.pos[1] - initial_y) >= movement_distance:
                is_moving = False  # Detiene el movimiento cuando se alcanza la distancia especificada
        
        if keys[pygame.K_SPACE]:
                kamehameha_active = True

        # Lógica del juego y dibujar pantalla
        screen.fill(WHITE)  # Llenar la pantalla con color blanco
        # Dibujar fondo primero
        screen.blit(background_image, (0, 0))

        # Dibujar jugador encima del fondo
        # screen.blit(player_pygame, player_pos)
        player.draw(screen)
        enemy.draw(screen)

        # Actualizar posición del Kamehameha
        if kamehameha_active:
            kamehameha_rect.x += kamehameha_speed

            # Desactivar el Kamehameha cuando sale de la pantalla
            if kamehameha_rect.left > width:
                kamehameha_active = False
                kamehameha_rect.x = player.rect.right        

        # Verificar colisión del Kamehameha con el enemigo
        if kamehameha_active and colision_kamehameha_enemigo(enemy.rect, kamehameha_rect):
            enemy.recibir_dano(1)
            kamehameha_active = False  # Desactivar el Kamehameha después de la colisión

        if kamehameha_active:
            pygame.draw.rect(screen, kamehameha_color, kamehameha_rect)

        # Mover y dibujar las bolas de energía del enemigo
        for bola_energia in lista_de_bolas_de_energia:
            bola_energia.mover()  # Mueve la bola de energía hacia la izquierda
            bola_energia.dibujar(screen)  # Dibuja la bola de energía en la pantalla

        if tiempo_para_crear_nueva_bola_de_energia == 0:
            nueva_bola = BolaEnergia(width, random.randint(0, height), 20, 20)  # Crea una nueva bola de energía
            lista_de_bolas_de_energia.append(nueva_bola)  # Agrega la bola de energía a la lista
            tiempo_para_crear_nueva_bola_de_energia = TIEMPO_ENTRE_BOLAS_DE_ENERGIA  # Reinicia el temporizador
        else:
            tiempo_para_crear_nueva_bola_de_energia -= 1  # Reduce el temporizador en cada frame

        # Verificar colisión de la bola de energía del enemigo con el jugador
        for b in lista_de_bolas_de_energia:
            if b.rect.colliderect(player.rect):
                player.recibir_dano(10)
                lista_de_bolas_de_energia.remove(b)  # Elimina la bola de energía después de la colisión
                bola_energia = b  # Asigna la bola de energía actual a la variable bola_energia

        if bola_energia is not None:
            if colision_bola_energia_jugador(player.rect, bola_energia.rect):
                player.recibir_dano(10)  # Reducir la salud del jugador en 10 puntos
    
        # Verificar si el enemigo ha perdido toda su vida
        if not enemy.esta_vivo():
            screen.blit(has_ganado_image, ((width - has_ganado_image.get_width()) // 2, (height - has_ganado_image.get_height()) // 2))
            pygame.display.flip()  # Actualizar la pantalla para mostrar el mensaje
            pygame.time.delay(2000)  # Esperar 2 segundos antes de salir del juego (2000 milisegundos)
            pygame.mixer.music.stop()
            running = False  # Salir del bucle principal y cerrar el juego

        # Verificar si el jugador ha perdido toda su vida
        if not player.esta_vivo():
            screen.blit(has_perdido_image, ((width - has_perdido_image.get_width()) // 2, (height - has_perdido_image.get_height()) // 2))
            pygame.display.flip()  # Actualizar la pantalla para mostrar el mensaje
            pygame.time.delay(2000)  # Esperar 2 segundos antes de salir del juego (2000 milisegundos)
            pygame.mixer.music.stop()
            running = False  # Salir del bucle principal y cerrar el juego


    pygame.display.flip()


pygame.display.quit()