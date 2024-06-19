import sys
import os
import time
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BlackboardServer')))

from BlackboardServer.models import Blackboard

class TestBlackboard(unittest.TestCase):

    def setUp(self):
        self.blackboard = Blackboard('test_blackboard', 3600)

    def test_blackboard_creation(self):
        self.assertEqual(self.blackboard.name, 'test_blackboard')
        self.assertTrue(self.blackboard.msg_valid())

    def test_set_and_get_message(self):
        self.blackboard.set_current_msg('Hello, World!')
        self.assertEqual(self.blackboard.get_current_msg(), 'Hello, World!')

    def test_blackboard_to_dict(self):
        self.blackboard.set_current_msg('Hello, World!')
        bb_dict = self.blackboard.to_dict()
        self.assertFalse(bb_dict['bb_empty'])
        self.assertTrue(bb_dict['msg_valid'])
        self.assertIsInstance(bb_dict['msg_time'], int)
    
    def test_blackboard_to_dict(self):
        self.blackboard= Blackboard('test_blackboard', 1)
        bb_dict = self.blackboard.to_dict()
        self.assertTrue(self.blackboard.msg_valid()==True)
        time.sleep(2)  # Wait for the message to expire
        self.assertTrue(self.blackboard.msg_valid()==False)

if __name__ == '__main__':
    unittest.main()
