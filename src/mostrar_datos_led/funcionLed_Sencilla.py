# Complete project details at https://RandomNerdTutorials.com
from machine import Pin, SoftI2C
import sh1106

try:
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
    display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
    display.sleep(False)
    display.fill(0)
    # display.text('Primero', 0, 0, 1)
    # display.text('Segundo', 0, 8, 1)
    # display.text('Tercero', 0, 16, 1)
    # display.text('Cuarto', 0, 24, 1)
    display.text('Connect: WIFI', 12, 16, 1)
    display.text('ACADEMICA_POLI 6E', 8, 36, 1)
    display.hline(16, 46, 96, 1)
    display.vline(4, 4, 56, 1)
    # Linea vertical derecha
    display.vline(124, 4, 56, 1)
    # Linea horizontal up
    display.hline(4, 4, 120, 1)
    # Linea vertical down
    display.hline(4, 60, 120, 1)
    display.show()
    # display.text('Quinto', 0, 32, 1)
    # display.text('Sexto', 0, 40, 1)
    # display.text('Septimo', 0, 48, 1)
    # display.text('Octavo', 0, 56, 1)
    # display.text('Noveno', 0, 64, 1)
    display.show()
    print("Terminó Ejecución OK")
except OSError as e:
    print('Fallo La Ejecución. %s' % e)
