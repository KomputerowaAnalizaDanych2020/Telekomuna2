import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import serial

from crccheck.crc import Crc32, CrcXmodem
from crccheck.checksum import Checksum32

'''
GUI napisane przy pomocy biblioteki tkinter oraz pygubu designer
'''

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "simpleGUI.ui")

# Domyślne ustawienia:
ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Znaki sterujące
SOH = bytearray.fromhex("01")
EOT = bytearray.fromhex("04")
ACK = bytearray.fromhex("06")
NAK = bytearray.fromhex("15")
CAN = bytearray.fromhex("18")
C = bytearray.fromhex("43")

'''
def read_file():
    f = open(path, "rb")
    bytesfile=f.read()
    return bytesfile


# Parzystość bitów
def checksuma(data: bytearray):
    temp_sum = 0
    for byte in data:
        temp_sum += int(byte)
        # print(temp_sum)
    return temp_sum % 256


# Podział danych na pakiety
def split_data(data_bytes):
    packets = []
    for packetnr in range(int(len(data_bytes) / 128) + (len(data_bytes) % 128 > 0)):
        packetarray = bytearray()
        for byte in range(128):
            if (byte + 128 * packetnr < len(data_bytes)):
                packetarray.append(data_bytes[byte + 128 * packetnr])
            else:
                packetarray.append(0)
        packets.append(packetarray)
    return packets


# Funkcja służaca wysłaniu pakietu
def send_packet(packet_to_send, numberp):
    while True:
        header = bytearray()
        header.append(int.from_bytes(SOH, 'big'))
        header.append(numberp+1)
        header.append(254-numberp)
        suma = crcinst.final()
        crcinst.process(packet_to_send)
        print(suma)
        print(crcinst.finalhex())
        full = header+packet_to_send
        full.append((suma >> 8) & 0xff)
        full.append(suma & 0xff)
        ser.write(full)
        print(full)
        print(len(full))
        ser.flush()
        answer = ser.read()
        print(answer)
        if answer == ACK:
            break
        if answer == CAN:
            break

        #print(numberp)


# Funkcja odpowiadająca za CRC
def crc16(data: bytearray, poly=0x1021):
    crc = 0x0000
    for b in data:
        cur_byte = 0xFF & b
        for _ in range(0, 8):
            if (crc & 0x0001) ^ (cur_byte & 0x0001):
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
            cur_byte >>= 1
    crc = (~crc & 0xFFFF)
    crc = (crc << 8) | ((crc >> 8) & 0xFF)
    
    return crc & 0xFFFF


crcinst = CrcXmodem()
path = 'test.txt'
databytes=read_file(path)
returnetpackets=split_data(databytes)
packet_number = 0
for bitpack in returnetpackets:
    #print(bitpack)
    #print(crc16(bitpack))
    while 1:

        if ser.read() == C:
            print(ser.read())
            send_packet(bitpack, packet_number)
            break
    packet_number += 1
ser.write(EOT)

'''

# Klasa GUI
class SimpleguiApp:
    def __init__(self, parent):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow = builder.get_object('background', parent)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    # Wybór COMa
    def choiceCOM1(self):
        ser.port = 'COM1'

    def choiceCOM2(self):
        ser.port = 'COM2'

    def choiceCOM3(self):
        ser.port = 'COM3'

    # Wybór bitu stopu
    def one(self):
        ser.stopbits = serial.STOPBITS_ONE

    def onePointFive(self):
        ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE

    def two(self):
        ser.stopbits = serial.STOPBITS_TWO

    # Wybór pliku, na którym operujemy
    def loadFile(self):
        # Wybor pliku do otwarcia poprzez menu
        root.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes='')

    def saveFile(self):
        # Wybor pliku do zapisu poprzez menu
        root.filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")

    # Wybór trybu
    def choiceCRC(self):
        root.quit()

    def choiceParity(self):
        root.quit()

    # Główne funkcje
    def sendFile(self):
        root.quit()

    def receiveFile(self):
        root.quit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Tytul')
    app = SimpleguiApp(root)
    app.run()
