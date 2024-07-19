from quart import Quart
from quart_cors import cors

from .routes import main  # Ensure your routes are adapted to use Quart

def create_app():
    app = Quart(__name__)
    cors(app)  # Setup CORS with Quart
    app.register_blueprint(main)

    return app