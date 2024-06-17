from flask import Flask
from config import Config
from views import blackboard_bp
from logger import logger  # Import the logger to initialize it early
import signal
import sys

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blackboard_bp, url_prefix='/v1')
    return app

def signal_handler(sig, frame):
    print('Ctrl+C detected! Shutting down gracefully...')
    logger.info('Ctrl+C detected! Shutting down gracefully...')
    sys.exit(0)

if __name__ == '__main__':
    app = create_app()
    signal.signal(signal.SIGINT, signal_handler)
    try:
        app.run(host='0.0.0.0', port=3000, threaded=True)
    except KeyboardInterrupt:
        print('Server interrupted by user')
        logger.info('Server interrupted by Server Commandline')
        sys.exit(0)
