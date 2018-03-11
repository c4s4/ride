#!/usr/bin/env python
# encoding: UTF-8

import unittest
from . import ride

ride.city = ride.City('3 4 2 3 2 10')


class CityTest(unittest.TestCase):
    def test_parse_city(self):
        '''Test city parsing'''
        city = ride.City('3 4 2 3 2 10')
        self.assertEqual(city.rows, 3)
        self.assertEqual(city.columns, 4)
        self.assertEqual(city.cars, 2)
        self.assertEqual(city.rides, 3)
        self.assertEqual(city.bonus, 2)
        self.assertEqual(city.steps, 10)

    def test_parse_bad_city(self):
        self.assertRaises(Exception, ride.City, 'foo')


class RideTest(unittest.TestCase):
    def test_parse_ride(self):
        r = ride.Ride(0, '0 0 1 3 2 9')
        self.assertEqual(r.a, 0)
        self.assertEqual(r.b, 0)
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 3)
        self.assertEqual(r.start, 2)
        self.assertEqual(r.end, 9)

    def test_ride_len(self):
        r = ride.Ride(0, '0 0 2 3 2 9')
        self.assertEqual(len(r), 5)
        r = ride.Ride(1, '0 0 0 0 2 9')
        self.assertEqual(len(r), 0)


class MoveTest(unittest.TestCase):
    def test_move(self):
        ride.Move.city = ride.City('3 4 2 3 2 10')
        # optimal move
        r = ride.Ride(0, '0 0 2 3 0 6')
        c = ride.Car(0)
        m = ride.Move(c, r)
        self.assertEqual(m.a, 0)
        self.assertEqual(m.b, 0)
        self.assertEqual(m.x, 2)
        self.assertEqual(m.y, 3)
        self.assertEqual(m.start, 0)
        self.assertEqual(m.end, 5)
        self.assertEqual(m.score, 7)
        self.assertEqual(m.value, 7.0 / 5.0)
        # car waits for the ride
        r = ride.Ride(0, '0 0 2 3 2 8')
        m = ride.Move(c, r)
        self.assertEqual(m.a, 0)
        self.assertEqual(m.b, 0)
        self.assertEqual(m.x, 2)
        self.assertEqual(m.y, 3)
        self.assertEqual(m.start, 0)
        self.assertEqual(m.end, 7)
        self.assertEqual(m.score, 7)
        self.assertEqual(m.value, 7.0 / 7.0)
        # car starts after early beginning
        r = ride.Ride(0, '0 0 2 3 0 8')
        c.x = 1
        m = ride.Move(c, r)
        self.assertEqual(m.a, 1)
        self.assertEqual(m.b, 0)
        self.assertEqual(m.x, 2)
        self.assertEqual(m.y, 3)
        self.assertEqual(m.start, 0)
        self.assertEqual(m.end, 6)
        self.assertEqual(m.score, 5)
        self.assertEqual(m.value, 5.0 / 6.0)


class ParseTest(unittest.TestCase):
    def test_parse(self):
        city, rides = ride.parse('3 4 2 3 2 10\n0 0 1 3 2 9\n0 0 1 1 1 9')
        # check city
        self.assertEqual(city.rows, 3)
        self.assertEqual(city.columns, 4)
        self.assertEqual(city.cars, 2)
        self.assertEqual(city.rides, 3)
        self.assertEqual(city.bonus, 2)
        self.assertEqual(city.steps, 10)
        # check rides order
        self.assertEqual(rides[0].index, 1)
        self.assertEqual(rides[1].index, 0)


class TestDistance(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(ride.distance(0, 0, 0, 0), 0)
        self.assertEqual(ride.distance(0, 0, 1, 0), 1)
        self.assertEqual(ride.distance(0, 0, -1, 0), 1)
        self.assertEqual(ride.distance(0, 0, 1, 1), 2)
        self.assertEqual(ride.distance(1, -1, 1, 3), 4)
        self.assertEqual(ride.distance(0, 0, 2, 3), 5)


if __name__ == '__main__':
    unittest.main()
