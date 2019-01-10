import time
import serial
import AMB8826
from threading import Timer


def timeout():
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex("FE"))


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

amount_of_messages = 20  # Setup for later
continue_test = True  # Setup for later
start_indication = "FF"  # Setup for later
message_filler = "0011223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "112233445566"  # 127 bytes  # Setup for later
while continue_test:  # Is active while the test runs until the test ended
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_string(start_indication))  # Sends the start signal
    start_time = int(round(time.time() * 1000))  # Remembering the start point
    x = 0  # Setup for later
    for x in range(amount_of_messages):  # Sending the whole amount of messages
        message = message_filler + '{0:02X}'.format(x)  # Filler plus the counter
        AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex(message))  # sending
        time.sleep(0.035)  # Wait until sending the next message
    t = Timer(5, timeout)  # Initializing the Timer
    t.start()  # Starting the timer
    answer = AMB8826.get_answer_address_mode_1(sender)  # waiting for an answer
    t.cancel()  # ending the timer
    if answer[len(answer) - 3] == 255:  # if the receiver sent the signal for a finished measurement
        end_time = int(round(time.time() * 1000))  # taking the end time
        duration = end_time - start_time  # calculation duration
        print("Duration: ", duration, "  Data rate: ", (128*amount_of_messages/(duration/1000)), " MB/s")
        continue_test = False
        t.cancel()

# ###################### USER CODE END ######################

sender.close()

