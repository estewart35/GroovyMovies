# app.py
# A simple Flask application to demonstrate the basics of a web server.

# Flask is used to create and manage the web application.
from flask import Flask, render_template, jsonify
from livereload import Server
from dotenv import load_dotenv
import os

# This makes our .env file available to use
# override=True makes sure it isn’t cached if we update it later.
load_dotenv(override=True)

# Importing our models and utilities
from models import db, Reviews
from utilities import initialize_db, seed_db

# Detect environment 
environment = os.getenv("ENV", "production")

# This sets up the Flask app so you can define routes and handle requests.
app = Flask(__name__) 
app.config["DEBUG"] = environment == "development"

# Setting up our database connections
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bind db to app
db.init_app(app)

# This defines the main route for the application. Routes map URLs to specific code.
@app.route("/")  
def hello():
	# This is the response sent back when someone visits the root URL.
	return render_template("index.html") 


# Let's add a rest api endpoint to retrieve our notes
@app.route("/api/reviews", methods=["GET"])
def get_notes():
	try:
		reviews = Reviews.query.all()
		return jsonify([{"id": n.id, "label": n.label, "rating": n.rating, "body": n.body} for n in reviews])
	except Exception as e:
		return jsonify({"error": "Unable to fetch reviews"}), 500
	

# Running the app with debug mode makes it easier to test and develop.
# Debug mode reloads the app automatically when code changes and shows detailed error messages.
if __name__ == "__main__":
	initialize_db(app, db)
	seed_db(app, db)
	
	server = Server(app.wsgi_app)
	server.watch("static/*")  # Watch template files for changes
	server.watch("templates/*")  # Watch template files for changes
	server.serve(port=5000)  # Start the server with live reload