import time
from threading import Timer
import serial
import AMB8826


sender = serial.Serial(  # initializes the receiver on COM4
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
if sender.isOpen():
    sender.close()
    sender.open()
    sender.isOpen()

# ###################### USER CODE BEGIN ######################
message_filler = "0011223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11"  # 122 bytes  # Setup for later
counter = 0
while True:
    appendix = '{0:02X}'.format(counter)
    if len(appendix) % 2 != 0:
        appendix = "0" + appendix
    message = message_filler + appendix
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex(message))
    counter += 1
    time.sleep(0.04)  # with 0.04 sending 25 messages per second
    print(counter)

# ###################### USER CODE END ######################

sender.close()
