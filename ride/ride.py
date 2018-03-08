#!/usr/bin/env python
# encoding: UTF-8

import sys


class City:

    def __init__(self, line):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad first line: '%s'" % line)
        self.rows = int(fields[0])
        self.columns  = int(fields[1])
        self.cars =  int(fields[2])
        self.rides = int(fields[3])
        self.bonus = int(fields[4])
        self.steps = int(fields[5])


class Ride:

    index = 0

    def __init__(self, line):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad ride line")
        self.a = int(fields[0])
        self.b = int(fields[1])
        self.x = int(fields[2])
        self.y = int(fields[3])
        self.start = int(fields[4])
        self.end = int(fields[5])
        self.index = Ride.index
        Ride.index += 1
    
    def __len__(self):
        return abs(self.a - self.x) + abs(self.b - self.y)

    def key(self):
        '''Key for rides sorting'''
        return self.start
    
    def __repr__(self):
        return str(self.index)


class Car:

    def __init__(self, index):
        self.index = index
        self.rides = []

    def add(self, ride):
        self.rides.append(ride)

    def __repr__(self):
        return "%s %s" % (str(len(self.rides)), ' '.join([str(r) for r in self.rides]))

def parse(source):
    lines = source.strip().split('\n')
    city = City(lines[0])
    rides = []
    for line in lines[1:]:
        rides.append(Ride(line))
    # sort rides with start time
    rides = sorted(rides, key=Ride.key)
    return city, rides


def assign(city, rides):
    cars = []
    for i in range(city.cars):
        cars.append(Car(i+1))
    car = 0
    for r in rides:
        cars[car].add(r)
        car = (car + 1) % city.cars
    return cars


def main(file):
    with open(file) as stream:
        source = stream.read().strip()
    city, rides = parse(source)
    cars = assign(city, rides)
    for car in cars:
        print(car)
