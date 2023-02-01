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

from serial.tools import list_ports
import serial

def read_serial(port):
    """data lezen van serial port en terugsturen als string."""
    line = port.read(1000)
    return line.decode()

def startPico():
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Using serial port", serial_port.name)
        else:
            print("[INFO] Opening serial port", serial_port.name, "...")
            serial_port.open()

        # onderste 2 lampjes neopixel kleuren geel
        data = "4\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

        serial_port.close()

def exitPico():
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Using serial port", serial_port.name)
        else:
            print("[INFO] Opening serial port", serial_port.name, "...")
            serial_port.open()

        # onderste 2 lampjes neopixel kleuren geel
        data = "3\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

        serial_port.close()

# port vinden waarmee pico pi is aangesloten
serial_ports = list_ports.comports()

# print("[INFO] Serial ports gevonden:")
# for i, port in enumerate(serial_ports):
#     print(str(i) + ". " + str(port.device))

# pico_port_index = int(input("Aan welke port is de Raspberry Pi Pico aan verbonden? "))
pico_port = serial_ports[0].device

startPico()


'''steamid voor test: 76561199040375838'''

def playersummaries(friendid):
    """Vraag de playersummary van steamid op
    return de response"""
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={friendid}").json()
    return response

def playername(steamid):
    """"haal de spelersnaam uit de response en voeg toe aan lijst
        return de lijst"""
    lst = []
    #voor elk element in response, voeg personaname toe aan lijst
    response = requests.get(f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamids={steamid}").json()
    for i in response['response']['players']:
        lst.append(i['personaname'])
    return lst[0]

def friendlist(steamid):
    """"Vraag naar vriendenlijst van steamid op api
    voeg de steamid's van vrienden toe aan lijst"""
    lst =[]
    #Voeg alle vrienden van het steamid toe aan lijst.
    try:
        response = requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&relationship=friend").json()
        for i in response['friendslist']['friends']:
            lst.append(i['steamid'])
    except:
        placeholder = True
    return lst


def friendsdata(steamid):
    '''voor elke vriend van steamid, pas functie playersummaries op hun steamid toe.'''
    friends = friendlist(steamid)
    #voer functie playersummaries uit op elk steamid in friends.
    for i in friends:
        return(playersummaries(i))

def onlinevrienden(steamid, getal):
    '''bepaal de vrienden van steamid
        kijk of de status van steamid overeenkomt met getal
        zoja voeg toe aan lijst
        return lijst en maak een string van de lijst voor gui toevoeging'''
    lst = []
    string = ''
    vriendenlijst = friendlist(steamid)
    #voor elk steamid kijk of de personastate overeenkomt met getal parameter.
    for i in vriendenlijst:
        data = playersummaries(i)
        for j in data['response']['players']:
            if j['personastate'] == getal:
                lst.append(j['personaname'])
            else:
                continue
    #voor elke element in de lijst, voeg deze toe aan de string.
    for i in lst:
        string += (i)
        string += '\n'

    return string


def gametime(steamid):
    '''haal alle gespeelde games van steamid op en de tijd
        voeg deze toe aan een dict en voeg de dict toe aan de lijst.'''
    lst = []
    #voor elke element in response, voeg de naam en tijd toe aan de dict en voeg dict toe aan lijst.
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
    '''verkrijg de games die steamid op zijn account heeft staan en voeg toe aan lijst'''
    lst = []
    #voor elk element in response voeg de naam toe aan lijst.
    response = requests.get(f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=89538EE3D15588D519ABB27D0E9FAAC1&steamid={steamid}&format=json&include_appinfo=1').json()
    for i in response['response']['games']:
        lst.append(i['name'])
    return lst

def ownedgamesallfriends(steamid):
    '''voor elke vriend in vriendenlijst,
        voer ownedgames functie uit en voeg toe aan lijst
        verkrijg vervolgens de frequentie van alle spellen met een dictionary
        sorteer de dictionary
        verander de makeup van de dict om goed te kunnen gebruiken in matplotlib.'''
    lst = []
    friends = friendlist(steamid)
    #voor elke steamid in friends voer de functie owner games uit en voeg toe aan de lijst
    for i in friends:
        try:
            games = ownedgames(i)
            for x in games:
                lst.append(x)
        except:
            continue
    #maak dict freqs aan
    freqs = {}
    for i in lst:
        #als i in freqs zit, verander de frequentie met +1
        if i in freqs:
            freqs[i] += 1
        #zoniet voeg de key i toe met frequentie 1
        else:
            freqs[i] = 1
    try:
        #ik heb een hekel aan de rainbow six siege test server en wil die er niet tussen hebben staan
        del freqs["Tom Clancy's Rainbow Six Siege - Test Server"]
    except:
        #de except is nodig, verder is deze regel nutteloos
        placeholder = True
    #sorteer de dictionary op de frequentie van keys
    res = dict(sorted(freqs.items(), key=itemgetter(1), reverse=True)[:5])
    lstname = []
    lstamount = []
    #verander de opmaak van de dictionary om 2 keys met alle waardes erin te hebben.
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
    '''vraag vriendenlijst op
        voer gametime functie uit op elk element in vriendenlijst
        vang error op met een except keyerror
        voeg de naam en speeltijd toe aan een dict'''
    totaalgametime = []
    friends = friendlist(steamid)
    #voor elk steamid in friends probeer functie gametime uit te voeren, als er een keyerror is negeer deze en continue
    for x in friends:
        try:
            data = gametime(x)
            totaalgametime.append(data)
        except KeyError:
            continue
    #om de dictionary goed te sorteren gebruik Counter
    totalegametime = Counter()
    #voeg elke dict uit totaalgametime toe aan totalegametime
    for d in totaalgametime:
        for j in d:
            totalegametime[j['name']] += j['time']
    return totalegametime
def meestgespeeldegames(steamid):
    '''vraag de totalegametime van alle vrienden op
    sorteer deze en pak de 5 grootste waardes'''
    gametime = totalgametimeallfriends(steamid)
    #sorteer gametime en pak de 5 grootste waardes
    maximaal = sorted(gametime, key=gametime.get, reverse=True)[:5]
    return maximaal

def meestgespeeldegamestijd(steamid):
    '''vraag de meestgespeelde games van steamid op
        vraag de totalegametime van alle vrienden van steamid op
        pak de tijd / 60 van meestgespeeldegames en voeg deze toe aan de lijst
        maak nieuwe dict aan en voeg hier de tijd en naam van het spel toe.
        '''
    games = meestgespeeldegames(steamid)
    lst =[]
    dict = {
        'game': [],
        'time': []
    }
    data = totalgametimeallfriends(steamid)
    #voor elke element in meestgespeeldegames(steamid)
    #tijd is data(i) / 60, voeg deze tijd toe aan de lijst
    for i in meestgespeeldegames(steamid):
        tijd = data[i]
        lst.append(tijd / 60)
    #voor elke element in de lijst voeg deze toe aan dict key 'tijd'
    for i in lst:
        dict['time'].append(i)
    #voor elke element in games voeg deze toe aan dict key 'game'
    for x in games:
        dict['game'].append(x)
    return dict



def steamdata():
    '''laad json bestand
        pak de namen van alle spellen erin
        return de eerste 5'''
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    #voor elke game in data, voeg de naam van het spel toe aan de lijst
    for game in data:
        lst.append(game['name'])
    return 'Eerste 5 spellen' + '\n' + lst[0] + '\n' + lst[1] + '\n' + lst[2] + '\n' + lst[3] + '\n' + lst[4]

def steamreviews():
    '''laad het json bestand
        kijk of de totale reviews van een spel meer zijn dan 3000
        als dit zo is bereken het % positieve reviews
        en voeg de game en % positieve reviews toe aan de dict.
        sorteer de dictionary en maak er een lijst van'''
    bestand = open('steam.json')
    data = json.load(bestand)
    dictreviews = {
                   }
    #voor elk element in data
    #check of de negatieve + positieve reviews meer zijn dan 300
    #dit doen we om te zorgen dan willekeurige spellen met 2 reviews in totaal niet meetellen
    #als er meer dan 3000 reviews zijn berekent % positieve reviews en voeg dit en de naam van het spel toe aan dict
    for i in data:
        if i['positive_ratings'] + i['negative_ratings'] > 3000:
            positief = i['positive_ratings']
            negatief = i['negative_ratings']
            positiefprocent = positief / (positief + negatief) * 100
            positiefprocent = round(positiefprocent, 2)
            teupdaten = {i['name']: positiefprocent}
            dictreviews.update(teupdaten)
    #sorteer de dictionary op de waardes en maak er een lijst van
    res = dict(sorted(dictreviews.items(), key=itemgetter(1), reverse=True)[:5])
    res2 = list(res.items())
    return res2


def sorteerdavgspeeltijd():
    '''laad het json bestand
        sorteer de data op de gemiddelde speeltijd en pak de hoogste 6 waardes,
        voeg de namen hiervan toe aan de lijst'''
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    #sorteer de data op de key 'average_playtime' en doe dit reversed (hoogste waardes eerst)
    data = sorted(data, key=lambda i: i['average_playtime'], reverse=True)
    #pak de hoogste 6 waardes
    data = (data[0:6])
    #voor elke element in data voeg de naam toe aan lijst
    for i in data:
        lst.append(i['name'])
    return '5 Spellen met hoogste gemiddelde speeltijd' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]

def sorteerdmediaanspeeltijd():
    '''laad het jsonbestand
        sorteer de data op mediaan van speeltijd en neem de hoogste waardes,
        voeg de namen hiervan toe aan lijst
        '''
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    #sorteer de data op de key 'median_playtime' en doe dit reversed (hoogste waardes eerst)
    data = sorted(data, key=lambda i: i['median_playtime'], reverse=True)
    #pak de hoogste 6 waardes
    data = (data[0:6])
    #voor elk element in data voeg de naam toe aan lijst
    for i in data:
        lst.append(i['name'])
    return 'Spellen met hoogste mediaan speeltijd' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]
