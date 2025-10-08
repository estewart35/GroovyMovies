# 📌 Groovy Movies

> A movie review platform where users can search films from a movie database, read details, and contribute their own ratings and reviews to share opinions with others.

---

## 🚀 Live Demo  
[View Project](https://groovy-movies.up.railway.app/)

---

## ✨ Features  
- User authentication with secure registration and login for personalized reviews
- Integration with The Movie Database (TMDb) API to fetch up-to-date movie information
- Full CRUD functionality for creating, editing, deleting, and viewing movie reviews

---

## 🛠️ Tech Stack  
- **Frontend:** Jinja2 Templates, Bootstrap
- **Backend:** Flask, Python
- **Database:** Postgres
- **Hosting:** Railway (backend & database)
- **APIs:** The Movie Database (TMDB) API

---

## 📸 Screenshots  
![Screenshot 1](https://raw.githubusercontent.com/estewart35/dev-portfolio/main/public/mockups/groovymovies_mockup_dark.svg)

---

## ⚡ Getting Started (Flask)

Clone the repo:  
```bash
git clone https://github.com/estewart35/GroovyMovies.git
cd GroovyMovies
```

Optionally, create and activate a virtual environment to isolate dependencies (recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

Create a `.env` file in the project root and add the required environment variables:
```bash
# .env
ENV=development
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URI=postgresql://username:password@host:port/database_name
SECRET_KEY=your_secret_key
TMDB_API_KEY=your_tmdb_api_key
```
*(Refer to `.env.example` in the repo for variable names.)*

Install dependencies and run locally:
```bash
pip install -r requirements.txt
flask run
```
