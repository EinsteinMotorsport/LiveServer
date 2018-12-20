import time
import serial
import AMB8826

sender_or_and_receiver = 1  # 1 for sender, 2 for both

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

if sender_or_and_receiver == 2:
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


# GET ALL PROPERTIES OF THE MODULES
print("SENDER: ")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("00"))
print("UART_Baudrate: ", AMB8826.get_single_input_buffer_answer_9(sender), "  e.g. [...0, 194, 1...] == 115200")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("01"))
print("RADIO_DefaultRfProfile: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("02"))
print("RADIO_DefaultRfTXPower: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("03"))
print("RADIO_DefaultRfChannel: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("04"))
print("MAC_DefaultAddressMode: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("06"))
print("MAC_NumRetrys: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("07"))
print("MAC_DefaultDestNetID: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("08"))
print("MAC_DefaultDestAddr: ", AMB8826.get_single_input_buffer_answer_7(sender), "penultimate bytes are the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("10"))
print("MAC_SourceNetID: ", AMB8826.get_single_input_buffer_answer_6(sender), "penultimate byte is the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("11"))
print("MAC_SourceAddr: ", AMB8826.get_single_input_buffer_answer_7(sender), "penultimate bytes are the info")
AMB8826.send_data(sender, AMB8826.___cmd_get_req___("13"))
print("RADIO_SnifferModeEnabled: ", AMB8826.get_single_input_buffer_answer_5(sender), "penultimate byte is the info")

sender.close()
if sender_or_and_receiver == 2:
    receiver.close()

