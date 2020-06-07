# implementation of card game - Memory
# click on the cards and try to find the equal numbers

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

deck = [0,1,2,3,4,5,6,7]
deck.extend([0,1,2,3,4,5,6,7])
random.shuffle(deck)
expose = [False]*len(deck)
value1 = 0
value2 = 0
counter = 0


# helper function to initialize globals
def new_game():
    global state, counter, expose
    state = 0
    counter = 0
    label.set_text("Turns = " + str(counter))
    expose = [False]*len(deck)
    random.shuffle(deck)

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    #click = int(pos[0]/50)
    global state, counter
    global value1, value2
    if state == 0:
        state = 1
        value1 = int(pos[0]/50)
        expose[value1] = True
        #print value1        
    elif state == 1:
        state = 2
        value2 = int(pos[0]/50)
        #print value2   
        expose[value2] = True
    else:
        if deck[value1] != deck[value2]:
            expose[value1] = False
            expose[value2] = False
        state = 1
        value1 = int(pos[0]/50)
        expose[value1] = True
        counter += 1
        label.set_text("Turns = " + str(counter))
        print counter
    
                       
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for back, j in enumerate(range(0,800,50)):
        canvas.draw_polygon([[j,0], [j+50,0], [j+50,100], [j,100]],1, "Black", "Green")
    for card, i in enumerate(range(0,800,50)):
        if expose[card] == True:
            canvas.draw_polygon([[i,0], [i+50,0], [i+50,100], [i,100]],1, "Black", "White")
            canvas.draw_text(str(deck[card]), [i,75], 80, "Black")
            

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.set_canvas_background("White")
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()