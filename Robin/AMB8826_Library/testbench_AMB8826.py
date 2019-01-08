import time
import serial
import AMB8826

sender_or_and_receiver = 2  # 1 for sender, 2 for both

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

if sender_or_and_receiver == 2:
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


AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex("01020203030304040404"))
# print("Received: ", AMB8826.get_single_input_buffer_answer_6(receiver))
print("Received (new): ", AMB8826.get_answer_address_mode_1(receiver))


# ###################### USER CODE END ######################

sender.close()
if sender_or_and_receiver == 2:
    receiver.close()

