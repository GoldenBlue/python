# Mini-project #6 - Blackjack

import simplegui
import random

game_description = "This is BlackJack! \n\n\
The computer and you are dealt two cards, each. The \n\
dealer's first card is hidden.\n\
If you 'hit', you get another card, if you 'pass', the \n\
dealer starts dealing himself cards. \n\
Higher number smaller or equal 21 wins. \n\
Numbers count their value, Faces count 10 \n\
Aces count 1 or 11. \n"

# define positions for text and drawing
TEXT_SIZE = 26

    # left side
TEXT_POS = ( (50,50), (50, 400) )
CARD_POS = ( (50,70), (50, 440) )

CARD_INDENT = 15  # card indentation

SCORE_POS = (100,250)
ACTION_TEXT_POS = (100, 300)

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
printed = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# the dictionary allows to easily insert output into the program
# you assign keys to the various output vars in <dic>,
# <expl> is for the "help" button, to explain what the functions do
# and if you want to test, whether a feature is requested
# you check against <show>{feature}

# define a dictionary for keys
dic = {
    "help":"h", "print":"p", "cheat":"c",
    "hit":"t", "deal":"d", "stand":"s"
    }
# show is a dictionary with boolean values
show = {
    "help":0, "print":0, "cheat":0,
    "hit": 0, "deal":0, "stand":0
    }

expl = { 
        "help": ", shows this help",
        "debug": ", shows some additional output",
        "print": ", print something",
        "cheat": ", don't know what this should do, yet",
        "hit": ", hits the current player",
        "deal": ", shuffles the deck and deals the cards",
        "stand": ", switches to the dealer"        
        }


# define card class
class Card:
    def __init__(self, suit, rank, visible = True ):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
            self.visible = visible
        else:
            self.suit = None
            self.rank = None
            self.visible = None
            print "Invalid card: ", suit, rank


    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True
        
    def turn(self):
        self.visible = not self.visible
        
    def is_hidden(self):
        return not self.visible
    
    def draw(self, canvas, pos):
        where = ( pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1] )
        if self.is_hidden():
            canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, where, CARD_SIZE)
        else:
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, where, CARD_SIZE)

            
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

    def __str__(self):
        for c in self.cards:
            print "the sum of the hand is ",self.value

    def add_card(self, card):
        self.cards.append(card)
        
    def play_card(self, card):
        if card in self.cards:
            return self.cards.pop(card)
        else:
            print "that card is not in this hand"
            return

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        self.value = 0
        has_ace = False
        for c in self.cards:
            r = c.get_rank()
            self.value += VALUES[r]
            if r == 'A':
                has_ace = True
        if has_ace:
            if self.value + 10 <= 21:
                self.value += 10
        return self.value

    def busted(self):
        return self.value > 21
    
    def is_hidden(self):
        # return the hidden value of the first card
        if len(self.cards) > 1:
            return self.cards[0].is_hidden()
        else:
            return False
    
    def show(self):
        for c in self.cards:
            c.show()
    
    def draw(self, canvas, p):        
        card_pos = CARD_POS[p]
        indent = 0
        for c in self.cards:
            pos = (card_pos[0]+indent, card_pos[1])
            c.draw(canvas, pos)
            indent += CARD_INDENT 

            
# define deck class
class Deck:
    def __init__(self):
        self.cards = list()
        for S in SUITS:
            for R in RANKS:
                self.cards.append(Card(S,R))
                
    def __str__(self):
        print self.count() + " cards in deck"
        
    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def count(self):
        return len(self.cards)
    
    def get_top3_cards(self):
        M = max(self.count(),3)
        l = Hand()
        for c in self.cards[0:M]:
            l.add_card(c)
        return str(l)


#define event handlers for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, deck
    global score
    
    if in_play:
        outcome = "Game Aborted, lost a Point! Hit or Stand"
        score -= 1
    else:
        outcome = "Dealing cards. Hit or Stand!"
        
    # initialize the deck and the hands        
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    # shuffle the deck
    deck.shuffle()

    # deal cards
    
    player_hand.add_card(deck.deal_card())
    c = deck.deal_card()
    c.hide()
    dealer_hand.add_card(c)
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    global player_hand, outcome, score, in_play
    
    if not in_play:
        return

    # if the hand is in play, hit the player
    player_hand.add_card(deck.deal_card())

    # if busted, assign an message to outcome, update in_play and score
    outcome = "player Hand: " + str(player_hand.get_value()) \
        + ". Hit or Stand?"
    
    if player_hand.busted():
        outcome = "Player lost. New Deal?"
        in_play = False
        score -= 1


# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with messages similar to "Hit or stand?" and "New deal?". (1 pt per message)

def stand():
    global in_play, score, outcome, hidden
    global dealer_hand, player_hand, deck
    
    if not in_play:
        return
       
    dealer_hand.show()
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer_hand.get_value() < min ( 17, player_hand.get_value()):
        dealer_hand.add_card(deck.deal_card())
    
    # assign a message to outcome, update in_play and score
    in_play = False
    
    if dealer_hand.busted():
        outcome = "Dealer busted! New Deal?"
        score += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value():
            outcome = "The Bank wins! New Deal?"
            score -= 1
        else:
            outcome = "Player wins! New Deal?"
            score += 1    

def game_help():
    print game_description
    
    for d_key in dic.keys():
        print str(dic[d_key])+": "+str(d_key)+str(expl[d_key])

# keydown handler
def keydown(key):

    global show

    if ( key == simplegui.KEY_MAP[dic["help"]] ):
        game_help()

    if ( key == simplegui.KEY_MAP[dic["cheat"]] ):
        print "CHEAT mode not implemented, yet!"
        pass

    if ( key == simplegui.KEY_MAP[dic["hit"]] ):
        hit()

    if ( key == simplegui.KEY_MAP[dic["deal"]] ):
        deal()

    if ( key == simplegui.KEY_MAP[dic["stand"]] ):
        stand()

    for keymap in dic.keys():
        if ( key == simplegui.KEY_MAP[dic[keymap]] ):
            show[keymap] = not show[keymap]

# draw handler    
def draw(canvas):
    global dealer_hand, player_hand, card_back, deck
    global show

#    canvas.draw_image(card_images, CARD_CENTER, CARD_SIZE, (500,500), CARD_SIZE)

    dealer_hand.draw(canvas,0)
    player_hand.draw(canvas,1)

    dealer_text = "Dealer:"

    if not dealer_hand.is_hidden():
        dealer_text += str(dealer_hand.get_value())
        
    canvas.draw_text(dealer_text, TEXT_POS[0], TEXT_SIZE,"Black")
        
    canvas.draw_text("Player:" + str(player_hand.get_value())
        , TEXT_POS[1], TEXT_SIZE,"Black")
  
    canvas.draw_text(outcome, ACTION_TEXT_POS, TEXT_SIZE, "Yellow")
    canvas.draw_text("score: " + str(score), SCORE_POS, TEXT_SIZE, "Red")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Help", game_help, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

# deal an initial hand
player_hand = Hand()
dealer_hand = Hand()
deck = Deck()

deal()

# get things rolling
frame.start()


# remember to review the gradic rubric