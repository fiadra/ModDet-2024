import matplotlib as mpl
import matplotlib.pyplot as plt
import math as m
import numpy as np


def celcius_to_kelvin(t):
    return t + 273.15


def kelvin_to_celcius(t):
    if t == 0:
        return 0
    return t - 273.15


def turned_off_from_8AM_to_4PM(i, j, t):
    if t < 8:
        return 1500
    if 8 <= t and t < 16:
        return 0
    if 16 <= t:
        return 3000


def kelvin_to_celcius_matrix(A):
    return np.array([np.vectorize(kelvin_to_celcius)(xi) for xi in A])


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
    ):
        self.base_temp = base_temp
        self.coeff = coeff
        self.temp_outside = temp_outside
        self.size = size
        self.hx = hx
        self.T = T
        self.ht = ht
        self.n_timeslips = int(T / ht)
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

    def add_radiator(self, radiator):
        self.radiators.append(radiator)

    def add_window(self, window):
        self.windows.append(window)

    def add_door(self, door):
        self.doors.append(door)

    def avg_temperature(self, t):
        s, k = 0
        t_0 = int(np.floor(t / self.ht))
        for room in self.Rooms:
            for i in range(room.x_coords[0], room.x_coords[1]):
                for j in range(room.y_coords[0], room.y_coords[1]):
                    s += self.Matrix[t_0][i][j]
                    k += 1
        return s / k

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
                            self.Matrix[t][i][j] += self.ht * radiator.power(
                                i, j, t * self.ht
                            )

                for window in self.windows:
                    for i in range(window.x_coords[0], window.x_coords[1]):
                        for j in range(window.y_coords[0], window.y_coords[1]):
                            self.Matrix[t][i][j] = self.temp_outside(t * self.ht)

                for door in self.doors:
                    s = 0
                    if door.direction == "horizontal":
                        for i in range(door.x_coords[0], door.x_coords[1]):
                            avg_temp = (
                                self.Matrix[t][i][door.y_coords[0] - 1]
                                + self.Matrix[t][i][door.y_coords[1] + 1]
                            ) / 2
                            s += avg_temp
                        s = s / (door.x_coords[1] - door.x_coords[0])
                        for i in range(door.x_coords[0], door.x_coords[1]):
                            for j in range(door.y_coords[0], door.y_coords[1]):
                                self.Matrix[t][i][j] = s
                    if door.direction == "vertical":
                        for j in range(door.y_coords[0], door.y_coords[1]):
                            avg_temp = (
                                self.Matrix[t][door.x_coords[0] - 1][j]
                                + self.Matrix[t][door.x_coords[1] + 1][j]
                            ) / 2
                            s += avg_temp
                        s = s / (door.y_coords[1] - door.y_coords[0])
                        for i in range(door.x_coords[0], door.x_coords[1]):
                            for j in range(door.y_coords[0], door.y_coords[1]):
                                self.Matrix[t][i][j] = s


apartment1 = Apartment(
    celcius_to_kelvin(20),
    0.25,
    lambda t: celcius_to_kelvin(np.sin(np.pi * t / 12)),
    (100, 50),
    0.1,
    24,
    0.01,
)

### Pokoje ###

apartment1.add_room(Room((2, 65), (2, 29)))  # duży pokój
apartment1.add_room(Room((2, 26), (33, 48)))  # kuchnia
apartment1.add_room(Room((30, 45), (33, 48)))  # łazienka
apartment1.add_room(Room((50, 65), (33, 48)))  # łącznik
apartment1.add_room(Room((69, 98), (22, 48)))  # sypialnia
apartment1.add_room(Room((69, 98), (2, 18)))  # przedpokój

### Grzejniki ###

apartment1.add_radiator(
    Radiator((2, 5), (5, 15), turned_off_from_8AM_to_4PM)
)  # duży pokój
apartment1.add_radiator(
    Radiator((35, 40), (35, 38), turned_off_from_8AM_to_4PM)
)  # łazienka
apartment1.add_radiator(
    Radiator((95, 98), (30, 40), turned_off_from_8AM_to_4PM)
)  # sypialnia
apartment1.add_radiator(
    Radiator((90, 95), (16, 20), turned_off_from_8AM_to_4PM)
)  # przedpokój

### Okna ###