def duurstespellen():
    '''laad het jsonbestand
        sorteer de data op de prijs en neem de hoogste waardes,
        voeg de namen hiervan toe aan lijst
        '''
    lst = []
    bestand = open('steam.json')
    data = json.load(bestand)
    #sorteer de data op de key 'price' en doe dit reversed (hoogste waardes eerst)
    data = sorted(data, key=lambda i: i['price'], reverse=True)
    #pak hoogste 6 waardes
    data = (data[0:6])
    #voor elk element in data voeg de naam toe aan lijst
    for i in data:
        lst.append(i['name'])
    return 'Duurste Spellen' '\n'+ '1: '+lst[0] + '\n' + '2: '+lst[1 ] + '\n' + '3: '+lst[2] + '\n' + '4: '+lst[3] +'\n' + '5: '+lst[4]

def zelfdespellenowned(steamid, friendid):
    '''neem de games die steamid heeft, en de spellen die friendid heeft
        vergelijk deze en voeg alleen overeenkomende waardes toe aan nieuwe lijst'''
    lst =[]
    mijngames = ownedgames(steamid)
    vriendgames = ownedgames(friendid)
    #voor elk element in mijngames, als deze ook on vriendgames zit, voeg dan toe aan lijst
    for x in mijngames:
        if x in vriendgames:
            lst.append(x)
    return lst
