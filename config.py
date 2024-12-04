
def addDatum(datum, globals, history, g):
    datum['start'] = "12:04"
    datum['end'] = "12:06"




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
}