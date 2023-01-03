from serial.tools import list_ports
import serial


def read_serial(port):
    """data lezen van serial port en terugsturen als string."""
    line = port.read(1000)
    return line.decode()


# port vinden waarmee pico pi is aangesloten
serial_ports = list_ports.comports()

print("[INFO] Serial ports gevonden:")
for i, port in enumerate(serial_ports):
    print(str(i) + ". " + str(port.device))

pico_port_index = int(input("Aan welke port is de Raspberry Pi Pico aan verbonden? "))
pico_port = serial_ports[pico_port_index].device

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    if serial_port.isOpen():
        print("[INFO] Using serial port", serial_port.name)
    else:
        print("[INFO] Opening serial port", serial_port.name, "...")
        serial_port.open()

    try:
        # Request user input
        commands = ['optie 1', 'optie 2', 'optie 3']
        while True:
            choice = input("Command? [" + ", ".join(commands) + "] ")

            if choice == 'optie 1':
                # neopixel kleurt rood
                data = "0\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif choice == 'optie 2':
                # neopixel kleurt groen en vanwege opstarten optie 2
                data = "1\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif choice == 'optie 3':
                data = "2\r"
                serial_port.write(data.encode())
                pico_output = read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', '')
                print("[pico] " + pico_output)
            elif choice == 'exit':
                # Exit user input loop
                break
            else:
                print("[WARN] Unknown command.")

    except KeyboardInterrupt:
        print("[INFO] Ctrl+C detected. Terminating.")
    finally:
        # Close connection to Pico
        serial_port.close()
        print("[INFO] Serial port gesloten, doei!.")
