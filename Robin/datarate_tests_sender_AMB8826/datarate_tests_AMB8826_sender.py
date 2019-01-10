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

# AMB8826.get_all_properties(sender)

continue_test = True
start_indication = "FF"
message_filler =    "00112233445566778899001122334455667788990011223344556677889900112233445566778899001122334455667788990011223344556677889900112233445566778899001122334455667788990011223344556677889900112233445566778899001122334455667788990011223344556677889900112233445566"  # 127 bytes
while continue_test:
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_string(start_indication))
    start_time = int(round(time.time() * 1000))
    x = 0
    for x in range(26):
        message = message_filler + '{0:02X}'.format(x)
        AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex(message))
        time.sleep(0.035)
    answer = AMB8826.get_answer_address_mode_1(sender)
    if answer[4] == 88:
        end_time = int(round(time.time() * 1000))
        duration = end_time - start_time
        print(duration)
        continue_test = False

# ###################### USER CODE END ######################

sender.close()

