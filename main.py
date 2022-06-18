
import sys
import pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OBJloader import *
import pyrr

# IMPORT OBJECT LOADER


pygame.init()
viewport = (1700, 900)
surface = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT1, GL_POSITION,  (1, 1, 1, 0.0))
glLightfv(GL_LIGHT1, GL_AMBIENT, (0.2, 1.5, 1.4, 1.0))
glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.6, 1, 1, 1.0))
glEnable(GL_LIGHT1)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glClearColor(1.0, 1.0, 1.0, 1.0)
color = (255, 255, 255)

# Changing surface color
surface.fill(color)
# glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
trackOBJ = OBJModel("assets/models/track2.obj", swapCoordinateYtoZ=True)

carOBJ = OBJModel("assets/models/Car2.obj")

carOBJ.loadOBJTexture("assets/textures/car_texture.png")
# obj.loadOBJTexture("assets/textures/trackTexture2.png")

trackOBJ.generateOBJContent()
carOBJ.generateOBJContent()

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(60.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
# checking pressed keys


car_x_position = -10.0
car_y_position = 0
car_z_position = 0
car_x_rotation = 0.0
while True:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()

    keys = pygame.key.get_pressed()  # checking pressed keys

    if keys[pygame.K_UP]:
        # if car_z_pos >= -4 or (car_z_pos < -4 and car_x_pos < -20):
        if car_x_rotation < 50.0 and car_x_position > -27:
            car_x_position -= 1
        elif car_x_rotation >= 45.0 and car_x_rotation < 145 and car_z_position > -22:
            if car_x_position > -25 and car_x_position < 5:
                pass
            else:
                car_z_position -= 1
            # car_y_pos += 0.3
        elif car_x_rotation > 145 and car_x_rotation < 245 and car_x_position < 12:
            car_x_position += 1
        elif car_x_rotation > 245 and car_x_rotation < 350 and car_z_position < -3:
            if car_x_position > -25 and car_x_position < 5:
                pass
            else:
                car_z_position += 1
            # car_y_pos -= 0.3
        elif car_x_rotation >= 350:
            car_x_rotation = 0
        # elif car_x_rotation > -45:
        #     car_z_position += 1
    if keys[pygame.K_DOWN]:
        # if car_z_pos >= -4 or (car_z_pos < -4 and car_x_pos < -20):
        if car_x_rotation <= 50.0 and car_x_position >= -27 and car_x_position < 7:
            car_x_position += 1
        elif car_x_rotation >= 45.0 and car_x_rotation <= 145 and car_z_position >= -22 and car_z_position <= -4:
            car_z_position += 1
            # car_y_pos += 0.3
        elif car_x_rotation > 145 and car_x_rotation <= 245 and car_x_position <= 12 and car_x_position >= -32:
            car_x_position -= 1
        elif car_x_rotation >= 245 and car_x_rotation <= 350 and car_z_position <= -3 and car_z_position >= -24:
            car_z_position -= 1
            # car_y_pos -= 0.3
        elif car_x_rotation >= 350:
            car_x_rotation = 0

    if keys[pygame.K_RIGHT]:
        car_x_rotation += 5

    if keys[pygame.K_LEFT]:
        car_x_rotation -= 5

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # RENDER OBJECT
    glTranslate(0., -7., - 30)
    if(car_x_rotation < 45.0):
        glRotate(0, 0, -1, 0)
        gluLookAt(car_x_position, car_y_position, car_z_position,
                  car_x_position-9, car_y_position, car_z_position-5, 0, 1, 0)

    if(car_x_rotation > 45.0 and car_x_rotation < 145.0):
        glRotate(50, 0, -1, 0)
        glTranslate(-12, 5, 10)
        gluLookAt(car_x_position, car_y_position, car_z_position,
                  car_x_position+6, car_y_position-2, car_z_position-3, 0, 1, 0)

    if(car_x_rotation > 145.0 and car_x_rotation < 245.0):
        glRotate(216, 0, -1, 0)
        glTranslate(-1, 2, -20)
        gluLookAt(car_x_position, car_y_position, car_z_position,
                  car_x_position-30, car_y_position, car_z_position-6, 0, 1, 0)
    if(car_x_rotation > 245.0 and car_x_rotation < 350.0):
        glRotate(240, 0, -1, 0)
        glTranslate(-15, -2, -8)
        gluLookAt(car_x_position, car_y_position, car_z_position,
                  car_x_position+6, car_y_position, car_z_position-3, 0, 1, 0)
    # glRotate(car_x_rot, 0, -1, 0)
    # gluLookAt(car_x_pos, car_y_pos, car_z_pos,
    #           car_x_pos-10, car_y_pos, car_z_pos-4, 0, 1, 0)
    glRotate(90, -1, 0, 0)
    glRotate(90, 0, 0, 1)
    trackOBJ.renderOBJ()

    glRotate(90, 1, 0, 0)
    glRotate(90, 0, 0, -1)
    glTranslate(0., 7.,  40)

    glTranslate(0., -22., -30)
    glRotate(90, 0, -1, 0)
    glRotate(90, 1, 0, 0)
    glTranslate(car_x_position, car_y_position+0.5, car_z_position)
    glRotate(car_x_rotation, 0, -1, 0)

    carOBJ.renderOBJ()

    pygame.display.flip()
