import time
import serial
import AMB8826

receiver = serial.Serial(  # initializes the receiver on COM4
    port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
if receiver.isOpen():
    receiver.close()
    receiver.open()
    receiver.isOpen()

# ###################### USER CODE BEGIN ######################

while True:
    print("Received (new): ", AMB8826.get_answer_address_mode_1(receiver))


# ###################### USER CODE END ######################

receiver.close()
