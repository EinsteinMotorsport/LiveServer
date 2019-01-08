import time


# ----------Sends the data it is given to the given sender----------
def send_data(sender, data):
    sender.write(bytes.fromhex(data))
    # print(data)


# ----------generates a Package from a String----------
def ___cmd_data_req___from_string(payload):
    # Needs start signal, command, length, payload and checksum
    # Standard start signal that can be changed. If you change it maybe you have to change the rest # of the format too
    start_signal = "02"
    # Standard command that can be changed. If you change it maybe you have to change the rest # of the format too
    command = "00"
    data = ""
    data += start_signal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        front_null = "0"
        payload = front_null + payload
    length = '{0:02X}'.format(len(payload) // 2)  # Int to String without the 0x up front
    data += length
    data += payload
    i = 0
    checksum = 0
    while i < len(data):  # going through the bytes of the string with a XOR
        checksum ^= int(data[i] + data[i + 1], 16)
        i += 2
    data += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    return data


# ----------generates a package from Hex numbers----------
# ----------e.g. generatePackageFromHexWithoutAddress('{0:02X}'.format(324375324987509759375347598))----------
def ___cmd_data_req___from_hex(payload):
    # Needs start signal, command, length, payload and checksum
    # Standard start signal that can be changed. If you change it maybe you have to change the rest # of the format too
    start_signal = "02"
    # Standard command that can be changed. If you change it maybe you have to change the rest # of the format too
    command = "00"
    data = ""
    data += start_signal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        front_null = "0"
        payload = front_null + payload
    length = '{0:02X}'.format(len(payload) // 2)  # Int to String without the 0x up front
    data += length
    data += payload
    i = 0
    checksum = 0
    while i < len(data):  # going through the bytes of the string with a XOR
        checksum ^= int(data[i] + data[i + 1], 16)
        i += 2
    data += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    return data


# ----------generates a package from Hex numbers----------
# ----------e.g. ___cmd_dataex_req___from_hex_address_mode_1('{0:02X}'.format(324375324987509759375347598))----------
def ___cmd_dataex_req___from_hex_address_mode_1(payload):
    # Needs start signal, command, length, payload and checksum
    start_signal = "02"
    command = "01"
    data = ""
    data += start_signal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        front_null = "0"
        payload = front_null + payload
    length = '{0:02X}'.format((len(payload) // 2) + 2)  # Int to String without the 0x up front and +2 for AddressMode 1
    data += length
    channel = "6A"
    data += channel
    destination_address = "07"
    data += destination_address
    data += payload
    i = 0
    checksum = 0
    while i < len(data):  # going through the bytes of the string with a XOR
        checksum ^= int(data[i] + data[i + 1], 16)
        i += 2
    data += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    return data


# ----------performs a simple ping test to get the delay between the sending of the message----------
# ----------and receiving of the confirmation message devided by 2 and returns it----------
def ping_test_without_address(sender):
    start_time = int(round(time.time() * 1000))
    send_data(sender, ___cmd_data_req___from_string("48656C6C6F20576F726C642121"))  # sends "Hello World!"
    # line = []
    while True:
        for c in sender.read():
            print(c)
            # line.append(c)
            if c == 67:
                end_time = int(round(time.time() * 1000))
                delta = end_time - start_time
                # line = []
                print("start time: ", start_time, "end time: ", end_time)
                return delta


# ----------performs a speed test to determine the possible data rate----------
def speed_test_without_address(sender, amount_of_data, number_of_validations, delta_intervals):
    # Sends as many packages to the sender, as defined in "amountOfData".
    # Lowers the interval by "deltaIntervals" between the data points until the data isn't received correctly anymore.
    # It goes back to a bigger interval and needs "numberOfValidations" correct transmits
    # If it doesn't get "numberOfValidations" correct transmits then it goes further back
    # Then it calculates the bits/s from the size of the payload
    # and the time needed
    # the size of the message has to be changed by modifying the code down below (the string in "generatePackage")

    interval = 60
    # data_send_correctly = True
    not_enough_validations = True
    end_point_reached = False
    counter_send_failed = 0
    counter_validations = 0
    # test_not_done = True
    start_time = 0
    end_time = 0

    while not_enough_validations:  # Needs this much correctly send data to be fine
        #  print("data_send_correctly :", data_send_correctly, "  interval: ",
        #        interval, "  counter_validations: ", counter_validations)
        sender.reset_input_buffer()
        sender.flushOutput()
        confirmation_counter = 0
        start_time = int(round(time.time() * 1000))
        for x in range(amount_of_data):  # Inner loop for every iteration that is used many times
            # sendData(sender, ___cmd_data_req___from_string('{0:02X}'.format(x)))
            send_data(sender, ___cmd_data_req___from_string("0011223344556677889900112233445566778899"
                                                            "0011223344556677889900112233445566778899"
                                                            "0011223344556677889900112233445566778899"
                                                            "0011223344556677889900112233445566778899"
                                                            "0011223344556677889900112233445566778899"
                                                            "0011223344556677889900112233445566778899"
                                                            "0011223344556677"))  # Are 128 bytes (max)
            time.sleep(interval / 1000)
            if get_confirmations(sender) == 1:
                confirmation_counter += 1
        end_time = int(round(time.time() * 1000))
        confirmation_answer = confirmation_counter
        print(interval / 1000)
        if confirmation_answer == amount_of_data:
            data_send_correctly = True
        else:
            data_send_correctly = False
            # if confirmation_answer == -1:  # confirmation error
            # break

        if data_send_correctly:
            if end_point_reached:  # Increase CounterValidations
                counter_validations = counter_validations + 1
            else:  # reduce the interval
                interval = interval - delta_intervals

        else:
            if counter_send_failed == 3:  # sets end_point_reached and increases interval
                end_point_reached = True
                interval = interval + delta_intervals
                counter_send_failed = 0

            else:  # Increases counter_send_failed
                counter_send_failed = counter_send_failed + 1

        if number_of_validations == counter_validations:
            not_enough_validations = False
        print("Failed: ", counter_send_failed)

    #  calculating and returning the efficiency
    # efficiency = 1000 / interval * amountOfData * 128
    efficiency = 1000 / (end_time - start_time) * amount_of_data * 128
    print("Reached: ", efficiency, " bytes per second without overhead")


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_confirmation(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            if c == 67:
                print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                return True


# ----------For receiving a full message in address mode 1----------
def get_answer_address_mode_1(sender):
    line = []
    counter = 0
    next_two_are_length = False
    receiving = False
    while True:
        for c in sender.read():
            line.append(c)
            if next_two_are_length:
                length = c + 2
                next_two_are_length = False
                counter = length
            if c == 129:
                next_two_are_length = True
                receiving = True
            else:
                counter = counter - 1
            if counter == 0 and receiving:
                return line


# ----------gets all confirmation messages it can find,----------
# ----------counts them and return the amount of confirmations it got----------
def get_confirmations(sender):
    line = []
    confirmation_counter = 0
    # print("SENDER IN WAITING: ", sender.in_waiting)
    while sender.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
        for c in sender.read(sender.in_waiting):
            #  print(c)
            line.append(c)
            if c == 66:
                print("No ACK received!!")
                print(line)
                if len(line) == 5:
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
            if c == 67:
                #  print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                if len(line) == 5:
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
                    line.pop(0)
                    confirmation_counter = confirmation_counter + 1
                    #  print(confirmation_counter)
                else:
                    print("ERROR, could not receive full confirmation!")
                    return -1
        # print("confirmation_counter: ", confirmation_counter)
        # print("Rest of line should be []: ", line)
    return confirmation_counter


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_input_buffer_answer_5(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            # print(c)
            if line.__len__() == 5:
                # print("Answer: ", line)
                return line


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_input_buffer_answer_6(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            # print(c)
            if line.__len__() == 6:
                # print("Answer: ", line)
                return line


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_input_buffer_answer_7(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            # print(c)
            if line.__len__() == 7:
                # print("Answer: ", line)
                return line


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_input_buffer_answer_8(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            # print(c)
            if line.__len__() == 8:
                # print("Answer: ", line)
                return line


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def get_single_input_buffer_answer_9(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            # print(c)
            if line.__len__() == 9:
                # print("Answer: ", line)
                return line


def ___cmd_reset_req___():
    # triggers a software reset of the module
    # example in the manual under 7.3.1
    message = ""
    start_signal = "02"
    message += start_signal
    command = "05"
    message += command
    length = "00"
    message += length
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_shutdown_req___():
    # triggers a shutdown of the module
    # example in the manual under 7.3.3
    message = ""
    start_signal = "02"
    message += start_signal
    command = "0E"
    message += command
    length = "00"
    message += length
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_standby_req___():
    # triggers the standby mode of the module
    # example in the manual under 7.3.4
    message = ""
    start_signal = "02"
    message += start_signal
    command = "0F"
    message += command
    length = "00"
    message += length
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_rssi_req___():
    # returns the RX level of the last received package
    # example in the manual under 7.3.6
    message = ""
    start_signal = "02"
    message += start_signal
    command = "0D"
    message += command
    length = "00"
    message += length
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_set_papower_req___():
    # set the RF TX-power of the module
    # example in the manual under 7.4.1
    message = ""
    start_signal = "02"
    message += start_signal
    command = "11"
    message += command
    length = "01"
    message += length
    power = ""  # enter the power here
    message += power
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_set_channel_req___():
    # set the radio channel of the module
    # example in the manual under 7.4.2
    message = ""
    start_signal = "02"
    message += start_signal
    command = "06"
    message += command
    length = "01"
    message += length
    channel = "6C"  # enter the channel here
    message += channel
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_set_destnetid_req___():
    # set the destination network id in  address mode 2 and 3 of the module
    # example in the manual under 7.4.3
    message = ""
    start_signal = "02"
    message += start_signal
    command = "07"
    message += command
    length = "01"
    message += length
    destination_network_id = ""  # enter the network id here
    message += destination_network_id
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_set_destaddr_req___():
    # set the destination address in  address mode 1, 2 and 3 of the module
    # example in the manual under 7.4.4
    message = ""
    start_signal = "02"
    message += start_signal
    command = "08"
    message += command
    length = "01"
    message += length
    destination_address = "02"  # enter the address here
    message += destination_address
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_set_req___(settings_index, parameter):
    # manipulate non volatile parameters depending on the settings index
    # example in the manual under 7.5.1
    message = ""
    start_signal = "02"
    message += start_signal
    command = "09"
    message += command
    if len(parameter) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        front_null = "0"
        parameter = front_null + parameter
    length = '{0:02X}'.format((len(parameter) // 2) + 1)  # Int to String without the 0x up front
    message += length
    message += settings_index
    message += parameter
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def ___cmd_get_req___(settings_index):
    # query user settings parameters
    # example in the manual under 7.5.2
    message = ""
    start_signal = "02"
    command = "0A"
    length = "01"
    message += start_signal
    message += command
    message += length
    message += settings_index
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    return message


def ___cmd_factory_reset_req___():
    # restore default user settings, also does software reset
    # example in the manual under 7.5.3
    message = ""
    start_signal = "02"
    command = "12"
    length = "00"
    message += start_signal
    message += command
    message += length
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message
