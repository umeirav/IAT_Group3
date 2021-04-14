from psychopy import visual, core, event  # import some libraries from PsychoPy
import random
import csv


# converts word bank into list of individual words
with open('wordBank.txt') as f:
    wordCue = [word for line in f for word in line.split()]


# Create all basic objects (window, fixation-cross, timer)
timer = core.Clock()
mywin = visual.Window(fullscr = True, monitor="testMonitor", units="deg")
fixCross = visual.TextStim(mywin, text = '+', height = 0.1)

# Key list variables that participants will use to indicate whether word is related to self or not
# right = self, left = other, q = quit game; the key left and right refer to arrows keys
keyL = ["right", "left", "q"]

# Other global variables
trial = 0


def startExperiment():

    '''
    This is the first function to be called.
    
    Part 1: It will display instructions for the experiment.

    Part 2: Initializes word list for all sessions

    Part 3: Calls practice func for each of the sessions

    Part 4: Indicates end of experiment, waits 5 secs and closes the application
    '''

    # Part 1
    instructions = ['Welcome to our experiment you will see a series of words \nwhere you will press `->` for if you think the words pertains to yourself \nand `<-` if it does not \npress any key to continue']
    pos = [[-9,8],[-4,6],[-4,4],[-6,2]]
    for i in range(len(instructions)):
        visual.TextStim(win=mywin, text=instructions[i], pos=[i], wrapWidth=500).draw()
    mywin.flip()
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        if len(allKeys) > 0:
            thisResp = allKeys[0]
    # Part 2
    wordlist = open("wordBank.txt").read().split()
    print(wordlist)
    sessions = [["SELF","OTHER"]*3,wordlist,wordlist]

    # Part 3
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Trial', 'Word', 'Key', 'Reaction Time'])
        for i,current in enumerate(sessions):
            random.shuffle(current)
            practice(i,current,i==0,writer)

    # Part 4
    visual.TextStim(win=mywin, text='End Of Experiment', pos=[0,0], wrapWidth=500).draw()
    mywin.flip()
    core.wait(2.0)
    core.quit()
    
def practice(num,wordlist,isPractice,writer):

    '''
    This function is called from the start experiment func

    Part 1: Displays Practice number and waits for 1 sec

    Part 2: Displays each word in the wordlist, after displaying the word,
            calls recordTime func with currenttime, clears the screen and waits
            100 microsecs

    Part 3: Indicates end of practice session and waits for 1 sec
    '''

    # Part 1
    
    print(f"\nprinting info for Run {num}: \n")
    if isPractice:  
         visual.TextStim(win=mywin, text='Practice '+str(num+1), pos=[0,0])    
    else:
        visual.TextStim(win=mywin, text='Real Test '+str(num), pos=[0,0]).draw()
    mywin.flip()
    core.wait(1)

    # Part 2
    for i in range(20):
        word = random.choice(wordlist)
        visual.TextStim(win=mywin, text=word, pos=[0,0]).draw()
        mywin.flip()
        recordTime(num, word, timer.getTime(),writer)
        mywin.flip()
        core.wait(0.1)

    # Part 3
    if isPractice:
        visual.TextStim(win=mywin, text='End of practice '+str(num+1), pos=[0,0]).draw()
    else:
        visual.TextStim(win=mywin, text='End of real test '+str(num), pos=[0,0]).draw()
    mywin.flip()
    core.wait(1)
    
def recordTime(trial,word,currentTime,writer):

    '''
    This func is called from practice func

    Part 1: Waits for until user presses a key

    Part 2: looks thorough all the keys user press to check if they pressed
            left or right key if left/right key is pressed then gets the
            currentTime (as newTime) and calculates reaction time.

    Part 3: Prints word, keyPressed, and reaction time.
            Sets `thisResp` so the program doesn't wait
    '''

    # Part 1
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            
            # Part 2
            if thisKey in ['right','left']:
                newTime = timer.getTime()
                reaction_time = newTime - currentTime

                # Part 3
                writer.writerow([trial, word, thisKey, reaction_time])
                print(f"Run number {trial}. Current Word: {word} {thisKey} was pressed reaction time is {reaction_time}")
                thisResp = thisKey

            
startExperiment() #Calls startExperiment func
