$(document).ready(function(){
    console.log("loading")
    mapdata()
    heatmap()
})
var received_data = "{{data}}";
console.log(received_data);
var mymap = L.map('mapid').setView([-1.280,36.850], 12);
var AccessToken = "sk.eyJ1IjoiYnJheW8iLCJhIjoiY2themRqc3c0MDFsazJzdGNxeGp6eGp3ZyJ9.ojqrVzXOlf6oQlbV7yExiQ" //hii ni yangu but its set to localhost so haiezi tumika after deployment :)

// base layer 
// used Mapbox api for this layer 
// Find the documentation here:  https://docs.mapbox.com/api/maps/#static-tiles
var baseLayer = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYnJheW8iLCJhIjoiY2themRmcXFoMDByMTJ4cW92bXgxZ3JvOCJ9.POhBtURTuvIe4tTnYqo7Mw', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJheW8iLCJhIjoiY2themRmcXFoMDByMTJ4cW92bXgxZ3JvOCJ9.POhBtURTuvIe4tTnYqo7Mw'
})

//   getting data from backend
function mapdata(){  
    $.ajax({
        url : "./map/",
        method: "GET",
        success: function(response){
            // console.log(response)
            var response = $.parseJSON(JSON.stringify(response))
            $.each(response, function(index, element){//loop through each object and create a circle ....you can choose any other 
                var circle = L.circle([element.lat,element.long], {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.5,
                    radius: 1000
                }).addTo(mymap);//adding to map defined huko juu
                circle.bindPopup(element.hashtag);//binding popup....... to show when clicked 
            })
            
        },  
    })

}
// Adding the layer to map
mymap.addLayer(baseLayer)

// getting heatmap data
function heatmap(){
    var locations = []
    $.ajax({
        url : " {% url 'getmap'%}",
        method: "GET",
        success: function(response){
            // console.log(response)
            var response = $.parseJSON(JSON.stringify(response))

            for (var i=0; i< response.length; i++){
                var coord= []//array to hold lat, long and intensity....from backend 
                var x = response[i]
                // console.log(x.lat)
                coord.push(x.lat+0.001,x.long+0.050,x.count*10)//hii addition ni ujinga tu ..trying to get different locations
                locations.push(coord) //creating 2d array of coordinates and intensity(array within an array)
            }
            
        },  
    })
    // adding the layer 
    // find the documentation ya heatlayer hapa: http://bl.ocks.org/awoodruff/0883d211538ed05a82fd1b82bd65bf34
    var heatmapLayer = L.heatLayer(locations, {radius: 35});
    mymap.addLayer(heatmapLayer);

}
