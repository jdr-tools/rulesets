import os, pytest, sys

os.environ['MONGODB_URL'] = 'mongodb://localhost:27017/arkaan_tests'

myPath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
sys.path.insert(0, myPath)

from rulesets import rulesets
