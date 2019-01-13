import time
from threading import Timer
import serial
import AMB8826
import logging
import datetime


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
time_stamp = 0
now = datetime.datetime.now()  # get the current time for the logging
filename = now.strftime("%Y_%m_%d___%H_%M_%S") + "_log.txt"  # create the filename of the new logfile
logging.basicConfig(filename=filename, level=logging.DEBUG, format='%(message)s   %(asctime)s')
logging.info("Ort: ")
while True:
    appendix = '{0:02X}'.format(counter)
    if len(appendix) % 2 != 0:
        appendix = "0" + appendix
    message = message_filler + appendix
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex(message))
    time_stamp = int(round(time.time() * 1000))
    print(counter, "  ", time_stamp)
    logging.info('%d %d %d', counter, time_stamp, time_stamp)
    counter += 1
    time.sleep(0.030)  # with 0.04 sending 25 messages per second

# ###################### USER CODE END ######################

sender.close()
