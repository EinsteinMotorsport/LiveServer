import time
import serial


def sendData(sender, data):
    sender.write(bytes.fromhex(data))
    print("SEND")
    # print(data)
    # print(bytes.fromhex(data))


def getSingleConfirmation(sender):
    line = []
    while True:
        for c in sender.read():
            line.append(c)
            if c == 67:
                print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                return True


def getConfirmations(sender):
    # line = []
    # getout = True
    # stopTime = int(round(time.time() * 1000)) + 1000
    # while getout:
    #     for c in sender.read():
    #         line.append(c)
    #         if c == 67:
    #             # print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
    #             return True
    #     if int(round(time.time() * 1000)) == stopTime:  # Checks if this took longer than 100 milliseconds
    #         return False

    # line = []
    # confirmationCounter = 0
    # if sender.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
    #     print("SENDER IN WAITING: ", sender.in_waiting)
    #     for c in sender.read(sender.in_waiting):
    #         #  print(c)
    #         line.append(c)
    #         if c == 67:
    #             #  print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
    #             print(line)
    #             line.pop(len(line) - 1)
    #             line.pop(len(line) - 1)
    #             line.pop(len(line) - 1)
    #             line.pop(len(line) - 1)
    #             line.pop(len(line) - 1)
    #             confirmationCounter = confirmationCounter + 1
    #             #  print(confirmationCounter)
    #     print(confirmationCounter)
    #     return confirmationCounter

    line = []
    confirmationCounter = 0
    print("SENDER IN WAITING: ", sender.in_waiting)
    while sender.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
        for c in sender.read(sender.in_waiting):
            #  print(c)
            line.append(c)
            if c == 67:
                #  print("If [2, 64, 1, 0, 67] == ", line, " then everything went right!")
                print(line)
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
        print("confirmationCounter: ", confirmationCounter)
        print("Rest of line should be []: ", line)
    return confirmationCounter


def generatePackageFromString(payload):
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


def generatePackageFromHex(payload):
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


def pingTest(sender, receiver):
    # Sends one Package and counts the milliseconds until the ACK comes back
    startTime = int(round(time.time() * 1000))
    sendData(sender, generatePackageFromString("48656C6C6F20576F726C642121"))  # sends "Hello World!"
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


def speedTest(sender, amountOfData, numberOfValidations, deltaIntervals):
    # Sends as many packages to the sender, as defined in "amountOfData".
    # Lowers the interval by "deltaIntervals" between the data points until the data isn't received correctly anymore.
    # It goes back to a bigger interval and needs "numberOfValidations" correct transmits
    # If it doesn't get "numberOfValidations" correct transmits then it goes further back
    # Then it calculates the bits/s from the size of the payload
    # and the time needed

    interval = 300
    dataSendCorrectly = True
    notEnoughValidations = True
    endPointReached = False
    counterSendFailed = 0
    counterValidations = 0
    testNotDone = True

    while notEnoughValidations:  # Needs this much correctly send data to be fine
        #  print("dataSendCorrectly :", dataSendCorrectly, "  interval: ",
        #        interval, "  counterValidations: ", counterValidations)
        sender.reset_input_buffer()
        sender.flushOutput()
        for x in range(amountOfData):  # Inner loop for every iteration that is used many times
            sendData(sender, generatePackageFromHex('{0:02X}'.format(x)))
        time.sleep(interval / 1000)
        confirmationAnswer = getConfirmations(sender)
        if confirmationAnswer == amountOfData:
            dataSendCorrectly = True
        else:
            dataSendCorrectly = False
            # if confirmationAnswer == -1:  # confirmation error
            # break
        time.sleep(interval / 1000)
        print(interval / 1000)

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
    efficiency = 1000 / interval * amountOfData
    print("Send: ", efficiency, " Messages per second")
