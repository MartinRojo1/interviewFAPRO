from flask import Flask
import view as view

app = Flask(__name__)

app.register_blueprint(view.router)

if __name__ == "__main__":
    app.run(debug=True,port=63463)