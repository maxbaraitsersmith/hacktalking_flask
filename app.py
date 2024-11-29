import numpy as np
from flask import Flask, request, render_template, jsonify
import random
import json
from config import config

app = Flask(__name__) 
graph = nx.Graph()
data = []

initialised = False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False) #dev
    #app.run(host='0.0.0.0', port=5000) #prod

def initialise():
    print("Initialised")

@app.before_request
def do_something_whenever_a_request_comes_in():
    global initialised
    if not initialised:
        initialised = True
        initialise()

@app.route("/")
def renderTemplate():
    return render_template('input.html')

@app.route("/addDatum", methods=['POST'])
def addDatum():
    global graph
    datum = request.get_json()
    config['globals'], graph = config['addDatum'](datum, config['globals'], graph, data)
    data.append(datum)
    return {}

@app.route("/getInputSuggestions", methods=['POST'])
def getInputSuggestions():
    return jsonify(config['input-suggestions'])