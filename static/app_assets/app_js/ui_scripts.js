$('input[type="submit"]').click(function(e) {
    e.preventDefault();
});

$(document).ready(function nearMeMap() {
    var mapProperties = {
        center: new google.maps.LatLng(-26.097576141357422, 28.050621032714844),
        zoom: 14,
    };
    var map = new google.maps.Map($('#nearMeMap'), mapProperties);
});