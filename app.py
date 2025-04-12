# app.py
# A simple Flask application to demonstrate the basics of a web server.

# Flask is used to create and manage the web application.
from flask import Flask  

# This sets up the Flask app so you can define routes and handle requests.
app = Flask(__name__)  

# This defines the main route for the application. Routes map URLs to specific code.
@app.route("/")  
def hello():
	# This is the response sent back when someone visits the root URL.
	return "Hello World"  

# Running the app with debug mode makes it easier to test and develop.
# Debug mode reloads the app automatically when code changes and shows detailed error messages.
if __name__ == "__main__":
	app.run(debug=True)  