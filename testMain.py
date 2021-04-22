import os
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import serial
import time
from crccheck.crc import CrcXmodem

'''
GUI napisane przy pomocy biblioteki tkinter oraz pygubu designer
'''

PROJECT_PATH = os.path.dirname(__file__)
PROJECT_UI = os.path.join(PROJECT_PATH, "simpleGUI.ui")

                                                                                        # Domyślne ustawienia portu COM:
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



                                                                                                # Klasa GUI
class X:
    def __init__(self, parent):
        self.filename='test.txt'
        self.choicemode=NAK
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
        print("WYBRANO COM1")


    def choiceCOM2(self):
        ser.port = 'COM2'
        print("WYBRANO COM2")


    def choiceCOM3(self):
        ser.port = 'COM3'
        print("WYBRANO COM3")


                                                                                             # Wybór bitu stopu
    def one(self):
        ser.stopbits = serial.STOPBITS_ONE
        print("1 BIT STOPU")

    def onePointFive(self):
        ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
        print("1.5 BIT STOPU")

    def two(self):
        ser.stopbits = serial.STOPBITS_TWO
        print("2 BIT STOPU")

                                                                                 # Wybór pliku, na którym operujemy
    def loadFile(self):
                                                                             # Wybor pliku do otwarcia poprzez menu
        self.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes='')

    def saveFile(self):
                                                                              # Wybor pliku do zapisu poprzez menu
        self.filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")

                                                                             # Wybór trybu CRC lub CHECKSUM
    def choiceCRC(self):
        self.choicemode=C
        print("TRYB CRC16")
        root.lab
        root.update()

    def choicechecksum(self):
        self.choicemode=NAK
        print("TRYB CHECKSUM")

                                                                                  # Główne funkcje
    def sendFile(self):
        self.send_data()

    def receiveFile(self):
        self.recive_data()

                                                                         # Funkcja czytająca z pliku binarnie
    def read_file(self):
        f = open(self.filename, "rb")
        bytesfile = f.read()
        return bytesfile


                                                                       # Podział danych na pakiety
    def split_data(self, data_bytes):                                   # Pakiet danych 128 bajty
        packets = []
        for packetnr in range(int(len(data_bytes) / 128) + (len(data_bytes) % 128 > 0)):
            packetarray = bytearray()
            for byte in range(128):
                if (byte + 128 * packetnr < len(data_bytes)):
                    packetarray.append(data_bytes[byte + 128 * packetnr])
                else:
                    packetarray.append(0)
            packets.append(packetarray)                                # Zwraca liste pakietow danych
        return packets
                                                                     # Wyslij pojedynczy pakiet
    def send_packet(self, packet_to_send, numberp,mode):
        while True:
            header = bytearray()                                        # Tworzymy nagłowek
            header.append(int.from_bytes(SOH, 'big'))
            header.append(numberp + 1)
            header.append(254 - numberp)
            full = header + packet_to_send
            if mode == C:                                               #Tworzymy pakiet kontrolny
                full = full + self.crc16_mine(packet_to_send)
            if mode == NAK:
                full.append(self.checksuma(packet_to_send))
            ser.write(full)                                             #Wysyłamy nagłowek,pakiet danych
                                                                        # i pakiet kontrolny
            #print(full)
            #print(len(full))
            ser.flush()
            answer = ser.read()
            #print(answer)
            if answer == ACK:                                           #Po wysłaniu pakiet sprawdzamy odpowiedz
                print("Wysłano pakiet nr ")
                print(header[1])
                break                                                   #Jeśli ACK lub CAN przerywamy transmisje
            if answer == CAN:                                           #Jeśli NAK ponawiamy transmisje
                break

    def send_data(self):
                                                                # Zczytujemy dane pliku i dzielimy na pakiety
        databytes = self.read_file()
        returnetpackets = self.split_data(databytes)
        packet_number = 0
        initial_answer = ser.read()                             # Czekamy na inicjalizacje transmisji przez odbiornik
        while initial_answer != C and initial_answer != NAK:
            initial_answer = ser.read()
            print(initial_answer)

            continue
        mode = initial_answer                                   # Wybór trybu odczytanego z odbiornika
        for bitpack in returnetpackets:                         # Wysył kolejnych pakietów
            ser.flush()
            self.send_packet(bitpack, packet_number, mode)
            packet_number += 1
                                                # Po zakończeniu transmisji wysyłamy sygnał End Of Transmission
        ser.write(EOT)
        if(ser.read())==ACK:
            print("100% danych wysłano poprawnie")

    # Funkcja licząca CRC

    def crc16(self, data: bytearray, poly=0x1021):
        crc = 0x0000
        for b in data:
            cur_byte = 0xFF & b                                             #Algorytm CRC XMODEM
            for _ in range(0, 8):
                if (crc & 0x0001) ^ (cur_byte & 0x0001):
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
                cur_byte >>= 1
        crc = (~crc & 0xFFFF)
        crc = (crc << 8) | ((crc >> 8) & 0xFF)

        return crc & 0xFFFF


                                                                        #Funkcja wyliczając sume kontrolna
    def checksuma(self, data: bytearray):
        temp_sum = 0
        for byte in data:
            temp_sum += int(byte)
        return temp_sum % 256

                                                                        #Funkcja licząca CRC
    def crc16_mine(self, packet_to_check):
        checkarray = bytearray()
        crcinst = CrcXmodem()
        crcinst.process(packet_to_check)
        suma = crcinst.final()
        checkarray.append((suma >> 8) & 0xff)
        checkarray.append(suma & 0xff)
        return checkarray
                                                                        #Funkcja nadająca tryb przez odbiornik
    def start_recive(self, mode):
        while 1:
            time.sleep(1)
            ser.write(mode)
            initial_recive = ser.read()
            if initial_recive == SOH:                                   #Jesli odbierzemy naglowek
                return initial_recive                                   #przejdz do odbioru

    def recive_data(self, mode=NAK):                                    # Funkcja odbierajaca dane
        initial_recive = self.start_recive(mode)
        file_bytes = bytearray()
        while 1:                                                        #odbiermy kolejno pakiety
            data_pack = self.recive_packet(mode, initial_recive)
            if data_pack:
                file_bytes = file_bytes + data_pack
            initial_recive = ser.read()
            if initial_recive == EOT:                                   #do otrzymania znaku EOT
                break
        ser.write(ACK)
        print("100% danych otrzymano poprawnie\n Plik ma postać: ")
        print(file_bytes)                                               #zapis do pliku
        f = open(self.filename, "wb")
        f.write(file_bytes)
        f.close()

    def recive_packet(self,mode, initial_recive):                       #odbierz pojedynczy pakiet
        recived_header = bytearray()                                    #naglowek
        recived_header += initial_recive
        recived_header += ser.read()
        recived_header += ser.read()
        packet = self.recive_data_packet()                              #dane
        if self.check_packet(mode, packet):                             #kontrola
            print("Otrzymano pakiet nr ")
            print(recived_header[1])
            return packet
        return False

    def recive_data_packet(self):                                       #odbierz pakiet danych
        packet_arr = bytearray()
        for byte in range(128):
            packet_arr += ser.read()
        return packet_arr

                                                                        # Sprawdzanie poprawności odebranego pakietu
    def check_packet(self, mode, packet):
        if mode == NAK:                                                 #tryb sumy kontrolnej
            check = bytearray()
            check += ser.read()
            selfcheck = bytearray()
            selfcheck.append(self.checksuma(packet))
            if selfcheck[0] == check[0]:                                #Sprawdz czy poprawne
                ser.write(ACK)
                return True
            else:                                                       # Wyślij odpowiedz
                ser.write(NAK)
                print(2)
                return False
        elif mode == C:                                               #tryb CRC
            check = bytearray()
            check += ser.read()
            check += ser.read()
            crc_16 = self.crc16_mine(packet)                           #sprawdz crc
            for byte in range(2):
                if crc_16[byte] != check[byte]:                         #wyslij odpowiedz
                    ser.write(NAK)
                    return False
                ser.write(ACK)
                return True




if __name__ == '__main__':
    root = tk.Tk()
    root.title('XMODEM_TELEKOMUNIKACJA')
    app = SimpleguiApp(root)
    app.run()
