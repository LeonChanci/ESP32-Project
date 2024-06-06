from machine import Pin, reset
import umail
import socket
import time
import gc
import coneccionwifi

gc.collect()

# Credenciales de la RED WIFI
RED_NAME = 'RED_NAME'
PASS = 'PASS'

# Configuración de los datos para el EMAIL
sender_email = 'arquitecturahardware1@gmail.com'
sender_name = 'Arquitectura Hardware 2024'
sender_app_password = 'lpdx gtxd ciks evzc'
recipient_email = 'arquitecturahardware1@gmail.com'
email_subject = 'Prueba Correo Electrónico desde la ESP32'

# Llamar función para conectarse a la RED WiFI
coneccionwifi.connect_wifi(RED_NAME, PASS)

# PIN de salida LED Azul de la ESP32
output1 = Pin(2, Pin.OUT)
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80))
    tcp_socket.listen(5)
    time.sleep(1)
    print('Configuración del Socket Correcta\n')
    print('\n********************************\n')
    print('¡Servidor Arriba! \n********************************\n')
except OSError as e:
    print('Fallo al configurar el socket. %s' % e)
    print('\n...Reiniciando...')
    time.sleep(3)
    reset()

# Función para enviar el EMAIL
def send_email():
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write("Hola desde la ESP32")
    print('Enviando Correo a la dirección: %s' % recipient_email)
    smtp.send()
    print('Correo Enviado exitosamente\n********************\n')
    smtp.quit()
# Función para crear el HTML del SERVIDOR WEB
def web_page():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>MicroPython Web Server - Envio Correo</title>
    <link rel="shortcut icon"
    href="https://raw.githubusercontent.com/LeonChanci/ESP32-Project/main/src/img/micropython-logo.png">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
        .body{
            padding: 0px; margin: 0px;
        }
        .home{
            padding: 0px 0px 10px 0px;
        }
        .nav{
            box-sizing: border-box; display: inline-block;
            background-color:#0E1424; width: 100%; height: auto;
        }
        .control{
            box-sizing: border-box; display: inline-block;
            padding: 0px 0px 15px 0px; background-color: #8A8FA3;
            border: 4px solid #0E1424; width: auto;
            height: auto; margin: 10px;
        }
        .myline {
            border: 2px solid #0E1424;
        }
        #t1{
            font-family: Helvetica; font-weight: bold;
            text-align: center; font-size: 39px; color: white;
        }
        #t2{
            font-family: sans-serif; font-weight: bold;
            text-align: center; font-size: 11px; color: #0E1424;
        }
        #imag{
            width: 160px; height: 160px; padding: 25px;
        }
        #on{
            border: 4px solid #009d71;
            background-color:white; color: #009d71;
            font-weight: bold; font-size: 20px;
            width: 150px; height: 50px; cursor:pointer;
        }
        #on:hover{
            background-color: #026842;
        }
        #on:active{
            background-color: #026842;
        }
        #off{
            border: 4px solid #DC143C;
            background-color:white; color: #DC143C;
            font-weight: bold; font-size: 20px;
            width: 150px; height: 50px; cursor:pointer;
        }
        #off:hover{
            background-color: #9C0720;
        }
        #off:active{
            background-color: #9C0720;
        }

        </style>
</head>
<body class="body">
  <div class="nav">
    <h1 id='t1'>MicroPython Web Server</h1>
  </div>
  <div class="home">
  <center>
    <h1>Enviar Correo - ON</h1>
    <div class="control">
    <img id="imag"
        src="https://raw.githubusercontent.com/LeonChanci/ESP32-Project/main/src/img/led_on_led_off.gif"
        alt="img">
    <hr class="myline"><br /> &ensp;
    <button id='on' type="button"
        onclick="window.location.href='/?control1=on'">ON
    </button> &ensp;
    <button id='off' type="button"
        onclick="window.location.href='/?control1=off'">OFF
    </button> &ensp;
    </div>
    </center>
        <footer>
            <center>
                <h3 id="t2"> Arquitectura del Hardware - 2024 </h3>
                <img
                    src="https://raw.githubusercontent.com/LeonChanci/ESP32-Project/main/src/img/micropython.png"
                    alt="img" width="100px">
            </center>
        </footer>
  </div>
</body>

</html>
"""
    return html

# Función para recibir las peticiones
while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = tcp_socket.accept()
        conn.settimeout(3.0)
        print('Nueva conexión desde: %s' % str(addr[0]))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        if request.find('/?control1=on') == 6:
            print('OUTPUT1: ON')
            output1.value(1)
            send_email()
        if request.find('/?control1=off') == 6:
            print('OUTPUT1: OFF')
            output1.value(0)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(web_page())
        conn.close()
    except OSError as e:
        print('Error 404 %s' % e)
        conn.close()
    time.sleep(0.1)
