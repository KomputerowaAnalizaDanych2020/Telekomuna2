from crccheck.crc import Crc32, CrcXmodem
from crccheck.checksum import Checksum32
import serial
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

def checksuma(data: bytearray):
    temp_sum =0
    for byte in data:
        temp_sum+=int(byte)
    return temp_sum % 256


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


def split_data(data_bytes):
    packets=[]
    for packetnr in range(int(len(data_bytes)/128) + (len(data_bytes)%128 > 0)):
        packetarray = bytearray()
        for byte in range(128):
            if(byte+128*packetnr<len(data_bytes)):
                packetarray.append(data_bytes[byte+128*packetnr])
            else:
                packetarray.append(0)
        packets.append(packetarray)
    return packets


def read_file(path):
    f = open(path, "rb")
    bytesfile=f.read()
    return bytesfile


def send_packet(packet_to_send,numberp,mode):
    crcinst = CrcXmodem()
    while True:
        header = bytearray()
        header.append(int.from_bytes(SOH,'big'))
        header.append(numberp+1)
        header.append(254-numberp)
        full=header+packet_to_send
        if mode==C:
            suma = crcinst.final()
            crcinst.process(packet_to_send)
            full.append((suma>>8) & 0xff)
            full.append(suma & 0xff)
        if mode==NAK:
            full.append(checksuma(packet_to_send))
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

path = 'test1.bmp'

def send_data(path):
    databytes = read_file(path)
    returnetpackets = split_data(databytes)
    packet_number = 0
    initialAnswer=ser.read()
    while initialAnswer!=C and initialAnswer!=NAK:
        initialAnswer=ser.read()
        print(initialAnswer)
        continue
    mode=initialAnswer
    for bitpack in returnetpackets:
        ser.flush()
        send_packet(bitpack,packet_number,mode)
        packet_number += 1
    ser.write(EOT)
send_data(path)
