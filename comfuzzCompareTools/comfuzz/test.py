
import time

fileName = "comfuzz"
t = time.time()
print("time: %f" %(t))
print("file name: %s" %(fileName))
fileName += str(round(t))
print("file name and time: %s" %(fileName))
