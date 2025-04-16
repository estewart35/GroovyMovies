# core/routes/web.py
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from core.extensions import db
from core.models import Reviews
import requests
import os

web = Blueprint("web", __name__)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@web.route("/")
def home():
    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    movies = response.json().get('results', [])
    
    return render_template("index.html", user=current_user, movies=movies)


@web.route("/search", methods=['GET'])
def search_movie():
    query = request.args.get('query')
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
        'page': 1
    }
    response = requests.get(url, params=params)
    movies = response.json().get('results', [])
    
    return render_template("index.html", user=current_user, movies=movies, query=query)


@web.route("/movies/<int:movie_id>")
def movie_details(movie_id):
   url = f"{TMDB_BASE_URL}/movie/{movie_id}"
   params = {
      'api_key': TMDB_API_KEY,
      'language': 'en-US'
   }
   response = requests.get(url, params=params)
   movie = response.json()

   reviews = Reviews.query.filter_by(movie_id=movie_id).all()
   return render_template("movie_details.html", reviews=reviews, movie=movie, user=current_user)


@web.route("/profile")
@login_required
def profile():
   return render_template("profile.html", user=current_user)


@web.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
   current_user.username = request.form["username"]

   password = request.form["password"]
   if password:
      current_user.set_password(password)

   db.session.commit()
   flash("Profile updated successfully!", "success")
   return redirect(url_for("web.profile"))


@web.route("/your-reviews")
@login_required
def your_reviews():
   reviews = current_user.reviews
   unique_movie_ids = set(review.movie_id for review in reviews)

   movies = []
   for movie_id in unique_movie_ids:
      url = f"{TMDB_BASE_URL}/movie/{movie_id}"
      params = {
         'api_key': TMDB_API_KEY,
         'language': 'en-US'
      }
      response = requests.get(url, params=params)
      movie = response.json()
      movies.append(movie)

   return render_template("your_reviews.html", movies=movies, user=current_user)


@web.route("/reviews", methods=["POST"])
@login_required
def create_review():
   movie_id = int(request.form.get("movie_id"))
   label = request.form.get("label")
   rating = int(request.form.get("rating"))
   body = request.form.get("body")

   if not label:
       flash("Label is required!", "error")
       return redirect(url_for("web.movie_details", movie_id=movie_id))
   
   if not rating:
       flash("Rating is required!", "error")
       return redirect(url_for("web.movie_details", movie_id=movie_id))

   new_review = Reviews(label=label, rating=rating, body=body, movie_id=movie_id, user_id=current_user.id)
   db.session.add(new_review)
   db.session.commit()

   flash("Review created successfully!", "success")
   return redirect(url_for("web.movie_details", movie_id=movie_id))


@web.route("/reviews/<int:review_id>", methods=["POST"])
@login_required
def manage_review(review_id):
   action = request.form.get("action")
   review = Reviews.query.filter_by(id=review_id, user_id=current_user.id).first_or_404()

   if action == "delete":
      db.session.delete(review)
      db.session.commit()
      flash("Review deleted successfully!", "success")
   elif action == "update":
      label = request.form.get("label")
      rating = int(request.form.get("rating"))
      body = request.form.get("body")

      if not label:
         flash("Label is required!", "error")
         return redirect(url_for("web.movie_details", movie_id=review.movie_id))

      if not rating:
         flash("Rating is required!", "error")
         return redirect(url_for("web.movie_details", movie_id=review.movie_id))

      review.label = label
      review.rating = rating
      review.body = body
      db.session.commit()
      flash("Review updated successfully!", "success")
   else:
      flash("Invalid action.", "error")

   return redirect(url_for("web.movie_details", movie_id=review.movie_id))
