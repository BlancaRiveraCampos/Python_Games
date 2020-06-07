# Mini-project - Blackjack

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []

    def __str__(self):
        string = ""
        for i in self.hand_list:
            string += i.__str__() + " "
        return "Hand contains " + string

    def add_card(self, card):
        self.hand_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
            # compute the value of the hand
        self.hand_value = 0
        card_ranks = [card.get_rank() for card in self.hand_list]
        for card in card_ranks:
            self.hand_value += VALUES[card]
        if not 'A' in card_ranks:
            return self.hand_value
        else:
            if self.hand_value + 10 <= 21:
                self.hand_value = self.hand_value + 10
                return self.hand_value
            else:
                return self.hand_value
   
    def draw(self, canvas, pos):
            # draw a hand on the canvas, use the draw method for cards
        for c in self.hand_list:
            c.draw(canvas, [pos[0],pos[1]])
            pos[0] += CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_list = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_list.append(Card(suit,rank))                

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_list)

    def deal_card(self):
        x = self.deck_list[0]
        self.deck_list.pop(0)
        return x
    
    def __str__(self):
        string = ""
        for i in self.deck_list:
            string += i.__str__() + " "
        return "Deck contains " + string


#define event handlers for buttons
def deal():
    global outcome, in_play, shuffle_deck, player_hand, dealer_hand, score

    if in_play == True:
        outcome = "Dealer wins. New deal?"
        score -= 1
        in_play = False
    else:
        shuffle_deck = Deck()
        shuffle_deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add_card(shuffle_deck.deal_card())
        player_hand.add_card(shuffle_deck.deal_card())
        dealer_hand.add_card(shuffle_deck.deal_card())
        dealer_hand.add_card(shuffle_deck.deal_card())

        in_play = True
        outcome = "Hit or stand?"

def hit():
    global player_hand, shuffle_deck, in_play, score, outcome
    # if the hand is in play, hit the player
    player_hand.get_value()
    if player_hand.hand_value <= 21:
        player_hand.add_card(shuffle_deck.deal_card())
        player_hand.get_value()
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.hand_value > 21:
            in_play = False
            score -= 1
            outcome = "You have busted. New deal?"
            print "You have busted", score
        
def stand():
    global player_hand, dealer_hand, shuffle_deck, in_play, score, outcome
    player_hand.get_value()
    if player_hand.hand_value > 21:
        in_play = False
        print "You have busted", score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    dealer_hand.get_value()
    while dealer_hand.hand_value < 17:
        dealer_hand.add_card(shuffle_deck.deal_card())
        dealer_hand.get_value()
    # assign a message to outcome, update in_play and score
    if dealer_hand.hand_value > 21:
        in_play = False
        score += 1
        outcome = "Dealer has busted. You win."
        print "Dealer has busted. You win."
    else:
        if player_hand.hand_value <= dealer_hand.hand_value:
            in_play = False
            score -= 1
            outcome = "Dealer wins. New deal?"
            print "Dealer wins.", score
        else:
            in_play = False
            score += 1
            outcome = "You win. New deal?"
            print "You win.", score

# draw handler    
def draw(canvas):
    global player_hand, dealer_hand, outcome, in_play, CARD_BACK_CENTER, CARD_BACK_SIZE
    player_hand.draw(canvas, [100,300])
    dealer_hand.draw(canvas, [100,100])
    canvas.draw_text(outcome, [100,250], 30, "White")
    canvas.draw_text(("Score " + str(score)), [450,100], 30, "White")
    canvas.draw_text("Black Jack", [200,500], 40, "White")
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [135,148], CARD_BACK_SIZE)
    else:
        dealer_hand.draw(canvas, [100,100])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()