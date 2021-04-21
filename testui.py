from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog

filename = 'test.bmp'


def wyslijClick():
    logi_text.insert(INSERT, "wyslij ")
    print("wyslij")


def odbierzClick():
    logi_text.insert(INSERT, "odbierz ")
    print("odbierz")


def loadFile():
    filename = filedialog.askopenfilename(initialdir="/", title="Wybierz plik", filetypes='')


def saveFile():
    filename = filedialog.asksaveasfilename(initialdir="/", title="Wybierz plik")


def bitradio():
    print("stopbit" + stopbit.get())


root = Tk()
stopbit = StringVar()
stopbit.set("1.0")
mode = StringVar()
mode.set("NAK")

root.title("Xmodem 229952|230039")

com_port = StringVar()
com_port.set("COM2")
tytul_label = Label(root, text="XMODEM", font=(None, 17, 'bold'),fg='blue')
tytul_label.grid(row=0, column=0, columnspan=6)

tytul_label = Label(root, text="USTAWIENIA", font=(None, 14, 'bold'))
tytul_label.grid(row=1, column=0, columnspan=4)


tryb_frame = LabelFrame(root, text="Tryb:", padx=40, pady=8)
tryb_frame.grid(row=5, column=0, columnspan=2)
tryb_CRC = Radiobutton(tryb_frame, text="CRC", variable=mode, value="C")
tryb_Checksum = Radiobutton(tryb_frame, text="Checksum", variable=mode, value="NAK")
tryb_CRC.grid(row=0, column=0)
tryb_Checksum.grid(row=0, column=1)

stopbit_frame = LabelFrame(root, text="Bity stopu:", padx=40, pady=8)
stopbit_frame.grid(row=6, column=0, columnspan=2)
bitone = Radiobutton(stopbit_frame, text="1bit", variable=stopbit, value="1.0", command=bitradio)
bitonehalf = Radiobutton(stopbit_frame, text="1.5bit", variable=stopbit, value="1.5", command=bitradio)
bittwo = Radiobutton(stopbit_frame, text="2bit", variable=stopbit, value="2.0", command=bitradio)
bitone.grid(row=0, column=0)
bitonehalf.grid(row=0, column=1)
bittwo.grid(row=0, column=2)


odczyt_label = Label(root, text="Odczyt z pliku:")
odczyt_label.grid(row=2, column=0)
odczyt_button = Button(root, text="Wybierz Plik", command=loadFile)
zapisz_button = Button(root, text="Wybierz Plik", command=saveFile)
odczyt_button.grid(row=2, column=1)
zapisz_button.grid(row=4, column=1)

port_label = Label(root, text="Port COM:")
port_label.grid(row=3, column=0)
port_menu = OptionMenu(root, com_port, "COM1", "COM2", "COM3", "COM4")
port_menu.grid(row=3, column=1)

zapis_label = Label(root, text="Zapis do pliku:")
zapis_label.grid(row=4, column=0)

szerokosc_label = Label(root, text="Szerokość pasma")
szerokosc_label.grid(row=7, column=0)

podpis_label = Label(root, text="©Daniel Malicki/Maciej Wlodarczyk")
podpis_label.grid(row=11, column=4)

szerokosc_entry = Entry(root, width=8)
szerokosc_entry.grid(row=7, column=1)
szerokosc_entry.insert(0, 9600)

logi_text = scrolledtext.ScrolledText(root, width=60, height=15)
logi_text.grid(row=2, column=4, rowspan=8)

wyslij_button = Button(root, text="Wyślij",font=(None, 13,'bold'), width=20, height=3,bg='green', command=wyslijClick)
odbierz_button = Button(root, text="Odbierz",font=(None, 13,'bold'), width=20, height=3,bg='red', command=odbierzClick)
odbierz_button.grid(row=2, column=5,rowspan=2)
wyslij_button.grid(row=6, column=5,rowspan=2)

"""
mybutton1 = Button(root,text=" Test !")
mybutton1.grid(row=0, column=0)
mybutton2 = Button(root,text=" Test2 !",pady=50)
mybutton2.grid(row=1, column=1)
e = Entry(root)
e.grid(row=2,column=2)

"""
root.mainloop()
