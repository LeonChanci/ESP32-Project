from machine import Pin
from time import sleep
import gc

gc.collect()
motion = False
def handle_interrupt(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin

led_esp32 = Pin(2, Pin.OUT)
pir_hc_sr501 = Pin(13, Pin.IN)
pir_hc_sr501.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
while True:
    if motion:
        print("¡Movimiento Detectado!")
        for _ in range(5):
            led_esp32.on()
            sleep(0.20)
            led_esp32.off()
            sleep(0.20)
        print("¡Movimiento Detenido!")
        motion = False
    sleep(1)
