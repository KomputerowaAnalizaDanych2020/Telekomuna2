import serial

ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)



if ser.isOpen():
    print(ser.name + ' is open...')

value = 1

while True:
    ser.write(str.encode(str(value)))
    value = int(input("Give me a number from 0 to 9: "))
