import network
import gc
gc.collect()

# Función para conectarse a la RED WIFI
def connect_wifi(nombreRed, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(nombreRed, password)
    while not station.isconnected():
        pass
    print('\n********************************\n')
    print('Conexión Exitosa con la red: %s' % nombreRed)
    print('IP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % station.ifconfig()[0:4])
