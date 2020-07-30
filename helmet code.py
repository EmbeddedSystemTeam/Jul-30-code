import board
import displayio
import digitalio
import time
from analogio import AnalogIn
import neopixel
from secrets import secrets
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
import busio
from digitalio import DigitalInOut
import adafruit_esp32spi.adafruit_esp32spi_socket as socket


esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)


spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

x = AnalogIn(board.A0)
y= AnalogIn(board.A1)
z = AnalogIn(board.A2)

requests.set_socket(socket, esp)

dot = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

h = 0
hits = h

url = 'http://608dev.net/sandbox/mostec/helmet'




if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
    print("ESP32 found and in idle mode")

print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

while True:
    if x.value > 40000:
        h += 1
        b += 1
        print ('WHAM')
        time.sleep(1)
    if x.value < 40000:
        dot[0] = [0,255,0]
    if h == 2:
        dot[0] = [100,255,0]
    elif h == 3:
        dot[0] = [200,200,0]
    elif h == 4:
        dot[0] = [255,100,0]
    elif h >= 5:
        dot[0] = [255,0,0]
        time.sleep(2)
        print ('pull player')

    try:
        n = requests.post("http://608dev.net/sandbox/mostec/helmet?hits=300")
        r = requests.get("http://608dev.net/sandbox/mostec/helmet?hits")
        first = r.text.split(":")
        second = first[1].split(",")
        third = second[0].split("'")
        s = third[1]
        b = (int(s))
    except Exception as e:
        print(e)


    print((x.value, y.value, z.value))
    print (h)
    print (b)
    time.sleep(0.05)
