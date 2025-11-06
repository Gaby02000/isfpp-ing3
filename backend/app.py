from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db import Base, engine, DATABASE_URL
from routes import api_bp
import os
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# Configurar CORS para permitir peticiones desde el frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})



# Configuración de la base de datos para Flask-Migrate
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Crear instancia de Flask-SQLAlchemy para Flask-Migrate
# Usamos el mismo Base que configuramos en db.py
db = SQLAlchemy(app, model_class=Base)

# Importar todos los modelos para que Flask-Migrate los detecte
# Los modelos deben usar el Base de db.py, no db.Model
from models import Seccion, Producto, Plato, Postre, Bebida, Sector, Mesa

# Configurar Flask-Migrate
# Flask-Migrate trabajará con el metadata de los modelos que usan Base
migrate = Migrate(app, db, directory='migrations')

# Solo crear tablas automáticamente en desarrollo (no recomendado para producción)
# En producción, usar migraciones: flask db upgrade
# Manejar errores de conexión de forma elegante
if os.getenv('FLASK_ENV') != 'production':
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/verificadas correctamente")
    except OperationalError as e:
        print(f"⚠️  No se pudo conectar a la base de datos: {e}")
        print("💡 Asegúrate de que PostgreSQL esté corriendo y la DATABASE_URL sea correcta")
        print(f"   DATABASE_URL actual: {DATABASE_URL}")

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=99, debug=True)
