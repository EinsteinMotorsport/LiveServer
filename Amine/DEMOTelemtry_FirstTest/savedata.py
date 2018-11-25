import pyaudio
import numpy as np

liste=[]
def save():


    chunk = 2048  # is the number of frames in the buffer.
    RATE = 44100  # rate is the number of samples of audio carried per second
    p = pyaudio.PyAudio()
    stream1 = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True,
                     frames_per_buffer=chunk)  # bits pro Sekunde=Samplerate*Samplebreite*Kanäle

    if True:  # Run the program if start Button pushed

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
            liste.append(thefreq)  # fill the list
            print(thefreq)





        else:
            thefreq = which * RATE / chunk
            print("%f Hz  %05d %s" % (thefreq, peak, bars))
            liste.append(thefreq)

    stream1.stop_stream()
    stream1.close()
    p.terminate()