apartment1.add_window(Window((0, 1), (5, 20)))
apartment1.add_window(Window((0, 1), (35, 42)))
apartment1.add_window(Window((100, 101), (30, 45)))

### Drzwi ###

apartment1.add_door(Door((10, 20), (29, 32), "horizontal"))  # duży pokój i kuchnia
apartment1.add_door(Door((53, 63), (29, 32), "horizontal"))  # duży pokój i łącznik
apartment1.add_door(Door((46, 50), (35, 45), "vertical"))  # łącznik i łazienka
apartment1.add_door(Door((65, 69), (35, 45), "vertical"))  # łącznik i sypialnia
apartment1.add_door(Door((65, 69), (5, 15), "vertical"))  # duży pokój i przedpokój

apartment1.simulate()

apartment2 = Apartment(
    celcius_to_kelvin(20),
    0.25,
    lambda t: celcius_to_kelvin(np.sin(np.pi * t / 12) - 20),
    (100, 50),
    0.1,
    24,
    0.01,
)

### Pokoje ###

apartment2.add_room(Room((2, 65), (2, 29)))  # duży pokój
apartment2.add_room(Room((2, 26), (33, 48)))  # kuchnia
apartment2.add_room(Room((30, 45), (33, 48)))  # łazienka
apartment2.add_room(Room((50, 65), (33, 48)))  # łącznik
apartment2.add_room(Room((69, 98), (22, 48)))  # sypialnia
apartment2.add_room(Room((69, 98), (2, 18)))  # przedpokój

### Grzejniki ###

apartment2.add_radiator(
    Radiator((2, 5), (5, 15), turned_off_from_8AM_to_4PM)
)  # duży pokój
apartment2.add_radiator(
    Radiator((35, 40), (35, 38), turned_off_from_8AM_to_4PM)
)  # łazienka
apartment2.add_radiator(
    Radiator((95, 98), (30, 40), turned_off_from_8AM_to_4PM)
)  # sypialnia
apartment2.add_radiator(
    Radiator((90, 95), (16, 20), turned_off_from_8AM_to_4PM)
)  # przedpokój

### Okna ###

apartment2.add_window(Window((0, 1), (5, 20)))
apartment2.add_window(Window((0, 1), (35, 42)))
apartment2.add_window(Window((100, 101), (30, 45)))

### Drzwi ###

apartment2.add_door(Door((10, 20), (29, 32), "horizontal"))  # duży pokój i kuchnia
apartment2.add_door(Door((53, 63), (29, 32), "horizontal"))  # duży pokój i łącznik
apartment2.add_door(Door((46, 50), (35, 45), "vertical"))  # łącznik i łazienka
apartment2.add_door(Door((65, 69), (35, 45), "vertical"))  # łącznik i sypialnia
apartment2.add_door(Door((65, 69), (5, 15), "vertical"))  # duży pokój i przedpokój

apartment2.simulate()

apartment3 = Apartment(
    celcius_to_kelvin(20),
    0.25,
    lambda t: celcius_to_kelvin(np.sin(np.pi * t / 12) + 50),
    (100, 50),
    0.1,
    24,
    0.01,
)

### Pokoje ###

apartment3.add_room(Room((2, 65), (2, 29)))  # duży pokój
apartment3.add_room(Room((2, 26), (33, 48)))  # kuchnia
apartment3.add_room(Room((30, 45), (33, 48)))  # łazienka
apartment3.add_room(Room((50, 65), (33, 48)))  # łącznik
apartment3.add_room(Room((69, 98), (22, 48)))  # sypialnia
apartment3.add_room(Room((69, 98), (2, 18)))  # przedpokój

### Grzejniki ###

apartment3.add_radiator(
    Radiator((2, 5), (5, 15), turned_off_from_8AM_to_4PM)
)  # duży pokój
apartment3.add_radiator(
    Radiator((35, 40), (35, 38), turned_off_from_8AM_to_4PM)
)  # łazienka
apartment3.add_radiator(
    Radiator((95, 98), (30, 40), turned_off_from_8AM_to_4PM)
)  # sypialnia
apartment3.add_radiator(
    Radiator((90, 95), (16, 20), turned_off_from_8AM_to_4PM)
)  # przedpokój

### Okna ###

apartment3.add_window(Window((0, 1), (5, 20)))
apartment3.add_window(Window((0, 1), (35, 42)))
apartment3.add_window(Window((100, 101), (30, 45)))

