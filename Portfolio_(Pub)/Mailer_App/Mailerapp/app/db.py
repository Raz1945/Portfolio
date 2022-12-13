import mysql.connector

# from decouple import config

import click

from flask import current_app, g

from flask.cli import with_appcontext

from .schema import instructions

# 'click' perimite ejecutar comandos en al terminal
# current.. mantiene la seccion activa
# g lo usamos para almacenar variables, en este caso para almacenar el usuario 

def get_db():
    # sino se encuentra entonces se crea la nueva propiedad "db" que se almacenara dentro de 'g'
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['DATABASE_HOST'],
            password=current_app.config['DATABASE_PASSWORD'],
            user=current_app.config['DATABASE_USER'], 
            database=current_app.config['DATABASE'],
        )

        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Funcion init-db (comando)
def init_db():
    db, c = get_db()

    for i in instructions: # Las instrucciones estan en schema.py
        c.execute(i)
    
    db.commit()

# 'init-db' es el nombre que le damos al comando de la funcion creada anteriormente
#  para ejecutar el comando python -m flask init-db
@click.command('init-db') 
@with_appcontext

def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)    