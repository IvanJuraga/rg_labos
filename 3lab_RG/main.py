from pyglet.window import key
from pyglet.gl import *
import pyglet
import os
import numpy as np
from math import cos, sin, radians
from scipy.optimize import minimize,minimize_scalar
import math
import ctypes

s = np.array((0.0, 0.0, 1.0))

WIDTH = 1400
HEIGHT = 800
Ociste = np.array([10.0, 10.0, 15.0])

window = pyglet.window.Window(resizable=True, width=WIDTH, height=HEIGHT)
pyglet.gl.glClearColor(1, 1, 1, 1)
i = 0

T0 = np.array([0.0, 0.0])
R0 = 15.0

T1 = np.array([0.4, 0.0])
R1 = 0.0

T2 = np.array([0.25, 0.0])
R2 = 0.0

pravci = np.array(
    ([[0.0, 0.0, 0.0, 1.0], [0.4, 0.0, 0.0, 1.0]], [[0.0, 0.0, 0.0, 1.0], [0.25, 0.0, 0.0, 1.0]],
     [[0.0, 0.0, 0.0, 1.0], [0.15, 0.0, 0.0, 1.0]]))

TRESHHOLD = 0.01
dest_point = np.array([0.4, 0.0])



def calc_new_end():
    global pravci, R2, R1, R0, end_point
    tmp_point = pravci[2][1].copy()

    glLoadIdentity()

    glTranslatef(T0[0], T0[1], 0.0)
    glRotatef(R0, 0, 0, 1)

    glTranslatef(T1[0], T1[1], 0.0)
    glRotatef(R1, 0, 0, 1)

    glTranslatef(T2[0], T2[1], 0.0)
    glRotatef(R2, 0, 0, 1)

    modelview = np.zeros((4, 4), dtype=np.float32)
    glGetFloatv(GL_MODELVIEW_MATRIX, modelview.ctypes.data_as(
        ctypes.POINTER(ctypes.c_float)))

    return np.matmul(tmp_point, modelview)[:2]


def min_R2(R2_min):
    global pravci, R1, R0
    tmp_point = pravci[2][1].copy()

    glLoadIdentity()

    glTranslatef(T0[0], T0[1], 0.0)
    glRotatef(R0, 0, 0, 1)

    glTranslatef(T1[0], T1[1], 0.0)
    glRotatef(R1, 0, 0, 1)

    glTranslatef(T2[0], T2[1], 0.0)
    glRotatef(R2_min, 0, 0, 1)

    modelview = np.zeros((4, 4), dtype=np.float32)
    glGetFloatv(GL_MODELVIEW_MATRIX, modelview.ctypes.data_as(
        ctypes.POINTER(ctypes.c_float)))

    tmp_point = np.matmul(tmp_point, modelview)

    return ((((tmp_point[0] - dest_point[0]) ** 2) + ((tmp_point[1] - dest_point[1]) ** 2)) ** 0.5)


def min_R1(R1_min):
    global pravci, R2, R0, end_point
    tmp_point = pravci[2][1].copy()

    glLoadIdentity()

    glTranslatef(T0[0], T0[1], 0.0)
    glRotatef(R0, 0, 0, 1)

    glTranslatef(T1[0], T1[1], 0.0)
    glRotatef(R1_min, 0, 0, 1)

    glTranslatef(T2[0], T2[1], 0.0)
    glRotatef(R2, 0, 0, 1)

    modelview = np.zeros((4, 4), dtype=np.float32)
    glGetFloatv(GL_MODELVIEW_MATRIX, modelview.ctypes.data_as(
        ctypes.POINTER(ctypes.c_float)))

    tmp_point = np.matmul(tmp_point, modelview)

    return ((((tmp_point[0] - dest_point[0]) ** 2) + ((tmp_point[1] - dest_point[1]) ** 2)) ** 0.5)


