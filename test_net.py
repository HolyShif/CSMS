import unittest
import inet_check

class TestNetOn(unittest.TestCase):

    def test_google(self):
        self.assertTrue(inet_check.check_connection("www.google.com"))
    def test_yahoo(self):
        self.assertTrue(inet_check.check_connection("www.yahoo.com"))
    def test_adafruitio(self):
        self.assertTrue(inet_check.check_connection("www.adafruit.io"))

class TestNetOff(unittest.TestCase):

    def test_google(self):
        self.assertFalse(inet_check.check_connection("www.google.com"))
    def test_yahoo(self):
        self.assertFalse(inet_check.check_connection("www.yahoo.com"))
    def test_adafruitio(self):
        self.assertFalse(inet_check.check_connection("www.adafruit.io"))


if __name__ == '__main__':
    log_file = 'test_results/testnet.txt'
    f = open(log_file, "w")
    runner = unittest.TextTestRunner(f)
    unittest.main(testRunner=runner)
    f.close()