### Drzwi ###

apartment3.add_door(Door((10, 20), (29, 32), "horizontal"))  # duży pokój i kuchnia
apartment3.add_door(Door((53, 63), (29, 32), "horizontal"))  # duży pokój i łącznik
apartment3.add_door(Door((46, 50), (35, 45), "vertical"))  # łącznik i łazienka
apartment3.add_door(Door((65, 69), (35, 45), "vertical"))  # łącznik i sypialnia
apartment3.add_door(Door((65, 69), (5, 15), "vertical"))  # duży pokój i przedpokój

apartment3.simulate()

norm = mpl.colors.Normalize(vmin=-1.0, vmax=1.0, clip=False)
X = np.linspace(0, 100, 101)
Y = np.linspace(0, 50, 51)
Z, W = np.meshgrid(Y, X)
# fig, axs = plt.subplots(3, 3, figsize=(10, 10), sharey=True)
# axs[0, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[1])))
# axs[0, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[1199])))
# axs[0, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[2399])))
# axs[1, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[1])))
# axs[1, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[1199])))
# axs[1, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[2399])))
# axs[2, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[1])))
# axs[2, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[1199])))
# axs[2, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[2399])))
# axs[0, 0].set_title("t = 0")
# axs[0, 1].set_title("t = 12")
# axs[0, 2].set_title("t = 24")
# axs[0, 0].set_ylabel("$T^{1}_{out}$")
# axs[1, 0].set_ylabel("$T^{2}_{out}$")
# axs[2, 0].set_ylabel("$T^{3}_{out}$")

fig, axs = plt.subplots(3, 3, figsize=(10, 10), sharey=True)
axs[0, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[799])))
axs[0, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[1599])))
axs[0, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment1.Matrix[2399])))
axs[1, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[799])))
axs[1, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[1599])))
axs[1, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment2.Matrix[2399])))
axs[2, 0].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[799])))
axs[2, 1].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[1599])))
axs[2, 2].pcolormesh(W, Z, norm(kelvin_to_celcius_matrix(apartment3.Matrix[2399])))
axs[0, 0].set_title("t = 8")
axs[0, 1].set_title("t = 16")
axs[0, 2].set_title("t = 24")
axs[0, 0].set_ylabel("$T^{1}_{out}$")
axs[1, 0].set_ylabel("$T^{2}_{out}$")
axs[2, 0].set_ylabel("$T^{3}_{out}$")


one_room_apartment_rad_next_to_window = Apartment(
    celcius_to_kelvin(20),
    0.25,
    lambda t: celcius_to_kelvin(5 * np.sin(t) - 100),
    (50, 50),
    0.1,
    24,
    0.01,
)

one_room_apartment_rad_next_to_window.add_room(Room((2, 48), (2, 48)))
one_room_apartment_rad_next_to_window.add_radiator(
    Radiator((3, 5), (20, 30), lambda i, j, t: 1000)
)
one_room_apartment_rad_next_to_window.add_window(Window((0, 2), (10, 40)))

one_room_apartment_rad_next_to_window.simulate()

one_room_apartment_rad_next_to_wall = Apartment(
    celcius_to_kelvin(20),
    0.25,
    lambda t: celcius_to_kelvin(5 * np.sin(t) - 100),
    (50, 50),
    0.1,
    24,
    0.01,
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
fig_one_room, axs_one_room = plt.subplots(2, 3, figsize=(10, 10), sharey=True)
axs_one_room[0, 0].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_window.Matrix[1])
)
axs_one_room[0, 1].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_window.Matrix[1199])
)
axs_one_room[0, 2].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_window.Matrix[2399])
)
axs_one_room[1, 0].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_wall.Matrix[1])
)
axs_one_room[1, 1].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_wall.Matrix[1199])
)
axs_one_room[1, 2].pcolormesh(
    W, Z, kelvin_to_celcius_matrix(one_room_apartment_rad_next_to_wall.Matrix[2399])
)
axs_one_room[0, 0].set_title("t = 0")
axs_one_room[0, 1].set_title("t = 12")
axs_one_room[0, 2].set_title("t = 24")
axs_one_room[0, 0].set_ylabel("Grzejnik przy oknie")
axs_one_room[0, 0].set_ylabel("Grzejnik przy ścianie")

plt.show()
