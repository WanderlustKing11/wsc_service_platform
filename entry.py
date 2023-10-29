from src import create_app
import os
from flask_cors import CORS

app = create_app()
cors = CORS(app, resources={r"/api/*": {"origins": "http://34.42.125.145:8080"}})
app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__":
    app.run(port=(os.environ.get("PORT", 8080)), host='0.0.0.0', debug=True)