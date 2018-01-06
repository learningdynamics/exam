#! /usr/bin/python3

import unittest
import pickle

from timeit import default_timer as timer
import sys

from ljal import AverageR


def run(todo, filename):
    for t in todo:
        print(t["msg"])
        start = timer()
        t["Rs"] = AverageR(t["n_samples"], t["fun"])
        end = timer()
        t["time"] = end - start
        # clean for pickling
        t["fun"] = None

    with open(filename, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(todo, f, pickle.HIGHEST_PROTOCOL)
