from wave import open as wavopen
import pyaudio
import math
import random
import struct

SAMPLE_LEN = 10000
noise_output = wavopen('noise.wav', 'wb')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

def sine_wave(x):
  #return 1000*math.sin(0.1*math.pi*x) 
  #return 1000*math.sin(0.04*math.pi*x) 
  return 10000*math.sin(440*2*math.pi*x/44100) 
  return 0



for i in range(0, SAMPLE_LEN):
        #value = random.randint(-32767, 32767)
        value = sine_wave(i)
        packed_value = struct.pack('h', value)
        noise_output.writeframes(packed_value)
        noise_output.writeframes(packed_value)

noise_output.close()

s = wavopen('noise.wav', 'rb')
s.readframes(s.getnframes())
s.close()

print("done writing")
CHUNK = 1024

wf = wavopen('noise.wav','rb')
p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
channels=wf.getnchannels(),
rate=wf.getframerate(),
output=True)

data = wf.readframes(CHUNK)

while data != '':
  stream.write(data)
  data = wf.readframes(CHUNK)

wf.close()
stream.stop_stream()
stream.close()

p.terminate()
