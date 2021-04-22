from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import os

from tkinter import filedialog
import serial
import time
from crccheck.crc import CrcXmodem

# Domyślne ustawienia portu COM:
ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=2
)
SOH = bytearray.fromhex("01")
EOT = bytearray.fromhex("04")
ACK = bytearray.fromhex("06")
NAK = bytearray.fromhex("15")
CAN = bytearray.fromhex("18")
C = bytearray.fromhex("43")
filename = 'test.bmp'


class XmodemGUI:
    def __init__(self):
        self.root = Tk()
        self.stopbit = StringVar()
        self.stopbit.set("1.0")
        self.mode = StringVar()
        self.mode.set("NAK")
        self.root.title("Xmodem 229952|230039")
        self.filename = None
        self.xmodem = ProtocolX(self)

        self.com_port = StringVar()
        self.com_port.set("COM2")
        self.tytul_label = Label(self.root, text="XMODEM", font=(None, 17, 'bold'), fg='blue')
        self.tytul_label.grid(row=0, column=0, columnspan=6)

        self.tytul_label = Label(self.root, text="USTAWIENIA", font=(None, 14, 'bold'))
        self.tytul_label.grid(row=1, column=0, columnspan=4)

        self.tryb_frame = LabelFrame(self.root, text="Tryb:", padx=40, pady=8)
        self.tryb_frame.grid(row=5, column=0, columnspan=2)
        self.tryb_CRC = Radiobutton(self.tryb_frame, text="CRC", variable=self.mode, value="C")
        self.tryb_Checksum = Radiobutton(self.tryb_frame, text="Checksum", variable=self.mode, value="NAK")
        self.tryb_CRC.grid(row=0, column=0)
        self.tryb_Checksum.grid(row=0, column=1)

        self.stopbit_frame = LabelFrame(self.root, text="Bity stopu:", padx=40, pady=8)
        self.stopbit_frame.grid(row=6, column=0, columnspan=2)
        self.bitone = Radiobutton(self.stopbit_frame, text="1bit", variable=self.stopbit, value="1.0",
                                  command=self.changeStopBit)
        self.bitonehalf = Radiobutton(self.stopbit_frame, text="1.5bit", variable=self.stopbit, value="1.5",
                                      command=self.changeStopBit)
        self.bittwo = Radiobutton(self.stopbit_frame, text="2bit", variable=self.stopbit, value="2.0",
                                  command=self.changeStopBit)
        self.bitone.grid(row=0, column=0)
        self.bitonehalf.grid(row=0, column=1)
        self.bittwo.grid(row=0, column=2)

        self.odczyt_label = Label(self.root, text="Odczyt z pliku:")
        self.odczyt_label.grid(row=2, column=0)
        self.odczyt_button = Button(self.root, text="Wybierz Plik", command=self.loadFile)
        self.zapisz_button = Button(self.root, text="Wybierz Plik", command=self.saveFile)
        self.odczyt_button.grid(row=2, column=1)
        self.zapisz_button.grid(row=4, column=1)

        self.port_label = Label(self.root, text="Port COM:")
        self.port_label.grid(row=3, column=0)
        self.port_menu = OptionMenu(self.root, self.com_port, "COM1", "COM2", "COM3", "COM4", command=self.changePort)
        self.port_menu.grid(row=3, column=1)

        self.zapis_label = Label(self.root, text="Zapis do pliku:")
        self.zapis_label.grid(row=4, column=0)

        self.szerokosc_label = Label(self.root, text="Szerokość pasma")
        self.szerokosc_label.grid(row=7, column=0)

        self.podpis_label = Label(self.root, text="©Daniel Malicki/Maciej Wlodarczyk")
        self.podpis_label.grid(row=12, column=4)

        self.szerokosc_entry = Entry(self.root, width=8)
        self.szerokosc_entry.grid(row=7, column=1)
        self.szerokosc_entry.insert(0, 9600)

        self.logi_text = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.logi_text.grid(row=2, column=4, rowspan=7)
        self.postep_label = Label(self.root, text="Postęp:")
        self.postep_label.grid(row=10, column=4)

        self.wyslij_button = Button(self.root, text="Wyślij", font=(None, 13, 'bold'), width=20, height=3, bg='green',
                                    command=self.wyslijClick)
        self.zatrzymaj_button = Button(self.root, text="Zatrzymaj", font=(None, 13, 'bold'), width=20, height=3,
                                       bg='red',
                                       command=self.zatrzymaj)
        self.odbierz_button = Button(self.root, text="Odbierz", font=(None, 13, 'bold'), width=20, height=3, bg='blue',
                                     command=self.odbierzClick)
        self.odbierz_button.grid(row=2, column=5, rowspan=2)
        self.zatrzymaj_button.grid(row=4, column=5, rowspan=2)
        self.wyslij_button.grid(row=6, column=5, rowspan=2)
        self.progress = ttk.Progressbar(self.root, orient=HORIZONTAL, length=500, mode='determinate')
        self.progress.grid(row=11, column=1, columnspan=4, sticky="E")

    def dodajprocent(self, value):
        self.progress['value'] = value

    def zatrzymaj(self):
        self.logi_text.delete('1.0', END)
        self.progress['value'] = 0
        self.xmodem.cancel_transmision()

    def wyslijClick(self):
        self.progress['value'] = 0
        if self.filename:
            ser.baudrate = int(self.szerokosc_entry.get())
            self.odbierz_button.config(state="disabled")
            self.wyslij_button.config(state="disabled")
            self.logi_text.delete(1.0, END)
            self.logi_text.insert(INSERT, "WYSYŁAM ")
            self.root.update()
            self.xmodem.send_data()
            self.wyslij_button.config(state="normal")
            self.odbierz_button.config(state="normal")
        else:
            self.errorFile()

    def printToLogi(self, text):
        self.logi_text.insert(INSERT, text)
        self.logi_text.see("end")

    def odbierzClick(self):
        self.progress['value'] = 0
        if self.filename:
            ser.baudrate = int(self.szerokosc_entry.get())
            self.odbierz_button.config(state="disabled")
            self.wyslij_button.config(state="disabled")
            self.root.update()
            time.sleep(1)                                                                           #possible mistake
            if self.mode.get() == "C":
                self.xmodem.recive_data(C, self)
            else:
                self.xmodem.recive_data(NAK, self)
            self.wyslij_button.config(state="normal")
            self.odbierz_button.config(state="normal")
        else:
            self.errorFile()

    def errorFile(self):
        messagebox.showerror("Błąd", "Podaj plik")

    def loadFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes='')
        self.xmodem.setFileName(self.filename)

    def saveFile(self):
        self.filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")
        self.xmodem.setFileName(self.filename)

    def bitradio(self):
        print("stopbit" + self.stopbit.get())

    def changePort(self, value):
        ser.port = self.com_port.get()

    def changeStopBit(self):
        if self.stopbit.get() == "1.0":
            serial.STOPBITS_ONE
        elif self.stopbit.get() == "2.0":
            serial.STOPBITS_TWO
        else:
            serial.STOPBITS_ONE_POINT_FIVE

    def start_gui(self):
        self.root.mainloop()


