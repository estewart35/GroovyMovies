# app.py
from core import create_app
from livereload import Server
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(override=True)

# Detect environment
environment = os.getenv("ENV", "production")

# Create the Flask app using the factory
app = create_app(environment)

if __name__ == "__main__":
	# Use livereload for development environment
	if environment == "development":
		server = Server(app.wsgi_app)
		server.watch("core/**/*.py")
		server.watch("core/**/*.html")
		server.watch("core/**/*.css")
		server.serve(port=5000)  # Start the server with livereload
	else:
		# Run in standard mode for production
		app.run(port=5000)