# Mini-project #6 - Blackjack

import simplegui
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
score = 0
message = ""
outcome = ""

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
        self.cards = []
        self.value = 0
        pass	# create Hand object

    def __str__(self):
        newStr = ""
        for card in self.cards:
            newStr += card.get_suit() + card.get_rank() + " "
        return newStr
           

    def add_card(self, card):
        self.cards.append(card)
        self.get_value()
        pass	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        for card in self.cards:
            value += VALUES[card.get_rank()]

        if any(card.get_rank() == 'A' for card in self.cards):
            if value + 10 <= 21:
                value += 10
        return value
   
    def draw(self, canvas, pos):
        for x in range(len(self.cards)):
            self.cards[x].draw(canvas, ((x * 100) + pos[0], pos[1]))
  
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for x in SUITS:
            for y in RANKS:
                self.cards.append(Card(x, y))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
        pass	# deal a card object from the deck
    
    def __str__(self):
        newStr = ""
        for card in self.cards:
            newStr += card.get_suit() + card.get_rank() + " "
        return newStr

    
#define event handlers for buttons
def deal():
    global in_play, deck, player, computer, message, outcome, score
    
    if in_play:
        print("Player loses!")
        outcome = "Player loses!"
        score -= 1
    
    deck = Deck()
    deck.shuffle()
    
    player = Hand()
    computer = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    computer.add_card(deck.deal_card())
    computer.add_card(deck.deal_card())
    
    outcome = ""
    in_play = True
    message = "Hit or Stand?"

def hit():
    global in_play, score, outcome, message
 
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        
        if player.get_value() > 21:
            outcome = "Dealer wins!"
            score -= 1
            in_play = False
            message = "New deal?"
    else:
        outcome = "You're busted."
    
       
def stand():
    global in_play, score, message, outcome
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while computer.get_value() < 17:
            computer.add_card(deck.deal_card())
        
        if computer.get_value() > 21:
            outcome = "Player wins!"
            score += 1
        elif player.get_value() > computer.get_value():
            outcome = "Player wins!"
            score += 1
        else:
            outcome = "Dealer wins!"
            score -= 1
            
        print("dealer " + str(computer.get_value()))
        print("player " + str(player.get_value()))
                  
        in_play = False
        message = "New deal?"
                  
    else:
        outcome = "You're busted."
    

# draw handler    
def draw(canvas):
    
    canvas.draw_text("Blackjack", (10, 50), 40, "Black", "sans-serif")
    canvas.draw_text("Score: " + str(score), (500, 50), 20, "Black")
    canvas.draw_line((0, 70), (600, 70), 2, "White")
    canvas.draw_text(message, (50, 110), 30, "Black")
    canvas.draw_line((0, 130), (600, 130), 2, "White")
    canvas.draw_text("Dealer", (50, 170), 30, "Black")
    canvas.draw_text(outcome, (400, 170), 30, "Black")
    canvas.draw_text("Player", (50, 400), 30, "Black")
    
    player.draw(canvas, (50, 420))
    computer.draw(canvas, (50, 190))
                               
    if in_play:
        canvas.draw_image(card_back, (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1]), CARD_BACK_SIZE, [50 + CARD_BACK_CENTER[0], 190 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
        
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
