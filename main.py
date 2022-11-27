import json
import tkinter
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests

'''steamid voor test: 76561198147947505'''
def playersummaries(friendid):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={friendid}").json()
    for i in response['response']['players']:
        username = i['personaname']
        return(username)

def friendlist(steamid):
    lst =[]
    response = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&relationship=friend").json()
    for i in response['friendslist']['friends']:
        lst.append(i['steamid'])
    return lst

def gametime(steamid):
    lst = []
    response = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&format=json&include_appinfo=1').json()
    for i in response['response']['games']:
        naam = i['name']
        time = (i['playtime_forever'])
        dict = {
            'name': naam,
            'time': time
        }
        lst.append(dict)
    print(lst)
    return lst

def test(steamid):
    lst = []
    friends = friendlist(steamid)
    for x in friends:
        response = requests.get(
            f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={x}&format=json&include_appinfo=1').json()
        for i in response['response']['games']:
            naam = i['name']
            time = (i['playtime_forever'])
            dict = {
                'name': naam,
                'time': time
            }
            lst.append(dict)
    print(lst)


def totalgametimeallfriends(steamid):
    totaalgametime = []
    friends = friendlist(steamid)
    for x in friends:
        totaalgametime.append(gametime(f'{x}'))
    print(totaalgametime)
test('76561198147947505')

def steamdata():

    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    for i in data:
        lst.append(i['name'])
    return 'Eerste 5 spellen' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]
games = str(steamdata())

def sorteerdavgspeeltijd():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['average_playtime'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    return '5 Spellen met hoogste gemiddelde speeltijd' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]
avgspeeltijd = sorteerdavgspeeltijd()

def sorteerdmediaanspeeltijd():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['median_playtime'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    return data
mediaanspeeltijd = sorteerdmediaanspeeltijd()

def aantaleigenaars():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['median_playtime'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    print(lst)
    return 'Meeste eigenaars' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]


def maindashboard():
    root = tkinter.Tk()
    root.maxsize=('1200x1000')
    root.title('Dashboard')
    root.config(background='#0C6991')
    dashboard = Frame(root, width=1200, height= 100, bg ='#0C6991')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height= 100.,bg='#0C6991')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#0C6991')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(dashboard, text='Dashboard', bg='#0C6991', font=('Times New Roman', 18))
    hoofdmenu.grid(row=0, column=0)
    optie1 = Label(menubar, text='Optie1', bg='red',font=('Times New Roman', 18), width= 20)
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Label(menubar, text='Optie2', bg='blue',font=('Times New Roman', 18), width= 20)
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Label(menubar, text='Optie3', bg='green',font=('Times New Roman', 18), width= 20)
    optie3.grid(row=1, column=2, pady=5)
    optie4 = Label(menubar, text='Optie4', bg='purple',font=('Times New Roman', 18), width= 20)
    optie4.grid(row=1, column=3, pady=5)
    optie5 = Label(menubar, text='Optie5', bg='orange',font=('Times New Roman', 18), width= 20)
    optie5.grid(row=1, column=4, pady=5)
    optie6 = Label(menubar, text='Optie6', bg='yellow',font=('Times New Roman', 18), width= 20)
    optie6.grid(row=1, column=5, pady=5)
    test1 = Label(scherm, text =games, bg='#0C6991', font=('Times New Roman', 11), width = 20)
    test1.grid(row=2, column=0, pady=5)
    test2 = Label(scherm, text =avgspeeltijd, bg='#0C6991', font=('Times New Roman', 11))
    test2.grid(row=2, column=1, pady=5)
    test3 = Label(scherm, text =aantaleigenaars(), bg='#0C6991', font=('Times New Roman', 11))
    test3.grid(row=2, column=2, pady=5)
    grafiek1 = plt.Figure(figsize = (6, 10), dpi=60)
    ax1 = grafiek1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(grafiek1, scherm)
    bar1.get_tk_widget().grid(row=2, column = 4)
    spd = pd.DataFrame(mediaanspeeltijd)
    spd = spd[['name', 'median_playtime']].groupby('name').sum()
    spd.plot(kind='bar', legend=True, ax = ax1)
    ax1.set_title('Spel vs mediaan speeltijd')

    root.mainloop()


