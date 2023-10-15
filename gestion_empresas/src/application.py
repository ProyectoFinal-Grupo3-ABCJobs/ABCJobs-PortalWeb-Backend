#import funtions as f
from flask import Flask, jsonify

application = Flask(__name__)
#data = f.load_file('./src/heroes.csv')

@application.route("/")
def index():
    return "Gestor Empresas nueva version",200
    #return jsonify(data)

@application.route("/ping")
def heroe():
    return "ping",200
    #return jsonify(data[id])

if __name__ == "__main__":
    application.run(host = "0.0.0.0", port = 5002, debug = True)