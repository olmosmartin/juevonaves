import pygame
from pygame.locals import *    
import random

pygame.init()
#------cambio de prueba
ancho = 800
alto = 600
cantidadEnemigos = 3

reloj = pygame.time.Clock()

pantalla = pygame.display.set_mode( (ancho, alto) )
pygame.key.set_repeat(1,25)
reloj = pygame.time.Clock()
#mi nave
imagenNave = pygame.image.load("nave.png")
rectanguloNave = imagenNave.get_rect()
#-------------------estrella de la muerte nave y disparo---------------
imagenNaveMuerte = pygame.image.load("estrelladelamuerte.jpg")#estrella de la muerte
rectanguloNaveMuerte = imagenNaveMuerte.get_rect()#estrella de la muerte

imagenDisparoMuerte = pygame.image.load("disparodelamuerte.jpg")#estrella de la muerte(disparo)
rectanguloDisparoMuerte = imagenDisparoMuerte.get_rect()#estrella de la muerte(disparo)

#---------------enemigo-sad--------------------------
imagenUfo=pygame.image.load("ufo.png")
rectangulosUfos={}
ufosEstado={}
velocidadesx={}
velocidadesy={}

#------------------------------------------------
#el disparo
imagenDisparo = pygame.image.load("disparo.png")    
rectanguloDisparo = imagenDisparo.get_rect()

#-----------------disparos enemigos------------------------
imagenDisparor = pygame.image.load("disparor.png")
rectangulosDisparors={}
disparorEstado={}

#----------------pantalla de inicio--------------------------
imagenPresent = pygame.image.load("inicio.jpg")
rectanguloPresent = imagenPresent.get_rect()
rectanguloPresent.top = 0
rectanguloPresent.left = 0

letra30 = pygame.font.SysFont("Arial", 30)
imagenTextoPresent = letra30.render('espacio para jugar',True, (200,200,200), (0,0,0) )
rectanguloTextoPresent = imagenTextoPresent.get_rect()
rectanguloTextoPresent.centerx = pantalla.get_rect().centerx
rectanguloTextoPresent.centery = 520
#-------------------------------------------------

partidaEnMarcha = True

while partidaEnMarcha:
    pygame.mixer.music.load('sonido.mp3')
    pygame.mixer.music.play(2)
#inicio
    pantalla.fill( (0,0,0) )
    pantalla.blit(imagenPresent, rectanguloPresent)
    pantalla.blit(imagenTextoPresent, rectanguloTextoPresent)
    pygame.display.flip()
    nivel=1

    entrarAlJuego = False
    while not entrarAlJuego:
        pygame.time.wait(100)
        for event in pygame.event.get(KEYUP):
            if event.key == K_SPACE:
                entrarAlJuego = True

#comienza una partida
    puntos=0;
    rectanguloNave.left = ancho/2
    rectanguloNave.top = alto-50
    velocidadEnemigo=2
    velocidadDisparoMuerte = 8#nuevo para estrella de la muerte
    velocidadDisparor = 6#nuevo para velocidad

    #--------------opciones de estrella de la muerte-----------------------------
    velocidadMuerte= 4
    rectanguloNaveMuerte.left = ancho/2
    rectanguloNaveMuerte.top = 50
    disparoMuerteEstado=False
    estrellaMuerteVisible=True
    rectanguloDisparoMuerte=imagenDisparoMuerte.get_rect()

    for i in range(0,cantidadEnemigos+1):
        rectangulosUfos[i]=imagenUfo.get_rect()
        rectangulosUfos[i].left = random.randrange(0,720)
        rectangulosUfos[i].top = random.randrange(0,200)
        ufosEstado[i]=True
        velocidadesx[i]=velocidadEnemigo
        velocidadesy[i]=velocidadEnemigo

    for i in range(0,cantidadEnemigos+1):
        rectangulosDisparors[i]=imagenDisparor.get_rect()
        disparorEstado[i]=False

    disparoEstado = False
    terminado = False

    while not terminado:
