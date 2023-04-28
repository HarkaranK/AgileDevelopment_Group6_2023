from myapp import create_app
from myapp.auth.models import User
from myapp.database.db import db

import sys

app = create_app()

# Adding this block to set up an application context
with app.app_context():
    db.create_all()