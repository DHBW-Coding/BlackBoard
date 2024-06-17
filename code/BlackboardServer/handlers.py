from flask import jsonify
from response_message import ResponseMessage
from models import Message, Blackboard
from worker import BlackboardWorker
import logging
from flask import Response, json
import json.decoder

logger = logging.getLogger('blackboard')

class RequestHandler:
    def __init__(self):
        self.worker = BlackboardWorker()

    def _create_response(self, response_message):
        response = jsonify(response_message.response_body)
        response.status_code = response_message.http_code
        return response

    def list_blackboards(self, ip):
        logger.info(f"{ip}: Listing all blackboards")
        blackboards = self.worker.get_bbs()
        return jsonify(blackboards)

    def delete_all_blackboards(self, ip):
        self.worker.delete_all_bbs()
        logger.info("Deleted all blackboards")
        return self._create_response(ResponseMessage.SUCCESS)

    def create_blackboard(self, ip, blackboard_name, validity):
        state = self.worker.create_bb(blackboard_name, validity)
        if state == 0:
            logger.info(f"{ip}: Created Blackboard '{blackboard_name}'")
            return self._create_response(ResponseMessage.SUCCESS)
        elif state == 1:
            logger.warning(f"{ip}: Invalid Parameters for Blackboard '{blackboard_name}'")
            return self._create_response(ResponseMessage.INVALID_PARAMETERS)
        elif state == 2:
            logger.info(f"{ip}: Blackboard '{blackboard_name}' already exists")
            return self._create_response(ResponseMessage.BB_EXISTS_ALREADY)

    def delete_blackboard(self, ip, blackboard_name):
        if not self.worker.delete_bb(blackboard_name):
            logger.warning(f"{ip}: Blackboard '{blackboard_name}' not found")
            return self._create_response(ResponseMessage.BB_NOT_FOUND)
        logger.info(f"{ip}: Blackboard '{blackboard_name}' deleted")
        return self._create_response(ResponseMessage.SUCCESS)

    def read_blackboard(self, ip, blackboard_name):
        message, state = self.worker.read_bb(blackboard_name)
        if state == 0:
            logger.info(f"{ip}: Reading blackboard '{blackboard_name}'")
            try:
                if isinstance(message, str):
                    message = json.loads(message)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON string: {e}")
                response = jsonify({"error": "Invalid JSON format"})
                response.status_code = 400
                return response
            response_data = json.dumps(message)

            response = Response(response=response_data, status=200, mimetype='application/json')
            return response
        if state == 1:
            logger.warning(f"{ip}: Blackboard '{blackboard_name}' not found")
            return self._create_response(ResponseMessage.BB_NOT_FOUND)
        if state == 2:
            logger.info(f"{ip}: Reading empty blackboard '{blackboard_name}'")
            return self._create_response(ResponseMessage.BB_IS_EMPTY)

    def get_blackboard_status(self, ip, blackboard_name):
        status = self.worker.bb_status(blackboard_name)
        if not status:
            logger.warning(f"{ip}: Blackboard '{blackboard_name}' not found")
            return self._create_response(ResponseMessage.BB_NOT_FOUND)
        logger.info(f"{ip}: Getting status of blackboard '{blackboard_name}'")
        response = jsonify(status)
        response.status_code = 200
        return response

    def clear_blackboard(self, ip, blackboard_name):
        if not self.worker.clear_bb(blackboard_name):
            logger.warning(f"{ip}: Blackboard '{blackboard_name}' not found")
            return self._create_response(ResponseMessage.BB_NOT_FOUND)
        logger.info(f"{ip}: Cleared blackboard '{blackboard_name}'")
        return self._create_response(ResponseMessage.SUCCESS)

    def write_to_blackboard(self, ip, blackboard_name, message): #200, 404 fehlt, 400 invalid parameters
        state = self.worker.writing_bb(blackboard_name, message)
        if state == 0:
            logger.info(f"{ip}: Wrote message to blackboard '{blackboard_name}'")
            return self._create_response(ResponseMessage.SUCCESS)
        if state == 1:
            logger.warning(f"{ip}: Invalid Parameters for Blackboard '{blackboard_name}'")
            return self._create_response(ResponseMessage.INVALID_PARAMETERS)
        if state == 2:
            logger.warning(f"{ip}: Blackboard '{blackboard_name}' not found")
            return self._create_response(ResponseMessage.BB_NOT_FOUND)
        