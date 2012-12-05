# program template for Spaceship
import simplegui
import math
import random

printonce = True

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0

rock_spawn_time = 1
num_rocks = 1
acceleration = 1.2
debris = 0.8

min_acc = 0
max_acc = 8
acc_steps = 20

missile_vel = .1
max_vel = 6
TURN_BREAK = 1/60

# keypresses and their actions are at the end, after my_ship is defined

# classes to hold informational texts on the screen
class InfoText:
    ''' an infotext gets a string and further needs only a value '''
    ''' that is changed accordingly '''
    def __init__ (self,string, pos, color="White", size = 28 ):
        self.string = string
        self.pos = pos
        self.color = color
        self.size = size
        self.value = str(0)
        if show["debug"]:
            print self.string , " text object created", 

    def __str__(self):
        return self.string + ": " + self.value
    
    def set_Name(self,txt):
        self.string = txt

    def get_Name(self):
        return self.string
    
    def set_Value(self,val):
        self.value = str(val)
        if show["debug"]:
            print "set " + str(self)

    def draw(self,canvas):

        if show["debug"]:
            print "drawing text " + str(self) + " to " + str(self.pos)

        canvas.draw_text(str(self), self.pos, self.size, self.color)

        
class Dict_Texts:
    def __init__ (self,array=[]):
        self.texts = []
        for entry in array:
            self.texts.append(entry)
        
    def __str__(self):
        str = ""
        for d in self.texts:
            str += d.get_Name() + " "
                        
    def set_Value_for_key(self,key,value):
        dtext = self.get_dtext_named(key)
        if dtext:
            dtext.set_Value(value)            
        else:
            if show["debug"]:
                print "key <"+str(key)+"> not found in self"
        
    def draw(self,canvas):
        for t in self.texts:
            t.draw(canvas)
            
    def get_dtext_named(self,key):
        if show["debug"]:
            print " looking for key <" + key + "> in texts"
        for dtext in self.texts:
            if key == dtext.get_Name():
                if show["debug"]:
                    print "found",dtext.get_Name()
                return dtext
        
# the dictionary allows to easily insert output into the program
# you assign keys to the various output vars in <dic>,
# <expl> is for the "help" button, to explain what the functions do
# and if you want to test, whether a feature is requested
# you check against <show>{feature}

# define a dictionary for keys
dic = { "index": "i", "help":"h", "debug":"d", "print":"p",
    "picture":"s", "collisions":"c", "keyUp": "up", "keyDown": "down", 
    "keyRight": "right", "keyLeft": "left", "keySpace": "space"
    }
# show is a dictionary with boolean values
show = { "index":0, "help":0, "debug":0, "print":0, "cheat":0,
    "picture":0, "collisions":1
    }

expl = { "index": ", niy",
        "help": ", shows this help",
        "debug": ", niy",
        "print": ", print additional information, if in debugging mode",
        "picture": ", niy",
        "collisions": ", toggle collision detection",
        "keyDown": ", decelerate spaceship",
        "keyLeft": ", turn spaceship left",
        "keyRight": ", turn spaceship right",
        "keyUp": ", increase acceleration",
        "keySpace": ", shoot"
        }

# keydown handler
def key_down(key):

    global show
    
        # if the action is defined
    for action in perform_down:
        if key == simplegui.KEY_MAP[action]:
         perform_down[action][0](perform_down[action][1])

            # additional keypresses
    if ( key == simplegui.KEY_MAP[dic["help"]] ):
        game_help()            
        
    for keymap in dic.keys():
        if ( key == simplegui.KEY_MAP[dic[keymap]] ):
            if keymap in show:
                show[keymap] = not show[keymap]

    if ( key == simplegui.KEY_MAP[dic["collisions"]] ):
        if show[collisions]:
            print "CHEAT mode! colissions turned on"
        else:
            print "colissions turned off"
                                          
def key_up(key):
    global show
    
    for action in perform_up:
        if key == simplegui.KEY_MAP[action]:
            perform_up[action][0](perform_up[action][1])
    
            
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

class Point2D:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))
    
    def set_pos(self,p):
        self.x = p.X()
        self.y = p.Y()

    def add_vec(self,p):
        self.x += p.X()
        self.y += p.Y()

    def mult(self,m):
        ''' multiply vector with a number '''
        self.x *= m
        self.y *= m
    
    def get_list(self):
        x=self.x
        y=self.y
        return list((x,y))

    def X(self):
        return (self.x)
    
    def Y(self):
        return (self.y)
    
    def copy(self):
        ''' return a copy of a point '''
        c = Point2D(self.x,self.y)
        return c
    
    def adjust_to_frame(self,w,h):
        if self.x > w:
            self.x-=w
        if self.x < 0:
            self.x+=w
        if self.y > h:
            self.y-=h
        if self.y < 0:
            self.y+=h
            
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return Point2D(math.cos(ang),math.sin(ang))

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, zoom_factor = 1):
        self.pos = Point2D(pos[0],pos[1])
        self.vel = Point2D(vel[0],vel[1])
        self.angle = angle
        self.angle_vel = 0
        self.info = info
        self.thrust = 0
        self.acc = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.zoom_factor = zoom_factor

    def draw(self,canvas):
        
        pic_center = self.image_center[0] + self.thrust * self.image_size[0]
            
        canvas.draw_image(self.image, (pic_center, self.image_center[1]), self.image_size,
            self.pos.get_list(), self.image_size * self.zoom_factor, self.angle)

    def shoot_missle(self,die):
        ''' the missile's beginning speed and dir equal the
            ship's * a constant '''
        # create a new missile
        
        # reset the missle's pos, vector and speed
        vec = angle_to_vector(self.angle)
        vec.mult(self.radius)

        mpos = self.pos.copy()
        mpos.add_vec(vec)

        mvel = vec.copy()
        mvel.mult(missile_vel)
        mvel.add_vec(self.vel)            

        a_missile = Sprite(mpos.get_list(), mvel.get_list(), 0, 0, missile_image, missile_info, missile_sound)
        missiles.append(a_missile)

        
    def turn(self,val):
        self.angle_vel = val/10
        
    def accel(self,acc):
        vec = angle_to_vector(self.angle)
        self.vel.add_vec(vec)
    
    def go(self,a):
        self.thrust = a
        
    def speedUp(self,s):
        self.thrust = s
        
    def update(self):
        ''' update the position according to speed and acc '''

        if self.thrust:
            ''' accelerate '''
            if self.acc < max_acc:
                self.acc += max_acc/acc_steps
            else:
                self.acc = max_acc
            ship_thrust_sound.play()
            
        else:
            ''' decelerate '''
            if self.acc > min_acc:
                self.acc -= 0.1
            else:
                self.acc = min_acc
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
            

