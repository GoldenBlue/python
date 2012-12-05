# implementation of card game - Memory

# idea for animation: Oleg Konovalov
# idea for more than 2-tuples: Oleg Konovalov

# we have a list of cards
# a list of indexes keeps track of exposed cards
# the index also determines the rect on the original picture
# now we have a picture as background
# we also have a timer, now, a cheat mode, can choose different pictures...


import simplegui
import random
import math


# the pictures in the following pic must be the same as PAIRS
# (else the pictures on the cards will look garbeled)
# the picture you use should have no additional information
# on it, since that makes it harder to find out where the
# pictures you actually want are... we could work with frames,
# but that's not done, so far

#override later, if necessary
FRAME = { "left":0,"top":0, "right":0, "bottom":0 }

# mind cards with symbols
#PICSTR="http://www.prs.heacademy.ac.uk/awesome/images/f/fd/75675.jpg"
#DATA = { "line": 3, "total": 30, "card_width": 140 }
#FRAME = { "left":0,"top":24, "right":0, "bottom":0 }
#DATA = { "line": 3, "total": 15, "card_width": 140 }
#FRAME = { "left":0,"top":24, "right":0, "bottom":370 }

#golemcards
#PICSTR = "http://www.curufea.com/games/warpspawn/golem_cards/Golem_Cards.jpg"
#DATA = { "line": 6, "total": 24, "card_width": 80 }

# playing cards, jacks and queens
PICSTR = "http://www.elftown.com/stuff/z/61513/jittobjects/Deck_of_Cards___Queens_Jacks_by_Jitter_Stock.png"
DATA = { "line": 2, "total": 8, "card_width": 120, "tuples":2 }
#DATA = { "line": 2, "total": 8, "card_width": 120, "tuples":4 }

#
### try to change vars only above this point...
#

# the dictionary allows to easily insert output into the program
# you assign keys to the various output vars in <dic>,
# <expl> is for the "help" button, to explain what the functions do
# and if you want to test, whether a feature is requested
# you check against <show>{feature}

# define a dictionary for keys
dic = { "index": "i", "help":"h", "debug":"d", "print":"p",
    "picture":"s", "cheat":"c"
    }
# show is a dictionary with boolean values
show = { "index":0, "help":0, "debug":0, "print":0, "cheat":0,
    "picture":0
    }

expl = { "index": ", draws the index on each card",
        "help": ", shows this help",
        "debug": ", shows some additional output",
        "print": ", print additional information, if in debugging mode",
        "picture": ", toggle between loaded image and cards",
        "cheat": ", reveal all tuples"
        }


# load the pic into memory
pic = simplegui.load_image(PICSTR)
NUM_X_PICS = DATA["line"]
PAIRS = DATA["total"]
C_WIDTH = DATA["card_width"]

# hom many equal cards are there in the deck?
NUMTUPLES = 2 

if "tuples" in DATA:
    NUMTUPLES = DATA["tuples"]

### some beauty vars, change at your liking
TEXT_SIZE = 40 # size of the winning text
INDENT = 5 # draw a border around the cards
show_pic = 0 # show the loaded picture
colors = [ "Brown", "Yellow", "White", "Black", "Grey" ]
win_color = colors[0]

TIMER_SPEED = 100 # speed in ms
FLIP_STATES=5 # animation frames of a flip

#
## the actual code starts, don't change numbers below here
#

NUM_Y_PICS = PAIRS / NUM_X_PICS

# the dimensions of the pic
PIC_WIDTH = pic.get_width() - ( FRAME["left"] + FRAME["right"] )
PIC_HEIGHT = pic.get_height() - ( FRAME["top"] + FRAME["bottom"] )
PIC_RATIO = PIC_HEIGHT / PIC_WIDTH
PIC_CENTER = ( PIC_WIDTH / 2 + FRAME["left"],
              PIC_HEIGHT / 2 + FRAME["top"] )

# the size of the source rectangles on the pic
P_WIDTH = PIC_WIDTH / NUM_X_PICS
P_HEIGHT = PIC_HEIGHT / NUM_Y_PICS

# calculate card height using width and pic ratio
C_HEIGHT = P_HEIGHT * C_WIDTH / P_WIDTH

CARDS=PAIRS*NUMTUPLES # number of memory cards depends on the pairs

# size of our card grid
XGRID = int(math.sqrt(CARDS))
YGRID = math.ceil( CARDS / XGRID )

card_list=[] # the list of all cards
revealed=[] # list to keep track of revealed pairs
current=[] # pair that is currently exposed 

moves=0 # how many moves did we do

# the size of the canvas depends on the size of the cards
YHEIGHT = YGRID * C_HEIGHT
XWIDTH = XGRID * C_WIDTH

