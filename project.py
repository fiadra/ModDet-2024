import matplotlib.pyplot as plt
import math as m
import numpy as np


def celcius_to_kelvin(t):
    return t + 273.15


def kelvin_to_celcius(t):
    return t - 273.15


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
    def __init__(self, x_coords, y_coords, direction):
        self.x_coords = x_coords
        self.y_coords = y_coords
        self.direction = direction


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
                    for i in range(room.x_coords[0], room.x_coords[1] + 1):
                        for j in range(room.y_coords[0], room.y_coords[1] + 1):
                            self.Matrix[t][i][j] = self.Matrix[t - 1][i][j] + (
                                self.coeff * self.ht / self.hx**2
                            ) * (
                                self.Matrix[t - 1][i + 1][j]
                                + self.Matrix[t - 1][i - 1][j]
                                + self.Matrix[t - 1][i][j - 1]
                                + self.Matrix[t - 1][i][j + 1]
                                - 4 * self.Matrix[t - 1][i][j]
                            )

                    for i in range(room.x_coords[0] - 1, room.x_coords[1] + 2):
                        self.Matrix[t][i][room.y_coords[0] - 1] = self.Matrix[t][i][
                            room.y_coords[0]
                        ]
                        self.Matrix[t][i][room.y_coords[1] + 1] = self.Matrix[t][i][
                            room.y_coords[1]
                        ]

                    for j in range(room.y_coords[0] - 1, room.y_coords[1] + 2):
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
                    if door.direction == "horizontal":
                        for i in range(door.x_coords[0], door.x_coords[1]):
                            avg_temp = (
                                self.Matrix[t][i][door.y_coords[0] - 1]
                                + self.Matrix[t][i][door.y_coords[1] + 1]
                            ) / 2
                            for j in range(door.y_coords[0], door.y_coords[1]):
                                self.Matrix[t][i][j] = avg_temp
                    if door.direction == "vertical":
                        for j in range(door.y_coords[0], door.y_coords[1]):
                            avg_temp = (
                                self.Matrix[t][door.x_coords[0] - 1][j]
                                + self.Matrix[t][door.x_coords[1] + 1][j]
                            ) / 2
                            for i in range(door.x_coords[0], door.x_coords[1]):
                                self.Matrix[t][i][j] = avg_temp


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

### Pokoje ###

apartment.add_room(Room((2, 120), (2, 59)))  # duży pokój
apartment.add_room(Room((2, 51), (63, 98)))  # kuchnia
apartment.add_room(Room((55, 100), (63, 98)))  # łazienka
apartment.add_room(Room((104, 120), (63, 98)))  # łącznik
apartment.add_room(Room((124, 198), (42, 98)))  # sypialnia
apartment.add_room(Room((124, 198), (2, 38)))  # przedpokój

### Grzejniki ###

apartment.add_radiator(Radiator((2, 5), (10, 30), lambda i, j, t: 1000))  # duży pokój
apartment.add_radiator(Radiator((70, 75), (68, 70), lambda i, j, t: 1000))  # łazienka
apartment.add_radiator(
    Radiator((195, 198), (60, 80), lambda i, j, t: 1000)
)  # sypialnia
apartment.add_radiator(
    Radiator((180, 190), (35, 38), lambda i, j, t: 1000)
)  # przedpokój

### Okna ###

apartment.add_window(Window((0, 1), (10, 40)))
apartment.add_window(Window((0, 1), (70, 85)))
apartment.add_window(Window((199, 200), (60, 90)))

### Drzwi ###

apartment.add_door(Door((20, 40), (59, 63), "horizontal"))  # duży pokój i kuchnia
apartment.add_door(Door((98, 118), (59, 63), "horizontal"))  # duży pokój i łącznik
apartment.add_door(Door((100, 104), (70, 90), "vertical"))  # łącznik i łazienka
apartment.add_door(Door((120, 124), (59, 63), "vertical"))  # łącznik i sypialnia
apartment.add_door(Door((120, 124), (10, 30), "vertical"))  # duży pokój i przedpokój

apartment.simulate()

X = np.linspace(0, 200, 201)
Y = np.linspace(0, 100, 101)
Z, W = np.meshgrid(Y, X)
fig, axs = plt.subplots(3, 3, figsize=(10, 10), sharey=True)
axs[0, 0].pcolormesh(W, Z, apartment.Matrix[0])
axs[0, 1].pcolormesh(W, Z, apartment.Matrix[49])
axs[0, 2].pcolormesh(W, Z, apartment.Matrix[99])

one_room_apartment_rad_next_to_window = Apartment(
    celcius_to_kelvin(20),
    0.1,
    lambda t: celcius_to_kelvin(5 * np.sin(t) - 100),
    (50, 50),
    0.1,
    10,
    0.01,
    int(6),
    int(4),
    int(3),
    int(5),
)

one_room_apartment_rad_next_to_window.add_room(Room((2, 48), (2, 48)))
one_room_apartment_rad_next_to_window.add_radiator(
    Radiator((3, 5), (20, 30), lambda i, j, t: 1000)
)
one_room_apartment_rad_next_to_window.add_window(Window((0, 2), (10, 40)))

one_room_apartment_rad_next_to_window.simulate()

one_room_apartment_rad_next_to_wall = Apartment(
    celcius_to_kelvin(20),
    0.1,
    lambda t: celcius_to_kelvin(5 * np.sin(t) - 100),
    (50, 50),
    0.1,
    10,
    0.01,
    int(6),
    int(4),
    int(3),
    int(5),
)
one_room_apartment_rad_next_to_wall.add_room(Room((2, 48), (2, 48)))
one_room_apartment_rad_next_to_wall.add_radiator(
    Radiator((46, 48), (20, 30), lambda i, j, t: 1000)
)
one_room_apartment_rad_next_to_wall.add_window(Window((0, 2), (10, 40)))

one_room_apartment_rad_next_to_wall.simulate()

X = np.linspace(0, 50, 51)
Y = np.linspace(0, 50, 51)
Z, W = np.meshgrid(Y, X)
fig_one_room, axs_one_room = plt.subplots(3, 3, figsize=(10, 10), sharey=True)
axs_one_room[0, 0].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_window.Matrix[0])
)
axs_one_room[0, 1].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_window.Matrix[499])
)
axs_one_room[0, 2].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_window.Matrix[999])
)
axs_one_room[1, 0].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_wall.Matrix[0])
)
axs_one_room[1, 1].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_wall.Matrix[499])
)
axs_one_room[1, 2].pcolormesh(
    W, Z, kelvin_to_celcius(one_room_apartment_rad_next_to_wall.Matrix[999])
)

plt.show()
