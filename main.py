import json
import tkinter
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import requests
from collections import Counter


'''steamid voor test: 76561198147947505'''
def playersummaries(friendid):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={friendid}").json()
    return response


def friendlist(steamid):
    lst =[]
    response = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&relationship=friend").json()
    for i in response['friendslist']['friends']:
        lst.append(i['steamid'])
    return lst

def friendsdata(steamid):
    friends = friendlist(steamid)
    for i in friends:
        return(playersummaries(i))


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
    return lst

def totalgametimeallfriends(steamid):
    totaalgametime = []
    friends = friendlist(steamid)
    for x in friends:
        try:
            data = gametime(x)
            totaalgametime.append(data)
        except KeyError:
            continue
    totalegametime = Counter()
    for d in totaalgametime:
        for j in d:
            totalegametime[j['name']] += j['time']
    return totalegametime

def meestgespeeldegames(steamid):
    gametime = totalgametimeallfriends(steamid)
    maximaal = sorted(gametime, key=gametime.get, reverse=True)[:5]
    return maximaal

def meestgespeeldegamestijd(steamid):
    games = meestgespeeldegames(steamid)
    lst =[]
    dict = {
        'game': [],
        'time': []
    }
    data = totalgametimeallfriends(steamid)
    for i in meestgespeeldegames(steamid):
        tijd = data[i]
        lst.append(tijd / 60)
    for i in lst:
        dict['time'].append(i)
    for x in games:
        dict['game'].append(x)
    return dict


#print(meestgespeeldegamestijd('76561198147947505'))

def steamdata():

    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    for i in data:
        lst.append(i['name'])
    return 'Eerste 5 spellen' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]

def sorteerdavgspeeltijd():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['average_playtime'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    return '5 Spellen met hoogste gemiddelde speeltijd' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]

def sorteerdmediaanspeeltijd():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['median_playtime'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    return 'Spellen met hoogste mediaan speeltijd' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]
def duurstespellen():
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    data = sorted(data, key=lambda i: i['price'], reverse=True)
    data = (data[0:6])
    for i in data:
        lst.append(i['name'])
    return 'Duurste Spellen' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]



def maindashboard():
    root = tkinter.Tk()
    root.attributes('-fullscreen',False)
    root.maxsize=('1200x1000')
    root.title('Dashboard')
    root.config(background='#1b2838')
    dashboard = Frame(root, width=1200, height= 100, bg ='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height= 100.,bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#171a21')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(dashboard, text='Dashboard', bg='#1b2838',fg ='#c7d5e0', font=('Times New Roman', 18))
    hoofdmenu.grid(row=0, column=0)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statestieken', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21',fg ='#c7d5e0',  font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    test1 = Label(scherm, text ='Hoofdscherm', bg='#1b2838', font=('Times New Roman', 11), width = 20)
    test1.grid(row=2, column=0, pady=5)
    root.mainloop()

def optie1dashboard():
    steamid = steamidentry.get()
    data1 = meestgespeeldegamestijd(steamid)
    df1 = pd.DataFrame(data1)
    root = tkinter.Tk()
    root.attributes('-fullscreen', False)
    root.maxsize = ('1200x1000')
    root.title('Statestieken')
    root.config(background='#1b2838')
    dashboard = Frame(root, width=1200, height=100, bg='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height=100., bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#171a21')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(dashboard, text='Statestieken', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    hoofdmenu.grid(row=0, column=0)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statestieken', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    figure1 = plt.Figure(figsize=(5, 8))
    ax1 = figure1.add_subplot(211)
    bar1 = FigureCanvasTkAgg(figure1, scherm)
    bar1.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    df1 = df1[['game', 'time']].groupby('game').sum()
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Vrienden speeltijd')
    root.mainloop()

def optie2dashboard():
    root = tkinter.Tk()
    root.attributes('-fullscreen', False)
    root.maxsize = ('1200x1000')
    root.title('Vrienden')
    root.config(background='#1b2838')
    dashboard = Frame(root, width=1200, height=100, bg='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height=100., bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#171a21')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(dashboard, text='Vrienden', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    hoofdmenu.grid(row=0, column=0)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statestieken', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 18), width=20,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    test1 = Label(scherm, text='Hoofdscherm', bg='#1b2838', font=('Times New Roman', 11), width=20)
    test1.grid(row=2, column=0, pady=5)
    root.mainloop()
    test1 = Label(scherm, text =sorteerdavgspeeltijd() , bg='#0C6991', font=('Times New Roman', 11), width = 50)
    test1.grid(row=2, column=0, pady=5)
    test2 = Label(scherm, text =duurstespellen(), bg='#0C6991', font=('Times New Roman', 11), width=50)
    test2.grid(row=2, column=1, pady=5)
    test3 = Label(scherm, text =sorteerdmediaanspeeltijd(), bg='#0C6991', font=('Times New Roman', 11), width=50)
    test3.grid(row=2, column=2, pady=5)
    root.mainloop()


def idcheck(steamid):
    lst = ['q', 'w', 'e', 'r', 't','y','u','i','o','p', 'a','s',
           'd','f','g','h', 'j','k','l','z','x','c','v','b','n','m']
    for x in steamid:
        if x in lst:
            root = tkinter.Tk()
            root.title('Steam')
            root.config(background='#1b2838')
            root.geometry = ('300x300')
            label1 = Label(root, text='Het steamid dat u heeft ingevoerd is niet juist', bg='#1b2838', fg='#c7d5e0',
                               font=('Times New Roman', 18))
            label1.pack(pady=150)
            break
        else:
            if len(steamid) == 17:
                maindashboard()
            else:
                root = tkinter.Tk()
                root.title('Steam')
                root.config(background='#1b2838')
                root.geometry = ('300x300')
                label1 = Label(root, text='Het steamid dat u heeft ingevoerd is niet juist', bg='#1b2838',fg ='#c7d5e0',  font=('Times New Roman', 18))
                label1.pack(pady=150)



root = tkinter.Tk()
root.title('Steam')
root.config(background='#1b2838')
root.geometry= ('300x300')
label1 = Label(root, text='Steamid:', bg='#1b2838',fg ='#c7d5e0',  font=('Times New Roman', 18))
label1.pack()
steamidentry = Entry(root, bg='White',fg ='#c7d5e0',  font=('Times New Roman', 18))
steamidentry.pack()
button = Button(root, text='Zie statestieken',bg='#1b2838',fg ='#c7d5e0',  font=('Times New Roman', 18), command=lambda: [root.iconify(), idcheck(steamidentry.get())])
button.pack()
root.mainloop()

