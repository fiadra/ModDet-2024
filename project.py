import matplotlib.pyplot as plt
import math as m
import numpy as np

class Room:
    def __init__(x_coord, y_coord):
        self.x_coords = x_coords
        self.y_coords = y.coords

class Radiator:
    def __init__(x_coord, y_coord, power):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.power    = power

class Window:
    def __init__(window_type, size):
        self.window_type = window_type
        self.size        = size

class Door:
    def __init__(door_type, size):
        self.door_type = door_type
        self.size      = size 

class Apartment:
    def __init__(base_temp, size, hx, T, ht, n_rooms, n_radiators, n_windows, n_doors): 
        self.base_temp   = base_temp
        self.size        = size
        self.hx          = hx
        self.T           = T
        self.ht          = ht
        self.n_timeslips = int(T/ht)
        self.n_rooms     = n_rooms
        self.n_radiators = n_radiators
        self.n_windows   = n_windows
        self.n_doors     = n.doors
        self.rooms       = []
        self.radiators   = []
        self.windows     = []
        self.doors       = []
        self.Matrix      = np.zeros((n_timeslips, size[0], size[1]))
        for i in range(size[0]):
            for j in range(size[1]):
                self.Matrix[0][i][j] = base.temp

    def add_room(room):
        self.rooms.append(room)
        if self.rooms.len() >= self.n_rooms:
            print("źle")

    def add_radiator(radiator):
        self.radiators.append(radiator)
        if self.radiators.len() >= self.n_radiators:
            print("źle")

    def add_window(window):
        self.windows.append(window)
        if self.windows.len() >= self.n_windows:
            print("źle")

    def add_door(door):
        self.doors.append(door)
        if self.doors.len() >= self.n_doors:
            print("źle")



















