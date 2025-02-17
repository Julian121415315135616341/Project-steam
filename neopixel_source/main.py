import time
import machine
import neopixel


def blink(n, s, color):
    """
    Knipper de lichtjes 'n' keer in kleur 'color', met interval van 's' seconden.
    :param n: Het aantal keer dat het licht moet knipperen. (int)
    :param s: De tijd tussen het knipperen (interval) in seconden. (float)
    :param color: De kleur van het knipperende licht. (tuple)
    """
    for _ in range(n):
        # Zet de lichtjes aan
        np.fill(color)
        np.write()

        # Wacht het interval
        time.sleep(s)

        # Zet de lichtjes uit
        np.fill((0, 0, 0))
        np.write()

        # Wacht het interval
        time.sleep(s)


def startup():
    """
    Groen lichtpatroon voor het opstarten van het programma.
    """
    # Zet de lichtjes een voor een aan, van onder naar boven.
    for i in range(8):
        np[i] = green
        np.write()
        time.sleep(0.1)

    # Zet de lichtjes uit
    np.fill((0, 0, 0))
    np.write()
    time.sleep(0.2)

    # Knipper 2 keer
    blink(2, 0.2, green)


def shutdown():
    """
    Rood lichtpatroon voor het afsluiten van het programma.
    """
    # Knipper 2 keer
    blink(2, 0.2, red)

    # Zet de lichtjes aan
    np.fill(red)
    np.write()
    time.sleep(0.2)

    # Zet de lichtjes een voor een uit, van boven naar onder.
    for i in reversed(range(8)):
        np[i] = (0, 0, 0)
        np.write()
        time.sleep(0.1)


# Definieer de neopixel
np = neopixel.NeoPixel(machine.Pin(13), 8)

# Definieer kleuren
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 165, 0)


# Main loop
while True:

    # Input ontvangen
    data = input()
    print("Received '" + data + "'.")

    # Home scherm is actief
    if data == '0':
        blink(2, 0.2, yellow)
        np.fill(yellow)
        np.write()
        time.sleep(1)

    # Statistieken scherm is actief
    elif data == '1':
        blink(2, 0.2, orange)
        np.fill(orange)
        np.write()
        time.sleep(1)

    # Vrienden scherm is actief
    elif data == '2':
        blink(2, 0.2, blue)
        np.fill(blue)
        np.write()
        time.sleep(1)

    # Programma wordt afgesloten
    elif data == '3':
        shutdown()
        time.sleep(1)

    # Programma wordt opgestart
    elif data == '4':
        startup()
        time.sleep(1)

    time.sleep(1)