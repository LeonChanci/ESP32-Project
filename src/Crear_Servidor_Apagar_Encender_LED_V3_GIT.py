from machine import Pin, reset
import network
import socket
import time

import gc
gc.collect() # Limpiar posible basura en memoria


#***********************************************************#
# Esta función es la encargada de coenctarse a la red WI-FI #
#***********************************************************#
nombreRed = 'NAME_RED'
key = 'CONTRASENA_RED'

wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    wlan.active(True)
    wlan.connect(nombreRed, key)
    print('Conectando a la red WiFi: %s' % nombreRed)
    timeout = time.ticks_ms()
    while not wlan.isconnected():
        if (time.ticks_diff (time.ticks_ms(), timeout) > 10000):
            break
    if wlan.isconnected():
        print('Conexión Exitosa con la red: %s' % nombreRed)
        print('IP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % wlan.ifconfig()[0:4])
    else:
        wlan.active(False)
        print('Falló la conexión a la red WiFi: %s' % nombreRed)
else:
    print('Connected\nIP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % wlan.ifconfig()[0:4])

#Output Pin
output1 = Pin(2, Pin.OUT)

#******************************************************************#
# Esta función es la encargada de crea un socket TCP (SOCK_STREAM) #
#******************************************************************#
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80)) # Desde cualquier IP se escucha en el puerto 80
    tcp_socket.listen(5) # Reconoce solo 5 socket a la vez
    time.sleep(1)
    print('Successful socket configuration\n')
except OSError as e:
    print('Failed to socket configuration. Rebooting...\n')
    time.sleep(3)
    reset()
print('Servidor Arriba! \n********************************\n')


#*****************************************************#
# Esta función es la encargada de crear la página web #
#*****************************************************#

def web_page():
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>MicroPython Web Server</title>
    <link rel="shortcut icon" href="https://raw.githubusercontent.com/jhonatan-lamina/web-images/main/icon-snake.png">
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style type="text/css">
	    *{
		padding: 0px; margin: 0px;
		}
		.home{
			padding: 0px 0px 10px 0px; background-color: #ffffff;
		}
		.nav{
			box-sizing: border-box; display: inline-block;
			padding: 10px 0px 10px 0px; background-color:#063d6d;
			width: 100%; height: auto;
		}
		.control{
			box-sizing: border-box; display: inline-block;
			padding: 0px 0px 15px 0px; background-color: #cccccc;
			border: 4px solid #063d6d; border-radius: 20px;
			width: auto; height: auto; margin: 30px;
		}
		.myline {
		  border: 2px solid #063d6d;
		}
		#t1{
			font-family: Helvetica; font-weight: bold;
			text-align: center; font-size: 50px; color: white;
		}
		#t2{
			font-family: Helvetica; font-weight: bold;
			text-align: center; font-size: 20px; color: white;
		}
		#t3{
			font-family: Helvetica; font-weight: bold;
			font-size: 30px; color: #063d6d;
		}
		#imag{
			width: 200px; height: 200px; padding: 25px;
		}
		#on{
			border: 4px solid green; border-radius: 20px;
			background-color:white; color: green;
			font-weight: bold; font-size: 20px;
			width: 150px; height: 50px; cursor:pointer;
		}
		#off{
			border: 4px solid red; border-radius: 20px;
			background-color:white; color: red;
			font-weight: bold; font-size: 20px;
			width: 150px; height: 50px; cursor:pointer;
		}
  	</style>
</head>
<body>
	<div class='nav'>
		<h1 id='t1'>MicroPyton Web Server</h1>
	</div>
	<div class="home">
		<center>
            <div class="control">
                <img id="imag" src="https://raw.githubusercontent.com/jhonatan-lamina/web-images/main/animated-lamp.gif" alt="img">
                <hr class="myline"><br /> &ensp;
                <button id='on' type="button" onclick="window.location.href='/?control1=on'">ON</button> &ensp;
                <button id='off' type="button" onclick="window.location.href='/?control1=off'">OFF</button> &ensp;
            </div>
		</center>
	</div>
</body>
</html>
"""
    return html

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
        #print('Request:  %s' % request)
        if request.find('/?control1=on') == 6:
            print('OUTPUT1: ON')
            output1.value(1)
        if request.find('/?control1=off') == 6:
            print('OUTPUT1: OFF')
            output1.value(0)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(web_page())
        conn.close()
    except OSError as e:
        conn.close()
    time.sleep(0.1)
# Escribe tu código aquí :-)
