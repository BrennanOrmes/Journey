var markersArray = []; // A 1D Array for holding one marker.
        
        function initMap() {
          var map = new google.maps.Map(document.getElementById('map'), {
            center: {lat: -34.397, lng: 150.644},
            zoom: 13
          });
          
          google.maps.event.addListener(map, 'click', function(event) {
            placeMarker(map, event.latLng);
            document.forms['formA'].elements['location'].value = event.latLng;
          });
          
          var infoWindow = new google.maps.InfoWindow({map: map});
  
          // Try HTML5 geolocation.
          if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
              var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };
  
              infoWindow.setPosition(pos);
              infoWindow.setContent('You are here.');
              map.setCenter(pos);
            }, function() {
              handleLocationError(true, infoWindow, map.getCenter());
            });
          } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());
          }
        }
  
        function handleLocationError(browserHasGeolocation, infoWindow, pos) {
          infoWindow.setPosition(pos);
          infoWindow.setContent(browserHasGeolocation ?
                                'Error: The Geolocation service failed.' :
                                'Error: Your browser doesn\'t support geolocation.');
        }
        
        function placeMarker(map, location) {
            var marker = new google.maps.Marker({
              position: location,
              map: map
            });
           
            clearOverlays();
            markersArray.push(marker);
            
            var infowindow = new google.maps.InfoWindow({
              content: 'Latitude: ' + location.lat() + '<br>Longitude: ' + location.lng()
            });
            infowindow.open(map,marker);
          }
          
        function clearOverlays() {
          for (var i = 0; i < markersArray.length; i++ ) {
            markersArray[i].setMap(null);
          }
          markersArray.length = 0;
          markersArray = [];
        }