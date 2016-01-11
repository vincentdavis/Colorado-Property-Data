from flask import Flask

app = Flask(__name__)
from app import ColoradoPropertyData

if __name__ == "__main__":
    app.run()