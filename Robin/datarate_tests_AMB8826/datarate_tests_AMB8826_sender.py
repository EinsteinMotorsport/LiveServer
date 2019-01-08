import time
import serial
import AMB8826


sender = serial.Serial(  # initializes the sender on COM3
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)
if sender.isOpen():
    sender.close()
    sender.open()
    sender.isOpen()


# ###################### USER CODE BEGIN ######################

while True:
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex("01020203030304040404"))
    time.sleep(1)


# ###################### USER CODE END ######################

sender.close()

