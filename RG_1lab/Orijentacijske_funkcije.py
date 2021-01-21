from math import acos, pi

import numpy as np
from numpy import linalg as LA


def vektorski_umnozak(poc_or, cilj_or, DCM=False):
    if not DCM:
        x = (poc_or[1] * cilj_or[2]) - (cilj_or[1] * poc_or[2])[0]
        y = -1 * ((poc_or[0] * cilj_or[2]) - (cilj_or[0] * poc_or[2]))[0]
        z = (poc_or[0] * cilj_or[1]) - (poc_or[1] * cilj_or[0])[0]
    else:
        x = (poc_or[1] * cilj_or[2]) - (cilj_or[1] * poc_or[2])
        y = -1 * ((poc_or[0] * cilj_or[2]) - (cilj_or[0] * poc_or[2]))
        z = (poc_or[0] * cilj_or[1]) - (poc_or[1] * cilj_or[0])
    return np.array((x, y, z))


def izracunaj_kut_rot(poc_or, cilj_or):
    return acos((np.dot(poc_or, cilj_or) / (LA.norm(poc_or, axis=0) * LA.norm(cilj_or, axis=0)))) * (180 / pi)
    # return acos((np.dot(poc_or, cilj_or) / (LA.norm(poc_or, axis=0) * LA.norm(cilj_or, axis=0))))


def izracunaj_DCM(tangente, tockePoligona):
    n = len(tockePoligona)

    DCM = list()
    for segment in range(n - 3):

        for idx, t in enumerate(np.arange(0, 1, 0.01)):

            # i=0
            p = np.zeros(3)
            for os in range(3):
                p[os] = tockePoligona[segment][os] * (-t + 1) + tockePoligona[segment + 1][os] * (3 * t - 2) + \
                        tockePoligona[segment + 2][os] * (-3 * t + 1) + tockePoligona[segment + 3][os] * t

            tangenta = np.resize(tangente[100 * segment + idx], (3,)) / LA.norm(np.resize(tangente[100 * segment + idx], (3,)))
            # tangenta = np.resize(tangente[100 * segment + idx], (3,)) / 2
            # p /= 2
            normala = vektorski_umnozak(tangenta, p , DCM=True) / LA.norm(vektorski_umnozak(tangenta, p, DCM=True))
            # normala = vektorski_umnozak(tangenta, p, DCM=True)
            # normale.append(normala)

            binormala = vektorski_umnozak(tangenta, normala,DCM= True) / LA.norm(vektorski_umnozak(tangenta, normala,DCM=True))
            # binormala = vektorski_umnozak(tangenta, normala, DCM=True)
            # binormale.append(binormala)
            DCM.append(np.array(([tangenta[0], normala[0], binormala[0]], [tangenta[1], normala[1], binormala[1]],
                                 [tangenta[2], normala[2], binormala[2]])))
        # tangente.append(np.array(curr_seg))

    # return tangente
    return np.array(DCM)
