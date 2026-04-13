import sys
import os
import json
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# test connection to the DB
DB_AVAILABLE   = False
TABLE_HAS_DATA = False
