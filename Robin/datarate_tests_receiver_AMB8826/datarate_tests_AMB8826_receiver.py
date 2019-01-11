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
amount_of_messages = 20  # Setup for later
received = []  # Setup for later
while True:  # is running the whole time and is not intended to stop
    keep_waiting = True  # Setup for later
    received.clear()  # Reset the received after every measurement
    start_time = 0  # Setup for later
    line = AMB8826.get_answer_address_mode_1(receiver)  # always look for messages
    if line.__sizeof__() != 0:  # is a message was received
        if line[len(line)-3] == 255:  # The signal to start a new measurement
            while keep_waiting:  # is active for one measurement
                error_counter = 0  # reset error counter every time a new measurement is started
                temp_line = AMB8826.get_answer_address_mode_1(receiver)  # Just a temp line for appending
                received.append(temp_line[len(temp_line) - 3])  # Appending to the received list
                print(received)
                if received[len(received)-1] == 254:  # This is the signal, that the sender noticed a timeout
                    print("Signal for timeout")
                    keep_waiting = False  # End the measurement
                    AMB8826.send_data(receiver, AMB8826.___cmd_data_req___from_hex("FF"))  # Wake up the sender
                    print("Receiver got the timeout and woke up sender")
                elif len(received) == amount_of_messages:  # the whole measurement data was received (excluding timeout)
                    for x in received:  # loop through the received message
                        if received[x] != x:  # check for errors
                            error_counter += error_counter
                    if error_counter == 0:  # if there were no errors
                        print("Successful measurement: ", received)
                        AMB8826.send_data(receiver, AMB8826.___cmd_data_req___from_hex("FF"))  # Tell sender
                        keep_waiting = False  # End measurement
                    else:
                        print("Error counter:  ", error_counter, "   What was received: ", received)
                        keep_waiting = False  # End measurement


# ###################### USER CODE END ######################

receiver.close()


