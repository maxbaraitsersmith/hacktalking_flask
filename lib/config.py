
def addDatum(datum, globals, history, g):

    #
    # Listens for whisper chunk and connects it with all annotations according to timestamp
    # Then creates chunk node connected to the previous chunk and all other chunks with the same annotation
    #

    if datum['type'] == 'whisper':
        annotations = []
        historyLen = len(history)

        previousWhisperDatum = None
        i=0
        while True: #find last whisper datum
            if i < historyLen:
                previousDatum = history[historyLen-i-1]
                if previousDatum['type'] == 'whisper':
                    previousWhisperDatum = previousDatum
                    break
            else:
                break
            i += 1

        if previousWhisperDatum:
            i = 0;
            while True: #collect annotations for the last whisper datum
                if i < historyLen:
                    previousInputDatum = history[historyLen-i-1]
                    if previousInputDatum['type'] == 'input':
                        inputTime = previousInputDatum['timestamp']-globals['startRecordingTimestamp']
                        if inputTime > float(previousWhisperDatum['start']):
                            if inputTime < float(datum['start']):
                                annotations.append(previousInputDatum['text'])
                        else: 
                            break
                else:
                    break
                i += 1

            annotations = list(set(annotations)) #remove duplicates

            t = g.addV('chunk')\
            .property('counter', globals['counter'])\
            .property('start1',float(previousWhisperDatum['start']))\
            .property('end1',float(previousWhisperDatum['end']))\
            .property('text',previousWhisperDatum['text'])

            for annotation in annotations:
                t = t.property('annotation', annotation)
            chunkNode = t.next()

            if globals['counter'] != 0: #add edge to previous node
                g.V().has("counter", globals['counter']-1).as_("a").addE('.').from_("a").to(chunkNode).next()

            #add link to all other nodes with same annotation.
            for annotation in annotations:
                g.V().has("annotation",annotation).as_("a").addE(annotation).from_("a").to(chunkNode).iterate()

            globals['counter'] += 1


            #add connection to next chunk
            #add links to other annotated nodes

    return globals

config = {
    "globals": {
        "startRecordingTimestamp": 0,
        "counter": 0
    },
    "input-suggestions": [
    ],
    "addDatum": addDatum,
}

# def addDatum(datum, globals, history, g):
#     #
#     # Creates daniel-style chunk islands with words interconnected by occurence
#     #
#     chunkNode = g.addV('chunk')\
#      .property('start',datum['start'])\
#      .property('end',datum['end'])\
#      .next()

#     words = datum['text'].split(" ")
#     wordVerts = []

#     for i in range(len(words)):
#         word = words[i]

#         wordAlreadyExists = False
#         for v in wordVerts:
#             if v['word'] == word:
#                 wordV = v['v']
#                 wordAlreadyExists = True
#                 break

#         if not wordAlreadyExists:
#             wordV = g.addV('word')\
#                         .property('word', word)\
#                         .next()
#             g.addE('partOf').property("strength", 1).from_(wordV).to(chunkNode).next()
#             wordVerts.append({"v": wordV, "word": word} )

#         if i != 0:
#             previousWordV = [word for word in wordVerts if word["word"] == words[i-1]][0]['v']
#             #edgeExists = g.V(previousWordV.id).out("partOf").hasId(wordV.id).hasNext()
#             g.addE('follows').property("strength", 10).from_(previousWordV).to(wordV).next()
            
#     return globals