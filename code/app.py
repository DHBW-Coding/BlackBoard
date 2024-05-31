from flask import Flask
from config import Config
from views import blackboard_bp
from logger import logger  # Import the logger to initialize it early

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(blackboard_bp, url_prefix='/v1')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, threaded=True)
