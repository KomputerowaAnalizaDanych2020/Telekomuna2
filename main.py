import serial
ser = serial.Serial(
    port='COM2',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def crc16(data: bytearray, poly=0x8408):
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
def split_data(data_bytes):
    packets=[]
    bytearray
    for packetnr in range(int(len(data_bytes)/128)):
        packetarray = bytearray()
        for byte in range(128):
            packetarray.append(data_bytes[byte*packetnr])
        packets.append(packetarray)
    return packets


def read_file(path):
    f = open(path, "rb")
    bytesfile=f.read()
    return bytesfile

def send_packet(packet_to_send):
    ser.write(packet_to_send)



path='test1.bmp'
databytes=read_file(path)
returnetpackets=split_data(databytes)
for bitpack in returnetpackets:
    #print(bitpack)
    #print(crc16(bitpack))
    send_packet(bitpack)

"""
if ser.isOpen():
    print(ser.name + ' is open...')

value = 1

while True:
    ser.write(str.encode(str(value)))
    value = int(input("Give me a number from 0 to 9: "))
"""