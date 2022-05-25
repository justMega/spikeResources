import board
import busio
import time

# definicija uart protokola
uart = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600,
                  timeout=0, parity=None, stop=1)

# ista funkcija za branje podatkov kot pri Spiku


def readFromSpike():
    message_started = False
    while 1:
        byte_read = uart.read(1)  # Read one byte over UART lines
        #data = e.write("10")
        if not (byte_read is None):
            if message_started:
                if byte_read == b">":
                    # End of message. Don't record the ">".
                    # Now we have a complete message. Convert it to a string, and split it up.
                    message_parts = "".join(message).split(",")
                    # print(message_parts[0])
                    message_started = False
                    return message_parts[0]
                else:
                    # Accumulate message byte.
                    try:
                        message.append(chr(byte_read[0]))
                    except:
                        pass
            if byte_read == b"<":
                # Start of message. Start accumulating bytes, but don't record the "<".
                message = []
                message_started = True
                # print(self.message_started)


# primer uporabe
i = 0
j = 5
while 1:
    ident = readFromSpike()
    if ident == "a":
        uart.write(bytes(f"<{i}>", "ascii"))
        print(i)
        time.sleep(0.1)
        i += 1
        if i > 5:
            i = 0
    elif ident == "b":
        uart.write(bytes(f"<{j}>", "ascii"))
        time.sleep(0.1)
        j += 1
        if j > 10:
            j = 5
