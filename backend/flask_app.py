# Este archivo es necesario para que Flask-Migrate funcione correctamente
# Flask-Migrate necesita una variable FLASK_APP que apunte a la aplicación

from app import app

if __name__ == '__main__':
    app.run()

