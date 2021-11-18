import unittest
import arribos

class MyTestCase(unittest.TestCase):
    def test_something(self):
        a,b = arribos.arr_t1_t2(5,100)
        print(a)
        self.assertEqual(b>100, True)

if __name__ == '__main__':
    unittest.main()