def min_R0(R0_min):
    global pravci, R2, R1, end_point
    tmp_point = pravci[2][1].copy()

    glLoadIdentity()

    glTranslatef(T0[0], T0[1], 0.0)
    glRotatef(R0_min, 0, 0, 1)

    glTranslatef(T1[0], T1[1], 0.0)
    glRotatef(R1, 0, 0, 1)

    glTranslatef(T2[0], T2[1], 0.0)
    glRotatef(R2, 0, 0, 1)

    modelview = np.zeros((4, 4), dtype=np.float32)
    glGetFloatv(GL_MODELVIEW_MATRIX, modelview.ctypes.data_as(
        ctypes.POINTER(ctypes.c_float)))

    tmp_point = np.matmul(tmp_point, modelview)


    return ((((tmp_point[0] - dest_point[0]) ** 2) + ((tmp_point[1] - dest_point[1]) ** 2)) ** 0.5)


@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1, 1, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_draw():
    global R0, R1, R2, T0, T1, T2, end_point, dest_point
    glLoadIdentity()
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    glTranslatef(T0[0], T0[1], 0.0)
    glRotatef(R0, 0, 0, 1)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex2f(pravci[0][0][0], pravci[0][0][1])
    glVertex2f(pravci[0][1][0], pravci[0][1][1])
    glEnd()

    glTranslatef(T1[0], T1[1], 0.0)
    glRotatef(R1, 0, 0, 1)
    glBegin(GL_LINES)
    glColor3f(0, 1, 0)
    glVertex2f(pravci[1][0][0], pravci[1][0][1])
    glVertex2f(pravci[1][1][0], pravci[1][1][1])
    glEnd()

    glTranslatef(T2[0], T2[1], 0.0)
    glRotatef(R2, 0, 0, 1)
    glBegin(GL_LINES)
    glColor3f(0, 0, 1)
    glVertex2f(pravci[2][0][0], pravci[2][0][1])
    glVertex2f(pravci[2][1][0], pravci[2][1][1])
    glEnd()


@window.event
def on_key_press(symbol, modifiers):
    global R0, R1, R2

    if symbol == key.T:
        window.close()
        exit(1)
    if symbol == key.A:
        R0 += 5
    if symbol == key.Z:
        R0 -= 5
    if symbol == key.S:
        R1 += 5
    if symbol == key.X:
        R1 -= 5
    if symbol == key.D:
        R2 += 5
    if symbol == key.C:
        R2 -= 5

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    dest_point[0] = round(-1 + (x / WIDTH) * 2, 2)
    dest_point[1] = round(-1 + (y / HEIGHT) * 2, 2)
    # print(x, y)
    # print(dest_point)
    calculate_CCD(x, y)

def check_end(p1, p2):
    return ((((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)) ** 0.5) < TRESHHOLD


def calculate_CCD(x, y, n_iter=5):
    global R0, R1, R2

    dest_point[0] = round(-1 + (x / WIDTH) * 2, 2)
    dest_point[1] = round(-1 + (y / HEIGHT) * 2, 2)

    for _ in range(n_iter):
        # R2_sugg = minimize(min_R2, R2, method='nelder-mead',
        #                    options={'xatol': 1e-6, 'disp': True}).x[0]
        R2_sugg = minimize_scalar(min_R2).x

        R2 = R2_sugg
        if check_end(calc_new_end(),dest_point):
            return

        # R1_sugg = minimize(min_R1, R1, method='nelder-mead',
        #                    options={'xatol': 1e-6, 'disp': True}).x[0]
        R1_sugg = minimize_scalar(min_R1).x

        R1 = R1_sugg
        if check_end(calc_new_end(),dest_point):
            return

        # R0_sugg = minimize(min_R0, R0, method='nelder-mead',
        #                    options={'xatol': 1e-6, 'disp': True}).x[0]
        R0_sugg = minimize_scalar(min_R0).x

        R0 = R0_sugg
        if check_end(calc_new_end(),dest_point):
            return


@window.event
def on_mouse_press(x, y, button, modifiers):
    dest_point[0] = round(-1 + (x / WIDTH) * 2, 2)
    dest_point[1] = round(-1 + (y / HEIGHT) * 2, 2)
    #
    # print("ZELIM NACI")
    print(x, y)
    print(dest_point)
    calculate_CCD(x, y)
    # print(R1)


def update(dt):
    pass


pyglet.clock.schedule_interval(update, 1 / 30)
pyglet.app.run()
