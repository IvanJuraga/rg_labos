import os

import numpy as np
import pyglet
from numpy import array, linalg, matmul
from pyglet.gl import *
from pyglet.window import key

from B_splajn import ucitavanjeKontrolnogPoligona, B_splajn_foo, tangente_foo
from Orijentacijske_funkcije import izracunaj_kut_rot, vektorski_umnozak, izracunaj_DCM

# <editor-fold desc=Global Var init>
filenameDict = {1: "tetrahedron", 2: "kocka",
                3: "medo2", 4: "bird",
                5: "teapot", 6: "frog",
                7: "all", 8: "bull",
                9: "porsche", 10: "arena",
                11: "dragon", 12: "temple",
                13: "skull"}

s = array((0.0, 0.0, 1.0))

USE_DCM = True

WIDTH = 640
HEIGHT = 480
Ociste = array([10.0, 10.0, 15.0])
popisVrhova_pocetni = []
popisPoligona = []
tockeKrivulje = []
ravnine = []  # [(A0,B0,C0,D0),(A1...)]
uputeZaCrtanje = []  # [(vrh10,vrh20,vrh30),(vrh11,vrh21,vrh31),...]
window = pyglet.window.Window(resizable=True, width=WIDTH, height=HEIGHT)
pyglet.gl.glClearColor(1, 1, 1, 1)
i = 0

ispisDict = {1: (1.05, 1.05, 245), 2: (1.9, 1.2, 300), 3: (30, 30, 20),
             4: (1, 1, 600), 5: (5, 3, 130), 6: (10, 7, 60),
             7: (1.25, 1.5, 500), 8: (3800, 2000, 1 / 6), 9: (0.8, 0.6, 800),
             10: (1.0, 0.9, 600), 11: (0.8, 0.7, 800), 12: (0.9, 0.8, 700),
             13: (0.75, 0.7, 800)}


# </editor-fold>

def ucitavanjePodataka(odabir):
    cwd = os.getcwd()
    file = open(cwd + "/resource/" + odabir + ".obj", "r")

    for linija in file:
        if (linija.startswith("v")):
            tocke = linija.split()
            popisVrhova_pocetni.append((float(tocke[1]), float(tocke[2]), float(tocke[3]), 1))

        if linija.startswith("f"):
            veze = linija.split()
            popisPoligona.append((int(veze[1]) - 1, int(veze[2]) - 1, int(veze[3]) - 1))


@window.event
def on_resize(width, height):
    # print("U funkciji sam...")
    # glViewport(0, 0, width, height)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(-10, 10, -10, 10, -10, 10)
    # glMatrixMode(GL_MODELVIEW)

    print("U funkciji sam...")
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width / height), 0.1, spirala_height + 20)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5, 5, 5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    # glClearColor(1.0,1.0,1.0,1.0)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    popisVrhova = popisVrhova_pocetni.copy()
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glTranslatef(-spirala_center[0], -spirala_center[1], -spirala_height - 20.0)
    # glTranslatef(spirala_center[0], spirala_center[1], -80.0)

    if not USE_DCM:
        os = vektorski_umnozak(s, tangente[i])
        kut = izracunaj_kut_rot(s, tangente[i])

    # glTranslatef(-13.0, -7.0, -80.0)

    for idx, crtez in enumerate(tockeKrivulje):
        if idx % 15 == 0:
            glBegin(GL_LINE_STRIP)
            glColor3f(0.0, 0.0, 1.0)
            glVertex3f(crtez[0], crtez[1], crtez[2])
            glVertex3f((crtez[0] + tangente[idx][0]), (crtez[1] + tangente[idx][1]), (crtez[2] + tangente[idx][2]))
            glEnd()

        glBegin(GL_POINTS)
        glColor3f(0.5, 0.5, 0.5)
        glVertex3f(crtez[0], crtez[1], crtez[2])

        glEnd()

    glTranslatef(tockeKrivulje[i][0], tockeKrivulje[i][1], tockeKrivulje[i][2])

    if USE_DCM:
        R_inv = linalg.inv(np.reshape(DCM[i], (3, 3)))
        # if i==1:
        #     print(R_inv)
        #     exit(0)

        for vidx in range(len(popisVrhova)):
            popisVrhova[vidx] = matmul(popisVrhova[vidx][:3], R_inv)

    else:
        glRotatef(kut, os[0], os[1], os[2])

    # glTranslatef(-obj_center[0], -obj_center[1], -obj_center[2])

    for crtez in popisPoligona:
        glBegin(GL_LINES)
        glColor3f(1, 1, 1)

        glVertex3f(popisVrhova[crtez[0]][0], popisVrhova[crtez[0]][1],
                   popisVrhova[crtez[0]][2])
        # print(popisVrhova[crtez[0]][0], popisVrhova[crtez[0]][1],
        #       popisVrhova[crtez[0]][2])

        glVertex3f(popisVrhova[crtez[1]][0], popisVrhova[crtez[1]][1],
                   popisVrhova[crtez[1]][2])
        # print(popisVrhova[crtez[1]][0], popisVrhova[crtez[1]][1],
        #       popisVrhova[crtez[1]][2])

        glVertex3f(popisVrhova[crtez[2]][0], popisVrhova[crtez[2]][1],
                   popisVrhova[crtez[2]][2])
        # print(popisVrhova[crtez[2]][0], popisVrhova[crtez[2]][1],
        #         #       popisVrhova[crtez[2]][2])
        #         # print("")

        # glVertex3f(popisVrhova[crtez[0]][0], popisVrhova[crtez[0]][1],
        #            popisVrhova[crtez[0]][2])
        glEnd()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.T:
        window.close()
        exit(1)


def update(dt):
    global i
    i += 1
    if (i >= len(tangente)):
        i = 0


# 1 trokut , 2 kocka, 3 medo
odabir = 2

print("ZA GASENJE PROGRAMA UNJETI TIPKU (T)erminate")


def calculate_object_center(obj_vrhovi):
    x_total = 0
    y_total = 0
    z_total = 0
    for vrh in obj_vrhovi:
        x_total += vrh[0]
        y_total += vrh[1]
        z_total += vrh[2]
    x_total /= len(obj_vrhovi)
    y_total /= len(obj_vrhovi)
    z_total /= len(obj_vrhovi)
    return array((x_total, y_total, z_total))


ucitavanjePodataka(filenameDict.get(odabir))
tockeKontPoligona = ucitavanjeKontrolnogPoligona()
tockeKrivulje = B_splajn_foo(tockeKontPoligona)
tangente = tangente_foo(tockeKontPoligona)

DCM = izracunaj_DCM(tangente, tockeKontPoligona)
print(np.resize(DCM[1], (3, 3)))
obj_center = calculate_object_center(popisVrhova_pocetni)

spirala_center = calculate_object_center(tockeKrivulje)
spirala_height = np.max(tockeKrivulje, axis=0)[2]

pyglet.clock.schedule_interval(update, 1 / 40)
pyglet.app.run()
