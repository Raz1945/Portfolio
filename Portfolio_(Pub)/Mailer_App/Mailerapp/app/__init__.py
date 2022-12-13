# Para ejecutar la aplicación, puede usar el comando Flask o el interruptor de 'Python -m Flask run'. 
# Antes de que pueda hacer eso, debe decirle a su terminal la aplicación con la que trabajará 
# exportando la FLASK_APP variable de entorno:
        # $ set FLASK_APP='nombre'.py
        # $ flask run ($ Python -m Flask 

# Algunos comandos:
    # python -m flask --app app/__init__ --debug run
    # python -m flask init-db

import os

from flask import Flask 

# create_app es util a la hora de crear distintas instancias
def create_app():
    # Inicio de la Aplicacion
    app = Flask(__name__)

    # Variable de Entorno
    app.config.from_mapping(
        SECRET_KEY ='aSf3@5;]fasd/.',
        
        SENDGRID_KEY=os.environ.get('SENDGRID_API_KEY'),

        FROM_EMAIL=os.environ.get('FROM_EMAIL'),

        DATABASE_HOST=os.environ.get('MYSQL_HOST'),
        DATABASE_USER=os.environ.get('MYSQL_USER'),
        DATABASE_PASSWORD=os.environ.get('MYSQL_PASSWORD'),
        DATABASE=os.environ.get('MYSQL_DATABASE'),
    )
    
    # Importo la funcion creada init-db
    from . import db
    db.init_app(app)

    # Importo Blueprint
    from. import mail
    app.register_blueprint(mail.bp)

    # index
    @app.route('/')
    def index():
        return '<h1>Index Page</h1>'

    # Inicio de sesión
    return app
    
        


