from flask import Blueprint, request
from handlers import RequestHandler

blackboard_bp = Blueprint('blackboard', __name__)
handler = RequestHandler()

@blackboard_bp.route('/blackboards', methods=['GET'])
def list_blackboards():
    client_ip = request.remote_addr
    return handler.list_blackboards(client_ip)

@blackboard_bp.route('/blackboards', methods=['DELETE'])
def delete_all_blackboards():
    client_ip = request.remote_addr
    return handler.delete_all_blackboards(client_ip)

@blackboard_bp.route('/blackboards/<blackboard_name>', methods=['POST'])
def create_blackboard(blackboard_name):
    client_ip = request.remote_addr
    data = request.get_json()
    validity = data.get('blackboardMessageValitdy')
    return handler.create_blackboard(client_ip, blackboard_name, validity)

@blackboard_bp.route('/blackboards/<blackboard_name>', methods=['DELETE'])
def delete_blackboard(blackboard_name):
    client_ip = request.remote_addr
    return handler.delete_blackboard(client_ip, blackboard_name)

@blackboard_bp.route('/blackboards/<blackboard_name>', methods=['GET'])
def read_blackboard(blackboard_name):
    client_ip = request.remote_addr
    return handler.read_blackboard(client_ip, blackboard_name)

@blackboard_bp.route('/blackboards/<blackboard_name>/status', methods=['GET'])
def get_blackboard_status(blackboard_name):
    client_ip = request.remote_addr
    return handler.get_blackboard_status(client_ip, blackboard_name)

@blackboard_bp.route('/blackboards/<blackboard_name>/clear', methods=['DELETE'])
def clear_blackboard(blackboard_name):
    client_ip = request.remote_addr
    return handler.clear_blackboard(client_ip, blackboard_name)

@blackboard_bp.route('/blackboards/<blackboard_name>/write', methods=['POST'])
def write_to_blackboard(blackboard_name):
    client_ip = request.remote_addr
    data = request.data.decode('utf-8')
    return handler.write_to_blackboard(client_ip, blackboard_name, data)
