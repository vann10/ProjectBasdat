from flask import Flask
from app.routes.routes import routes
from app.routes.routesAbsensiSiswa import routesAbsensiSiswa
from app.routes.routesAbsensiGuru import routesAbsensiGuru
from app.routes.routesDataGuru import routesDataGuru
from app.routes.routesDataSiswa import routesDataSiswa
from app.routes.routesJadwal import routesJadwal
from app.routes.routesKelas import routesKelas
from app.routes.routesMapel import routesMapel
from app.routes.routesNilai import routesNilai
from app.routes.routesEvaluasi import routesEvaluasi
from app.routes.routesPembayaran import routesPembayaran
from dotenv import load_dotenv
import os

def create_app():
    # Load the environment variables from .env file
    load_dotenv()

    # Create the Flask app
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

    # Set the secret key using an environment variable
    app.config['SECRET_KEY'] = '1234'

    # Register the routes blueprint
    app.register_blueprint(routes)
    app.register_blueprint(routesAbsensiSiswa)
    app.register_blueprint(routesAbsensiGuru)
    app.register_blueprint(routesDataGuru)
    app.register_blueprint(routesDataSiswa)
    app.register_blueprint(routesJadwal)
    app.register_blueprint(routesKelas)
    app.register_blueprint(routesMapel)
    app.register_blueprint(routesNilai)
    app.register_blueprint(routesEvaluasi)
    app.register_blueprint(routesPembayaran)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
