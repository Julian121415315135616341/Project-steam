import json
import tkinter
from operator import itemgetter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import matplotlib.pyplot as plt
import requests
from collections import Counter
from tkinter import *
import PIL.Image
import PIL.ImageTk




'''steamid voor test: 76561199040375838'''

def playersummaries(friendid):
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={friendid}").json()
    return response

def playername(steamid):
    lst = []
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={steamid}").json()
    for i in response['response']['players']:
        lst.append(i['personaname'])
    return lst[0]

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

def onlinevrienden(steamid):
    online = []
    busy = []
    offline =[]
    away = []
    snooze = []
    vriendenlijst = friendlist(steamid)
    for i in vriendenlijst:
        data = playersummaries(i)
        if data['response']['personastate'] == 0:
            offline.append(data['response']['personaname'])
    return offline

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
def ownedgames(steamid):
    lst = []
    response = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&format=json&include_appinfo=1').json()
    for i in response['response']['games']:
        lst.append(i['name'])
    return lst

def ownedgamesallfriends(steamid):
    lst = []
    friends = friendlist(steamid)
    for i in friends:
        try:
            games = ownedgames(i)
            for x in games:
                lst.append(x)
        except:
            continue
    freqs = {}
    for i in lst:
        if i in freqs:
            freqs[i] += 1
        else:
            freqs[i] = 1
    try:
        del freqs["Tom Clancy's Rainbow Six Siege - Test Server"]
    except:
        gay = True

    res = dict(sorted(freqs.items(), key=itemgetter(1), reverse=True)[:5])
    lstname = []
    lstamount = []
    for i in res.keys():
        lstname.append(i)
    for y in res.values():
        lstamount.append(y)
    dicteigenaar = {
        'game': [],
        'aantal': []
    }
    for i in lstname:
        dicteigenaar['aantal'].append(str(i))
    for x in lstamount:
        dicteigenaar['game'].append(str(x))
    return dicteigenaar


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



def steamdata():

    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    for i in data:
        lst.append(i['name'])
    return 'Eerste 5 spellen' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]

def steamreviews():
    bestand = open('steam.json')
    data = json.load(bestand)
    dictreviews = {
                   }
    for i in data:
        if i['positive_ratings'] + i['negative_ratings'] > 3000:
            positief = i['positive_ratings']
            negatief = i['negative_ratings']
            positiefprocent = positief / (positief + negatief) * 100
            positiefprocent = round(positiefprocent, 2)
            teupdaten = {i['name']: positiefprocent}
            dictreviews.update(teupdaten)
    res = dict(sorted(dictreviews.items(), key=itemgetter(1), reverse=True)[:5])
    res2 = list(res.items())
    return res2


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

def zelfdespellenowned(steamid, friendid):
    lst =[]
    mijngames = ownedgames(steamid)
    vriendgames = ownedgames(friendid)
    for x in mijngames:
        if x in vriendgames:
            lst.append(x)
    return lst
def zelfdespellengui(steamid, friendid):
    root2 = tkinter.Tk()
    root2.maxsize = ('700x350')
    root2.title('Games')
    root2.config(background='#1b2838')
    data = zelfdespellenowned(steamid, friendid)
    label1= Label(root2, text=(f'Spellen die {playername(steamid)} en {playername(friendid)} allebei hebben:'), bg='#1b2838', font=('Times New Roman', 18), anchor='center')
    label1.pack(padx=250, pady= 20)
    text = Text(root2, bg='#1b2838')
    text.tag_configure("center", justify='center')
    text.pack(padx=250)
    for i in data:
        text.insert(END, i +'\n')
    text.tag_add("center", "1.0", "end")



