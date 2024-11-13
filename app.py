from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

# App config
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db = SQLAlchemy(app)
api = Api(app)

# Models

# Resources

if __name__ == "__main__":
    app.run(debug=True)