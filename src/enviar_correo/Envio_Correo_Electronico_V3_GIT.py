from machine import Pin, reset
import umail
import network
import socket
import time

# Your network credentials
nombreRed = 'nombreRed'
password = 'password'

# Email details
sender_email = 'arquitecturahardware1@gmail.com'
sender_name = 'ArquitecturaHardware'
sender_app_password = 'lpdx gtxd ciks evzc'
recipient_email = 'arquitecturahardware1@gmail.com'
email_subject = 'Prueba Correo desde la ESP32'

def connect_wifi(nombreRed, password):
  #Connect to your network
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(nombreRed, password)
  while station.isconnected() == False:
    pass
  print('Conexión Exitosa con la red: %s' % nombreRed)
  print('IP: %s\nSUBNET: %s\nGATEWAY: %s\nDNS: %s' % station.ifconfig()[0:4])

# Connect to your network
connect_wifi(nombreRed, password)

# Output Pin
output1 = Pin(2, Pin.OUT)
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('', 80)) # Desde cualquier IP se escucha en el puerto 80
    tcp_socket.listen(5) # Reconoce solo 5 socket a la vez
    time.sleep(1)
    print('Configuración del Socket corresta\n')
except OSError as e:
    print('Fallo al configurar el socket. Reiniciando...\n')
    time.sleep(3)
    reset()
    print('Servidor Arriba! \n********************************\n')

# Send the email
def send_email():
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write("Hola desde la ESP32")
    smtp.send()
    smtp.quit()

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
        conn.close()
    time.sleep(0.1)
