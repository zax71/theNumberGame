# Imports
import os, sys, random, yaml
from termcolor import colored




# Functions
def lines(color, length):
    text = ""
    for i in range(0, length):
        text = text + "="
    text = colored(text, color)
    return text

def loadConfig():
    configFile = ""

    try:
        with open('config.yml', "r") as f:
            configFile = yaml.load(f, Loader=yaml.FullLoader)
    except:
        defaultConfig = open('defaultConfig.yml', "r")
        f = open('config.yml', 'w')
        f.write(defaultConfig.read())
    finally:
        with open('config.yml', "r") as f:
            configFile = yaml.load(f, Loader=yaml.FullLoader)
    
    return configFile

def askGuess():
    correctGuess = False

    while correctGuess == False:
        guess = input("What number do you guess? ")

        if guess.isdigit() == True:
            correctGuess = True
        else:
            print("Guess must be a whole number")
    return int(guess)

def hint(guess, number):
    if guess > number:
        return "higher"
    elif guess < number:
        return "lower"
# Variables
config = loadConfig()

termColumns = os.get_terminal_size()[0]
correctNumber = random.randint(int(config["rangeMin"]), int(config["rangeMax"]))
hinted = 0
guesses = 0
menuAnswer = 0
acceptedAnswer = False
winner = False


# Welcome

print(lines("green", termColumns))

print("Welcome to Zax71's number guessing game!\n\nYour objective: Guess what number i'm thinking of. It is between", str(config["rangeMin"]), "and", str(config["rangeMax"]))

print("i'll give you only " + str(config["guesses"]) + " clues after your first guess so be careful!")

# Main game loop

for i in range(0, config["guesses"]):
    guesses = i+1
    print(lines("green", termColumns) + "\n")
    # Ask the user to guess
    guess = askGuess()

    #print("Correct number: " + str(correctNumber))

    # If they won...
    if guess == correctNumber:
        winner = True
        break
    # Or if they didn't
    else:
        print("\nIncorrect answer :( you have", config["guesses"]-guesses, "guesses left.\n")
        acceptedAnswer = False
        # Keep looping until they give a valid answer
        while acceptedAnswer == False:
            
            # Work out the number of hints remaning
            remaningHints = config["hints"]-hinted

            # Menu
            print("What would you like to do?\n")
            if remaningHints == 0:
                print(colored('[1] Take a hint', 'red'))
                print("[2] Continue")
                print("[3] Give up\n")
            else:
                print("[1] Take a hint")
                print("[2] Continue")
                print("[3] Give up\n")
            
            # Ask the question
            menuAnswer = input("What do you pick? ")

            # Decode the answer and take the correct action
            if remaningHints != 0 and menuAnswer == "1":
                # Increment the number of hints given out
                hinted += 1
                
                # Call out function to give us a hint, and print the output
                print("hint: " + hint(correctNumber, guess))

                # Tell the user how many hints are remaning
                print(remaningHints, "hints remaning")
                
                # Accept the answer to break the loop
                acceptedAnswer = True
                

            elif remaningHints <= 0 and menuAnswer == "1":
                print("You can't take more hints than you have!")
                # Deny the answer to repeat the loop
                acceptedAnswer = False

            elif menuAnswer == "2":
                print("Okay! No hints for you.")
                # Accept the answer to break the loop
                acceptedAnswer = True
            
            elif menuAnswer == "3":
                print("Exiting")
                # Accept the answer to break the loop (no need to do this here but eh)
                acceptedAnswer = True
                sys.exit()

            else:
                print("Answer must be one of the following options")
                # Deny the answer to repeat the loop
                acceptedAnswer = False

# Ending text
print(lines("green", termColumns) + "\n")

if winner == False:
    print("Well, you didn't guess it in", str(guesses), "guesses. The correct answer was", correctNumber, "Try again next time!")
elif winner == True:
    print("Well done, you got the number correct in", str(guesses), "guesses. Winner! Winner! Woop woop!")