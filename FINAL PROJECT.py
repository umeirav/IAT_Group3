from psychopy import visual, core, event  # import some libraries from PsychoPy
import random
import csv

def main():
    
    '''
        This is the main function
        It creates global variables for timer, window and writer (csv)
        Also, creates a csv file results.
        
        Since the sesssions can be ran in two different ways a way is selected
        on random and the startSession is called for each value in the order
        
        Once all values in selectOrder are called, "End of Experiment" text is 
        displayed and the window closes in 5 secs.
    '''
    
    global timer, mywin, writer
    timer = core.Clock()
    mywin = visual.Window(fullscr= True, monitor="testMonitor", units="deg")
    
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Run Number', 'Word', 'Key', 'Reaction Time'])
        selectOrder = random.choice([[1,2,3,4,5], [1,4,5,2,3]])
        for num, selectSession in enumerate(selectOrder):
            startSession(num+1, selectSession) #Calls startExperiment func
            
    visual.TextStim(win=mywin, text='End Of Experiment', pos=[0,0], wrapWidth=500).draw()
    mywin.flip()
    core.wait(2.0)
    core.quit()
    
# converts word bank into list of individual words
#with open('wordBank.txt') as f:
#    wordCue = [word for line in f for word in line.split()]


# Create all basic objects (window, fixation-cross, timer)

#fixCross = visual.TextStim(mywin, text = '+', height = 0.1)

# Key list variables that participants will use to indicate whether word is related to self or not
# right = self, left = other, q = quit game; the key left and right refer to arrows keys
# keyL = ["right", "left", "q"]

# Other global variables
# trial = 0


def startSession(sessionNum, selectSession):

    '''
    This function to is called from the main function.
    
    Initalizes wordlist as values from wordBank.txt
    
    Part 1: It will display instructions for each session, the instruction is selected 
            from instructions list based on selectSession value. 

    Part 2: Initializes word list for each session, wordlist is selected using selectSession
            PS: SELF and OTHER has two extra characters to make it uniform with other
                words from the wordBank

    Part 3: Wordlist is shuffled and practice func is called with 
            sessionNum,wordlist,isPractice,selectSession in [4,5] : reversed
            Practice is called again for sets 3 and 5 with isPractice as False 
            (this time the data is recorded)
    '''

    wordlist = open("wordBank.txt").read().split()
    # Part 1
    instructions = [
        'Welcome to our experiment you will see a series of words \nwhere you will press `p` if the word is "SELF"\nand `q` if the word is "OTHER" \npress any key to continue\n\n\nPlease make sure to press the right key',
        'Press `p` for a positive word\nand `q` for a negative word\npress any key to continue\n\n\nPlease make sure to press the right key',
        'For this session you will have a practice round, followed by the main round\n\nPress `p` if the word is "SELF" or positive \nand `q` if the word is "OTHER" or negative \npress any key to continue\n\n\nPlease make sure to press the right key',
        'Press `q` for a positive word\nand `p` for a negative word\npress any key to continue\n\n\nPlease make sure to press the right key',
        'For this session you will have a practice round, followed by the main round\n\nPress `q` if the word is "SELF" or negative \nand `p` if the word is "OTHER or positive \npress any key to continue\n\n\nPlease make sure to press the right key',
    ]
    
    # Part 2 
    wordlist = [
        ["SELF:p","OTHER:u"]*5,
        random.sample(wordlist,k=30),
        ["SELF:p","OTHER:u"]*15 + random.sample(wordlist,k=30),
        random.sample(wordlist,k=30),
        ["SELF:p","OTHER:u"]*15 + random.sample(wordlist,k=30)
    ]
        
    visual.TextStim(win=mywin, text=instructions[selectSession-1], pos=[0,0], wrapWidth=500).draw()
    mywin.flip()
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        if len(allKeys) > 0:
            thisResp = allKeys[0]
    # Part 3
        current = wordlist[selectSession-1]
        random.shuffle(current)
        practice(sessionNum,current,True,selectSession in [4,5])
        if selectSession in [3, 5]:
            practice(selectSession,current,False,selectSession in [4,5])
    