# we need sizes for the source image
#CARD_PIC_HEIGHT = PIC_HEIGHT / YGRID
#CARD_PIC_WIDTH = PIC_WIDTH / XGRID / 2
#CARD_PIC_SIZE = (CARD_PIC_HEIGHT, CARD_PIC_WIDTH)

flips = [] # a list to hold the indexes and state counters of the cards that are being flipped
blinking = 0

lastclick = [0,0] # for debugging, remember the last mouseclick

# helper function that draws a rect with width of a card
def draw_card(canvas,index, revealed):

    global pic
        
    ''' draws a card at pos index that is secret or not '''
    
    pos = index2cords(index, XGRID) # get the grid coords of index
    pos_pic = index2cords(card_list[index], NUM_X_PICS)
    
    # get the canvas coords
    x1 = pos[0] * C_WIDTH
    y1 = pos[1] * C_HEIGHT
    
    # we only need the center of the card
    p_x = ( pos_pic[0] + 0.5 ) * P_WIDTH + FRAME["left"]
    p_y = ( pos_pic[1] + 0.5 ) * P_HEIGHT + FRAME["top"]
    center_source = ( p_x, p_y )
    
    # debug output
    if show["print"]:
        print "index["+ str(index)+"] => "+str(card_list[index])
    
    x2 = x1 + C_WIDTH
    y2 = y1 + C_HEIGHT
 
    # "center" of the card for text
    center_text = ( (x1+x2) / 2 - 10, (y1+y2)/2 + C_HEIGHT/4 )
    
    # center of the card
    center = ( (x1+x2) / 2, (y1+y2) / 2 )
    
    # calculate the width of the frame
    n = FLIP_STATES
    # find the current step for this card
    cur = 0
    for d in flips:
        if d[0] == index:
            cur = d[1]

    mult = 1
    if cur: # 0 <= cur <= n = FLIP_STATES
        mult = 2 * cur / n - 1 # -1 <= mult <= 1 
        if mult < 0:
            mult = -mult
        else:
            revealed = not revealed

    dx = C_WIDTH * ( 1 - mult ) / 2
    x1 += dx
    x2 -= dx
    
    if revealed:
        # draw a revealed card
        canvas.draw_polygon( [ (x1,y1), (x2,y1), (x2,y2),
                              (x1,y2) ], INDENT, "Black", "White")

        canvas.draw_image(pic, center_source, ( P_WIDTH, P_HEIGHT ),
            center, ((C_WIDTH-2*INDENT)*mult, C_HEIGHT-2*INDENT) )
#        canvas.draw_text( str(card_list[index]),
#                        center_text, TEXT_SIZE, "Red")
        
    else: # draw a hidden card
        canvas.draw_polygon( [ (x1,y1), (x2,y1), (x2,y2),
                              (x1,y2) ], INDENT, "Black", "Green")
                          
        if ( show["index"] ):
            canvas.draw_text( str(index), center_text, (TEXT_SIZE-10)*mult, "Yellow")
  
# helper function to initialize globals
def init():
    global card_list, revealed, current, moves
    
    card_list = range(PAIRS)
    for i in range(1,NUMTUPLES):
        card_list += range(PAIRS)
        
    random.shuffle(card_list)
    revealed = []
    current = []
    moves = 0
    l.set_text("Moves = " + str(moves))
    flips = []
    blinking = 0

#	uncomment to DEBUG
#    print card_list
#    print str(len(revealed)) + "/" + str(len(card_list))

# helper function to convert mouse coordinates to index
def cords2index(pos):

    # calculate index
    my_index = pos[0] // C_WIDTH + ( pos[1] // C_HEIGHT ) * XGRID
    return my_index

