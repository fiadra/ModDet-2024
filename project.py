import matplotlib.pyplot as plt
import math as m
import numpy as np

class Room:
    def __init__(x_coords, y_coords):
        self.x_coords = x_coords
        self.y_coords = y.coords

class Radiator:
    def __init__(x_coords, y_coords, power):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.power    = power

class Window:
    def __init__(x_coords, y_coords):
        self.x_coords = x_coords 
        self.y_coords = y_coords

class Door:
    def __init__(x_coords, y_coords):
        self.x_coords  = x_coords 
        self.y_coords  = y_coords 


class Apartment:
    def __init__(base_temp, coeff, temp_outside, size, hx, T, ht, n_rooms, n_radiators, n_windows, n_doors): 
        self.base_temp   = base_temp
        self.coeff       = coeff
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

    def simulate():
        for t in range(n_timeslips):
            if t == 0:
                for room in self.rooms:
                    for i in range(room.x_coords[0], room.x_coords[1]):
                        for j in range(room.y_coords[0]. room.y_coords[1]):
                            self.Matrix[0][i][j] = self.base_temp

                for window in self.windows:
                    for i in range(window.x_coords[0], window.x_coords[1]):
                        for j in range(window.y_coords[0], window.y_coords[1]):
                            self.Matrix[0][i][j] = temp_outside[0]

            else:
                for room in self.rooms:
                    for i in range(room.x_coords[0], room.x_coords[1]):
                        for j in range(room.y_coords[0]. room.y_coords[1]):
                            self.Matrix[t][i][j] = self.Matrix[t-1][i][j] + (self.coeff * ht / hx**2) * \
                            ( self.Matrix[t-1][i+1][j] + self.Matrix[t-1][i-1][j] + self.Matrix[t-1][i][j-1] + self.Matrix[t-1][i][j+1] - 4 * self.Matrix[t-1][i][j] )

                    for i in range(room.x_coords[0]-1, room.x_coords[1]+1):
                        self.Matrix[t][i][room.y_coords[0]-1] = \
                                self.Matrix[t][i][room.y_coords[0]]
                        self.Matrix[t][i][room.y_coords[1]+1] = \
                                self.Matrix[t][i][room.y_coords[1]]               

                    for j in range(room.y_coords[0]-1, room.y_coords[1]+1):
                        self.Matrix[t][room.x_coords[0]-1][j] = \
                                self.Matrix[t][room.x_coords[0]][j]
                        self.Matrix[t][room.x_coords[1]+1][j] = \
                                self.Matrix[t][room.x_coords[1]][j]

                for radiator in self.radiators:
                    for i in range(radiator.x_coords[0], radiator.x_coords[1]):
                        for j in range(radiator.y_coords[0]. radiator.y_coords[1]):
                            self.Matrix[t][i][j] += radiator.power(t, i, j)
 
                for window in self.windows:
                    for i in range(window.x_coords[0], window.x_coords[1]):
                        for j in range(window.y_coords[0]. window.y_coords[1]):
                            self.Matrix[t][i][j] = self.temp_outside(t) 
  
                for door in self.doors:
                    for i in range(door.x_coords[0], door.x_coords[1]):
                        for j in range(door.y_coords[0]. door.y_coords[1]):
                            self.Matrix[t][i][j] = self.base_temp 
 

