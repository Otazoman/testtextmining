from unittest import TestCase

import sys, os
sys.path.append('../') 
import sample

class TestSample(TestCase):
    """ test class of sample.py
    """
    def test_added(self):
        value1 = 2
        value2 = 6
        expected = 8
        actual = sample.tashizan(value1,value2)
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    main()
