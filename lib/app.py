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
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import T

import pydub
import pyaudio
from pydub.playback import play
import math

db_url = 'ws://localhost:8182/gremlin'
#db_url = 'ws://dc-max.local:8182/gremlin'
if db_url:
    connection = DriverRemoteConnection(db_url, 'g', message_serializer=serializer.GraphSONSerializersV3d0())
    g = traversal().with_remote(connection)
    #g.V().drop().iterate()

    client = Client(db_url,'g')
    client.submit("""
        mgmt = graph.openManagement()
        mgmt.makePropertyKey('annotation').dataType(String).cardinality(LIST).make();
        mgmt.commit()
    """) #this must be run first time after the graph is created, otherwise the cardinality will be auto set to SINGLE
    
else: g = None

app = Flask(__name__) 
CORS(app)

data = []
randomWalking = False

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

@app.route("/startRecordingTimestamp", methods=['POST'])
def startRecordingTimestamp():
    datum = request.get_json()['ts']
    config['globals']['startRecordingTimestamp'] = datum
    return {}

@app.route("/getInputSuggestions", methods=['POST'])
def getInputSuggestions():
    return jsonify(config['input-suggestions'])

def randomWalk(data, g):
    global randomWalking

    if (data['label'] == "chunk"):
        if not randomWalking:
            print("Started random walk")
            randomWalking = True
            _id = data['id']
            while randomWalking:
                connectedNodes = g.V().hasId(_id).both().where(__.not_(__.hasId(_id))).toList()
                connectedNodes = list(set(connectedNodes)) #remove duplicates
                rand = random.choice(connectedNodes)
                props = g.V(rand).elementMap().toList()
                playChunk(props[0])
                _id = props[0][T.id]

        else:
            print("Ended random walk")
            randomWalking = False

def playChunk(data):
    if 'timestamp' in data:
        audioChunksPath = 'data/'+data['timestamp']+'/chunks'
    else:
        audioChunksPath = '../hacktalking_whisper/chunks'
    playAudio(data['start1'],data['end1'], audioChunksPath)

def readAudioChunk(second,audioChunksPath):
    second = int(math.floor(second))
    path = f'{audioChunksPath}/{math.floor(second)}.wav'
    return pydub.AudioSegment.from_wav(path)


def playAudio(start, end, audioChunksPath): #in seconds
    startOffset = start % 1    
    sound = readAudioChunk(start, audioChunksPath)
    sound = sound[startOffset*1000:]

    second = math.floor(start)+1
    while True:
        chunk = readAudioChunk(second,audioChunksPath)
        if end-second < 1:
            if end-second > 0:
                sound += chunk [:(end-second)*1000]
            break
        else:
            sound += chunk
            second += 1

    play(sound)

    return {}

@app.route("/query", methods=['POST'])
def query():
    data = request.get_json()
    randomWalk(data, g)
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