class ProtocolX:
    def __init__(self, gui):
        self.stop = False
        self.gui = gui
        self.choicemode = NAK

    def setFileName(self, filename):
        self.filename = filename
        # Główne funkcje

    def sendFile(self):
        self.send_data()

    def receiveFile(self, mode=NAK):
        self.recive_data(mode)

        # Funkcja czytająca z pliku binarnie

    def read_file(self):
        f = open(self.gui.filename, "rb")
        bytesfile = f.read()
        return bytesfile

    def cancel_transmision(self):
        self.gui.root.update()

        self.stop = True
        self.gui.printToLogi("ZATRZYMANO TRANSMISJE")

        # Podział danych na pakiety

    def split_data(self, data_bytes):  # Pakiet danych 128 bajty
        packets = []
        for packetnr in range(int(len(data_bytes) / 128) + (len(data_bytes) % 128 > 0)):
            packetarray = bytearray()
            for byte in range(128):
                if (byte + 128 * packetnr < len(data_bytes)):
                    packetarray.append(data_bytes[byte + 128 * packetnr])
                else:
                    packetarray.append(0)
            packets.append(packetarray)  # Zwraca liste pakietow danych
        return packets
        # Wyslij pojedynczy pakiet

    def send_packet(self, packet_to_send, numberp, mode):
        while True:
            header = bytearray()  # Tworzymy nagłowek
            self.gui.root.update()
            if self.stop:
                ser.write(CAN)
                self.stop = False
                return False
            header.append(int.from_bytes(SOH, 'big'))
            header.append(numberp)
            header.append(255 - numberp)
            full = header + packet_to_send
            if mode == C:  # Tworzymy pakiet kontrolny
                full = full + self.crc16_mine(packet_to_send)
            if mode == NAK:
                full.append(self.checksuma(packet_to_send))
            ser.write(full)  # Wysyłamy nagłowek,pakiet danych
            # i pakiet kontrolny
            # print(full)
            # print(len(full))
            ser.flush()
            answer = ser.read()
            # print(answer)
            if answer == ACK:  # Po wysłaniu pakiet sprawdzamy odpowiedz
                break  # Jeśli ACK lub CAN przerywamy transmisje
            if answer == CAN:  # Jeśli NAK ponawiamy transmisje
                break
            else:
                print(answer)
        return True

    def send_data(self):
        # Zczytujemy dane pliku i dzielimy na pakiety
        databytes = self.read_file()
        returnetpackets = self.split_data(databytes)
        progress = len(returnetpackets)
        current_proggress = 0
        packet_number = 1
        ser.flush()
        initial_answer = ser.read()  # Czekamy na inicjalizacje transmisji przez odbiornik
        while initial_answer != C and initial_answer != NAK:
            ser.flush()
            initial_answer = ser.read()
            print(initial_answer)
            continue
        mode = initial_answer  # Wybór trybu odczytanego z odbiornika
        for bitpack in returnetpackets:  # Wysył kolejnych pakietów
            ser.flush()

            if self.send_packet(bitpack, packet_number, mode) == False:
                return
            info = "\nWyslano pakiet nr " + str(packet_number)
            self.gui.printToLogi(info)
            packet_number += 1
            current_proggress += 1
            self.gui.dodajprocent(int(current_proggress*100/progress))
            if packet_number > 255:
                packet_number = 0
            # Po zakończeniu transmisji wysyłamy sygnał End Of Transmission
        ser.write(EOT)
        if (ser.read()) == ACK:
            self.gui.printToLogi("\n100% DANYCH WYSLANO POPRAWNIE\n")

    # Funkcja licząca CRC

    def crc16(self, data: bytearray, poly=0x1021):
        crc = 0x0000
        for b in data:
            cur_byte = 0xFF & b  # Algorytm CRC XMODEM
            for _ in range(0, 8):
                if (crc & 0x0001) ^ (cur_byte & 0x0001):
                    crc = (crc >> 1) ^ poly
                else:
                    crc >>= 1
                cur_byte >>= 1
        crc = (~crc & 0xFFFF)
        crc = (crc << 8) | ((crc >> 8) & 0xFF)

        return crc & 0xFFFF

        # Funkcja wyliczając sume kontrolna

    def checksuma(self, data: bytearray):
        temp_sum = 0
        for byte in data:
            temp_sum += int(byte)
        return temp_sum % 256

        # Funkcja licząca CRC

    def crc16_mine(self, packet_to_check):
        checkarray = bytearray()
        crcinst = CrcXmodem()
        crcinst.process(packet_to_check)
        suma = crcinst.final()
        checkarray.append((suma >> 8) & 0xff)
        checkarray.append(suma & 0xff)
        return checkarray
        # Funkcja nadająca tryb przez odbiornik

    def start_recive(self, mode):
        while 1:
            time.sleep(0.1)
            self.gui.root.update()
            ser.write(mode)
            ser.flush()
            initial_recive = ser.read()
            if initial_recive == SOH:  # Jesli odbierzemy naglowek
                return initial_recive  # przejdz do odbioru

    def recive_data(self, mode, GUI):  # Funkcja odbierajaca dane
        self.gui.printToLogi("ODBIERAMY")
        initial_recive = self.start_recive(mode)
        file_bytes = bytearray()
        while 1:  # odbiermy kolejno pakiety
            data_pack = self.recive_packet(mode, initial_recive)
            if data_pack:
                file_bytes = file_bytes + data_pack
            initial_recive = ser.read()

            if initial_recive == EOT:  # do otrzymania znaku EOT
                break
            if data_pack == False:
                return
        ser.write(ACK)
        self.gui.printToLogi("\n100% danych otrzymano poprawnie\n")
        f = open(self.gui.filename, "wb")
        f.write(file_bytes)
        f.close()

    def recive_packet(self, mode, initial_recive):  # odbierz pojedynczy pakiet
        while True:
            recived_header = bytearray()  # naglowek
            recived_header += initial_recive
            recived_header += ser.read()
            recived_header += ser.read()
            packet = self.recive_data_packet()  # dane
            self.gui.root.update()
            if self.stop:
                ser.write(CAN)
                self.stop = False
                return False
            if self.check_packet(mode, packet):  # kontrola
                info = "\nOtrzymano pakiet nr " + str(recived_header[1])
                self.gui.printToLogi(info)

                return packet

    def recive_data_packet(self):  # odbierz pakiet danych
        packet_arr = bytearray()
        for byte in range(128):
            self.gui.root.update()
            packet_arr += ser.read()
        return packet_arr

        # Sprawdzanie poprawności odebranego pakietu

    def check_packet(self, mode, packet):
        if mode == NAK:  # tryb sumy kontrolnej
            check = bytearray()
            check += ser.read()
            selfcheck = bytearray()
            selfcheck.append(self.checksuma(packet))
            if selfcheck[0] == check[0]:  # Sprawdz czy poprawne
                ser.write(ACK)
                return True
            else:  # Wyślij odpowiedz
                ser.write(NAK)
                print(2)
                return False
        elif mode == C:  # tryb CRC
            check = bytearray()
            check += ser.read()
            check += ser.read()
            crc_16 = self.crc16_mine(packet)  # sprawdz crc
            for byte in range(2):
                if crc_16[byte] != check[byte]:  # wyslij odpowiedz
                    ser.write(NAK)
                    return False
                ser.write(ACK)
                return True


app = XmodemGUI()
app.start_gui()


