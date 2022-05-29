import json
import sys

if sys.argc < 3:
    print("usage: python change_data.py input.json output.json")

with open(sys.argv[1],"r") as f:
    data = json.loads(f.read())
    final = []
    print(data)
    for i in range(73):
        print(data[i]["Preu"])
        final.append({
            "id": data[i]["id"],
            "Preu": {
                "2014":data[i]["Preu"],
                "2015":data[i+73*0]["Preu"],
                "2016":data[i+73*1]["Preu"],
                "2017":data[i+73*2]["Preu"],
                "2018":data[i+73*3]["Preu"],
                "2019":data[i+73*4]["Preu"],
                "2020":data[i+73*5]["Preu"],
                "2021":data[i+73*6]["Preu"]
            },
            "PreuM2": {
                "2014":data[i]["PreuM2"],
                "2015":data[i+73*0]["PreuM2"],
                "2016":data[i+73*1]["PreuM2"],
                "2017":data[i+73*2]["PreuM2"],
                "2018":data[i+73*3]["PreuM2"],
                "2019":data[i+73*4]["PreuM2"],
                "2020":data[i+73*5]["PreuM2"],
                "2021":data[i+73*6]["PreuM2"]
            },
            "Codi_Districte": data[i]["Codi_Districte"],
            "Nom_Districte": data[i]["Nom_Districte"],
            "Nom_Barri": data[i]["Nom_Barri"]
        })
    with open(sys.argv[2], "w") as f2:
        f2.write(json.dumps(final))