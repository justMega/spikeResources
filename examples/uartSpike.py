# LEGO type:standard slot:2 autostart

import utime
import hub
from hub import port


portB = port.B
portB.mode(1)
utime.sleep_ms(2000)
portB.baud(9600)


class picoSensor:
    def __init__(self, port, timeOut: int, id: str):
        self.port = port
        self.message_started = False
        self.timeOut = timeOut
        self.id = id

    def read(self):
        self.write("<"+self.id+">")
        start = utime.time()
        # print(start)
        while 1:
            byte_read = self.port.read(1)  # Read one byte over UART lines
            #data = e.write("10")
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

    def write(self, str):
        self.port.write(str)


pico = picoSensor(portB, 3, "a")
pico1 = picoSensor(portB, 3, "b")

while 1:
    val1 = 0
    val = pico.read()
    if val % 2 == 0:
        val1 = pico1.read()
    print("this is val: ", val+val1, " ", type(val))
    hub.display.show(str(val))
