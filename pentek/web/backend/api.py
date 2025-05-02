from flask import Flask
from flask_cors import CORS
from web.backend.routes import api_routes
from web.backend.socketio_instance import socketio

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])
socketio.init_app(app)

app.register_blueprint(api_routes, url_prefix='/api')

@app.route('/')
def home():
    return "Pentesting Web App Backend Running!"

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
