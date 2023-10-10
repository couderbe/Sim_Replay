from src.main.python.tools.queue import Queue
import unittest


class QueueTest(unittest.TestCase):
    def test_queue_full(self):
        queue = Queue(5)
        queue.add(0)
        queue.add(1)
        queue.add(2)
        queue.add(3)
        queue.add(4)
        queue.add(5)
        self.assertEqual(queue.get_values(),[1,2,3,4,5])
        self.assertEqual(queue.get_size(),5)