# LEGO type:standard slot:2 autostart

import utime
import hub
from hub import port

# definicija porta - kje je priključen pico
portB = port.B
"""
MODE_DEFAULT = 0
MODE_FULL_DUPLEX = 1
MODE_HALF_DUPLEX = 2
MODE_GPIO = 3
"""
portB.mode(1)
# potrebno počakati par sekund, da se naložijo potrebne funkcije
utime.sleep_ms(2000)
# nastavitev hitrosti komunikacije, se mora ujemati z hitrostju na pico
portB.baud(9600)

"""
razred picoSensor - podobno kot npr. ColorSensor
potrebuje 3 parametre: 
*port - kje je priključen pico
*timeOut - koliko časa preden se komunikacija zaključi - primer pico se med vožnjo robota odklopi
a spike tega ne ve, čaka v neskončnost, da prejme konec sporočila -> timeOut bo v takšnem primeru
prekinil program in dal ERROR
*id - poseben znak za posamezen senzor mora biti podan kot string -> z njegovo pomočjo lahko pico 
ve kateri senzor želimo klicati
"""


class picoSensor:
    # funkcija, ki skrbi za inicializacijo
    def __init__(self, port, timeOut: int, id: str):
        self.port = port
        self.message_started = False
        self.timeOut = timeOut
        self.id = id

    """
    funkcija za branje podatkov, ki jih posreduje pico
    najprej pico pošlje id senzorja nato pa čaka na sporočilo
    sporočilo je oblike <podatek>, kjer znak < označuje začetek podatka, znak > pa konec
    funkcija vrne podatek kot int
    """

    def read(self):
        self.write("<"+self.id+">")
        start = utime.time()
        while 1:
            byte_read = self.port.read(1)  # Read one byte over UART lines
            if not (byte_read is None):
                if self.message_started:
                    if byte_read == b">":
                        # End of message. Don't record the ">".
                        # Now we have a complete message. Convert it to a string, and split it up.
                        message_parts = "".join(message).split(",")
                        # print(message_parts[0])
                        self.message_started = False
                        return int(message_parts[0])
                    else:
                        # Accumulate message byte.
                        try:
                            message.append(chr(byte_read[0]))
                        except:
                            pass
                if byte_read == b"<":
                    # Start of message. Start accumulating bytes, but don't record the "<".
                    message = []
                    self.message_started = True
                    # print(self.message_started)
                if utime.time() - start >= self.timeOut:
                    raise Exception("Timeout exceded. Is pi pico connected?")

    # s to funkcijo lahko pošjemo poljubno sporočilo pico
    def write(self, str):
        self.port.write(str)


# definicija senzorjev
pico = picoSensor(portB, 3, "a")
pico1 = picoSensor(portB, 3, "b")

# primer uporabe
while 1:
    val1 = 0
    val = pico.read()
    if val % 2 == 0:
        val1 = pico1.read()
    print("this is val: ", val+val1, " ", type(val))
    hub.display.show(str(val))
