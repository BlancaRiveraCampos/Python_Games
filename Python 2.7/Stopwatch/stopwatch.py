# template for "Stopwatch: The Game"
# you need to stop the watch when the miliseconds are on 0
# a global score on the right upper corner will keep track on the # of times you stop the watch 
# and how many times you succeded

# define global variables
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
counter = 0
interval = 100
score = [0,0]
active = True
y = 0
x = 0


# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    total_secs = t // 10
    A = total_secs // 60
    secs = total_secs % 60
    B = secs // 10
    C = secs % 10
    D = t % 10
    return str(A) + ":" + str(B) + str(C) + "." + str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()
    global active
    active == True

def stop():
    timer.stop()
    global score
    global counter
    global active
    active = False
    if active == False:
        global y
        y = y + 1
        score[1] = y
        if counter % 10 == 0:
            global x
            x = x + 1
            score[0] = x
    

def reset():
    global counter
    global score
    global active
    global x,y
    counter = 0
    score = [0,0]
    x = 0
    y = 0
    active = True
    timer.stop()
    

# define event handler for timer with 0.1 sec interval
def tick():
    global counter
    global interval
    counter = counter + (interval/100)
    return int(counter)

# define draw handler
def draw(canvas):
    global counter
    global score
    canvas.draw_text(format(counter),[120,150],36,"White")
    canvas.draw_text(str(score),[250,50],18,"White")
    
# create frame
frame = simplegui.create_frame("Stopwatch",300,300)
frame.set_draw_handler(draw)
frame.add_button("Start",start,100)
frame.add_button("Stop",stop,100)
frame.add_button("Reset",reset,100)
timer = simplegui.create_timer(interval,tick)


# start frame
frame.start()