def zelfdespellengui(steamid, friendid):
    root2 = tkinter.Tk()
    root2.maxsize = ('800x350')
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
    optie1 = Button(menubar, text='Home', bg='#171a21', fg ='#c7d5e0', highlightthickness=4, font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21',fg ='#c7d5e0',  font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg ='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), exitPico()])
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

    # Open a connection to the Pico
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Using serial port", serial_port.name)
        else:
            print("[INFO] Opening serial port", serial_port.name, "...")
            serial_port.open()

        # onderste 2 lampjes neopixel kleuren geel
        data = "0\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

        serial_port.close()

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
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', highlightthickness=4, fg='#c7d5e0', font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                     command=lambda: [root.destroy(), exitPico()])
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

    # Open a connection to the Pico
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Using serial port", serial_port.name)
        else:
            print("[INFO] Opening serial port", serial_port.name, "...")
            serial_port.open()

        # 2 lampjes neopixel kleuren groen
        data = "1\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

        serial_port.close()

def optie2dashboard():
    steamid = steamidentry.get()
    online = (onlinevrienden(steamid, 1))
    busy = (onlinevrienden(steamid, 2))
    offline = (onlinevrienden(steamid, 0))
    away = (onlinevrienden(steamid, 3))
    snooze = (onlinevrienden(steamid, 4))
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
    scherm = Frame(root, width=1200, height=300, bg='#1b2838')
    scherm.grid(row=2, column=0, pady=5)
    scherm2 = Frame(root, width=1200, height=500, bg='#1b2838')
    scherm2.grid(row=3, column=0)
    hoofdmenu = Label(master=dashboard, image=converted_image, width=1200, height=100, bg='#1b2838')
    hoofdmenu.grid(row=0, column=10)
    optie1 = Button(menubar, text='Home', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), maindashboard()])
    optie1.grid(row=1, column=0, pady=5)
    optie2 = Button(menubar, text='Statistieken', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                    command=lambda: [root.destroy(), optie1dashboard()])
    optie2.grid(row=1, column=1, pady=5)
    optie3 = Button(menubar, text='Vrienden', bg='#171a21', highlightthickness=4, fg='#c7d5e0', font=('Times New Roman', 24, 'bold', 'underline'), width=21,
                    command=lambda: [root.destroy(), optie2dashboard()])
    optie3.grid(row=1, column=2, pady=5)
    stoppen = Button(menubar, text='Stoppen', bg='#171a21', fg='#c7d5e0', font=('Times New Roman', 24), width=21,
                     command=lambda: [root.destroy(), exitPico()])
    stoppen.grid(row=1, column=3, pady=5)
    label1 = Label(scherm, text='Steamid vriend:', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    label1.grid(row=3, column=1)
    steamidentryvriend = Entry(scherm, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    steamidentryvriend.grid(row=3, column=2)
    button = Button(scherm, text='Zie spellen die jullie beide hebben', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18),
                    command=lambda: [zelfdespellengui(steamidentry.get(), steamidentryvriend.get())])
    button.grid(row=4, column=2)

    onlinelabel = Label(scherm2, text='Online vrienden: ', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    onlinelabel.grid(row=5, column=0,padx=20)
    onlinelabel2 = Label(scherm2, text=online,bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 11),width=20)
    onlinelabel2.grid(row=6, column=0,sticky=N)

    offlinelabel = Label(scherm2, text='Offline vrienden: ', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    offlinelabel.grid(row=5, column=1, padx=20)
    offlinelabel2 = Label(scherm2, text=offline, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 11), width=20)
    offlinelabel2.grid(row=6, column=1,sticky=N)

    busylabel = Label(scherm2, text='Busy vrienden: ', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    busylabel.grid(row=5, column=2, padx=20)
    busylabel2 = Label(scherm2, text=busy, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 11))
    busylabel2.grid(row=6, column=2,sticky=N)

    snoozelabel = Label(scherm2, text='Snooze vrienden: ', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    snoozelabel.grid(row=5, column=3,padx=20)
    snoozelabel2 = Label(scherm2, text=snooze, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 11))
    snoozelabel2.grid(row=6, column=3,sticky=N)

    awaylabel = Label(scherm2, text='Away vrienden: ', bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 18))
    awaylabel.grid(row=5, column=4,padx=20)
    awaylabel2 = Label(scherm2, text=away, bg='#1b2838', fg='#c7d5e0', font=('Times New Roman', 11))
    awaylabel2.grid(row=6, column=4,sticky=N)

    # Open a connection to the Pico
    with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
        if serial_port.isOpen():
            print("[INFO] Using serial port", serial_port.name)
        else:
            print("[INFO] Opening serial port", serial_port.name, "...")
            serial_port.open()

        # onderste 2 lampjes neopixel kleuren geel
        data = "2\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

        serial_port.close()

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
button = Button(root, text='Zie statistieken',bg='#1b2838',fg ='#c7d5e0',  font=('Times New Roman', 18), command=lambda: [root.iconify(), idcheck(steamidentry.get())])
button.pack()
root.mainloop()

