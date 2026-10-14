import unittest
from rente import Rent   

class TestRent(unittest.TestCase):
    def setUp(self):
        self.rent = Rent()

    def test_jaarlijkse_rente(self):
        self.assertEqual(self.rent.jaarlijkse_rente(5000, 0.25), 12.5)
        self.assertEqual(self.rent.jaarlijkse_rente(15000, 0.25), 37.5)
        self.assertEqual(self.rent.jaarlijkse_rente(30000, 0.1), 30.0)
        self.assertEqual(self.rent.jaarlijkse_rente(60000, 0.25), 150.0)
        self.assertEqual(self.rent.jaarlijkse_rente(150000, 0.5), 750.0)