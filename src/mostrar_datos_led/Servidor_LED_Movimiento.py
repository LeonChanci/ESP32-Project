from machine import Pin, reset, RTC, SoftI2C
from time import sleep
import _thread
import umail
import socket
import time
import gc
import coneccionwifi
import sh1106

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(2), 0x3c)
buzzer = Pin(3, Pin.OUT)
# display.sleep(False)
# display.fill(0)
# display.text('Holii', 0, 0, 1)
# display.show()


gc.collect()

# Credenciales de la RED WIFI
RED_NAME = 'TIGO_UNE'
PASS = '12345678'

# Configuración de los datos para el EMAIL
sender_email = 'luisa.598@hotmail.com'
sender_name = 'Arquitectura Hardware 2024'
sender_app_password = 'lpdx gtxd ciks evzc'
recipient_email = 'jonier01@gmail.com'
email_subject = 'Prueba Correo Electrónico desde la ESP32'

# Llamar función para conectarse a la RED WiFI
coneccionwifi.connect_wifi(RED_NAME, PASS)

# Obtener Fecha y Hora Actual
(year, month, day, weekday, hour, minute, second, milisecond) = RTC().datetime()
RTC().init((year, month, day, weekday, hour-5, minute, second, milisecond))

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
    print('...Reiniciando...\n')
    time.sleep(3)
    reset()

def web_page():
    html_page = """
<!DOCTYPE html>
 <html>
  <head>
    <title>MicroPython Web Server - Sensor Movimiento</title>
    <link rel="shortcut icon"
    href="https://raw.githubusercontent.com/LeonChanci/ESP32-Project/main/src/img/micropython-logo.png">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
  <script>
   var AjaxSolicitud = new XMLHttpRequest();

   function CargarAjax(ajaxURL)
   {
    AjaxSolicitud.open('GET',ajaxURL,true);
    AjaxSolicitud.onreadystatechange = function()
    {
     if(AjaxSolicitud.readyState == 4 && AjaxSolicitud.status==200)
     {
      var AjaxRespuesta = AjaxSolicitud.responseText;
      var tmpArray = AjaxRespuesta.split("|");
      document.getElementById('movimiento').innerHTML = tmpArray[0];
      document.getElementById('fecha').innerHTML = tmpArray[1];
      document.getElementById('hora').innerHTML = tmpArray[2];
     }
    }
    AjaxSolicitud.send();
   }

   function cargar_datos_sensor()
   {
     CargarAjax('cargar_datos');
   }

   setInterval(cargar_datos_sensor, 2000);

  </script>
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
        #buttonSensar{
            border: 4px solid #009d71;
            background-color:white; color: #009d71;
            font-weight: bold; font-size: 13px;
            width: 150px; height: 50px; cursor:pointer;
        }
        #buttonSensar:hover{
            background-color: #026842;
        }
        #buttonSensar:active{
            background-color: #026842;
        }
        </style>
  </head>
  <body class='body'>
   <div class='nav'>
    <h1 id='t1'>MicroPython Web Server</h1>
   </div>
   <div class="home">
    <center>
    <h1>Sensor Movimiento - Ajax</h1>
     <div id='main' class="control">
      <div id='content'>
       <p>Movimiento: <strong><span id='movimiento'>--.-</span></strong></p>
       <p>Fecha: <strong><span id='fecha'>--.-</span></strong></p>
       <p>Hora: <strong><span id='hora'>--.-</span></strong></p>
       <hr class="myline"><br /> &ensp;
       <button id='buttonSensar' type="button"
        onclick="window.location.href='/?sensar=on'">Último Movimiento
       </button> &ensp;
      </div>
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
    return html_page

motion = False
last_move = "FALSE" + "|" + "..." + "|" + "..."
movimiento = "0"

def pintar(texto):
    display.fill(0)
    display.text(texto, 0, 0, 1)
    display.show()
    buzzer.value(1)

pintar('Holiiii')

def pintar2(texto):
    display.fill(0)
    display.text(texto, 0, 0, 1)
    display.show()
    buzzer.value(0)

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


def handle_interrupt(pin):
    global interrupt_pin
    global motion
    global last_move
    global movimiento
    interrupt_pin = pin
    motion = True
    last_move = "cargando..." + "|" + "cargando..." + "|" + "cargando..."
    movimiento = "0"

# led_esp32 = Pin(2, Pin.OUT)
pir_hc_sr501 = Pin(2, Pin.IN)
pir_hc_sr501.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

def motion_thread():
    global motion
    global last_move
    global movimiento
    global display
    while True:
        if motion:
            print("¡Movimiento Detectado!")
            for _ in range(5):
                # led_esp32.on()
                sleep(0.10)
                # led_esp32.off()
                sleep(0.10)
                movimiento = "TRUE"
                pintar('Detectado')
                # send_email()
                # display.fill(0)
                # display.text('Detectado', 0, 0, 1)
                # display.show()

                fecha = "{:02d}/{:02d}/{}".format(RTC().datetime()[2], RTC().datetime()[1], RTC().datetime()[0])
                hora = "{:02d}:{:02d}:{:02d}:{:02d}".format(RTC().datetime()[4], RTC().datetime()[5], RTC().datetime()[6], RTC().datetime()[7])
                last_move = movimiento + "|" + fecha + "|" + hora
            print("¡Movimiento Detenido!")
            pintar2(' ')
            # display.fill(0)
            # display.show()
            motion = False
            return last_move
        sleep(1)
        return last_move
    return last_move


def response_thread():
    while True:
        if gc.mem_free() < 102000:
            gc.collect()

        conexion, addr = tcp_socket.accept()
        request = conexion.recv(1024)
        request = str(request)
        response = request.find('/cargar_datos')
        last_move = motion_thread()
        print('Sensor Listo - Sensando: %s' % last_move)
        if response == 6:
            respuesta = last_move
        else:
            respuesta = web_page()

        conexion.send('HTTP/1.1 200 OK\n')
        conexion.send('Content-Type: text/html\n')
        conexion.send('Connection: close\n\n')
        conexion.sendall(respuesta)
        conexion.close()

_thread.start_new_thread(motion_thread, ())
_thread.start_new_thread(response_thread, ())
