import json

def meestgespeeld():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    for i in data:
        lst.append(i['name'])

    print(lst[0:5])
meestgespeeld()

print('League is gay')
print("hallo123")
print('kutgit')
print('123')
print("iets er achter")