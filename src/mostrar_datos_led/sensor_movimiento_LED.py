# Complete project details at https://RandomNerdTutorials.com
from machine import Pin, SoftI2C
import sh1106
import time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.fill(0)
display.text('Prueba de inicio', 0, 25, 1)
display.show()

pir_sensor = Pin(13, Pin.IN)

while True:
    # Check the PIR sensor value
    val_sensor = pir_sensor.value()
    time.sleep(0.1)
    if val_sensor == 0:
        print(val_sensor)
    else:
        print(val_sensor)
        display.fill(0)
        display.text('*Move Detected*', 0, 25, 1)
        display.show()
    time.sleep(1.5)
    val_sensor = 0
    display.fill(0)
    display.show()