#        ''' slow down rotation'''
#        if self.angle_vel > 0:
#            self.angle_vel -= TURN_BREAK/30
#        else:
#            self.angle_vel += TURN_BREAK/30
#
#        if abs(self.angle_vel) < TURN_BREAK/30:
#            self.angle_vel = 0
            
            
        ''' rotate '''
        self.angle += self.angle_vel


        ''' calc new velocity, based on acc '''
        new_vel = angle_to_vector(self.angle)
        new_vel.mult(self.acc)        
        self.vel.set_pos(new_vel)
        
        ''' calc new position, based on velocity ''' 
        self.pos.add_vec(self.vel)
        
        ''' make sure we keep in the frame '''
        # control the bounds (should be done by frame?)
        self.pos.adjust_to_frame(width,height)
                            
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, zoom_factor = 1):
        self.pos = Point2D(pos[0],pos[1])
        self.vel = Point2D(vel[0],vel[1])
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.zoom_factor = zoom_factor
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()   
           
    def stop(self):
        ''' stops the movement of the sprite '''
        self.start((0,0))

    def start(self,vec):
        ''' sets the beginning velocity of the sprite '''
        self.vel.set_vec(vec)

        
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,
            self.pos.get_list(), self.image_size * self.zoom_factor, self.angle)
   
    def dead(self):
        return self.lifespan < self.age
    
    def randomize(self):
        ''' creates and returns a random rock '''
        self.pos = Point2D(random.randrange(0,width),random.randrange(0,height))
        vel = angle_to_vector(random.random()*math.pi*2)
        vel.mult(random.randrange(1,max_vel))
        self.vel = vel
        self.angle_vel = random.randrange(-10,10)/100
        
    def update(self):
        ''' update the position according to speed '''

        # age: what do we do if we reach self.lifespan?
        self.age += 1        
        
        ''' rotate '''
        self.angle += self.angle_vel

        ''' calc new position, based on velocity ''' 
        self.pos.add_vec(self.vel)
        
        ''' make sure we keep in the frame '''
        # control the bounds (should be done by frame?)
        self.pos.adjust_to_frame(width,height)
                  

# LOS class
class List_of_sprites:
    def __init__(self,sprites=()):
        self.sprites = list(sprites)
    
    def append(self,sprite):
        self.sprites.append(sprite)
        
    def remove(self,sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
        
    def draw(self,canvas):
        for s in self.sprites:
            s.draw(canvas)

    def randomize(self):
        for s in self.sprites:
            s.randomize()
            
    def update(self):
        for s in self.sprites:
            s.update()
            if s.dead():
                 self.remove(s)
        
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])

    # draw ship and sprites
    my_ship.draw(canvas)
    rocks.draw(canvas)
#    a_missile.draw(canvas)
    missiles.draw(canvas)

    ''' draw text on top of everything '''
    TXTs.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    rocks.update()
    missiles.update() # a_missile.update()
    
    # update the texts
    TXTs.set_Value_for_key("score",score)
    TXTs.set_Value_for_key("lives",lives)

def create_a_rock():
    ''' creates and returns a random rock '''
    a_rock = Sprite((0,0), (0,0), 0, 0, asteroid_image, asteroid_info)
    a_rock.randomize()
    return a_rock
    
# timer handler that spawns a rock    
def rock_spawner():
    global time, rocks
    
    time += 1
    
    if (time % rock_spawn_time == 0):
        rocks.randomize()

            
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)

# initialize ship and lists_of_sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
rocks = List_of_sprites()
missiles = List_of_sprites()

# populate the screen with rocks
for i in range(0,num_rocks):
    rocks.append(create_a_rock())

# set the texts with their positions
TXTs = Dict_Texts( [
    InfoText("lives", ( 50, 40 )),
    InfoText("score",( width - 150, 40 ))
] )

# set the key actions
perform_down = {
    "space": (my_ship.shoot_missle,0),
    "left": (my_ship.turn,-1),
    "right": (my_ship.turn,1),
    "up": (my_ship.go,1),
}

perform_up = {
    "left": (my_ship.turn,0),
    "right": (my_ship.turn,0),
    "up": (my_ship.go,0),
}
    

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
