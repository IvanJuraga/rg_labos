import numpy as np
from pyglet.gl import *
from os import getcwd
import pyglet
from scipy.special import binom


uputaZaCrtanje = []
tockePoligona = []


def ucitavanjeKontrolnogPoligona():
    print("Iscitavanje tocaka")
    cwd = getcwd()
    file = open(cwd + "/resource/" + "spiral.obj", "r")

    for linija in file:
        if (linija.startswith("p")):
            tocke = linija.split()
            tockePoligona.append((float(tocke[1]), float(tocke[2]), float(tocke[3]), 1))
    file.close()
    return tockePoligona


def izracunRavnina():
    print("Racunamo Uputuzacrtanje")
    uputaZaCrtanje.clear()
    i = len(tockePoligona) - 1
    while (i > 0):
        uputaZaCrtanje.append(((tockePoligona[i]), (tockePoligona[i - 1])))
        i = i - 1


def B_splajn_foo(tockePoligona):
    segmenti = list()
    n = len(tockePoligona)
    curr_seg = list()
    for segment in range(n - 3):

        for t in np.arange(0, 1, 0.01):

            # i=0
            p = [0, 0, 0]
            T = np.array([t ** 3, t ** 2, t, 1])
            B = np.array(([-1.0, 3.0, -3.0, 1.0], [3.0, -6.0, 3.0, 0.0], [-3.0, 0.0, 3.0, 0.0], [1.0, 4.0, 1.0, 0.0]))
            B = np.dot(1 / 6, B)
            for os in range(3):
                R = np.array(([tockePoligona[segment][os]], [tockePoligona[segment + 1][os]],
                              [tockePoligona[segment + 2][os]], [tockePoligona[segment + 3][os]]))
                p[os] = np.matmul(np.matmul(T, B), R)
            curr_seg.append(np.array(p))
        # segmenti.append(np.array(curr_seg))

    # return segmenti
    return np.array(curr_seg)


def tangente_foo(tockePoligona):
    n = len(tockePoligona)
    curr_seg = list()
    for segment in range(n - 3):

        for t in np.arange(0, 1, 0.01):

            # i=0
            p = [0, 0, 0]
            T = np.array([t ** 2, t, 1])
            B = np.array(([-1.0, 3.0, -3.0, 1.0], [2.0, -4.0, 2.0, 0.0], [-1.0, 0.0, 1.0, 0.0]))
            B = np.dot(1 / 2, B)
            for os in range(3):
                R = np.array(([tockePoligona[segment][os]], [tockePoligona[segment + 1][os]],
                              [tockePoligona[segment + 2][os]], [tockePoligona[segment + 3][os]]))
                p[os] = np.matmul(np.matmul(T, B), R)
            curr_seg.append(np.array(p))
        # tangente.append(np.array(curr_seg))

    # return tangente
    return np.array(curr_seg)


# window = pyglet.window.Window(resizable=True, width=1400, height=800)
# pyglet.gl.glClearColor(1, 1, 1, 1)
#
#
# @window.event
# def on_resize(width, height):
#     print("U funkciji sam...")
#     glViewport(0, 0, width, height)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(-1, 1, -1, 1, -1, 1)
#     glMatrixMode(GL_MODELVIEW)
#
#
# @window.event
# def on_draw():
#     izracunRavnina()
#     # print(uputaZaCrtanje)
#     glClearColor(0, 0, 0, 1)
#     glClear(GL_COLOR_BUFFER_BIT)
#     glLoadIdentity()
#
#     if (len(uputaZaCrtanje) > 0):
#         for crtez in uputaZaCrtanje:
#             glBegin(GL_LINE_STRIP)
#             glColor3f(1, 1, 1)
#             glVertex2f((crtez[0][0]), (crtez[0][1]))
#             glVertex2f((crtez[1][0]), (crtez[1][1]))
#             glEnd()
#         segmenti = B_splajn_foo(tockePoligona)
#         tangente = tangente_foo(tockePoligona)
#         # print(tockeKrivulje)
#         for idx_tocke, tocka in enumerate(segmenti):
#             # Crtanje tocke krivulje
#             glBegin(GL_POINTS)
#             r = 1 if idx_tocke > 0 and idx_tocke < 100 else 0
#             g = 1 if (idx_tocke > 100 and idx_tocke < 200) else 0
#             b = 1 if idx_tocke > 200 else 0
#             glColor3f(r, g, b)
#             print(tocka)
#             glVertex2f(tocka[0], tocka[1])
#             glEnd()
#
#             # Crtanje tangente na tu tocku
#             # if idx_tocke % 10 == 0:
#             #     glBegin(GL_LINE_STRIP)
#             #     glColor3f(0.5, 0.5, 0.5)
#             #     glVertex2f(tocka[0], tocka[1])
#             #     glVertex2f((tocka[0] + tangente[idx_tocke][0]), (tocka[1] + tangente[idx_tocke][1]))
#             #     glEnd()
#
#
# print("Pocetak")
# a = ucitavanjeKontrolnogPoligona()
# B_splajn_foo(a)
# tangente_foo(a)
# pyglet.app.run()
