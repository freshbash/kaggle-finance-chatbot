from flask import Flask, request, session
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_session import Session
# from data_structures import Queue
from string import Template
from dotenv import load_dotenv
import os

# os.environ["KAGGLE_CONFIG_DIR"] = os.path.join(os.getcwd(), "model")

# load_dotenv()
os.environ["KERAS_BACKEND"] = "jax"
os.environ["XLA_PYTHON_CLIENT_MEM_FRACTION"] = "1.00"

import keras
import keras_nlp
import jax
import kagglehub

print(keras_nlp.__version__)

# Download latest version
# path = kagglehub.model_download("bhashwar22/gemma-for-finance/keras/gemma-for-finance")

# print("Path to model files:", path)

# App config
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SESSION_TYPE"] = "filesystem"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
Session(app)
# db = SQLAlchemy(app)
api = Api(app)

# Models


# Resources
class Chat(Resource):
    def post(self):
        query = request.get_json().get("query")

        if query == "":
            return "It seems you accidentally pressed Return(Enter). Please ask a query so I can help you.", 200

        context = '''You are an intelligent personal finance assistant designed to help users understand various financial concepts. You are supposed to provide concise and easy-to-understand explanations for the requested questions, ensuring the users feel informed and confident about managing their money. If you receive any non-finance related query, please return the following response: \"Unrelated Topic\"'''

        query = "user: " + query
        
        if session.get("conversation_history", 0) == 0:
            session["conversation_history"] = []

        past_conv = session["conversation_history"][:6]

        conversation = "\n\n".join(past_conv)

        template = Template("""Context: $context\n\nPAST CONVERSATIONS:\n\n$past_conversations\n\nCURRENT QUERY:\n\n$current_query\n\nbot:""")
        
        prompt = template.substitute(context=context, past_conversations=conversation, current_query=query)

        print(f"Final prompt:\n\n{prompt}")

        # my_model = None

        # output = my_model.generate(prompt, max_length=256)

        # print(output)

        session["conversation_history"].append(query)
        print(f"Session: {session["conversation_history"]}")
        # session["conversation_history"].append(bot_response)

        return "OK", 200


api.add_resource(Chat, "/api/get_response")

if __name__ == "__main__":
    app.run(debug=True)
