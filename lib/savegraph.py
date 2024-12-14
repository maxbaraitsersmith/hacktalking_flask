import sys
from gremlin_python.driver.client import Client

from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import gremlin_python.driver.serializer as serializer

timestamp = sys.argv[1]

print(f"Requesting graph {timestamp} to be exported from the database")

#db_url = 'ws://localhost:8182/gremlin'
db_url = 'ws://dc-max.local:8182/gremlin'

connection = DriverRemoteConnection(db_url, 'g', message_serializer=serializer.GraphSONSerializersV3d0())
g = traversal().with_remote(connection)
g.V().property("timestamp", timestamp).iterate()

client = Client(db_url, 'g')
client.submit(f'graph.io(IoCore.graphson()).writeGraph("exports/{timestamp}.json")')