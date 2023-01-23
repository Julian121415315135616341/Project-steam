import time
import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(13), 8)

# wachten voor data.
while True:

    data = input()

    print("Received '" + data + "'.")

    if data == '0':
        print("Optie 1 gekozen")
        np[0] = (255, 255, 0)
        np[1] = (255, 255, 0)
        np.write()
        time.sleep(1)
    elif data == '1':
        print("Optie 2 gekozen")
        np[2] = (0, 255, 0)
        np[3] = (0, 255, 0)
        np.write()
        time.sleep(1)
    elif data == '2':
        print("Optie 3 gekozen")
        np[4] = (0, 0, 255)
        np[5] = (0, 0, 255)
        np.write()
        time.sleep(1)
    elif data == '3':
        print("Optie 4 EXIT gekozen")
        # Knipperpatroon bovenste twee lampjes
        for _ in range(0, 4):
            np[6] = (255, 0, 0)
            np[7] = (255, 0, 0)
            np.write()
            time.sleep(0.2)
            np[6] = (0, 0, 0)
            np[7] = (0, 0, 0)
            np.write()
            time.sleep(0.2)


    time.sleep(1)