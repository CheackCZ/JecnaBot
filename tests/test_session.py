import sys
import os

# Add the 'src' directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from session import Session

import unittest

class TestOfSession(unittest.TestCase):
    pass