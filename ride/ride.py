#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import time
import os.path

city = None


class City:
    def __init__(self, line):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad first line: '%s'" % line)
        self.rows = int(fields[0])
        self.columns = int(fields[1])
        self.cars = int(fields[2])
        self.rides = int(fields[3])
        self.bonus = int(fields[4])
        self.steps = int(fields[5])


class Ride:
    def __init__(self, index, line):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad ride line")
        self.a = int(fields[0])
        self.b = int(fields[1])
        self.x = int(fields[2])
        self.y = int(fields[3])
        self.start = int(fields[4])
        self.end = int(fields[5])
        self.index = index

    def __repr__(self):
        return str(self.index)

    def __len__(self):
        return abs(self.a - self.x) + abs(self.b - self.y)

    def key(self):
        '''Key for rides sorting'''
        return self.start


class Move:
    def __init__(self, car, ride):
        score = 0
        # date of the beginning of the ride
        begin = max(car.t + distance(car.x, car.y, ride.a, ride.b), ride.start)
        end = begin + len(ride)
        if begin == ride.start:
            score += city.bonus
        if end < ride.end:
            score += len(ride)
        self.ride = ride
        self.score = score
        self.a = car.x
        self.b = car.y
        self.x = ride.x
        self.y = ride.y
        self.start = car.t
        self.end = end
        self.value = float(self.score) / float(end - car.t)
        self.car = car

    def __repr__(self):
        return '<score car=%s, a=%s, b=%s, x=%s, y=%s, start=%s, end=%s>' % \
               (self.car, self.a, self.b, self.x, self.y, self.start, self.end)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.a == other.a and \
                   self.b == other.b and \
                   self.x == other.x and \
                   self.y == other.y and \
                   self.start == other.start and \
                   self.end == other.end
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class Car:
    def __init__(self, index):
        self.index = index
        self.moves = []
        self.x = 0
        self.y = 0
        self.t = 0

    def add(self, move):
        self.moves.append(move)
        self.x = move.x
        self.y = move.y
        self.t = move.end

    def __repr__(self):
        return "%s %s" % (str(len(self.moves)),
                          ' '.join([str(m.ride.index) for m in self.moves]))


def distance(a, b, x, y):
    return abs(x - a) + abs(y - b)


def parse(source):
    global city
    lines = source.strip().split('\n')
    city = City(lines[0])
    Move.city = city
    rides = []
    index = 0
    for line in lines[1:]:
        rides.append(Ride(index, line))
        index += 1
    # sort rides with start time
    rides = sorted(rides, key=Ride.key)
    return city, rides


def assign_rides_sort(rides):
    cars = [Car(i) for i in range(city.cars)]
    index = 0
    for ride in rides:
        car = cars[index]
        move = Move(car, ride)
        car.add(move)
        index = (index + 1) % city.cars
    return cars


def assign_rides_value(rides):
    cars = [Car(i) for i in range(city.cars)]
    remaining = rides[:]
    for ride in remaining:
        best = None
        for car in cars:
            if car.t < city.steps:
                move = Move(car, ride)
                if best is None or move.value > best.value or \
                    (move.value == best.value and move.end < best.end):
                    best = move
        remaining.remove(best.ride)
        best.car.add(best)
    return cars


def write_file(cars, file, output):
    result = ''
    for car in cars:
        result += str(car) + '\n'
    path = os.path.join(output, file[:-3] + '.out')
    with open(path, 'w') as stream:
        stream.write(result)


def compute_score(cars):
    score = 0
    for car in cars:
        for move in car.moves:
            score += move.score
    return score


def process_file(file, input, output):
    print('%s:' % file)
    start = time.time()
    path = os.path.join(input, file)
    with open(path) as stream:
        source = stream.read().strip()
    city, rides = parse(source)
    cars = assign(rides)
    duration = time.time() - start
    print("  duration: %.3fs" % duration)
    score = compute_score(cars)
    print("  score: %s" % score)
    write_file(cars, file, output)
    return score


def process_directory(input, output):
    files = sorted([
        f for f in os.listdir(input)
        if os.path.isfile(os.path.join(input, f)) and f.endswith('.in')
    ])
    score = 0
    report = ''
    for file in files:
        s = process_file(file, input, output)
        report += '%s %s\n' % ((file + ':').ljust(20), s)
        score += s
    report += '%s %s\n' % ('total:'.ljust(20), score)
    with open(os.path.join(output, 'README'), 'w') as stream:
        stream.write(report)
    print("total: %s" % score)


def main():
    if len(sys.argv) != 3:
        print("You must pass input and output directories")
    process_directory(sys.argv[1], sys.argv[2])


# assignation function for rides, possible values
# - assign_rides_sort
# - assign_rides_value
assign = assign_rides_sort

if __name__ == '__main__':
    main()
