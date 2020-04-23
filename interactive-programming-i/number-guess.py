import simplegui
import random
import math

secret_number = 0
default_guesses = 7
guesses_remaining = 0
default_range = 99


# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, guesses_remaining, default_range, default_guesses
    secret_number = random.randint(1, default_range)
    guesses_remaining = default_guesses
    print "Starting new game..."

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global default_range, default_guesses
    default_range = 99
    default_guesses = 7
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global default_range, default_guesses
    default_range = 999
    default_guesses = 10
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    guess_int = int(guess)
    print("Guess was " + guess)
    
    global secret_number, guesses_remaining
    
    if (guess_int == secret_number):
        print "Correct!"
        new_game()
    elif (guess_int > secret_number):
        guesses_remaining -= 1
        print "Lower!"
    else:
        guesses_remaining -= 1
        print "Higher!"
        
    if (guesses_remaining == 0):
        print "You lose!"
        new_game()
    else:
        print "Guesses remaining: " + str(guesses_remaining)
    
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
f.add_input("Enter a guess", input_guess, 200)
f.add_button("Set range as 100", range100, 200)
f.add_button("Set range as 1000", range1000, 200)

# call new_game 
new_game()

