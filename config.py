

def addDatum(datum, globals, history, g):
    words = datum['text'].split(" ")

    for i in range(len(words)):
        word = words[i]
        g.addV('word').property('word', word).property('start', datum['start']).property('end', datum['end']).property('counter', globals['counter']).iterate()
        if globals['counter'] > 0 and i > 0:
            newV = g.V().has('counter', globals['counter']).next()
            lastV = g.V().has('counter', globals['counter']-1).next()
            g.addE('.').from_(newV).to(lastV).next()
        globals['counter'] += 1

    return globals

def query(graph):
    query = """
        MATCH (a)-[]->(b)
        RETURN a.label
    """

    return output
    
config = {
    "globals": {
        "counter": 0,
    },
    "input-suggestions": [
        'Max',
        'Lilli',
        'Pietro',
        'Maryam',
    ],
    "addDatum": addDatum,
    "query": query,
}