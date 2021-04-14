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


#This function takes the pressed key and returns the direction of that key. Also gives easy way to quite game
def printRespKeyPr(k):
    if (k[0] == "q"):
        core.quit()
    elif (k[0] == "left"):
        return("left")
    elif (k[0] == "right"):
        return("Right")
    else:
        print("oops. Something unexpected")



#Postitions for instructions
TOP_POS = [0,+3]
CENTER_POS = [0,0]
BOTTOM_POS = [0,-4]

def set_msg(txt,type):
    if (type == 'TITLE'):
        m = visual.TextStim(mywin,text=txt, pos=TOP_POS, bold=True,wrapWidth = 30)
    elif (type == 'MAIN'):
        m = visual.TextStim(mywin,text=txt, pos=CENTER_POS,wrapWidth = 30)
    elif (type == 'KEY'):
        m = visual.TextStim(mywin,text=txt, pos=BOTTOM_POS,wrapWidth = 30)
    m.draw()

#Can change instruction wording here with the title being the first phrase the main is the middle. Calls onto set_msg function which takes the text and looks to see which position the text should be in. 
def display_instructions():
    set_msg('INTRODUCTION','TITLE')
    set_msg('AXB control','MAIN')
    set_msg('Press any key to continue','KEY')
    mywin.flip()
    core.wait(0.5)
    event.waitKeys()

def display_instructions_prac_so():
    set_msg('You will see a series of words in which you will respond to each word according to a category','TITLE')
    set_msg('The words `self` and `other` will appear where you will press the `->` arrow key for `self` and `<-` for other','MAIN')
    set_msg('Press any key to continue','KEY')
    mywin.flip()
    core.wait(0.5)
    event.waitKeys()

#Initiates word list for all sessions
wordbank = open("wordBank.txt").read().split()
prac_word_so = ["SELF","OTHER"]*3

#Variables setting condition and order of blocks
session_1 = [1,2,3,4,5]
session_2 = [1,4,5,2,3]
session = [session_1, session_2]

#Shuffling the sessions to randomize which order is going
random.shuffle(session)


#Creates CSV File for Data
with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Trial', 'Word', 'Key', 'Reaction Time'])



########Start of Experiment##########

def startExperiment():
    cond = 0
    #Part 1: Running first prac block
    #The command session[0][cond] calls on the first number of the first list in session which will always be 1 because cond is set to 0 in the beginning

    if session[0][cond] == 1:
        display_instructions_prac_so()
        prac_so(cond, prac_word_so)
        cond =+ 1

    else:
        core.quit()







def prac_so(num, wordlist):

    for i in range(20):
        word = random.choice(prac_word_so)
        visual.TextStim(win=mywin, text=word, pos=[0,0]).draw()
        mywin.flip()
        k = event.waitKeys(keyList=keyL)
        print(printRespKeyPr(k))
        mywin.flip()
        core.wait(0.1)
        



        
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


