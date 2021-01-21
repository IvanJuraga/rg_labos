from pyglet.window import key
from pyglet.gl import *
import pyglet
import os
from numpy import matmul, subtract, dot, array
from B_splajn import ucitavanjeKontrolnogPoligona, B_splajn_foo, tangente_foo

# <editor-fold desc=Global Var init>
filenameDict = {1: "tetrahedron", 2: "kocka",
                3: "teddy", 4: "bird",
                5: "teapot", 6: "frog",
                7: "all", 8: "bull",
                9: "porsche", 10: "arena",
                11: "dragon", 12: "temple",
                13: "skull"}

s = array((0.0, 0.0, 1.0))

WIDTH = 640
HEIGHT = 480
Ociste = array([10.0, 10.0, 15.0])
popisVrhova = []
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

@window.event
def on_resize(width, height):
    # print("U funkciji sam...")
    # glViewport(0, 0, width, height)
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(-10, 10, -10, 10, -10, 10)
    # glMatrixMode(GL_MODELVIEW)

    print("U funkciji sam...")
    glViewport(-10, -10, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width / height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    # glClearColor(1.0,1.0,1.0,1.0)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glTranslatef(-5.0, -5.0, -70.0)
    # ZOOM = 10.0
    # glScalef(ZOOM, ZOOM, ZOOM)

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


# 1 trokut , 2 kocka
odabir = 2

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


tockeKontPoligona = ucitavanjeKontrolnogPoligona()
tockeKrivulje = B_splajn_foo(tockeKontPoligona)
tangente = tangente_foo(tockeKontPoligona)

pyglet.clock.schedule_interval(update, 1 / 30)
pyglet.app.run()
