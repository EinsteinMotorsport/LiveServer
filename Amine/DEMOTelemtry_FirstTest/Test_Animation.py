import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from drawnow import *
import pyaudio
import numpy as np
from tkinter import *
import matplotlib.backends.backend_tkagg
from matplotlib.figure import Figure

liste = []
freqme=0
run = False

def makeFig():


    fig = Figure(figsize=(7, 7), dpi=100)

    a1 = fig.add_subplot(111)


    a1.set_ylabel('Amplitude [Hz]')
    a1.set_title('Frequency')
    a1.plot(liste, 'ro-')
    a1.grid()



    canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(x=370, y=10)

def detecting():
    global i
    global control
    global counter2
    global counter1
    global freqme


    chunk = 2048  # is the number of frames in the buffer.
    RATE = 44100  # rate is the number of samples of audio carried per second
    p = pyaudio.PyAudio()
    stream1 = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                     frames_per_buffer=chunk)  # bits pro Sekunde=Samplerate*Samplebreite*Kanäle

    if run:  # Run the program if start Button pushed

        data = stream1.read(chunk)  # read the informations from microphone
        indata = np.fromstring(stream1.read(chunk),
                               dtype=np.int16)  # 1-D array initialized from raw binary data in a string

        fftData = abs(np.fft.rfft(indata)) ** 2  # Take the fft and square each value

        which = fftData[1:].argmax() + 1  # find the maximum

        peak = np.average(np.abs(indata))  # find the average



        if which != len(fftData) - 1:
            # find the frequency and output it
            y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
            x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
            thefreq = (which + x1) * RATE / chunk
            freqme=thefreq
           # print("%.2fHz /%05d/ %.4fV / %s" % (thefreq, peak,m.log10(thevolt),bars))
            liste.append(thefreq)  # fill the list
            print(thefreq)
            makeFig()




        else:
            thefreq = which * RATE / chunk
            print("%f Hz  %05d %s" % (thefreq, peak, bars))
            liste.append(thefreq)

    stream1.stop_stream()
    stream1.close()
    p.terminate()
    root.after(1, detecting)


def start():
    global run
    run=True


root = Tk()
root.geometry("1120x800")
root.title("MENU")
app = Frame(root)
app.grid()


# --------------- Buttons --------------#
start = Button(app, text="Start", bg="green", fg="black", command=start)
start.grid()


detecting()
app.mainloop()