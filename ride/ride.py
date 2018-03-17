#!/usr/bin/env python
# encoding: UTF-8

import os
import sys
import time
import os.path


class EqualMixin:

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class City(EqualMixin):

    @staticmethod
    def parse(line):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad first line: '%s'" % line)
        return City(
            rows=int(fields[0]),
            cols=int(fields[1]),
            cars=int(fields[2]),
            rides=int(fields[3]),
            bonus=int(fields[4]),
            steps=int(fields[5]))

    def __init__(self, rows, cols, cars, rides, bonus, steps):
        self.rows = rows
        self.cols = cols
        self.cars = cars
        self.rides = rides
        self.bonus = bonus
        self.steps = steps


class Ride(EqualMixin):

    @staticmethod
    def parse(index, line, city):
        fields = line.split(' ')
        if len(fields) != 6:
            raise Exception("Bad ride line: '%s'" % line)
        return Ride(
            index=index,
            a=int(fields[0]),
            b=int(fields[1]),
            x=int(fields[2]),
            y=int(fields[3]),
            start=int(fields[4]),
            end=int(fields[5]),
            city=city)

    def __init__(self, index, a, b, x, y, start, end, city):
        self.index = index
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.start = start
        self.end = end
        self.city = city

    def len(self):
        return distance(self.a, self.b, self.x, self.y)

    def key(self):
        return self.start


class Car(EqualMixin):

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

    def __str__(self):
        return "%s %s" % (str(len(self.moves)),
                          ' '.join([str(m.ride.index) for m in self.moves]))


class Move(EqualMixin):

    def __init__(self, car, ride):
        self.car = car
        self.ride = ride
        self.a = car.x
        self.b = car.y
        self.x = ride.x
        self.y = ride.y
        self.start = car.t
        score = 0
        begin = max(car.t + distance(car.x, car.y, ride.a, ride.b), ride.start)
        end = begin + ride.len()
        if begin <= ride.start:
            score += ride.city.bonus
        if end <= ride.end:
            score += ride.len()
        self.end = end
        self.score = score
        self.value = float(score) / float(end - car.t) - (0.1*end) / city.steps


def distance(a, b, x, y):
    return abs(x - a) + abs(y - b)


def parse(source):
    global city
    lines = source.strip().split('\n')
    city = City.parse(lines[0])
    Move.city = city
    rides = []
    index = 0
    for line in lines[1:]:
        rides.append(Ride.parse(index, line, city))
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
    for car in cars:
        while car.t < city.steps and len(remaining) > 0:
            best = None
            for ride in remaining:
                move = Move(car, ride)
                if best == None or best.value < move.value:
                    best = move
            remaining.remove(best.ride)
            car.add(best)
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
    _, rides = parse(source)
    cars = assign(rides)
    duration = time.time() - start
    print("  duration: %.3fs" % duration)
    score = compute_score(cars)
    print("  score: %s" % score)
    sys.stdout.flush()
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


# cars assignation:
# - assign_rides_sort
# - assign_rides_value
assign = assign_rides_sort

if __name__ == '__main__':
    main()