def maindashboard():
    root = tkinter.Toplevel()
    data = steamreviews()
    root.attributes('-fullscreen',True)
    root.maxsize=('1200x1000')
    root.title('Dashboard')
    root.config(background='#1b2838')
    image = PIL.Image.open('steamlogo2.png')
    resized_image = image.resize((1200, 100))
    converted_image = PIL.ImageTk.PhotoImage(resized_image)
    dashboard = Frame(root, width=1200, height= 100, bg ='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height= 100.,bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#1b2838')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(master=dashboard, image=converted_image, width=1200, height=100, bg ='#1b2838')
    hoofdmenu.grid(row=0, column=10)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21',fg ='#c7d5e0',  font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy()])
    stoppen.grid(row=1, column=3, pady=5)
    test1 = Label(scherm, text='Hoofdscherm', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    test1.grid(row=2, column=0, pady=5)
    label2 = Label(scherm, text=sorteerdavgspeeltijd(), bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    label2.grid(row=2, column=0, pady=5)
    label3 = Label(scherm, text=duurstespellen(), bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    label3.grid(row=2, column=1, pady=100)
    label4 = Label(scherm, text=sorteerdmediaanspeeltijd(), bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    label4.grid(row=2, column=2, pady=5)
    labellist = Label(scherm, text='De 5 spellen met hoogste procentuele positieve reviews', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    labellist.grid(row=3, column=1, pady=10)
    x = 4
    for i in data:
        Label5 = Label(scherm, text =i, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
        Label5.grid(row=x, column=1)
        x+=1
    root.mainloop()
##76561198347428691
#76561198147947505
#76561199040375838

def optie1dashboard():
    steamid = steamidentry.get()
    data1 = meestgespeeldegamestijd(steamid)
    data2 = ownedgamesallfriends(steamid)
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    root = tkinter.Toplevel()
    root.attributes('-fullscreen', True)
    root.maxsize = ('1200x1000')
    root.title('Statistieken')
    root.config(background='#1b2838')
    image = PIL.Image.open('steamlogo2.png')
    resized_image = image.resize((1200, 100))
    converted_image = PIL.ImageTk.PhotoImage(resized_image)
    dashboard = Frame(root, width=1200, height=100, bg='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height=100., bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#171a21')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(master=dashboard, image=converted_image, width=1200, height=100, bg='#1b2838')
    hoofdmenu.grid(row=0, column=10)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                     command=lambda: [root.destroy()])
    stoppen.grid(row=1, column=3, pady=5)
    figure1 = plt.Figure(figsize=(5, 8))
    figure1.patch.set_facecolor('#1b2838')
    ax1 = figure1.add_subplot(211)
    bar1 = FigureCanvasTkAgg(figure1, scherm)
    bar1.get_tk_widget().pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    df1 = df1[['game', 'time']].groupby('game').sum()
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Vrienden speeltijd', color='#c7d5e0')
    ax1.set_title(f'Speeltijd vrienden van {playername(steamid)}', color='#c7d5e0')
    ax1.patch.set_facecolor('#1b2838')
    ax1.tick_params(axis='x', colors='#c7d5e0')
    ax1.tick_params(axis='y', colors='#c7d5e0')

    figure2 = plt.Figure(figsize=(5, 8))
    figure2.patch.set_facecolor('#1b2838')
    ax2 = figure2.add_subplot(211)
    bar2 = FigureCanvasTkAgg(figure2, scherm)
    bar2.get_tk_widget().pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
    df2 = df2[['aantal', 'game']].groupby('aantal').sum().astype(float)
    df2.plot(kind='bar', legend=True, ax=ax2)
    ax2.set_title('Spellen die jouw vrienden hebben.', color='#c7d5e0')
    ax2.set_title(f'Spellen van vrienden van {playername(steamid)}', color='#c7d5e0')
    ax2.patch.set_facecolor('#1b2838')
    ax2.tick_params(axis='x', colors='#c7d5e0')
    ax2.tick_params(axis='y', colors='#c7d5e0')

def optie2dashboard():
    root = tkinter.Toplevel()
    root.attributes('-fullscreen', True)
    root.maxsize = ('1200x1000')
    root.title('Vrienden')
    root.config(background='#1b2838')
    image = PIL.Image.open('steamlogo2.png')
    resized_image = image.resize((1200, 100))
    converted_image = PIL.ImageTk.PhotoImage(resized_image)
    dashboard = Frame(root, width=1200, height=100, bg='#171a21')
    dashboard.grid(row=0, column=0, pady=5)
    menubar = Frame(root, width=1200, height=100., bg='#1b2838')
    menubar.grid(row=1, column=0, pady=5)
    scherm = Frame(root, width=1200, height=800, bg='#1b2838')
    scherm.grid(row=2, column=0, pady=5)
    hoofdmenu = Label(master=dashboard, image=converted_image, width=1200, height=100, bg='#1b2838')
    hoofdmenu.grid(row=0, column=10)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                     command=lambda: [root.destroy()])
    stoppen.grid(row=1, column=3, pady=5)
    label1 = Label(scherm, text='Steamid vriend:', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    label1.grid(row=3, column=1)
    steamidentryvriend = Entry(scherm, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    steamidentryvriend.grid(row=3, column=2)
    button = Button(scherm, text='Zie spellen die jullie beide hebben', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18),
                    command=lambda: [zelfdespellengui(steamidentry.get(), steamidentryvriend.get())])
    button.grid(row=4, column=2)
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
                break


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

