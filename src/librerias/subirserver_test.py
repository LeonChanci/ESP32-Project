import machine
import socket
import time
import gc
gc.collect()

# Función para configurar el Socket para Subir el Servidor
def up_socket():
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.bind(('', 80))
        tcp_socket.listen(5)
        time.sleep(1)
        print('Configuración del Socket Correcta\n')
        print('\n********************************\n')
        print('¡Servidor Arriba! \n********************************\n')
        return tcp_socket
    except OSError as e:
        print('Fallo al configurar el socket. %s' % e)
        print('\n...Reiniciando...')
        time.sleep(3)
        machine.reset()
