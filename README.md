# iotForUS

Get an alarm from a remote area (through LAN) if smoke is detected
#Client Side
import socket
import RPi.GPIO as GPIO
import time

HOST = '' #copy it from server side
PORT = 5000

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        while True:
            data = s.recv(1024).decode('utf-8')
            print(data)
            if str(data) == 'Alert':
                print('Gas Leakage Detected')
                GPIO.output(36,True)
                time.sleep(3)
                GPIO.output(36,False)
                time.sleep(3)
except:
    s.close()
    GPIO.cleanup()
#Get an alarm from a remote area (through LAN) if smoke is detected
#Server Side
import socket
import time
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

HOST = '' #use ifconfig
PORT = 5000

SPI_DEVICE = 0
SPI_PORT = 0

mcp = Adafruit_MCP3008.MCP3008(spi = SPI.SpiDev(SPI_PORT,SPI_DEVICE))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST,PORT))
        s.listen()
        print('Server Started')
        conn,addr = s.accept()
        with conn:
            print('Connnected By: ',addr)
            while True:
                value = mcp.read_adc(0)
                print('Gas value ',value,' units')
                if value > 300:
                    data = 'Alert'.encode('utf-8')
                    conn.sendall(data)
                time.sleep(3)
except:
    s.close()
    GPIO.cleanup()
