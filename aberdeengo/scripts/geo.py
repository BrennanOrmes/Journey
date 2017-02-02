from geopy import geocoders

#This stuff might not be needed, if the events can be added the way I intend it to, 
#then we will not have to worry about user input. 

g = geocoders.GoogleV3(domain="google.maps.uk")

place, location = g.geocode(u"Aberdeen, Scotland".encode('utf-8'))

#For test purposes
print place 
print location 