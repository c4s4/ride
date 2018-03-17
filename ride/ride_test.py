#!/usr/bin/env python
# encoding: UTF-8

import unittest
from .ride import City, Ride, Car, Move, distance, parse


class CityTest(unittest.TestCase):

    def test_parse_city(self):
        expected = City(rows=3, cols=4, cars=2, rides=3, bonus=2, steps=10)
        actual = City.parse('3 4 2 3 2 10')
        self.assertEqual(expected, actual)

    def test_parse_bad_city(self):
        self.assertRaises(Exception, City.parse, 'foo')


class RideTest(unittest.TestCase):

    def test_parse_ride(self):
        city = City(rows=3, cols=4, cars=2, rides=3, bonus=2, steps=10)
        expected = Ride(index=0, a=0, b=0, x=1, y=3, start=2, end=9, city=city)
        actual = Ride.parse(index=0, line='0 0 1 3 2 9', city=city)
        self.assertEqual(expected, actual)

    def test_ride_len(self):
        city = City(rows=3, cols=4, cars=2, rides=3, bonus=2, steps=10)
        ride = Ride(index=0, a=0, b=0, x=2, y=3, start=2, end=9, city=city)
        self.assertEqual(ride.len(), 5)
        ride = Ride(index=0, a=0, b=0, x=0, y=0, start=2, end=9, city=city)
        self.assertEqual(ride.len(), 0)


class MoveTest(unittest.TestCase):

    def test_move(self):
        # optimal move
        city = City(rows=3, cols=4, cars=2, rides=3, bonus=2, steps=10)
        ride = Ride(index=0, a=0, b=0, x=2, y=3, start=0, end=6, city=city)
        car = Car(0)
        move = Move(car, ride)
        self.assertEqual(move.a, 0)
        self.assertEqual(move.b, 0)
        self.assertEqual(move.x, 2)
        self.assertEqual(move.y, 3)
        self.assertEqual(move.start, 0)
        self.assertEqual(move.end, 5)
        self.assertEqual(move.score, 7)
        #self.assertEqual(move.value, 7.0 / 5.0)
        # car waits for the ride
        ride = Ride(index=0, a=0, b=0, x=2, y=3, start=2, end=8, city=city)
        move = Move(car, ride)
        self.assertEqual(move.a, 0)
        self.assertEqual(move.b, 0)
        self.assertEqual(move.x, 2)
        self.assertEqual(move.y, 3)
        self.assertEqual(move.start, 0)
        self.assertEqual(move.end, 7)
        self.assertEqual(move.score, 7)
        #self.assertEqual(move.value, 7.0 / 7.0)
        # car starts after early beginning
        ride = Ride(index=0, a=0, b=0, x=2, y=3, start=0, end=8, city=city)
        car.x = 1
        move = Move(car, ride)
        self.assertEqual(move.a, 1)
        self.assertEqual(move.b, 0)
        self.assertEqual(move.x, 2)
        self.assertEqual(move.y, 3)
        self.assertEqual(move.start, 0)
        self.assertEqual(move.end, 6)
        self.assertEqual(move.score, 5)
        #self.assertEqual(move.value, 5.0 / 6.0)


class TestDistance(unittest.TestCase):

    def test_distance(self):
        self.assertEqual(distance(0, 0, 0, 0), 0)
        self.assertEqual(distance(0, 0, 1, 0), 1)
        self.assertEqual(distance(0, 0, -1, 0), 1)
        self.assertEqual(distance(0, 0, 1, 1), 2)
        self.assertEqual(distance(1, -1, 1, 3), 4)
        self.assertEqual(distance(0, 0, 2, 3), 5)


class ParseTest(unittest.TestCase):

    def test_parse(self):
        ecity = City(rows=3, cols=4, cars=2, rides=3, bonus=2, steps=10)
        ride_1 = Ride(index=0, a=0, b=0, x=1, y=3, start=2, end=9, city=ecity)
        ride_2 = Ride(index=1, a=0, b=0, x=1, y=1, start=1, end=9, city=ecity)
        city, rides = parse('3 4 2 3 2 10\n0 0 1 3 2 9\n0 0 1 1 1 9')
        self.assertEqual(ecity, city)
        self.assertEqual(2, len(rides))
        self.assertEqual(ride_1, rides[1])
        self.assertEqual(ride_2, rides[0])


if __name__ == '__main__':
    unittest.main()
