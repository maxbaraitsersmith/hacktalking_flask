import numpy as np
import networkx as nx
from flask import Flask, request, render_template, jsonify
import random
import json
from config import config
import matplotlib.pyplot as plt

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
    plotGraph()
    return {}

@app.route("/getInputSuggestions", methods=['POST'])
def getInputSuggestions():
    return jsonify(config['input-suggestions'])


def plotGraph():
    pos = nx.spring_layout(graph, scale=1)
    plt.clf()
    nodesWithData = graph.nodes(data="label")
    labels = dict((x, y) for x, y in nodesWithData) #convert list of tuples to list of dicts
    nx.draw(graph, pos,with_labels=True, labels=labels)
    edge_labels = nx.get_edge_attributes(graph,'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels = edge_labels)
    plt.show()