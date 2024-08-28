import time
import sys
import os

def main():

    while True:
        proccessor()
        

def proccessor():

    filename = None
    reader =follow(filename)


    while True:
    
        #Fetch new data
        line = next(reader)


        #Convert to format
        msg = line
        if not msg:
            time.sleep(1)
            continue

        #Send data 
        print(msg)

        #Wait for next round
        time.sleep(.01)




def follow(filename):

    if filename:
        input_file = open(filename,encoding="utf-8")
        input_file.seek(0,os.SEEK_END)
    else:
        input_file = sys.stdin
    
    # Go to the end of the file
    while True:
        line = input_file.readline()
        yield line


main()