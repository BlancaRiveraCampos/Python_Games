# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors


def name_to_number(name):
    if(name == "rock"):
        return 0
    elif(name == "Spock"):
        return 1
    elif(name == "paper"):
        return 2
    elif(name == "lizard"):
        return 3
    elif(name == "scissors"):
        return 4
    else:
        return "Error: wrong name"


def number_to_name(number):
    if(number == 0):
        return "rock"
    elif(number == 1):
        return "Spock"
    elif(number == 2):
        return "paper"
    elif(number == 3):
        return "lizard"
    elif(number == 4):
        return "scissors"
    else:
        return "Error: wrong number"
    
import random

def rpsls(player_choice): 
    print "Player chooses " + player_choice
    player_number = name_to_number(player_choice)
    comp_number = random.randrange(0,5)
    print "Computer chooses " + number_to_name(comp_number)
    num = (player_number - comp_number)%5
    if(num == 1) or (num == 2):
        print "Player wins!" + "\n"
    elif(num == 3) or (num == 4):
        print "Computer wins!" + "\n"
    elif(num == 0):
        print "Player and computer tie!" + "\n"
    else:
        print "Error" + "\n"
    
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")
