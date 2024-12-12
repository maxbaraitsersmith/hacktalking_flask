import numpy as np
from flask import Flask, request, render_template, jsonify
from flask import Flask
from flask_cors import CORS
import random
import json
from config import config
import math
import datetime
import time

from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import gremlin_python.driver.serializer as serializer
from gremlin_python.driver.client import Client

audioChunksPath = "../hacktalking_whisper/chunks"

#db_url = 'ws://localhost:8182/gremlin'
db_url = 'ws://dc-max.local:8182/gremlin'
if db_url:
    connection = DriverRemoteConnection(db_url, 'g', message_serializer=serializer.GraphSONSerializersV3d0())
    client = Client(db_url, 'g')
    g = traversal().with_remote(connection)
    g.V().drop().iterate()
else: g = Nonee

app = Flask(__name__) 
CORS(app)

data = []

initialised = False

@app.route("/")
def renderInput():
    return render_template('input.html')

@app.route("/audio")
def renderAudio():
    return render_template('audio.html')

@app.route("/addDatum", methods=['POST'])
def addDatum():
    datum = request.get_json()
    config['globals'] = config['addDatum'](datum, config['globals'], data, g)
    data.append(datum)
    return {}

@app.route("/getInputSuggestions", methods=['POST'])
def getInputSuggestions():
    return jsonify(config['input-suggestions'])

def readAudioChunk(second):
    second = int(math.floor(second))
    path = f'{audioChunksPath}/{math.floor(second)}.wav'
    return pydub.AudioSegment.from_wav(path)

@app.route("/query", methods=['POST'])
def query():
    data = request.get_json()
    config['query'](data, g)
    return {}

def initialise():
    print("Initialised")

@app.before_request
def do_something_whenever_a_request_comes_in():
    global initialised
    if not initialised:
        initialised = True
        initialise()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=False) #dev
    #app.run(host='0.0.0.0', port=5000) #prod
