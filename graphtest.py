from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
import gremlin_python.driver.serializer as serializer

db_url = 'ws://localhost:8182/gremlin'
g = traversal().with_remote(DriverRemoteConnection(db_url,'g', message_serializer=serializer.GraphSONSerializersV3d0()))

#g.addV('word')

#print( g.V().both().name.to_list() )
#query = g.V(4216).values('newprop').toList()
query = g.V().toList()
#query = g.addV('person').property('name','stephen').next()
print(query)