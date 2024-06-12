import unittest
from flask import Flask, request, jsonify
import os
import sys
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

    def test_list_blackboards(self):
        response = self.client.get('/blackboards')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Success"})

    def test_create_blackboard_success(self):
        response = self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Success"})

    def test_create_blackboard_invalid_parameters(self):
        response = self.client.post('/blackboards', json={'name': 'x' * 33, 'validity': 10})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid Parameters provided."})

    def test_create_blackboard_exists(self):
        self.client.post('/blackboards', json={'name': 'existing_bb', 'validity': 10})
        response = self.client.post('/blackboards', json={'name': 'existing_bb', 'validity': 10})
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.get_json(), {"error": "Blackboard already exists."})

    def test_delete_blackboard_success(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        response = self.client.delete('/blackboards/test_bb')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Success"})

    def test_delete_blackboard_not_found(self):
        response = self.client.delete('/blackboards/nonexistent_bb')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Blackboard not found."})

    def test_read_blackboard_success(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        self.client.post('/blackboards/test_bb/write', json={'message': 'test message'})
        response = self.client.get('/blackboards/test_bb/message')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], {"message": "test message"})

    def test_read_blackboard_not_found(self):
        response = self.client.get('/blackboards/nonexistent_bb/message')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Blackboard not found."})

    def test_read_blackboard_empty(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        response = self.client.get('/blackboards/test_bb/message')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Blackboard is empty."})

    def test_get_blackboard_status_not_found(self):
        response = self.client.get('/blackboards/nonexistent_bb/status')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Blackboard not found."})

    def test_clear_blackboard_success(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        response = self.client.post('/blackboards/test_bb/clear')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Success"})

    def test_clear_blackboard_not_found(self):
        response = self.client.post('/blackboards/nonexistent_bb/clear')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Blackboard not found."})

    def test_write_to_blackboard_success(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        response = self.client.post('/blackboards/test_bb/write', json={'message': 'test message'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Success"})

    def test_write_to_blackboard_invalid_parameters(self):
        self.client.post('/blackboards', json={'name': 'test_bb', 'validity': 10})
        response = self.client.post('/blackboards/test_bb/write', json={'message': 'x' * 256})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid Parameters provided."})

    def test_write_to_blackboard_not_found(self):
        response = self.client.post('/blackboards/nonexistent_bb/write', json={'message': 'test message'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Blackboard not found."})


if __name__ == '__main__':
    unittest.main()
