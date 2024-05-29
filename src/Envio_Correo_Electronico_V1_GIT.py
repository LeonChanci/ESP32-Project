import umail
import network

# Your network credentials
ssid = 'NAME_RED'
password = '123'

# Email details
sender_email = 'arquitecturahardware1@gmail.com'
sender_name = 'Arquitectura Hardware 2024'
sender_app_password = 'lpdx gtxd ciks evzc'
recipient_email ='arquitecturahardware1@gmail.com'
email_subject ='Test Email'

def connect_wifi(ssid, password):
  #Connect to your network
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())

# Connect to your network
connect_wifi(ssid, password)

# Send the email
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
smtp.login(sender_email, sender_app_password)
smtp.to(recipient_email)
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
smtp.write("Hello from ESP32")
smtp.send()
smtp.quit()
