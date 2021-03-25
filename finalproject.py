from psychopy import visual, core, event  # import some libraries from PsychoPy
import random

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
    
def practice(num,wordlist):
    print(f"\nprinting info for Practice {num}: \n")
    visual.TextStim(win=mywin, text='Practice '+str(num), pos=[0,0]).draw()
    mywin.flip()
    core.wait(1)
    for i in wordlist:
        visual.TextStim(win=mywin, text=i, pos=[0,0]).draw()
        mywin.flip()
        recordTime(i, timer.getTime())
        mywin.flip()
        core.wait(0.1)
    visual.TextStim(win=mywin, text='End of practice '+str(num), pos=[0,0]).draw()
    mywin.flip()
    core.wait(1)
    
def recordTime(word, currentTime):
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if thisKey in ['right','left']:
                newTime = timer.getTime()
                reaction_time = newTime - currentTime 
                print(f"Current Word: {word} {thisKey} was pressed reaction time is {reaction_time}")
                thisResp = thisKey


timer = core.Clock()
mywin = visual.Window([800,600], monitor="testMonitor", units="deg")
startExperiment()