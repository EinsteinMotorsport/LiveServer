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

counter = 0
while True:
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex('{0:02X}'.format(counter)))
    counter += 1
    time.sleep(0.04)  # with 0.04 sending 25 messages per second
    print(counter)

# ###################### USER CODE END ######################

sender.close()
