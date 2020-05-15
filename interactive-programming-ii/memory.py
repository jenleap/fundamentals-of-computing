# implementation of card game - Memory

import simplegui
import random

CARD_SIZE = 50
state = 0
turns = 0

cards = range(8) + range(8)
exposed = []
flipped = []

# helper function to initialize globals
def new_game():
    global state, exposed, flipped, turns
    state = 0
    exposed = []
    flipped = []
    turns = 0
    
    random.shuffle(cards)
    for x in range(len(cards)):
        exposed.append(False)
    

# define event handlers
def mouseclick(pos):
    global state, flipped, exposed, turns
    
    index = round(pos[0] / CARD_SIZE)
    
    if index not in flipped:
        turns += 1
        if state == 2:
            state = 0
            if cards[flipped[0]] != cards[flipped[1]]:
                exposed[flipped[0]] = False
                exposed[flipped[1]] = False
            flipped = []
    
        if not exposed[index]:
            exposed[index] = True
            flipped.append(index)
            state += 1
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = " + str(turns))
    for index in range(len(cards)):
        if exposed[index]:
            canvas.draw_text(str(cards[index]), ((CARD_SIZE * index) + (CARD_SIZE / 2), 50), 30, "Green")
        else:
            canvas.draw_polygon([((index * CARD_SIZE), 0), (((index + 1) * CARD_SIZE), 0), (((index + 1) * CARD_SIZE), 100), ((index * CARD_SIZE), 100)], 5, "White", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()