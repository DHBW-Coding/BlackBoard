import sys
import os
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BlackboardServer')))

from BlackboardServer.models import Message

class TestMessage(unittest.TestCase):

    def test_message_creation(self):
        message = Message('Hello, World!')
        self.assertEqual(message.get_text(), 'Hello, World!')
        self.assertIsInstance(message.get_time(), int)

    def test_message_to_string(self):
        message = Message('Hello, World!')
        message_str = message.to_string()
        self.assertTrue(message_str.endswith(':Hello, World!'))

if __name__ == '__main__':
    unittest.main()