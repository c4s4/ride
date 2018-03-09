#!/usr/bin/env python
# encoding: UTF-8
'''
This is a sample source file for Python template project.
'''

import sys
from ride import City
from ride import Ride
from ride import main

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You must pass file on command line")
    main(sys.argv[1])
