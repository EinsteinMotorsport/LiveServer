import time
from threading import Timer
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

received = []
get_new_time = True
while True:
    if get_new_time:
        start_time = int(round(time.time() * 1000))
        get_new_time = False
        print("Got new Time, start time: ", start_time)
        # got a one second tick here
    line = AMB8826.get_answer_address_mode_1(receiver)
    end_time = int(round(time.time() * 1000))
    if end_time - start_time > 1000:
        get_new_time = True
    offset = 3
    buffer = 0
    for x in range(len(line)-6-122):
        buffer = buffer + line[len(line) - offset] * pow(16, (offset - 3)*2)
        offset += 1
    received.append(buffer)
    print(buffer)

# ###################### USER CODE END ######################

receiver.close()