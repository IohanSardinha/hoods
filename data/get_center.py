import json

with open("polys3.json") as file:
    centers = []
    polygons = json.loads(file.read())
    for i, polygon in enumerate(polygons):
        lat = 0
        lng = 0
        for point in polygon["points"]:
            lat += point["lat"]
            lng += point["lng"]
        lat /= len(polygon["points"])
        lng /= len(polygon["points"])

        centers.append({
            "id":i,
            "center":{
            "lat":lat,
            "lng":lng
            }
        })
    
    with open("centers.json", "w") as f2:
        f2.write(json.dumps(centers))