import numpy as np
from flask import Flask, request, render_template, jsonify
import random
import json
from config import config

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
import gremlin_python.driver.serializer as serializer

connection = DriverRemoteConnection('ws://dc-max.local:8182/gremlin', 'g', message_serializer=serializer.GraphSONSerializersV3d0()) # The connection should be closed on shut down to close open connections with connection.close()
g = traversal().with_remote(connection) #traversal().withRemote(connection)
g.V().drop().iterate()

app = Flask(__name__) 
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
    datum = request.get_json()
    config['globals'] = config['addDatum'](datum, config['globals'], data, g)
    data.append(datum)
    return {}

@app.route("/getInputSuggestions", methods=['POST'])
def getInputSuggestions():
    return jsonify(config['input-suggestions'])