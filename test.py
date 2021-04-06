from psychopy import visual, core, event  # import some libraries from PsychoPy
import random
import csv


# converts word bank into list of individual words
with open('wordBank.txt') as f:
    wordCue = [word for line in f for word in line.split()]


# Create all basic objects (window, fixation-cross, timer)
timer = core.Clock()
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")
fixCross = visual.TextStim(mywin, text = '+', height = 0.1)

# Key list variables that participants will use to indicate whether word is related to self or not
# right = self, left = other, q = quit game; the key left and right refer to arrows keys
keyL = ["right", "left", "q"]

# Other global variables
trial = 0


def startExperiment():
    instructions = ['This is a test', 
    'you will now see a series of words',
    'press `->` for self and `<-` for other',
    'press any key to continue']
    pos = [[-9,8],[-4,6],[-4,4],[-6,2]]
    for i in range(len(instructions)):
        visual.TextStim(win=mywin, text=instructions[i], pos=pos[i], wrapWidth=500).draw()
    mywin.flip()
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        if len(allKeys) > 0:
            thisResp = allKeys[0]
    sessions = [["Self","Other"]*3,["Joy", "Vomit"]*3,["Self", "Joy", "Other", "Vomit"]*3]
    sessions.append(sessions[1])
    sessions.append(sessions[2])
    for i,current in enumerate(sessions):
        random.shuffle(current)
        practice(i+1,current)
    visual.TextStim(win=mywin, text='End Of Experiment', pos=[0,0], wrapWidth=500).draw()
    mywin.flip()
    core.wait(5.0)
