#!/usr/bin/env python
# encoding: UTF-8

import unittest
from . import ride


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
        r = ride.Ride('0 0 1 3 2 9')
        self.assertEqual(r.a, 0)
        self.assertEqual(r.b, 0)
        self.assertEqual(r.x, 1)
        self.assertEqual(r.y, 3)
        self.assertEqual(r.start, 2)
        self.assertEqual(r.end, 9)

    def test_ride_len(self):
        r = ride.Ride('0 0 2 3 2 9')
        self.assertEqual(len(r), 5)
        r = ride.Ride('0 0 0 0 2 9')
        self.assertEqual(len(r), 0)

    def test_ride_score(self):
        c = ride.City('3 4 2 3 2 10')
        ride.Ride.city = c
        r = ride.Ride('0 0 2 3 2 9')
        self.assertEqual(r.score(0, 0, 0), (7, 2, 3, 7))
        r = ride.Ride('0 0 2 3 0 9')
        self.assertEqual(r.score(0, 0, 0), (7, 2, 3, 5))
        r = ride.Ride('0 0 2 3 0 1')
        self.assertEqual(r.score(0, 0, 0), (2, 2, 3, 5))
        r = ride.Ride('0 0 2 3 0 5')
        self.assertEqual(r.score(0, 0, 0), (2, 2, 3, 5))
        r = ride.Ride('0 0 2 3 0 6')
        self.assertEqual(r.score(0, 0, 0), (7, 2, 3, 5))
        # when car waits
        r = ride.Ride('0 0 2 3 2 8')
        self.assertEqual(r.score(0, 0, 0), (7, 2, 3, 7))


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


if __name__ == '__main__':
    unittest.main()
