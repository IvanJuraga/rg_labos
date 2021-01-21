from pyglet.window import key
from pyglet.gl import *
import pyglet
import os
from numpy import matmul, subtract, dot, array, append
import numpy as np
from random import uniform

s = array((0.0, 0.0, 1.0))

WIDTH = 1400
HEIGHT = 800
Ociste = array([10.0, 10.0, 15.0])
popisVrhova = []
popisPahulja = []
popisPoligona = []
window = pyglet.window.Window(resizable=True, width=WIDTH, height=HEIGHT)
pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
pyglet.gl.glClearColor(1, 1, 1, 1)

i = 0

O_x = 0
O_y = 0
O_z = 0

G_x = 10
G_y = 10
G_z = 0

kut = 0


def stvaranje_prvih_pahulja(broj_pahulja):
    for i in range(broj_pahulja):
        x = uniform(0.470, 0.480)
        y = uniform(-0.0570, -0.0580)
        z = 0.0
    # x = 0.0
    # y = uniform(-0.0570, -0.0580)
    # z = 0.0
        life = np.random.randint(5, 10)
        sampl = np.array((x, y, z, life))
        popisPahulja.append(sampl)


# </editor-fold>

def ucitavanjePodataka():
    file = open("auto.obj", "r")

    for linija in file:
        if (linija.startswith("v")):
            tocke = linija.split()
            popisVrhova.append((float(tocke[1]), float(tocke[2]), float(tocke[3]), 1))

        if linija.startswith("f"):
            veze = linija.split()
            popisPoligona.append((int(veze[1]) - 1, int(veze[2]) - 1, int(veze[3]) - 1))


@window.event
def on_resize(width, height):
    global O_x, O_y, O_z, G_x, G_y, G_z, kut
    print("U funkciji sam...")
    glViewport(-10, -10, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(kut, float(width / height), 0.5, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    print(O_x, O_y, O_z, kut)
    gluLookAt(O_x, O_y, O_z, G_x, G_y, G_z, 0.0, 0.0, 1.0)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    glLoadIdentity()
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # glEnable( GL_BLEND )
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    # for tocka in popisPahulja:
    #     glPointSize(10)
    #     glBegin(GL_POINTS)
    #     alfa = 1
    #     glColor4f(1, 0, 1, alfa)
    #     glVertex3f(tocka[0], tocka[1], tocka[2])
    #     glEnd()
    glRotatef(270, 0.0, 1.0, 0.0)
    glColor3f(1, 1, 1)
    glEnable(smoke.target)
    glBindTexture(smoke.target, smoke.id)
    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE)
    glBegin(GL_QUADS)
    for p in popisPahulja:
        size = 0.04
        glTexCoord2f(0, 0)
        glVertex3f(p[0] - size, p[1] - size, p[2])
        glTexCoord2f(1, 0)
        glVertex3f(p[0] + size, p[1] - size, p[2])
        glTexCoord2f(1, 1)
        glVertex3f(p[0] + size, p[1] + size, p[2])
        glTexCoord2f(0, 1)
        glVertex3f(p[0] - size, p[1] + size, p[2])
    glEnd()
    glDisable(GL_BLEND)
    glDisable(smoke.target)

    for crtez in popisPoligona:
        glBegin(GL_LINES)
        # glColor3f(0.59, 0.3, 0.0)
        glColor3f(1.0, 1.0, 1.0)

        glVertex3f(popisVrhova[crtez[0]][0], popisVrhova[crtez[0]][1],
                   popisVrhova[crtez[0]][2])
        glVertex3f(popisVrhova[crtez[1]][0], popisVrhova[crtez[1]][1],
                   popisVrhova[crtez[1]][2])

        glVertex3f(popisVrhova[crtez[2]][0], popisVrhova[crtez[2]][1],
                   popisVrhova[crtez[2]][2])
        glEnd()


@window.event
def on_key_press(symbol, modifiers):
    global O_x, O_y, O_z, G_x, G_y, G_z, kut

    if symbol == key.T:
        window.close()
        exit(1)
    if symbol == key.A:
        O_x += 5
        on_resize(window.width, window.height)
    if symbol == key.S:
        O_y += 5
        on_resize(window.width, window.height)
    if symbol == key.D:
        O_z += 5
        on_resize(window.width, window.height)
    if symbol == key.Z:
        O_x -= 5
        on_resize(window.width, window.height)
    if symbol == key.X:
        O_y -= 5
        on_resize(window.width, window.height)
    if symbol == key.C:
        O_z -= 5
        on_resize(window.width, window.height)
    if symbol == key.G:
        kut += 4
        on_resize(window.width, window.height)
    if symbol == key.H:
        kut -= 4
        on_resize(window.width, window.height)


@window.event
def on_mouse_press(x, y, button, modifiers):
    print("burek")
    print(x / window.width, y / window.height)


def update(dt):
    global i
    i += 1
    for i in range(len(popisPahulja)):
        popisPahulja[i][0] += uniform(0.005, 0.01)
        popisPahulja[i][1] += uniform(0.005, 0.01)
        popisPahulja[i][3] -= 1
        if (popisPahulja[i][3] < 0):
            popisPahulja[i][0] = uniform(0.470, 0.480)
            popisPahulja[i][1] = uniform(-0.0570, -0.0580)
            popisPahulja[i][2] = 0.0
            popisPahulja[i][3] = np.random.randint(5, 10)


print("ZA GASENJE PROGRAMA UNJETI TIPKU (T)erminate")


def calculate_object_center():
    x_total = 0
    y_total = 0
    z_total = 0
    for vrh in popisVrhova:
        x_total += vrh[0]
        y_total += vrh[1]
        z_total += vrh[2]
    x_total /= len(popisVrhova)
    y_total /= len(popisVrhova)
    z_total /= len(popisVrhova)
    return array((x_total, y_total, z_total))


smoke = pyglet.image.load('smoke.bmp').get_texture()
ucitavanjePodataka()
stvaranje_prvih_pahulja(broj_pahulja=15)
# print(len(popisPahulja))
# systems = [particleSystem(200)]
obj_center = calculate_object_center()

pyglet.clock.schedule_interval(update, 1 / 30)
pyglet.app.run()
