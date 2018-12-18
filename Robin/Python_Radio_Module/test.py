import time
import serial
import testLibrary

sender = serial.Serial(  # initializes the sender on COM3
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)
receiver = serial.Serial(  # initializes the receiver on COM4
    # port='COM4',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# ----------Opening sender and receiver if not already happened----------
if sender.isOpen():
    sender.close()
    sender.open()
    sender.isOpen()
# if receiver.isOpen():
#     receiver.close()
#     receiver.open()
#     receiver.isOpen()

# ----------Just the "Hello World!" examples for "generatePackageFromStringWithoutAdress"----------
# testLibrary.sendData(sender, "02000C48656C6C6F20576F726C64210F")  # sends "Hello World!"
# testing = int(round(time.time() * 1000))
# counter = 0
# for x in range(100):
# testLibrary.sendData(sender, testLibrary.generatePackageFromStringWithoutAdress("0011223344556677889900112233445566778899"
#                                                                        "0011223344556677889900112233445566778899"
#                                                                        "0011223344556677889900112233445566778899"
#                                                                        "0011223344556677889900112233445566778899"
#                                                                        "0011223344556677889900112233445566778899"
#                                                                        "0011223344556677889900112233445566778899"
#                                                                        "0011223344556677"))  # Are 128 bytes (max)
#     time.sleep(0.0241)
#     if testLibrary.getConfirmationsWithoutAdress(sender) == 1:
#         counter += 1
# testing -= int(round(time.time() * 1000))
# print("Time Delta in ms: ", testing*-1, "   Number of Packages received: ", counter)

# time.sleep(1)
# testLibrary.getSingleConfirmationWithoutAdress(sender)


# ----------Sends the int via "generatePackageFromHexWithoutAdress" and checks for confirmation----------
# testLibrary.sendData(sender, testLibrary.generatePackageFromHexWithoutAdress('{0:02X}'.format(324375324987509759375347598)))
# time.sleep(0.1)
# testLibrary.getConfirmationsWithoutAdress(sender)

# ----------The speed Test----------
testLibrary.speedTestWithoutAdress(sender, 10, 3, 1)  # def speedTestWithoutAdress(sender, amountOfData, numberOfValidations, deltaIntervals):

# ----------The ping test----------
# print("PING: ", testLibrary.pingTestWithoutAdress(sender, receiver))  # does a ping test with one message and returns milliseconds

# time.sleep(1)

sender.close()
receiver.close()
