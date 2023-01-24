import unittest
import simplequeue
import random

class MyTestCase(unittest.TestCase):
    def test_something(self):
        q = simplequeue.Queue(10)
        q.enqueue(10)
        x = q.dequeue()
        self.assertEqual(10, x)

    def test_automated(self):
        q = simplequeue.Queue(10)
        for i in range(100):
            if random.random() < 0.5:
                q.enqueue(1)
            else:
                x = q.dequeue()
            q.checkRep()




if __name__ == '__main__':
    unittest.main()
