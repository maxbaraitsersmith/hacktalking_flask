from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import gremlin_python.driver.serializer as serializer

print(f"Clearing graph")

#db_url = 'ws://localhost:8182/gremlin'
db_url = 'ws://dc-max.local:8182/gremlin'

connection = DriverRemoteConnection(db_url, 'g', message_serializer=serializer.GraphSONSerializersV3d0())
g = traversal().with_remote(connection)
g.V().drop().iterate()