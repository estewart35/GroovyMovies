# utilities.py

from models import Reviews

def initialize_db(app, db):
	"""
	Initializes the database by creating all the tables.
	"""
	with app.app_context():
		db.create_all()

def seed_db(app, db):
	"""
	Seeds the database with initial data if no data exists.
	"""
	with app.app_context():
		if Reviews.query.count() == 0:
			db.session.add_all(
            	[
                	Reviews(label="Okay", rating=3, body="Okay review"),
                	Reviews(label="Fantastic!", rating=5, body="Fantastic review"),
                	Reviews(label="Trash", rating=1, body="Trash Review"),
            	]
        	)
			db.session.commit()