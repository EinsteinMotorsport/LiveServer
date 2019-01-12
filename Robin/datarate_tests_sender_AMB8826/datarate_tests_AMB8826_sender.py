import time
import serial
import AMB8826
from threading import Timer
import logging
import datetime


def timeout():
    AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex("FE"))
    print("TIMEOUT FUNCTION TRIGGERED")


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

now = datetime.datetime.now()  # get the current time for the logging
filename = now.strftime("%Y_%m_%d___%H_%M_%S") + "_log.txt"  # create the filename of the new logfile
logging.basicConfig(filename=filename , level=logging.DEBUG, format='%(message)s   %(asctime)s')  # config logfile
amount_of_messages = 20  # Setup for later
continue_test = True  # Setup for later
start_indication = "FF"  # Setup for later
message_filler = "0011223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "11223344556677889900112233445566778899001122334455667788990011223344556677889900" \
                 "112233445566"  # 127 bytes  # Setup for later
sleep_time = 0.04  # Setup for later
keep_alive = True  # Setup for later
lower_sleep_time = False  # Setup for later
timeout_value = 40  # Setup for later

logging.info("Ort: Hagmann Umzüge c.a. 120m nach der Kreuzung - Gardena/Parkplatz nach Magirus / beide aud der straße")

while keep_alive:  # keeps the whole program running
    continue_test = True
    if lower_sleep_time:  # if a measurement was successful then the sleep time is lowered
        sleep_time = sleep_time - 0.000  # decrement
        lower_sleep_time = False
    while continue_test:  # Is active while the test runs until the test ended
        AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_string(start_indication))  # Sends the start signal
        start_time = int(round(time.time() * 1000))  # Remembering the start point
        x = 0  # Setup for later
        for x in range(amount_of_messages):  # Sending the whole amount of messages
            message = message_filler + '{0:02X}'.format(x)  # Filler plus the counter
            AMB8826.send_data(sender, AMB8826.___cmd_data_req___from_hex(message))  # sending
            time.sleep(sleep_time)  # Wait until sending the next message
        t = Timer(timeout_value, timeout)  # Initializing the Timer
        t.start()  # Starting the timer
        answer = AMB8826.get_answer_address_mode_1(sender)  # waiting for an answer
        t.cancel()  # ending the timer
        if answer[len(answer) - 3] == 255:  # if the receiver sent the signal for a finished measurement
            end_time = int(round(time.time() * 1000))  # taking the end time
            duration = end_time - start_time  # calculation duration
            if duration / 1000 > timeout_value:
                print("TIMEOUT")
                logging.info('TIMEOUT Sleep time: %f  Duration: %d  Data rate: %f  MB/s ', sleep_time,
                             duration, (128 * amount_of_messages / (duration / 1000)))  # log tht latest results
                keep_alive = False
            else:
                print("Sleep time: ", sleep_time, "Duration: ", duration, "  Data rate: ",
                      (128*amount_of_messages/(duration/1000)), " MB/s")
                logging.info('Sleep time: %f  Duration: %d  Data rate: %f  MB/s', sleep_time,
                             duration, (128*amount_of_messages/(duration/1000)))  # log tht latest results
                lower_sleep_time = True
            continue_test = False  # Exit current measurement
            t.cancel()  # end timer



# ###################### USER CODE END ######################

sender.close()

