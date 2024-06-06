# The MicroPython Project - ESP32
<p align="center">
  <img src="https://raw.githubusercontent.com/LeonChanci/ESP32-Project/main/src/img/micropython.png" alt="MicroPython Logo" alt="img" width="500px"/>
</p>

This is the `MicroPython` project, which aims to put an implementation of `Python` on microcontrollers and small embedded systems. You can find the official website at [micropython.org](http://www.micropython.org).



## Politécnico Colombiano Jaime Isaza Cadavid
### *Arquitectura del Hardware 2024-1*

Introducción
---------------

El proyecto que se desarrollará se centra en el desarrollo de funcionalidades utilizando el microcontrolador `ESP32`(System on a chip / Sistema en un Chip). Este dispositivo nos permitirá crear un servidor con el que podemos controlar (apagar o encender un LED en la `ESP32`). También podremos observar cómo funciona la detección de movimiento por infrarrojo usando un sensor `Pir HC-SR501` y al detectar movimiento podríamos hacer una funcionalidad como enviar un mensaje por correo electrónico o mensaje de texto indicando que hubo un movimiento; simulando una alarma. Se podría usar también un dispositivo `Leds 8x8 MAX7219` para mostrar información recopilada.

La importancia de este proyecto radica en investigar cómo se puede programar una placa electrónica (que solo entiende lenguaje de máquina) utilizando el lenguaje de alto nivel como lo es Python; en este caso MicroPython


Objetivos
---------------

El objetivo principal de este trabajo es explorar y desarrollar cuatro funcionalidades utilizando la `ESP32`. Estas funcionalidades se programaran en el lenguaje de `Python` (`MicroPython`) y abarcan desde la interacción con sensores hasta la comunicación por mensajería e inalámbrica y la visualización de datos. A lo largo de este documento, describiremos las funcionalidades a desarrollar y se subirá el código a Git como medio de versionamiento de código.

- **Desarrollo en MicroPython:** Utilizar `MicroPython` como lenguaje de alto nivel para desarrollar las funcionalidades utilizando las librerías disponibles que nos ofrece el lenguaje de programación.
- **Versionar el código fuente:** Utilizar la herramienta `Git` como medio de versionamiento del código de las diferentes funcionalidades.
- **Implementar sensores:** Conectar y calibrar un sensor de movimiento (`Pir HC-SR501`) al `ESP32`.
- **Configurar comunicación:** Establecer una conexión `Wi-Fi` con el `ESP32` y configurar la transmisión de datos por correo electrónico o por otro medio.
- **Crear y configurar un servidor:** Establecer la comunicación a un servidor para mandar y/o recibir peticiones desde la web.
- **Utilizar otros dispositivos:** Conectar otros dispositivos como un `Leds 8x8 MAX7219` para mostrar diferentes datos recopilados en la `ESP32`.


Funcionalidades
---------------
-  Crear Servidor Web
-  Sensor de movimiento
-  Mensajería (enviar correo electrónico o SMS)
-  LED (mostrar datos en LED)

