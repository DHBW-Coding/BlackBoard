import sys
import os
import time
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BlackboardServer')))

from BlackboardServer.worker import BlackboardWorker

class TestBlackboardWorker(unittest.TestCase):

    def setUp(self):
        self.worker = BlackboardWorker()

    def test_create_blackboard(self):
        result = self.worker.create_bb('test_blackboard', 3600)
        self.assertEqual(result, 0)
        self.assertIn('test_blackboard', self.worker.blackboards)
    
    def test_create_blackboard_with_long_name(self):
        result = self.worker.create_bb('a'*33, 3600)
        self.assertEqual(result, 1)
    
    def test_create_duplicate_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        result = self.worker.create_bb('test_blackboard', 3600)
        self.assertEqual(result, 2)

    def test_delete_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        result = self.worker.delete_bb('test_blackboard')
        self.assertTrue(result)
        self.assertNotIn('test_blackboard', self.worker.blackboards)

    def test_delete_nonexistent_blackboard(self):
        result = self.worker.delete_bb('nonexistent_blackboard')
        self.assertFalse(result)

    def test_write_to_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        result = self.worker.writing_bb('test_blackboard', 'Hello, World!')
        self.assertEqual(result, 0)
        self.assertEqual(self.worker.blackboards['test_blackboard'].get_current_msg(), 'Hello, World!')

    def test_write_to_nonexistent_blackboard(self):
        result = self.worker.writing_bb('nonexistent_blackboard', 'Hello, World!')
        self.assertEqual(result, 2)

    def test_clear_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        self.worker.writing_bb('test_blackboard', 'Hello, World!')
        result = self.worker.clear_bb('test_blackboard')
        message, state = self.worker.read_bb('test_blackboard')
        self.assertEqual(state, 2)
        self.assertEqual(message, '')

    def test_clear_nonexistent_blackboard(self):
        result = self.worker.clear_bb('nonexistent_blackboard')
        self.assertFalse(result)

    def test_read_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        self.worker.writing_bb('test_blackboard', 'Hello, World!')
        message, state = self.worker.read_bb('test_blackboard')
        self.assertEqual(state, 0)
        self.assertEqual(message, 'Hello, World!')
    
    def test_read_sec_blackboard_message(self):
        self.worker.create_bb('test_blackboard', 3600)
        self.worker.writing_bb('test_blackboard', 'Hello, World1!')
        message, state = self.worker.read_bb('test_blackboard')
        self.assertEqual(state, 0)
        self.assertEqual(message, 'Hello, World1!')
        self.worker.writing_bb('test_blackboard', 'Hello, World2!')
        message, state = self.worker.read_bb('test_blackboard')
        self.assertEqual(state, 0)
        self.assertEqual(message, 'Hello, World2!')

    def test_read_empty_blackboard(self):
        self.worker.create_bb('test_blackboard', 3600)
        message, state = self.worker.read_bb('test_blackboard')
        self.assertEqual(state, 2)
        self.assertEqual(message, '')

    def test_get_blackboard_status(self):
        self.worker.create_bb('test_blackboard', 3600)
        status = self.worker.bb_status('test_blackboard')
        self.assertIsNotNone(status)

    def test_get_nonexistent_blackboard_status(self):
        status = self.worker.bb_status('nonexistent_blackboard')
        self.assertFalse(status)

    def test_delete_all_blackboards(self):
        self.worker.create_bb('test_blackboard1', 3600)
        self.worker.create_bb('test_blackboard2', 3600)
        result = self.worker.delete_all_bbs()
        self.assertTrue(result)
        self.assertEqual(len(self.worker.blackboards), 0)
    
    def test_read_blackboard(self):
        self.worker.create_bb('test_blackboard', 1)
        bb_dict = self.worker.bb_status('test_blackboard')
        self.assertFalse(bb_dict['bb_empty'])
        self.assertTrue(bb_dict['msg_valid'])
        self.assertIsInstance(bb_dict['msg_time'], int)
        time.sleep(2)
        bb_dict = self.worker.bb_status('test_blackboard')
        self.assertFalse(bb_dict['bb_empty'])
        self.assertFalse(bb_dict['msg_valid'])
        self.assertIsInstance(bb_dict['msg_time'], int)
    

if __name__ == '__main__':
    unittest.main()
