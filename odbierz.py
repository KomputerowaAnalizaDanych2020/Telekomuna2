import serial
import time
ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
SOH=bytearray.fromhex("01")
EOT=bytearray.fromhex("04")
ACK=bytearray.fromhex("06")
NAK=bytearray.fromhex("15")
CAN=bytearray.fromhex("18")
C=bytearray.fromhex("43")
ser.write(C)

while 1:

    answer = ser.read()
    print(answer)
    time.sleep(0.1)
    ser.write(ACK)

    print("\nKOLEJNY PAKIET-----------------------------------------------\n")