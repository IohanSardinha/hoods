import json

min_left = 10000
min_down = 10000
max_right = -10000
max_up = -10000


with open('polys.json', 'r') as f:
    ob = json.load(f)
    for i in ob:
        print(i)
        b = i['bounds']
        if b['left'] < min_left:
            min_left = b['left']

        if b['right'] > max_right:
            max_right = b['right']

        if b['top'] > max_up:
            max_up = b['top']
        
        if b['bottom'] < min_down:
            min_down = b['bottom']


print(f'up{max_up}')
print(f'down{min_down}')
print(f'right{max_right}')
print(f'left{min_left}')
