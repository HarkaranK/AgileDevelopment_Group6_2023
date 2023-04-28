from myapp import create_app
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
from myapp.auth.models import User
from myapp.database.db import db

import sys

=======
from myapp.database.db import db

>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
from myapp.database.db import db

>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
=======
from myapp.database.db import db

>>>>>>> 97281a16867be91c438e72be78e8cbbdac1a0671
app = create_app()

# Adding this block to set up an application context
with app.app_context():
    db.create_all()