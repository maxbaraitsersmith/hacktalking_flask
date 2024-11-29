from grandcypher import GrandCypher

def addDatum(datum, globals, graph, history):
    nodeID = globals['counter']

    graph.add_nodes_from([(nodeID,{
        "label": datum['text'],
        "start": datum['start'],
        "start": datum['end'],
    }) ] )

    globals['counter'] += 1

    return [globals, graph]

def query(graph):
    query = """
        MATCH (a)-[]->(b)
        RETURN a.label
    """

    cypher = GrandCypher(graph)
    output = cypher.run(query)
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