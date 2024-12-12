import sys
from gremlin_python.driver.client import Client

timestamp = sys.argv[1]

print(f"Requesting graph {timestamp} to be exported from the database")

#db_url = 'ws://localhost:8182/gremlin'
db_url = 'ws://dc-max.local:8182/gremlin'
client = Client(db_url, 'g')
client.submit(f'graph.io(IoCore.graphml()).writeGraph("exports/{timestamp}.xml")')