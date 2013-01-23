var marker;

function initializeMap()
{
	var initialLatLng = new google.maps.LatLng(33.889833, 35.492878); //Beirut by default
    var myOptions = {
      zoom: 15,
      center: initialLatLng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

	google.maps.event.addListener(map, 'click', function(point){
		currentLatLng = point.latLng;
		marker.setPosition(currentLatLng);
		document.getElementById("locationField").value = marker.getPosition().lat().toFixed(6) + ',' + marker.getPosition().lng().toFixed(6);
	});
	
	marker = new google.maps.Marker({
      position: initialLatLng, 
      map: map
  });
}