# helper function to convert index to grid coords
def index2cords(my_index,xgrid):
    
    # calculate coordinates
    x = ( my_index % xgrid )
    y = ( my_index // xgrid )
    
    return (x,y)
     
# define event handlers
def mouseclick(pos):
    
    global lastclick, current, revealed, moves
    #global flips
    
    if show["picture"]:
        return
    
    # check if we are in the boundaries
    if pos[0] < 0 or pos[0] > XWIDTH:
        return
    
    lastclick = (pos)
    
    ''' updates the moves counter and adds the selected card
        to the current list or to the revealed list '''
    ''' initiates flipping animation '''
    
    # calculate the index by the horizontal position
    index = cords2index(pos)
    if ( index > CARDS - 1 ): # out of range
        return
    
    # if there are less than two current cards, add a card to
    # current list
       
    if index not in current + revealed:
        
        flips.append([index,FLIP_STATES])
        current.append(index)

       
        if len(current) <= NUMTUPLES:
            mem = card_list[current[0]]
            equal = 1
            for i in current:
                equal = equal and card_list[i] == mem

            if (equal and len(current) == NUMTUPLES ):
                    revealed += current
        
        else:
            # unflip the other cards
            for i in current:
                if i not in revealed:
                    flips.append([i,FLIP_STATES])
            current = [index]
            

        # update the moves
        moves += 1
        l.set_text("Moves = " + str(moves//2))
        
# switch the color
def switch_color(color_index):
    if color_index in colors:
        index = colors.index(color_index)
        index += 1
        index %= len(colors)
        return colors[index]

# go through the list of cards to be flipped and add smth
def flip_cards():
    global flips
    # counter for every index
    
#    if len(flips) == 0 and not blinking:
#        t.stop()
        
    for c in flips:
        if c[1] == 0: # remove the index from the list
            flips.remove(c)
        else:
            c[1] -= 1
            
def load_image(link):
    global pic 
    pic = simplegui.load_image("")

def set_x_pics(n):
    global num_x_pics
    num_x_pics = int(n)
    init()
    
# a timer for animation clicks (iterates through an array)
# and switches color
def timer():

    global win_color
    win_color = switch_color(win_color)
    
    flip_cards()
    pass

# cards are logically WIDTH x HEIGHT pixels in size    
def draw(canvas):
    global show

    ''' iterate through the card_list and print every card
        if it is revealed or current '''

    # just show the picture, and return, if wanted
    if show["picture"]:
        if PIC_RATIO > 1:
            compress = 1
        else:
            compress = PIC_RATIO
        if compress * YHEIGHT < YHEIGHT:
            compress = 1
        
        canvas.draw_image(pic, (PIC_CENTER), (PIC_WIDTH, PIC_HEIGHT),
             (XWIDTH / 2 , YHEIGHT / 2), (XWIDTH / 2, YHEIGHT * compress))
        return
        
    # the position of a card is determined by the index:
            
    for index in range(len(card_list)):
        draw_card(canvas,index, index in revealed + current)

    
    if len(revealed) == PAIRS * 2:
        global blinking
        if (not blinking):
            t.start()
            blinking = 1
            
        canvas.draw_text("You Won in " + str(moves//2),
                         (XWIDTH//2-100, YHEIGHT//2 + 20), 24, win_color)
        canvas.draw_text("moves!",
                         (XWIDTH//2-40, YHEIGHT//2 + 50), 24, win_color)

    if ( show["debug"] ):
        canvas.draw_text("COLS: " + str(XGRID),(5, YHEIGHT - 27), 6, "Yellow")
        canvas.draw_text("ROWS: " + str(YGRID),(5, YHEIGHT - 19), 6, "Yellow")
        canvas.draw_text("lastclick: " + str(lastclick) +
            "[" + str(cords2index(lastclick)) + "]", (5, YHEIGHT - 11), 6, "Yellow")
        
    if show["print"]:
        print
        print "Grid dimensions are: (", XGRID , "x" ,YGRID, ")"
        print "pic card size is: [" + str(P_WIDTH) +"," + str(P_HEIGHT) + "]"
        print
    
    # draw the image next to our puzzle
#    if show_pic:
#        canvas.draw_image(pic, (PIC_WIDTH/2, PIC_HEIGHT/2), (PIC_WIDTH, PIC_HEIGHT),
#             (XWIDTH * 1.5, YHEIGHT / 2), (XWIDTH, YHEIGHT))
        
    show["print"] = 0 # only ever print once!

# utility function to find tuples
def find_tuples():
    # returns an indexed list by value
    # tuples[value] = index1,...,indexN
    tuples = []
    
    for value in range(PAIRS):
        tlist = []
        for index in range(CARDS):
            if card_list[index] == value:
                tlist.append(index)

        tuples.append(tlist)

    return tuples

def game_help():
    print "This is a simple memory game. You can set the"
    print "number of cards in the source code, near the top"
    print "(the variable is <PAIRS>)"
    print
    print "RULES:"
    print "pic two cards, if they match, the cards stay open"
    print "if they don't match, they are hidden when you"
    print "click on the next card"
    print
    print "Keys you can use in this game:"
    for d_key in dic.keys():
        print str(dic[d_key])+": "+str(d_key)+str(expl[d_key])

# keydown handler
def keydown(key):

    global show

    if ( key == simplegui.KEY_MAP[dic["help"]] ):
        game_help()

    if ( key == simplegui.KEY_MAP[dic["cheat"]] ):
        print "CHEAT mode! following tuples found:"
        for l in find_tuples():
            print l
        print
        
    for keymap in dic.keys():
        if ( key == simplegui.KEY_MAP[dic[keymap]] ):
            show[keymap] = not show[keymap]


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", XWIDTH + show_pic * ( XWIDTH + 10 ), YHEIGHT )

frame.add_button("Restart", init)
frame.add_button("Help", game_help)
#frame.add_input("http address to the picture", load_image, 100)
#frame.add_input("1st line pics, restart", set_x_pics, 30)

l=frame.add_label("Moves = " + str(moves))
t = simplegui.create_timer(TIMER_SPEED,timer)

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

# get things rolling
t.start()
frame.start()


# Always remember to review the grading rubric