import sys
from gremlin_python.driver.client import Client

chunks_source_path = "/home/max/Type/DC/3_winter_2024-5/shared_understandings/git/hacktalking_whisper/chunks"
chunks_destination_path = "/home/max/Type/DC/3_winter_2024-5/shared_understandings/git/hacktalking_flask/chunks"

timestamp = sys.argv[0]

print(f"Requesting graph {timestamp} to be exported from the database")

#db_url = 'ws://localhost:8182/gremlin'
db_url = 'ws://dc-max.local:8182/gremlin'
client = Client(db_url, 'g')
client.submit(f'graph.io(IoCore.graphml()).writeGraph("exports/graph_{timestamp}.xml")')