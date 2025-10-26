from flask import Flask
from db import Base, engine
from routes import api_bp 

app = Flask(__name__)
Base.metadata.create_all(bind=engine)
app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=99, debug=True)
