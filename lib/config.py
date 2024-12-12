import pydub
import pyaudio
from pydub.playback import play

def addDatum(datum, globals, history, g):
    #
    # Creates daniel-style chunk islands with words interconnected by occurence
    #
    chunkNode = g.addV('chunk')\
     .property('start',datum['start'])\
     .property('end',datum['end'])\
     .next()

    words = datum['text'].split(" ")
    wordVerts = []

    for i in range(len(words)):
        word = words[i]

        wordAlreadyExists = False
        for v in wordVerts:
            if v['word'] == word:
                wordV = v['v']
                wordAlreadyExists = True
                break

        if not wordAlreadyExists:
            wordV = g.addV('word')\
                        .property('word', word)\
                        .next()
            g.addE('partOf').property("strength", 1).from_(wordV).to(chunkNode).next()
            wordVerts.append({"v": wordV, "word": word} )

        if i != 0:
            previousWordV = [word for word in wordVerts if word["word"] == words[i-1]][0]['v']
            #edgeExists = g.V(previousWordV.id).out("partOf").hasId(wordV.id).hasNext()
            g.addE('follows').property("strength", 10).from_(previousWordV).to(wordV).next()
            
    return globals

def query(data, g):
    if (data['label'] == "chunk"):
        
        start = float( data['properties']['start'][0]['value'] )
        end = float( data['properties']['end'][0]['value'] )
        playAudio(start,end)

config = {
    "globals": {
        "counter": 0,
    },
    "input-suggestions": [
        'Max',
        'Lilli',
        'Pietro',
        'Maryam',
        'This is cool This is not cool',
    ],
    "addDatum": addDatum,
    "query": query
}

def playAudio(start, end): #in seconds
    startOffset = start % 1    
    sound = readAudioChunk(start)
    sound = sound[startOffset*1000:]

    second = math.floor(start)+1
    while True:
        print(second)
        chunk = readAudioChunk(second)
        if end-second < 1:
            if end-second > 0:
                sound += chunk [:(end-second)*1000]
            break
        else:
            sound += chunk
            second += 1

    play(sound)

    return {}