import worldnews as wn
from time import sleep
print "Starting Aggregator"
print "India:"
wn.main('india')
print "Sleeping for 60 seconds"
sleep(60)
print "WorldNews:"
wn.main('worldnews')
print "Sleeping for 30 seconds"
sleep(30)
print "Technology"
wn.main('technology')
print "Sleeping for 30 seconds"
sleep(30)
print "Science"
wn.main('science')
print "Aggregation Complete"
