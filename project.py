import matplotlib.pyplot as plt
import math as m
import numpy as np


def celcius_to_kelvin(t):
    return t + 273.15


class Room:
    def __init__(self, x_coords, y_coords):
        self.x_coords = x_coords
        self.y_coords = y_coords


class Radiator:
    def __init__(self, x_coords, y_coords, power):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.power = power


class Window:
    def __init__(self, x_coords, y_coords):
        self.x_coords = x_coords
        self.y_coords = y_coords


class Door:
    def __init__(self, x_coords, y_coords):
        self.x_coords = x_coords
        self.y_coords = y_coords


class Apartment:
    def __init__(
        self,
        base_temp,
        coeff,
        temp_outside,
        size,
        hx,
        T,
        ht,
        n_rooms,
        n_radiators,
        n_windows,
        n_doors,
    ):
        self.base_temp = base_temp
        self.coeff = coeff
        self.temp_outside = temp_outside
        self.size = size
        self.hx = hx
        self.T = T
        self.ht = ht
        self.n_timeslips = int(T / ht)
        self.n_rooms = n_rooms
        self.n_radiators = n_radiators
        self.n_windows = n_windows
        self.n_doors = n_doors
        self.rooms = []
        self.radiators = []
        self.windows = []
        self.doors = []
        self.Matrix = np.zeros((self.n_timeslips, self.size[0] + 1, self.size[1] + 1))
        for i in range(size[0] + 1):
            for j in range(size[1] + 1):
                self.Matrix[0][i][j] = base_temp

    def add_room(self, room):
        self.rooms.append(room)
        if len(self.rooms) > self.n_rooms:
            print("źle")

    def add_radiator(self, radiator):
        self.radiators.append(radiator)
        if len(self.radiators) > self.n_radiators:
            print("źle")

    def add_window(self, window):
        self.windows.append(window)
        if len(self.windows) > self.n_windows:
            print("źle")

    def add_door(self, door):
        self.doors.append(door)
        if len(self.doors) > self.n_doors:
            print("źle")

    def simulate(self):
        for t in range(self.n_timeslips):
            if t == 0:
                for room in self.rooms:
                    for i in range(room.x_coords[0], room.x_coords[1]):
                        for j in range(room.y_coords[0], room.y_coords[1]):
                            self.Matrix[0][i][j] = self.base_temp

                for window in self.windows:
                    for i in range(window.x_coords[0], window.x_coords[1]):
                        for j in range(window.y_coords[0], window.y_coords[1]):
                            self.Matrix[0][i][j] = self.temp_outside(0)

            else:
                for room in self.rooms:
                    for i in range(room.x_coords[0], room.x_coords[1]):
                        for j in range(room.y_coords[0], room.y_coords[1]):
                            self.Matrix[t][i][j] = self.Matrix[t - 1][i][j] + (
                                self.coeff * self.ht / self.hx**2
                            ) * (
                                self.Matrix[t - 1][i + 1][j]
                                + self.Matrix[t - 1][i - 1][j]
                                + self.Matrix[t - 1][i][j - 1]
                                + self.Matrix[t - 1][i][j + 1]
                                - 4 * self.Matrix[t - 1][i][j]
                            )

                    for i in range(room.x_coords[0] - 1, room.x_coords[1] + 1):
                        self.Matrix[t][i][room.y_coords[0] - 1] = self.Matrix[t][i][
                            room.y_coords[0]
                        ]
                        self.Matrix[t][i][room.y_coords[1] + 1] = self.Matrix[t][i][
                            room.y_coords[1]
                        ]

                    for j in range(room.y_coords[0] - 1, room.y_coords[1] + 1):
                        self.Matrix[t][room.x_coords[0] - 1][j] = self.Matrix[t][
                            room.x_coords[0]
                        ][j]
                        self.Matrix[t][room.x_coords[1] + 1][j] = self.Matrix[t][
                            room.x_coords[1]
                        ][j]

                for radiator in self.radiators:
                    for i in range(radiator.x_coords[0], radiator.x_coords[1]):
                        for j in range(radiator.y_coords[0], radiator.y_coords[1]):
                            self.Matrix[t][i][j] += self.ht * radiator.power(i, j, t)

                for window in self.windows:
                    for i in range(window.x_coords[0], window.x_coords[1]):
                        for j in range(window.y_coords[0], window.y_coords[1]):
                            self.Matrix[t][i][j] = self.temp_outside(t * self.ht)

                for door in self.doors:
                    for i in range(door.x_coords[0], door.x_coords[1]):
                        for j in range(door.y_coords[0], door.y_coords[1]):
                            self.Matrix[t][i][j] = self.base_temp


apartment = Apartment(
    celcius_to_kelvin(20),
    0.1,
    lambda t: celcius_to_kelvin(np.sin(t) + 10),
    (200, 100),
    0.1,
    1,
    0.01,
    int(6),
    int(4),
    int(3),
    int(5),
)

apartment.add_room(Room((2, 120), (2, 59)))
apartment.add_room(Room((2, 51), (63, 98)))
apartment.add_room(Room((55, 100), (63, 98)))
apartment.add_room(Room((104, 120), (63, 98)))
apartment.add_room(Room((124, 198), (42, 98)))
apartment.add_room(Room((124, 198), (2, 38)))
apartment.add_radiator(Radiator((2, 5), (10, 30), lambda i, j, t: 0.1))
apartment.add_window(Window((0, 1), (10, 40)))
apartment.add_window(Window((0, 1), (70, 85)))
apartment.add_window(Window((199, 200), (60, 90)))
apartment.simulate()

X = np.linspace(0, 200, 201)
Y = np.linspace(0, 100, 101)
Z, W = np.meshgrid(Y, X)
fig, axs = plt.subplots(3, 3, figsize=(10, 10), sharey=True)
axs[0, 0].pcolormesh(W, Z, apartment.Matrix[0])
axs[0, 1].pcolormesh(W, Z, apartment.Matrix[49])
axs[0, 2].pcolormesh(W, Z, apartment.Matrix[99])
plt.show()
