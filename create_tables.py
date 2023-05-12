from myapp import create_app
from myapp.database.db import db

app, socketio = create_app()

# Adding this block to set up an application context
with app.app_context():
    db.create_all()