# prueba respuesta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminado = True
                partidaEnMarcha = False
        #botones de nave
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and rectanguloNave.left > 0:
            rectanguloNave.left -= 4
        if keys[K_RIGHT] and rectanguloNave.left < 700:
            rectanguloNave.left += 4
        if keys[K_UP] and rectanguloNave.top > 0:
            rectanguloNave.top += -4
        if keys[K_DOWN] and rectanguloNave.top < 520:
            rectanguloNave.top += 4
        if keys[K_SPACE] and not disparoEstado:
            disparoEstado = True
            if disparoEstado:
                sonido = pygame.mixer.Sound("sonidoDisparos.wav") #sonido!!!!!!!
                sonido.play() #sonido!!!!!!!
            rectanguloDisparo.left = rectanguloNave.left + 18
            rectanguloDisparo.top = rectanguloNave.top - 25


        #----------------------movimientos de estrella de la muerte(tambien disparo)--------------
        rectanguloNaveMuerte.left += velocidadMuerte
        if rectanguloNaveMuerte.left < 0 or rectanguloNaveMuerte.right > ancho:
            velocidadMuerte = -velocidadMuerte

        if not disparoMuerteEstado and estrellaMuerteVisible:
            disparoMuerteEstado=True
            sonido = pygame.mixer.Sound("sonidoDisparos.wav") #sonido!!!!!!!
            sonido.play() #sonido!!!!!!!
            rectanguloDisparoMuerte.left = rectanguloNaveMuerte.left +50
            rectanguloDisparoMuerte.top = rectanguloNaveMuerte.top +30

        if disparoMuerteEstado:
            rectanguloDisparoMuerte.top += velocidadDisparoMuerte
            if rectanguloDisparoMuerte.top > 600:
                disparoMuerteEstado = False


