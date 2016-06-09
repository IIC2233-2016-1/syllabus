# -*- coding: utf-8 -*-
import os
import pickle
import json


class FacebookProfile:

    def __init__(self, pid, nombre, amigos):
        self.nombre = nombre
        self.pid = pid
        self.amigos = amigos


class TwitterProfile:

    def __init__(self, pid, handle, seguidos, seguidores):
        self.handle = handle
        self.pid = pid
        self.seguidos = seguidos
        self.seguidores = seguidores


class InstagramProfile:

    def __init__(self, pid, handle, seguidos, seguidores):
        self.handle = handle
        self.pid = pid
        self.seguidos = seguidos
        self.seguidores = seguidores


if __name__ == '__main__':
    print('Aquí deben recoger la info de las personas!')
