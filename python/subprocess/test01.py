#!/usr/bin/python
import subprocess
import time

parallelLevel = 3
processSlot = []
cmdList = []

def cmd_init():
    for x in range(0, parallelLevel):
        processSlot.append(subprocess.Popen(['sleep', '1']))

def cmd_add(cmd):
    cmdList.append(cmd)

def cmd_exec():

    cmdMax = len(cmdList)
    cmdIndex = 0

    while 1:
        
        runningProcess = 0
        
        for i in range(0, parallelLevel):

            if processSlot[i].poll() != 0:
                runningProcess += 1
                continue

            if cmdIndex < cmdMax:
                print "Slot "+str(i)+", running cmd "+str(cmdIndex)
                processSlot[i] = subprocess.Popen(cmdList[cmdIndex].split())
                runningProcess += 1
                cmdIndex += 1

        
        time.sleep(1)

        if (cmdIndex >= cmdMax) and (runningProcess == 0):
            quit()

#######################

cmd_init()
cmd_add("sleep 10")
cmd_add("df")
cmd_add("sleep 13")
cmd_add("sleep 15")
cmd_add("sleep 16")
cmd_add("sleep 17")
cmd_add("sleep 18")

cmd_exec()




