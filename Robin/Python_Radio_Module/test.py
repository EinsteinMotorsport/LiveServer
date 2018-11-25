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

# ----------Just the "Hello World!" examples for "generatePackageFromString"----------
# testLibrary.sendData(sender, "02000C48656C6C6F20576F726C64210F")  # sends "Hello World!"
for x in range(20):
    testLibrary.sendData(sender, testLibrary.generatePackageFromString("0011223344556677889900112233445566778899"
                                                                       "0011223344556677889900112233445566778899"
                                                                       "0011223344556677889900112233445566778899"
                                                                       "0011223344556677889900112233445566778899"
                                                                       "0011223344556677889900112233445566778899"
                                                                       "0011223344556677889900112233445566778899"
                                                                       "0011223344556677"))  # Are 128 bytes (max)
time.sleep(3)
#testLibrary.getSingleConfirmation(sender)
testLibrary.getConfirmations(sender)

# ----------Sends the int via "generatePackageFromHex" and checks for confirmation----------
# testLibrary.sendData(sender, testLibrary.generatePackageFromHex('{0:02X}'.format(324375324987509759375347598)))
# time.sleep(0.1)
# testLibrary.getConfirmations(sender)

# ----------The speed Test----------
# testLibrary.speedTest(sender, 50, 3, 10)  # def speedTest(sender, amountOfData, numberOfValidations, deltaIntervals):

# ----------The ping test----------
# print("PING: ", testLibrary.pingTest(sender, receiver))  # does a ping test with one message and returns milliseconds

# time.sleep(1)

sender.close()
receiver.close()
