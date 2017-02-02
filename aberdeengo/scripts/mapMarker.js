// This is old code. Keep for now incase we need it for later. - B

var markers = []; // A 1D Array for holding one marker.
        
        function myMap() {
          var mapCanvas = document.getElementById("map");
          var myCenter=new google.maps.LatLng(51.508742,-0.120850); //Just a placeholder location for the map to load up.
          var mapOptions = {center: myCenter, zoom: 5};
          var map = new google.maps.Map(mapCanvas, mapOptions);
          google.maps.event.addListener(map, 'click', function(event) {
            deleteMarkers(); // Call this so when the user clicks again on the map it will remove there old marker.
            placeMarker(map, event.latLng);
          });
        }
        
        function placeMarker(map, location) {
          var marker = new google.maps.Marker({
            position: location,
            map: map
          });
          
          markers.push(marker);
          
          var infowindow = new google.maps.InfoWindow({
            content: 'Latitude: ' + location.lat() + '<br>Longitude: ' + location.lng()
          });
          infowindow.open(map,marker);
        }
        
        
        function clearMarkers(){
          setMapOnAll(null);
          setMapOnAll(map);
        }
        
        function deleteMarkers(){
            markers = [];
            clearMarkers();
        }