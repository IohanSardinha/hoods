// Initialize and add the map
import polys from './polys.json';
import rent_data from "./rent_data.json";

// Given a polygon bounds, calculate its center
function calcPolyCenter(bounds){
    return {
        lat: (bounds.top + bounds.bottom) / 2,
        lng: (bounds.left + bounds.right) / 2,
    }
}

// Given a polygon bounds, return a new LatLngBounds item
function getLatLngBounds(bounds){
    let sw = new google.maps.LatLng(bounds.bottom, bounds.left);
    let ne = new google.maps.LatLng(bounds.top, bounds.right);
    return new google.maps.LatLngBounds(sw, ne);
}

function initMap() {
    // The location of Uluru
    const center = { lat: 41.3956224, lng: 2.1559663 };
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12.33,
        center: center,
    });

    const placesService = new google.maps.places.PlacesService(map);

    // Parameters for calls to places API
    const RADIUS = 1500;
    const TYPES = ["restaurant"];
    
    var hoods = [];

    let prices = [];
    
    for(let i = 0; i < 73; i++){
        let price = rent_data[String(i)]["Preu"];
        if(price != null) prices.push(price);
    }

    let min_price = Math.min(prices);
    let max_price = Math.max(prices);

    let i= 73*7;
    for(let poly of polys){
        
        let price = rent_data[String(i)]["Preu"];
        let price_range = (price - min_price) / (max_price-min_price);
        let color;
        if (price == null) color = "#555555";
        else color = "#" + (price_range*255).toString(16) + ((price_range-1)*255).toString(16) +"00";
        
        let draw = new google.maps.Polygon({
            paths: poly.points,
            strokeWeight: 1,
            fillColor:color
        });
        hoods.push(draw);
        
        let name = rent_data[String(i)]["Nom_Barri"];

        draw.addListener("mouseover", ()=>{
            console.log(name);
        });

        // listener that whenever we click on a polygon, adds to the map markers of nearby restaurants.
        draw.addListener("click", () => {
            let bounds = getLatLngBounds(poly.bounds);

            let request = {
                bounds: bounds,
                type: TYPES
            };

            // var avgRating = 0.0;
            // var restaurantCount = 0;

            placesService.nearbySearch(request, (res, status) => {
                if (status == google.maps.places.PlacesServiceStatus.OK) {
                    res.forEach(result => {
                        new google.maps.Marker({
                            position: result.geometry.location,
                            map,
                            title: "Hello World!",
                        });

                        // if(result.rating){
                        //     avgRating = avgRating + result.rating;
                        //     restaurantCount++;
                        // }
                    });
                }
            });

            // avgRating = avgRating / restaurantCount;
            // console.log("Average restaurant rating: ", avgRating);
        });

        draw.setMap(map);
        i++;
    }
    
    //let Codi_Barri = 56
    //hoods[Codi_Barri-1].setOptions({fillColor:"#FF0000"});
  }
  
  window.initMap = initMap;