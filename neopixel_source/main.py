import time
import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(13), 8)

# wachten voor data.
while True:

    data = input()

    print("Received '" + data + "'.")

    if data == '0':
        np[0] = (255, 255, 0)
        np[1] = (255, 255, 0)
        np[2] = (0, 0, 0)
        np[3] = (0, 0, 0)
        np[4] = (0, 0, 0)
        np[5] = (0, 0, 0)
        np[6] = (0, 0, 0)
        np[7] = (0, 0, 0)
        np.write()
        time.sleep(1)
    elif data == '1':
        np[0] = (0, 0, 0)
        np[1] = (0, 0, 0)
        np[2] = (0, 255, 0)
        np[3] = (0, 255, 0)
        np[4] = (0, 0, 0)
        np[5] = (0, 0, 0)
        np[6] = (0, 0, 0)
        np[7] = (0, 0, 0)
        np.write()
        time.sleep(1)
    elif data == '2':
        np[0] = (0, 0, 0)
        np[1] = (0, 0, 0)
        np[2] = (0, 0, 0)
        np[3] = (0, 0, 0)
        np[4] = (0, 0, 255)
        np[5] = (0, 0, 255)
        np[6] = (0, 0, 0)
        np[7] = (0, 0, 0)
        np.write()
        time.sleep(1)
    elif data == '3':
        # EXIT optie, rood knipperen alle lampjes
        for _ in range(0, 4):
            np[0] = (255, 0, 0)
            np[1] = (255, 0, 0)
            np[2] = (255, 0, 0)
            np[3] = (255, 0, 0)
            np[4] = (255, 0, 0)
            np[5] = (255, 0, 0)
            np[6] = (255, 0, 0)
            np[7] = (255, 0, 0)
            np.write()
            time.sleep(0.2)
            np[0] = (0, 0, 0)
            np[1] = (0, 0, 0)
            np[2] = (0, 0, 0)
            np[3] = (0, 0, 0)
            np[4] = (0, 0, 0)
            np[5] = (0, 0, 0)
            np[6] = (0, 0, 0)
            np[7] = (0, 0, 0)
            np.write()
            time.sleep(0.2)
    elif data == '4':
        # Opstarten, groen knipperen alle lampjes
        for _ in range(0, 4):
            np[0] = (0, 255, 0)
            np[1] = (0, 255, 0)
            np[2] = (0, 255, 0)
            np[3] = (0, 255, 0)
            np[4] = (0, 255, 0)
            np[5] = (0, 255, 0)
            np[6] = (0, 255, 0)
            np[7] = (0, 255, 0)
            np.write()
            time.sleep(0.2)
            np[0] = (0, 0, 0)
            np[1] = (0, 0, 0)
            np[2] = (0, 0, 0)
            np[3] = (0, 0, 0)
            np[4] = (0, 0, 0)
            np[5] = (0, 0, 0)
            np[6] = (0, 0, 0)
            np[7] = (0, 0, 0)
            np.write()
            time.sleep(0.2)

    time.sleep(1)