def practice(num,wordlist,isPractice,reverse):

    '''
    This function is called from the start session func

    Part 1: Displays Practice number and waits for 1 sec
            start and end text is updated based on real or practice set

    Part 2: Displays each word in the wordlist, after displaying the word,
            calls recordTime func with word, currenttime, postiveWord?, reverse?, averageData
            clears the screen and waits 100 microsecs. 
            All words in the lists are displayed.

    Part 3: Indicates end of practice/real session and waits for 1 sec
    
    Data is recorded for real sets only
    averageData is used to calculate average of positiveWord/negativeWord
    reaction time when correct key is pressed
    '''

    endText = f'End of real test {num}'
    startText = f'Real Test {num}'
    
    if isPractice:
        startText = f'Practice {num}'
        endText = f'End of practice {num}'
        print(f"\nprinting info for Run {num}: \n")
    
    # Part 1
    visual.TextStim(win=mywin, text=startText, pos=[0,0]).draw()
    
    mywin.flip()
    core.wait(1)

    averageData = [[0,0],[0,0]]
    # Part 2
    for item in wordlist:
        word = item[:-2]
        visual.TextStim(win=mywin, text=word, pos=[0,0]).draw()
        mywin.flip()
        toWrite = recordTime(word, timer.getTime(),item[-1] == 'p',reverse,averageData)
        if not isPractice:
            writer.writerow([num] + toWrite)
        mywin.flip()
        core.wait(0.1)
    if averageData[0][1] == 0: positiveReactionTime = 0
    else: positiveReactionTime = averageData[0][0]/averageData[0][1]
    
    if averageData[1][1] == 0: negativeReactionTime = 0
    else: negativeReactionTime = averageData[1][0]/averageData[1][1]
    # Part 3
    if not isPractice:
        writer.writerow([])
        writer.writerow(["Positive Word Reaction Time Average", "Sum of Positive Reaction Time", "No of correct keystorks"])
        writer.writerow([positiveReactionTime]+averageData[0])
        writer.writerow(["Negative Word Reaction Time Average", "Sum of Negative Reaction Time", "No of correct keystorks"])
        writer.writerow([negativeReactionTime]+averageData[1])
        writer.writerow([])
        visual.TextStim(win=mywin, text=endText, pos=[0,0]).draw()
    mywin.flip()
    core.wait(1)
    
def recordTime(word, currentTime, isPositive, reverse, averageData):

    '''
    This func is called from practice func

    Part 1: Waits for until user presses a key

    Part 2: looks thorough all the keys user press to check if they pressed
            `q` or `p` key 
            
            if q/p key is pressed then gets the
            currentTime (as newTime) and calculates reaction time.
            
            if a key corresponding to the word (positive/negative) is pressed, 
            the reaction time is added to positive/negative average
            
            

    Part 3: Prints word, keyPressed, and reaction time.
            Sets `thisResp` so the program doesn't wait
            
    returns [word, keyPressed, reaction_time]
    '''
    keyOption = ['q','p']
    if reverse:
        keyOption = keyOption[::-1]
    
    # Part 1
    thisResp=None
    while thisResp==None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            # Part 2
            if thisKey in keyOption:
                newTime = timer.getTime()
                reaction_time = newTime - currentTime
                if isPositive and thisKey == keyOption[1]:
                        averageData[0][0] += reaction_time
                        averageData[0][1] += 1.0
                elif not isPositive and thisKey == keyOption[0]:
                        averageData[1][0] += reaction_time
                        averageData[1][1] += 1.0         
                # Part 3
                thisResp = thisKey
    print(f"Current Word: {word} {thisKey} was pressed reaction time is {reaction_time}")
    return [word, thisKey, reaction_time]

main()
