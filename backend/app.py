from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"mensaje": "API de rotisería funcionando correctamente!"}

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 7000)))
