import time


# ----------Sends the data it is given to the given sender----------
def sendData(sender, data):
    sender.write(bytes.fromhex(data))
    # print("SEND")
    # print(data)
    # print(bytes.fromhex(data))


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def getSingleConfirmationWithoutAdress(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            if c == 67:
                print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                return True


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def getSingleConfirmationWithAdressmode1(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            if line.__len__() == 5:
                print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                return True


# ----------gets all confirmation messages it can find,----------
# ----------counts them and return the amount of confirmations it got----------
def getConfirmationsWithoutAdress(sender):
    line = []
    confirmationCounter = 0
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
                    confirmationCounter = confirmationCounter + 1
                    #  print(confirmationCounter)
                else:
                    print("ERROR, could not receive full confirmation!")
                    return -1
        # print("confirmationCounter: ", confirmationCounter)
        # print("Rest of line should be []: ", line)
    return confirmationCounter


# ----------generates a Package from a String----------
def generatePackageFromStringWithoutAdress(payload):
    # Needs start signal, command, length, payload and checksum
    # Standard start signal that can be changed. If you change it maybe you have to change the rest # of the format too
    startSignal = "02"
    # Standard command that can be changed. If you change it maybe you have to change the rest # of the format too
    command = "00"
    data = ""
    data += startSignal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        frontNull = "0"
        payload = frontNull + payload
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
# ----------e.g. generatePackageFromHexWithoutAdress('{0:02X}'.format(324375324987509759375347598))----------
def generatePackageFromHexWithoutAdress(payload):
    # Needs start signal, command, length, payload and checksum
    # Standard start signal that can be changed. If you change it maybe you have to change the rest # of the format too
    startSignal = "02"
    # Standard command that can be changed. If you change it maybe you have to change the rest # of the format too
    command = "00"
    data = ""
    data += startSignal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        frontNull = "0"
        payload = frontNull + payload
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
# ----------e.g. generatePackageFromHexWithAdressmode1('{0:02X}'.format(324375324987509759375347598))----------
def generatePackageFromHexWithAdressmode1(payload):
    # Needs start signal, command, length, payload and checksum
    startSignal = "02"
    command = "01"
    data = ""
    data += startSignal
    data += command
    if len(payload) % 2 != 0:  # Checks if the payload has an odd size and adds an leading zero
        frontNull = "0"
        payload = frontNull + payload
    length = '{0:02X}'.format((len(payload) // 2)+2)  # Int to String without the 0x up front and +2 for AddressMode 1
    data += length
    channel = "6C"
    data += channel
    destinationAdress = "02"
    data += destinationAdress
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
def pingTestWithoutAdress(sender, receiver):
    startTime = int(round(time.time() * 1000))
    sendData(sender, generatePackageFromStringWithoutAdress("48656C6C6F20576F726C642121"))  # sends "Hello World!"
    # line = []
    while True:
        for c in sender.read():
            print(c)
            # line.append(c)
            if c == 67:
                endTime = int(round(time.time() * 1000))
                delta = endTime - startTime
                # line = []
                print("Startzeit: ", startTime, "Endzeit: ", endTime)
                return delta


def speedTestWithoutAdress(sender, amountOfData, numberOfValidations, deltaIntervals):
    # Sends as many packages to the sender, as defined in "amountOfData".
    # Lowers the interval by "deltaIntervals" between the data points until the data isn't received correctly anymore.
    # It goes back to a bigger interval and needs "numberOfValidations" correct transmits
    # If it doesn't get "numberOfValidations" correct transmits then it goes further back
    # Then it calculates the bits/s from the size of the payload
    # and the time needed
    # the size of the message has to be changed by modifying the code down below (the string in "generatePackage")

    interval = 60
    dataSendCorrectly = True
    notEnoughValidations = True
    endPointReached = False
    counterSendFailed = 0
    counterValidations = 0
    testNotDone = True
    starttime = 0
    endtime = 0

    while notEnoughValidations:  # Needs this much correctly send data to be fine
        #  print("dataSendCorrectly :", dataSendCorrectly, "  interval: ",
        #        interval, "  counterValidations: ", counterValidations)
        sender.reset_input_buffer()
        sender.flushOutput()
        confirmationcounter = 0
        starttime = int(round(time.time() * 1000))
        for x in range(amountOfData):  # Inner loop for every iteration that is used many times
            # sendData(sender, generatePackageFromHexWithoutAdress('{0:02X}'.format(x))) # counting up from 0 to "amountOfData"
            sendData(sender, generatePackageFromStringWithoutAdress("0011223344556677889900112233445566778899"
                                                       "0011223344556677889900112233445566778899"
                                                       "0011223344556677889900112233445566778899"
                                                       "0011223344556677889900112233445566778899"
                                                       "0011223344556677889900112233445566778899"
                                                       "0011223344556677889900112233445566778899"
                                                       "0011223344556677"))  # Are 128 bytes (max)
            time.sleep(interval / 1000)
            if getConfirmationsWithoutAdress(sender) == 1:
                confirmationcounter += 1
        endtime = int(round(time.time() * 1000))
        confirmationAnswer = confirmationcounter
        print(interval / 1000)
        if confirmationAnswer == amountOfData:
            dataSendCorrectly = True
        else:
            dataSendCorrectly = False
            # if confirmationAnswer == -1:  # confirmation error
            # break

        if dataSendCorrectly:
            if endPointReached:  # Increase CounterValidations
                counterValidations = counterValidations + 1
            else:  # reduce the interval
                interval = interval - deltaIntervals

        else:
            if counterSendFailed == 3:  # sets endPointReached and increases interval
                endPointReached = True
                interval = interval + deltaIntervals
                counterSendFailed = 0

            else:  # Increases counterSendFailed
                counterSendFailed = counterSendFailed + 1

        if numberOfValidations == counterValidations:
            notEnoughValidations = False
        print("Failed: ", counterSendFailed)

    #  calculating and returning the efficiency
    # efficiency = 1000 / interval * amountOfData * 128
    efficiency = 1000 / (endtime - starttime) * amountOfData * 128
    print("Reached: ", efficiency, " bytes per second without overhead")


def generate___MAC_SourceAddr___FromHex(address):
    # With this function you can configure the MAC_SourceAddr parameter with LSB 0x01
    # example in the manual under 8.4.10.1
    message = ""
    startSignal = "02"
    command = "09"
    length = "02"
    settingsIndex = "0B"
    message += startSignal
    message += command
    message += length
    message += settingsIndex
    message += address
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message

def generate___CMD_SET_REQ___FromHex(addressmode):
    # example in the manual under 8.4.5.1
    message = ""
    startSignal = "02"
    command = "09"
    length = "02"
    settingsIndex = "04"
    message += startSignal
    message += command
    message += length
    message += settingsIndex
    message += addressmode
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message

def generate___CMD_GET_REQ___(settingsIndex):
    # example in the manual under 8.4.5.2
    message = ""
    startSignal = "02"
    command = "0A"
    length = "01"
    message += startSignal
    message += command
    message += length
    message += settingsIndex
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def generate___RADIO_DefaultRfChannel___():
    # example in the manual under 7.4.2
    message = ""
    startSignal = "02"
    command = "06"
    length = "01"
    channel = "6C"
    message += startSignal
    message += command
    message += length
    message += channel
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


def generate___CMD_SET_REQ___():
    # example in the manual under 8.4.6.1
    message = ""
    startSignal = "02"
    command = "09"
    length = "02"
    settingsIndex = "06"  # 06 for numberofRetrys, 0D for sniffermode
    numRetrys = "01"
    message += startSignal
    message += command
    message += length
    message += settingsIndex
    message += numRetrys
    i = 0
    checksum = 0
    while i < len(message):  # going through the bytes of the string with a XOR
        checksum ^= int(message[i] + message[i + 1], 16)
        i += 2
    message += '{0:02X}'.format(checksum)  # converting the int checksum to a Hex without the 0x up front
    print("Message: ", message)
    return message


# ----------Only tries to get a single confirmation message and returns true if it got one----------
def getSingleInputBufferAnswer(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            print(c)
            if line.__len__() == 7:
                print("Answer: ", line, " (has to be [2, 73, 1, 0, 74])")
                return True
