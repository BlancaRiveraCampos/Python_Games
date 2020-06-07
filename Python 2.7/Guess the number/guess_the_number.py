# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math

N = 0
n_guess = 0

# helper function to start and restart the game
def new_game():
    global secret_number
    global n_guess
    if(N == 100):
        n_guess = math.log((N - 0 + 1),2)
        n_guess = math.ceil(n_guess)
        print "New game. Range is from 0 to", N, "\n", "Number of remaining guesses", int(n_guess)
    elif(N == 1000):
        n_guess = math.log((N - 0 + 1),2)
        n_guess = math.ceil(n_guess)
        print "New game. Range is from 0 to", N, "\n", "Number of remaining guesses", int(n_guess)
    else:
        secret_number = random.randrange(0,100)
        n_guess = math.log((99 - 0 + 1),2)
        n_guess = math.ceil(n_guess)
        print "New game. Range is from 0 to 100", "\n", "Number of remaining guesses", int(n_guess)
    return n_guess
    


# define event handlers for control panel
def range100():
    global secret_number
    global N
    N = 100
    secret_number = random.randrange(0,N)
    new_game()

def range1000():
    global secret_number
    global N
    N = 1000
    secret_number = random.randrange(0,N)
    new_game()
    
def input_guess(guess):
    guess = int(guess)
    global n_guess
    print "Guess was", guess
    global secret_number
    if(n_guess == 0):
        print "Game over"
        new_game()
    elif(guess > secret_number):
        n_guess = n_guess - 1
        print "Lower.", "\n", "Number of remaining guesses", int(n_guess)
    elif(guess < secret_number):
        n_guess = n_guess - 1
        print "Higher.", "\n", "Number of remaining guesses", int(n_guess)
    elif(guess == secret_number):
        print "Correct!"
        new_game()

    
# create frame
frame = simplegui.create_frame("Guess the number",200,200)

# register event handlers for control elements and start frame
frame.add_input("Enter guess",input_guess,100)
frame.add_button("Range [0,100)",range100,200)
frame.add_button("Range [0,1000)",range1000,200)
new_game()
frame.start()