import time
import sys

def main():

    while True:
        proccessor()
        

def proccessor():

    input_file = sys.stdin
    reader =follow(input_file)


    while True:
    
        #Fetch new data
        line = next(reader)

        if not line:
            time.sleep(1)
            continue

        #Convert to format
        msg = line

        #Send data 
        print(msg)

        #Wait for next round
        time.sleep(.01)




def follow(thefile):
    
    # Go to the end of the file
    #thefile.seek(0,2) 
    
    while True:
        line = thefile.readline()
        yield line

main()