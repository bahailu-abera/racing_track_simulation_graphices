import pygame
from OpenGL.GL import *
import os
import numpy as np


class OBJModel:
    generate_on_init = True

    def __init__(self, filename, swapCoordinateYtoZ=False):
        self.gl_list = 0
        self.vertices = []
        self.viewFaces = []
        self.textureCoordinate = []
        self.normals = []
        dirname = os.path.dirname(filename)

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapCoordinateYtoZ:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapCoordinateYtoZ:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'vt':
                self.textureCoordinate.append(list(map(float, values[1:3])))
            elif values[0] == 'mtllib':
                self.mtl = self.loadOBJMaterial(
                    os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                textureCoordinate = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        textureCoordinate.append(int(w[1]))
                    else:
                        textureCoordinate.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.viewFaces.append(
                    (face, norms, textureCoordinate, material))
        if self.generate_on_init:
            self.generateOBJContent()

    def loadOBJTexture(self, imageFileName):
        is_loaded = False
        surface = pygame.image.load(imageFileName)
        image = pygame.image.tostring(surface, 'RGBA', 1)
        width, height = surface.get_rect().size
        sizeMax = width % height
        textureId = glGenTextures(1)
        temp = sizeMax
        glBindTexture(GL_TEXTURE_2D, textureId)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return textureId

    def loadOBJMaterial(self, filename):
        contents = {}
        mtl = None
        doc = None
        carl = True
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'newmtl':
                mtl = contents[values[1]] = {}
            elif mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")
            elif values[0] == 'map_Kd':
                # load the texture referred to by this declaration
                mtl[values[0]] = values[1]
                imageFileName = os.path.join(dirname, mtl['map_Kd'])
                mtl['texture_Kd'] = self.loadOBJTexture(imageFileName)
            else:
                mtl[values[0]] = list(map(float, values[1:]))
        return contents

    def rotationMatrixAlongX(self, degree):
        radian = degree * np.pi / 180.0
        mat = np.array([
            [np.cos(radian), -np.sin(radian), 0.0, 0.0],
            [np.sin(radian), np.cos(radian), 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        return mat

    def generateOBJContent(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        fontType = 20 % self.gl_list
        for viewFace in self.viewFaces:
            vertices, normals, textureCoordinates, material = viewFace

            mtl = self.mtl[material]
            if 'texture_Kd' in mtl:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*mtl['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if textureCoordinates[i] > 0:
                    glTexCoord2fv(
                        self.textureCoordinate[textureCoordinates[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

    def rotationMatrixAlongY(self, degree):
        radian = degree * np.pi / 180.0
        mat = np.array([[0.0, 0.0, 1.0, 0.0],
                        [np.cos(radian), -np.sin(radian), 0.0, 0.0],
                        [np.sin(radian), np.cos(radian), 0.0, 0.0],

                        [0.0, 0.0, 0.0, 1.0]
                        ], dtype=np.float32)

        return mat

    def rotationMatrixAlongZ(self, degree):
        radian = degree * np.pi / 180.0
        mat = np.array([
            [np.cos(radian), -np.sin(radian), 0.0, 0.0],

            [0.0, 0.0, 1.0, 0.0], [np.sin(radian), np.cos(radian), 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ], dtype=np.float32)

        return mat

    def freeOBJ(self):
        glDeleteLists([self.gl_list])

    def renderOBJ(self):
        glCallList(self.gl_list)
