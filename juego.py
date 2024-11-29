import pygame
import os
import random

pygame.init()

ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('RUBIO GALEANA SAUL')

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)

ruta_base = os.path.dirname(_file_)

def cargar_imagen(ruta, tamaño=None):
    imagen = pygame.image.load(ruta)
    if tamaño:
        imagen = pygame.transform.scale(imagen, tamaño)
    return imagen

imagenes = [
    os.path.join(ruta_base, "logo.jpg"),
    os.path.join(ruta_base, "imagen 1.jpg"),
    os.path.join(ruta_base, "imagen 2.jpg"),
    os.path.join(ruta_base, "imagen 3.jpg"),
    os.path.join(ruta_base, "imagen 4.jpg"),
    os.path.join(ruta_base, "imagen 5.jpg"),
    os.path.join(ruta_base, "imagen 6.jpg"),
    os.path.join(ruta_base, "imagen 7.jpg"),
]

carro_img = cargar_imagen(os.path.join(ruta_base, "carro.png"), (80, 80))
tanque_img = cargar_imagen(os.path.join(ruta_base, "tanque.jpg"), (100, 100))
panel_solar_img = cargar_imagen(os.path.join(ruta_base, "panel solar.jpg"), (60, 60))

archivo_perder = os.path.join(ruta_base, "imagen lose.jpg")
if os.path.exists(archivo_perder):
    perder_img = cargar_imagen(archivo_perder)
else:
    perder_img = None

reloj = pygame.time.Clock()

def mostrar_texto(texto, tamano, color, x, y):
    fuente = pygame.font.SysFont('Arial', tamano)
    texto = fuente.render(texto, True, color)
    ventana.blit(texto, (x, y))

class Jugador(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()
        self.image = carro_img
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO // 2
        self.rect.y = ALTO - 100
        self.velocidad = 10
        self.puntos = 0

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

    def recoger_panel_solar(self, paneles):
        colisiones = pygame.sprite.spritecollide(self, paneles, True)
        for panel in colisiones:
            self.puntos += 1

class ObjetoCaida(pygame.sprite.Sprite):
    def _init_(self, tipo):
        super()._init_()
        self.tipo = tipo
        if self.tipo == 'tanque':
            self.image = tanque_img
        elif self.tipo == 'panel':
            self.image = panel_solar_img

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-150, -50)

    def update(self):
        self.rect.y += 5
        if self.rect.top > ALTO:
            self.rect.y = random.randint(-150, -50)
            self.rect.x = random.randint(0, ANCHO - self.rect.width)

def mostrar_imagen_final(ruta_imagen):
    imagen = cargar_imagen(ruta_imagen)
    ventana.fill(BLANCO)
    ventana.blit(imagen, (0, 0))
    mostrar_texto("Presiona cualquier tecla para continuar", 30, NEGRO, 200, 500)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def nivel_2():
    panel_solar_pequeno = cargar_imagen(os.path.join(ruta_base, "panel solar.jpg"), (50, 50))
    tesi_pequeno = cargar_imagen(os.path.join(ruta_base, "tesi.jpg"), (200, 200))

    ventana.fill(BLANCO)

    paneles_pos = []
    for i in range(6):
        x = 100 + (i % 3) * 120
        y = 100 + (i // 3) * 120
        paneles_pos.append((x, y))

    for i, (x, y) in enumerate(paneles_pos):
        if i != 5:
            ventana.blit(panel_solar_pequeno, (x, y))

    ventana.blit(tesi_pequeno, (ANCHO // 2 - 100, ALTO // 2 - 100))

    mostrar_texto("¡Has llegado al nivel 2! Presiona cualquier tecla para continuar", 30, VERDE, 200, 500)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                esperando = False

def juego():
    jugador = Jugador()

    todos_los_sprites = pygame.sprite.Group()
    todos_los_sprites.add(jugador)

    paneles_solares = pygame.sprite.Group()
    tanques = pygame.sprite.Group()

    for i in range(5):
        panel = ObjetoCaida('panel')
        paneles_solares.add(panel)
        todos_los_sprites.add(panel)

    for i in range(3):
        tanque = ObjetoCaida('tanque')
        tanques.add(tanque)
        todos_los_sprites.add(tanque)

    en_juego = True
    while en_juego:
        ventana.fill(BLANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_juego = False

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        jugador.recoger_panel_solar(paneles_solares)

        if jugador.puntos >= 20:  
            ventana.fill(NEGRO)
            mostrar_texto("¡Felicidades! Has ganado el nivel 1", 40, VERDE, 200, 250)
            pygame.display.update()
            pygame.time.wait(2000)
            
            mostrar_imagen_final(os.path.join(ruta_base, "imagen 2_1.jpg"))
            
            mostrar_imagen_final(os.path.join(ruta_base, "imagen 2_2.jpg"))
            
            mostrar_imagen_final(os.path.join(ruta_base, "tesi.jpg"))
            
            mostrar_imagen_final(os.path.join(ruta_base, "imagen 2_3.jpg"))
            
            mostrar_imagen_final(os.path.join(ruta_base, "imagen 2_4.jpg"))
            
            nivel_2()
            break

        if pygame.sprite.spritecollide(jugador, tanques, False):
            if perder_img:
                ventana.blit(perder_img, (0, 0))
            mostrar_texto('¡Perdiste! Presiona Q para salir o R para reiniciar', 30, ROJO, 200, 300)
            pygame.display.update()
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        esperando = False
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_q:
                            en_juego = False
                            esperando = False
                        if evento.key == pygame.K_r:
                            juego()
                            esperando = False
            break

        if len(paneles_solares) < 5:
            panel = ObjetoCaida('panel')
            paneles_solares.add(panel)
            todos_los_sprites.add(panel)

        if len(tanques) < 3:
            tanque = ObjetoCaida('tanque')
            tanques.add(tanque)
            todos_los_sprites.add(tanque)

        todos_los_sprites.update()
        todos_los_sprites.draw(ventana)
        mostrar_texto(f'Paneles solares: {jugador.puntos}', 20, NEGRO, 650, 10)
        pygame.display.update()
        reloj.tick(30)

def pantalla_intro():
    imagen_index = 0
    while imagen_index < len(imagenes):
        ventana.fill(BLANCO)
        img = cargar_imagen(imagenes[imagen_index])
        ventana.blit(img, (0, 0))
        mostrar_texto("Presiona cualquier tecla para continuar", 30, NEGRO, 200, 500)
        pygame.display.update()
        
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    esperando = False
                    imagen_index += 1

pantalla_intro()
juego()
pygame.quit()
quit()