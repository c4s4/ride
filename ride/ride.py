#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import time
import os.path


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

    index = 0
    city = None

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

    def __repr__(self):
        return str(self.index)

    def __len__(self):
        return abs(self.a - self.x) + abs(self.b - self.y)

    def key(self):
        '''Key for rides sorting'''
        return self.start

    def score(self, x, y, t):
        '''
        Compute score for a ride.
        Return:
        - score
        - x of arrival
        - y of arrival
        - time of arrival
        '''
        if self.city is None:
            raise Exception("City was not set in Ride class")
        score = 0
        # date of the beginning of the ride
        begin = max(t, self.start)
        end = begin + len(self)
        if begin == self.start:
            score += self.city.bonus
        if end < self.end:
            score += len(self)
        return score, self.x, self.y, end


class Car:
    def __init__(self, index):
        self.index = index
        self.rides = []

    def add(self, ride):
        self.rides.append(ride)

    def __repr__(self):
        return "%s %s" % (str(len(self.rides)),
                          ' '.join([str(r) for r in self.rides]))


def parse(source):
    lines = source.strip().split('\n')
    city = City(lines[0])
    Ride.city = city
    rides = []
    for line in lines[1:]:
        rides.append(Ride(line))
    # sort rides with start time
    rides = sorted(rides, key=Ride.key)
    return city, rides


def assign_rides(rides):
    cars = []
    for i in range(Ride.city.cars):
        cars.append(Car(i + 1))
    car = 0
    for r in rides:
        cars[car].add(r)
        car = (car + 1) % Ride.city.cars
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
        x, y, t = 0, 0, 0
        for ride in car.rides:
            s, x, y, t = ride.score(x, y, t)
            score += s
    return score


def process_file(file, input, output):
    print('%s:' % file)
    start = time.time()
    path = os.path.join(input, file)
    with open(path) as stream:
        source = stream.read().strip()
    city, rides = parse(source)
    cars = assign_rides(rides)
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
        report += '%s %s\n' % ((file+':').ljust(20), s)
        score += s
    report += '%s %s' % ('total:'.ljust(20), score)
    with open(os.path.join(output, 'README'), 'w') as stream:
        stream.write(report)
    print("total: %s" % score)


def main():
    if len(sys.argv) != 3:
        print("You must pass input and output directories")
    process_directory(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
