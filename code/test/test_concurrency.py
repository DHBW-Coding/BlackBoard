import unittest
from flask import Flask, request, jsonify
import sys
import os
import time
import unittest
import concurrent.futures

#to actually test this ramp up the maximum text size of the server to 1024*1024*1024 (1GB) (change worker.py wrinting_bb())

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BlackboardServer')))
from BlackboardServer.handlers import RequestHandler
import json


class TestRequestHandler(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.handler = RequestHandler()

        # Create routes for testing
        self.app.add_url_rule('/blackboards', 'list_blackboards', lambda: self.handler.list_blackboards('127.0.0.1'),
                              methods=['GET'])
        self.app.add_url_rule('/blackboards', 'delete_all_blackboards',
                              lambda: self.handler.delete_all_blackboards('127.0.0.1'), methods=['DELETE'])
        self.app.add_url_rule('/blackboards', 'create_blackboard',
                              lambda: self.handler.create_blackboard('127.0.0.1', request.json['name'],
                                                                     request.json['validity']), methods=['POST'])
        self.app.add_url_rule('/blackboards/<string:name>', 'delete_blackboard',
                              lambda name: self.handler.delete_blackboard('127.0.0.1', name), methods=['DELETE'])
        self.app.add_url_rule('/blackboards/<string:name>/message', 'read_blackboard',
                              lambda name: self.handler.read_blackboard('127.0.0.1', name), methods=['GET'])
        self.app.add_url_rule('/blackboards/<string:name>/status', 'get_blackboard_status',
                              lambda name: self.handler.get_blackboard_status('127.0.0.1', name), methods=['GET'])
        self.app.add_url_rule('/blackboards/<string:name>/clear', 'clear_blackboard',
                              lambda name: self.handler.clear_blackboard('127.0.0.1', name), methods=['POST'])
        self.app.add_url_rule('/blackboards/<string:name>/write', 'write_to_blackboard',
                              lambda name: self.handler.write_to_blackboard('127.0.0.1', name, request.json['message']),
                              methods=['POST'])

        self.client = self.app.test_client()

    def test_multi_write_read(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        #write testmessag to bb 'test_bb'
        for i in range(1,50):
            response = self.client.post('/blackboards/test_bb/write', json={'message': 'test message{i}'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {"message": "Success"})
            #read message from bb 'test_bb'
            response = self.client.get('/blackboards/test_bb/message')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json()['message'], 'test message{i}')
    
    def test_multi_write_read_concurrent(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        n_mb_size=1
        one_mb_ones = '1' * n_mb_size* (1024 * 1024)  # 1MB of '1's
        one_mb_zeros = '0' *n_mb_size* (1024 * 1024)  # 1MB of '0's


        def write_message(i):
            response = self.client.post(f'/blackboards/test_bb{i}/write', json={'message': one_mb_ones})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {"message": "Success"})
        def create_bb(i):
            self.client.post('/blackboards', json={'name': f'test_bb{i}', 'validity': 10})
            response = self.client.post(f'/blackboards/test_bb{i}/write', json={'message': one_mb_zeros})
            self.assertEqual(response.status_code, 200)


        def read_message(i):
            response = self.client.get(f'/blackboards/test_bb{i}/message')
            self.assertEqual(response.status_code, 200)
            message = response.get_json()['message']
            self.assertTrue(
           message == one_mb_ones or message == one_mb_zeros,
            f"Unexpected message: {message}"
        )

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            write=2
            read=20
            for i in range(1, write):
               create_bb(i)
            for i in range(1, write):
                for j in range(1, read):
                    futures.append(executor.submit(read_message, i))
                futures.append(executor.submit(write_message, i))
                for j in range(1, read):
                    futures.append(executor.submit(read_message, i))

            for future in concurrent.futures.as_completed(futures):
                future.result()






if __name__ == '__main__':
    unittest.main()