from machine import Pin
import time import sleep

pir_hc_sr501 = Pin(13, Pin.IN)  # Configura el pin GPIO13 como entrada

while True:
    if pir_hc_sr501.value():  # Si se detecta movimiento
        print("¡Movimiento detectado!")
    time.sleep(3)  # Espera 1 segundo antes de volver a verificar
