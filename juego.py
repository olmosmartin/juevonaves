import pygame
from pygame.locals import *    
import random

pygame.init()
#------cambio de prueba
ancho = 800
alto = 600
cantidadEnemigos = 2
fin = False    
reloj = pygame.time.Clock()

pantalla = pygame.display.set_mode( (ancho, alto) )
pygame.key.set_repeat(1,25)
reloj = pygame.time.Clock()
#mi nave
imagenNave = pygame.image.load("nave.png")
rectanguloNave = imagenNave.get_rect()
rectanguloNave.left = ancho/2
rectanguloNave.top = 519
naveEstado=True
#---------------enemigo-sad--------------------------
imagenUfo=pygame.image.load("ufo.png")
rectangulosUfos={}
ufosEstado={}
velocidadesx={}
velocidadesy={}
for i in range(0,cantidadEnemigos+1):
    rectangulosUfos[i]=imagenUfo.get_rect()
    rectangulosUfos[i].left = random.randrange(0,720)
    rectangulosUfos[i].top = random.randrange(0,200)
    ufosEstado[i]=True
    velocidadesx[i]=3
    velocidadesy[i]=3
    #sonido
pygame.mixer.music.load('sonido.mp3')
pygame.mixer.music.play(2)
#----------------------------
#------------------------------------------------
#el disparo
imagenDisparo = pygame.image.load("disparo.png")    
rectanguloDisparo = imagenDisparo.get_rect()        
disparoEstado = False
#-----------------disparos enemigos------------------------
imagenDisparor = pygame.image.load("disparor.png")
rectangulosDisparors={}
disparorEstado={}
for i in range(0,cantidadEnemigos+1):
    rectangulosDisparors[i]=imagenDisparor.get_rect()
    disparorEstado[i]=False
#-------------------------------------------------

while not fin:                                     
    for event in pygame.event.get():                     
        if event.type == pygame.QUIT: fin = True
#botones de la nave
        keys = pygame.key.get_pressed()                 
    if keys[K_LEFT] and rectanguloNave.left > 0:                         
        rectanguloNave.left -= 4          
    if keys[K_RIGHT] and rectanguloNave.left < 700:                       
        rectanguloNave.left += 4       
    if keys[K_UP] and rectanguloNave.top > 0:
        rectanguloNave.top += -4
    if keys[K_DOWN] and rectanguloNave.top < 520:
        rectanguloNave.top += 4
#boton de disparo
    if keys[K_SPACE] and not disparoEstado and naveEstado:         
        disparoEstado = True                       
        rectanguloDisparo.left = rectanguloNave.left +23 
        rectanguloDisparo.top = rectanguloNave.top - 25  
#movimiento del enemigo
    for i in range(0,cantidadEnemigos+1):
        rectangulosUfos[i].left += velocidadesx[i]
        if rectangulosUfos[i].left < 0 or rectangulosUfos[i].right > ancho:
            velocidadesx[i] =- velocidadesx[i]
#movimiento disparo enemigo
        if not disparorEstado[i] and ufosEstado[i]:
            disparorEstado[i]=True
            rectangulosDisparors[i].left = rectangulosUfos[i].left +50
            rectangulosDisparors[i].top = rectangulosUfos[i].top +30

#movimiento disparo enemigo
    for i in range(0,cantidadEnemigos+1):
        if disparorEstado[i]:
            rectangulosDisparors[i].top += 6
            if rectangulosDisparors[i].top > 600:
                disparorEstado[i] = False
    
#movimiento del disparo
    if disparoEstado:                      
        rectanguloDisparo.top -= 6         
        if rectanguloDisparo.top <= 0:     
            disparoEstado = False          

#Comprobar colisiones (contra enemigo)
    for i in range(0,cantidadEnemigos+1):
        if naveEstado and disparoEstado and ufosEstado[i]:
            if rectanguloDisparo.colliderect( rectangulosUfos[i]):
                ufosEstado[i]=False
                disparoEstado=False

        if disparoEstado and ufosEstado[i]:
            if rectanguloDisparo.colliderect( rectangulosUfos[i]):
                ufosEstado[i]=False
                disparoEstado=False
    
    #probar colisiones del disparo enemigo contra mi nave
    for i in range(0,cantidadEnemigos+1):
        if naveEstado and disparorEstado[i]:
            if rectangulosDisparors[i].colliderect( rectanguloNave):
                naveEstado=False
    
    cantidadEnemigosActual=0
    for i in range(0,cantidadEnemigos+1):
        if ufosEstado[i]:
            cantidadEnemigosActual=cantidadEnemigosActual+1
    
    if cantidadEnemigosActual==0:
        fin = True

    
    pantalla.fill( (0,0,0) )
    if naveEstado:
        pantalla.blit(imagenNave, rectanguloNave)
    for i in range(0,cantidadEnemigos+1):
        if ufosEstado[i]:
            pantalla.blit(imagenUfo, rectangulosUfos[i])
#mientras el disparo no llega al final lo dibuja
    if disparoEstado:                      
        pantalla.blit(imagenDisparo, rectanguloDisparo)
#mientras no llega disparo enemigo lo dibuja
    for i in range(0,cantidadEnemigos+1):
        if disparorEstado[i]:                    
            pantalla.blit(imagenDisparor, rectangulosDisparors[i])
    pygame.display.flip()
    
    reloj.tick(60)

pygame.quit()
