import json

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
from tornado.ioloop import PeriodicCallback
import tornado.web
from random import randint, random  # Random generator
#import Data


byte=[b'40',b'22,',b'22,22',b'10',b'10',b'50,55,49']
byt2=[b'0,5,,7,0',b'1,122,erwer',b'2,22,22',b'100']
#Config
port = 7777 #Websocket Port
timeInterval= 1000 #Milliseconds

class WSHandler(tornado.websocket.WebSocketHandler):



	#check_origin fixes an error 403 with Tornado
	#http://stackoverflow.com/questions/24851207/tornado-403-get-warning-when-opening-websocket
    def check_origin(self, origin):

        return True

    def open(self):

		#Send message periodic via socket upon a time interval
        self.callback = PeriodicCallback(self.send_values, timeInterval)
        self.callback.start()

    def send_values(self):
		#Generates random values to send via websocket
        print('send data')
        #x=randint(1,70)
        #s=str(x)
        #liste = []
        #liste.append(s)

        listwert = []
        Id = 0
        list = self.InputData(byte)

        for i in list:
            del listwert[:]
            listwert.append(i)
            if Id == 0:
                einheit = "Km/h²"
            elif Id == 1:
                einheit = "Km/h"
            elif Id == 2:
                einheit = "Bar"
            elif Id == 3:
                einheit = "Gang"
            elif Id == 4:
                einheit = "Thaco"
            elif Id == 5:
                einheit = "°C"
            else:
                einheit = ""
            info = {'ID': Id, 'Wert': listwert, 'Einheit': einheit}
            ToSendInfo = json.dumps(info)
            Id += 1
            print("----",ToSendInfo)
            self.write_message(ToSendInfo)
        #tosend=Data.Datensatz(byt2)
        # for i in x:
        #     for j in i:
        #
        #         self.write_message(j)
        #         print(j)

    def on_message(self, message):
        pass

    def on_close(self):
        self.callback.stop()

    def InputData(self,InputListe):
        SinputList = []
        for line in InputListe:
            # he call .decode('ascii') converts the raw bytes to a string.
            # .split(',') splits the string on commas.
            s = line.decode("utf-8").split(',')
            SinputList.append(s)
        return SinputList

application = tornado.web.Application([
    (r'/service', WSHandler),
])


http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(port)
tornado.ioloop.IOLoop.instance().start()