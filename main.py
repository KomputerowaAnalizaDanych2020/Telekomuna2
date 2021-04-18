import serial


def crc16(data: bytes, poly=0x8408):
    crc = 0xFFFF
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

def read_file(path):
    f = open(path, "rb")
    return f

path='test.txt'

ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

databytes=read_file(path)
sumacrc=crc16(databytes)
print(sumacrc)
if ser.isOpen():
    print(ser.name + ' is open...')

value = 1

while True:
    ser.write(str.encode(str(value)))
    value = int(input("Give me a number from 0 to 9: "))
