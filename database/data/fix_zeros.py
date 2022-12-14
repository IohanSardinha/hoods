import json
import sys

if sys.argc < 3:
    print("usage: python change_data.py input.json output.json")


with open(sys.argv[1],"r") as f:
    data = json.loads(f.read())
    #for j in range(10):
    for i in range(73):
        for year in range(2014,2022):
            if data[i]["Preu"][str(year)] == 0:
                for next_year in range(year+1, 2022):
                    if not data[i]["Preu"][str(next_year)] == 0:
                        data[i]["Preu"][str(year)] = data[i]["Preu"][str(next_year)]
                        break

            if data[i]["Preu"][str(year)] == 0:
                for prev_year in range(year, 2013, -1):
                    if not data[i]["Preu"][str(prev_year)] == 0:
                        data[i]["Preu"][str(year)] = data[i]["Preu"][str(prev_year)]
                        break

            if data[i]["PreuM2"][str(year)] == 0:
                for next_year in range(year+1, 2022):
                    if not data[i]["PreuM2"][str(next_year)] == 0:
                        data[i]["PreuM2"][str(year)] = data[i]["PreuM2"][str(next_year)]
                        break
                    
            if data[i]["PreuM2"][str(year)] == 0:
                for prev_year in range(year, 2013, -1):
                    if not data[i]["PreuM2"][str(prev_year)] == 0:
                        data[i]["PreuM2"][str(year)] = data[i]["PreuM2"][str(prev_year)]
                        break
        

    
            
        
    with open(sys.argv[2], "w") as f2:
        f2.write(json.dumps(data))