#movimiento del enemigo
        for i in range(0,cantidadEnemigos+1):
            rectangulosUfos[i].left += velocidadesx[i]
            if rectangulosUfos[i].left < 0 or rectangulosUfos[i].right > ancho:
                velocidadesx[i] =- velocidadesx[i]
    #movimiento disparo enemigo
            if not disparorEstado[i] and ufosEstado[i]:
                disparorEstado[i]=True
                sonido = pygame.mixer.Sound("sonidoDisparos.wav") #sonido!!!!!!!
                sonido.play() #sonido!!!!!!!
                rectangulosDisparors[i].left = rectangulosUfos[i].left +50
                rectangulosDisparors[i].top = rectangulosUfos[i].top +30

    #movimiento disparo enemigo
        for i in range(0,cantidadEnemigos+1):
            if disparorEstado[i]:
                rectangulosDisparors[i].top += velocidadDisparor
                if rectangulosDisparors[i].top > 600:
                    disparorEstado[i] = False

    #movimiento del disparo
        if disparoEstado:
            rectanguloDisparo.top -= 6
            if rectanguloDisparo.top <= 0:
                disparoEstado = False

    #Comprobar colisiones (contra enemigo)
        for i in range(0,cantidadEnemigos+1):
            if ufosEstado[i]:
                if rectanguloNave.colliderect( rectangulosUfos[i]):
                    terminado=True

                if disparoEstado:
                    if rectanguloDisparo.colliderect( rectangulosUfos[i]):
                        ufosEstado[i]=False
                        sonido = pygame.mixer.Sound("explode.wav") #sonido!!!!!!!
                        sonido.play() #sonido!!!!!!!
                        puntos+=10
                        disparoEstado=False

        #probar colisiones del disparo enemigo contra mi nave
        for i in range(0,cantidadEnemigos+1):
            if disparorEstado[i]:
                if rectangulosDisparors[i].colliderect( rectanguloNave):
                    sonido = pygame.mixer.Sound("explode.wav") #sonido!!!!!!!
                    sonido.play() #sonido!!!!!!!
                    terminado=True

        #-----------prueba coliciones estrella de la muerte(tambien disparo)-----------------------
        if disparoMuerteEstado:
            if rectanguloDisparoMuerte.colliderect( rectanguloNave):
                sonido = pygame.mixer.Sound("explode.wav") #sonido!!!!!!!
                sonido.play() #sonido!!!!!!!
                terminado=True

            if disparoEstado:
                if rectanguloDisparo.colliderect( rectanguloNaveMuerte) :
                    estrellaMuerteVisible = False
                    sonido = pygame.mixer.Sound("explode.wav") #sonido!!!!!!!
                    sonido.play() #sonido!!!!!!!
                    disparoEstado = False
                    puntos+=30

        if disparoMuerteEstado:
            if rectanguloDisparoMuerte.colliderect( rectanguloNave):
                sonido = pygame.mixer.Sound("explode.wav") #sonido!!!!!!!
                sonido.play() #sonido!!!!!!!
                terminado=True


        cantidadEnemigosActual=0
        for i in range(0,cantidadEnemigos+1):
            if ufosEstado[i]:
                cantidadEnemigosActual=cantidadEnemigosActual+1
        #--------------control de niveles---------------------------------
        if cantidadEnemigosActual==0 and not estrellaMuerteVisible:
            nivel=nivel+1
            estrellaMuerteVisible=True
            velocidadDisparoMuerte += 1
            velocidadDisparor += 1

            if(velocidadMuerte<0):
                velocidadMuerte=velocidadMuerte-1
            if(velocidadMuerte>0):
                velocidadMuerte=velocidadMuerte+1

            for i in range(0,cantidadEnemigos+1):
                ufosEstado[i]=True
                #incrementa velocidad por nivel
                if(velocidadesx[i]<0):
                    velocidadesx[i]=velocidadesx[i]-1
                if(velocidadesx[i]>0):
                    velocidadesx[i]=velocidadesx[i]+1

        #------------dibujos en pantalla----------------------------
        pantalla.fill( (0,0,0) )
        imagenEstrellas = pygame.image.load("estrellas2.jpg")
        rectanguloEstrellas = imagenEstrellas.get_rect()
        rectanguloEstrellas.top = 0
        rectanguloEstrellas.left = 0
        pantalla.blit(imagenEstrellas, rectanguloEstrellas)
        for i in range(0,cantidadEnemigos+1):
            if ufosEstado[i]:
                pantalla.blit(imagenUfo, rectangulosUfos[i])
        if disparoEstado:
            pantalla.blit(imagenDisparo, rectanguloDisparo)
        pantalla.blit(imagenNave, rectanguloNave)

        #dibuja disparo de la muerte y estrella de la muerte--------
        if disparoMuerteEstado:
            pantalla.blit(imagenDisparoMuerte, rectanguloDisparoMuerte)

        if estrellaMuerteVisible:
            pantalla.blit(imagenNaveMuerte, rectanguloNaveMuerte)

        for i in range(0,cantidadEnemigos+1):
                if disparorEstado[i]:
                    pantalla.blit(imagenDisparor, rectangulosDisparors[i])
        #----------------------pantalla game over-------------------------
                    
        if terminado==True:
            pantalla.fill( (0,0,0) )
            imagenFin = pygame.image.load("gameover.jpg")
            rectanguloFin = imagenFin.get_rect()
            rectanguloFin.top = 0
            rectanguloFin.left = 0
            pantalla.blit(imagenFin, rectanguloFin)
            pygame.display.flip()
            pygame.time.wait(1000)

        #cambio de nivel en pantalla-------------------------------------------------------
        imagenNivel = letra30.render('nivel: '+str(nivel),True, (200,200,200), (0,0,0) )
        rectanguloNivel = imagenNivel.get_rect()
        rectanguloNivel.left = 150
        rectanguloNivel.top = 10
        pantalla.blit(imagenNivel, rectanguloNivel)

        #puntaje en pantalla----------------------------------------------------------------
        imagenPuntos = letra30.render('Puntos '+str(puntos),True, (200,200,200), (0,0,0) )
        rectanguloPuntos = imagenPuntos.get_rect()
        rectanguloPuntos.left = 10
        rectanguloPuntos.top = 10
        pantalla.blit(imagenPuntos, rectanguloPuntos)

        pygame.display.flip()

        reloj.tick(60)

pygame.quit()
