# program template for Asteroids
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False

#initialize empty sets
rock_group = set([])
missile_group = set([])
explosion_group = set([])

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_info_2 = ImageInfo([135,45], [90,90], 35)
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

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust == True:
            canvas.draw_image(self.image, [self.image_center[0]*2 + self.image_center[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        self.forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += self.forward[0] * 0.5
            self.vel[1] += self.forward[1] * 0.5
        if self.pos[0] + self.radius <= 0:
            self.pos[0] = self.pos[0] + WIDTH
        elif self.pos[0] >= WIDTH:
            self.pos[0] = WIDTH - self.pos[0]
        elif self.pos[1] + self.radius <= 0:
            self.pos[1] = self.pos[1] + HEIGHT
        elif self.pos[1] >= HEIGHT:
            self.pos[1] = HEIGHT - self.pos[1]
        self.vel[0] *= (1 - .02)
        self.vel[1] *= (1 - .02)
    
    def increase_angle_vel(self):
        self.angle_vel += .2
        
    def decrease_angle_vel(self):
        self.angle_vel -= .2
    
    def thrusters_on(self):
        self.thrust = True
        self.sound = ship_thrust_sound
        self.sound.play()
    
    def thrusters_off(self):
        self.thrust = False
        self.sound.rewind()
    
    def shoot(self):
        global missile_group
        a_missile = Sprite([self.pos[0]+ self.forward[0]*self.radius, self.pos[1]+self.forward[1]*self.radius], [self.vel[0]+self.forward[0]*2,self.vel[1]+self.forward[1]*2], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.current_explosion_index = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        if self.animated:
            explosion_size = explosion_info.get_size()
            explosion_center = explosion_info.get_center()
            explosion_dim = explosion_info.get_lifespan()
            self.current_explosion_index = int((self.age % explosion_dim) // 1)
            current_explosion_center = [explosion_center[0] + self.current_explosion_index * explosion_size[0], explosion_center[1]]
            canvas.draw_image(explosion_image, current_explosion_center, explosion_size, self.pos, explosion_size)
            self.age += 0.01
            if self.current_explosion_index == 23:
                self.animated = False
                explosion_sound.rewind()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        if self.pos[0] + self.radius <= 0:
            self.pos[0] = self.pos[0] + WIDTH
        elif self.pos[0] >= WIDTH:
            self.pos[0] = WIDTH - self.pos[0]
        elif self.pos[1] + self.radius <= 0:
            self.pos[1] = self.pos[1] + HEIGHT
        elif self.pos[1] >= HEIGHT:
            self.pos[1] = HEIGHT - self.pos[1]
        self.angle += self.angle_vel
        self.lifespan = 200
        self.age += 1
        if self.age < self.lifespan:
            return False
        else:
            return True
      
    def collide(self, other_object):
        other_object_center = other_object.get_position()
        other_object_radius = other_object.get_radius()
        distance = dist(self.pos, other_object_center) 
        if distance < self.radius + other_object_radius:
            return True
        else:
            return False
        

#Key and mouse events
def keydown(key):
    global my_ship
    if simplegui.KEY_MAP["right"] == key:
        my_ship.increase_angle_vel()
    elif simplegui.KEY_MAP["left"] == key:
        my_ship.decrease_angle_vel()
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_on()
    elif simplegui.KEY_MAP["space"] == key:
        my_ship.shoot()

def keyup(key):
    global my_ship
    if simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel = 0
    elif simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel = 0
    elif simplegui.KEY_MAP["up"] == key:
        my_ship.thrusters_off()

def mouse(pos):
    global started, WIDTH, HEIGHT
    inwidth = (0 < pos[0] < WIDTH)
    inheight = (0 < pos[1] < HEIGHT)
    if (not started) and inwidth and inheight:
        started = True
        timer.start()
           
def draw(canvas):
    global time, started, rock_group, lives, missile_group, score, explosion_group
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    # update ship
    my_ship.update()
    
    #check collisions
    collisions = group_collide(rock_group, my_ship)
    if collisions:
        lives -= 1
    
    collisions2 = group_group_collide(missile_group, rock_group)
    score += collisions2
    
    #update lives and score
    canvas.draw_text("Lives : " + str(lives), [50,50], 25, "White")
    canvas.draw_text("Score : " + str(score), [50,80], 25, "White")
    
    #draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], splash_info.get_size())
    
    #restart game
    if lives < 0:
        started = False
        rock_group = set([])
        lives = 3
        score = 0
        timer.stop()
        soundtrack.rewind()
        soundtrack.play()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, my_ship
    a_rock = Sprite([random.randrange(0,WIDTH), random.randrange(0,HEIGHT)], [random.random() * 0.3,random.random() * 0.3],0, (random.random() * 0.1),asteroid_image,asteroid_info)
    if len(rock_group) < 12:
        if dist(a_rock.get_position(), my_ship.get_position()) >= 100:
            rock_group.add(a_rock)
                
#helper functions for collisions and groups
def process_sprite_group(group,canvas):
    global rock_group, missile_group, explosion_group
    group_copy = list(group)
    for sprite in group_copy:
        sprite.update()
        sprite.draw(canvas)

    mg = set([sprite for sprite in missile_group if not sprite.update()])
    missile_group = mg
    eg = set([sprite for sprite in explosion_group if not (sprite.current_explosion_index == 23)])
    explosion_group = eg

def group_collide(group, other_object):
    global explosion_group, missile_group
    mg = set([sprite for sprite in missile_group if not other_object])
    for rock in group:
        if rock.collide(other_object) == True:
            a_explosion = Sprite(rock.get_position(),[0,0],0,0, explosion_image, explosion_info)
            explosion_group.add(a_explosion)
            group.remove(rock)
            missile_group = mg
            explosion_sound.play()
            return True
    return False

def group_group_collide(group1, group2):
    count = 0
    g1 = [sprite for sprite in group1 if group_collide(group2, sprite)]
    count = len(g1)

    return count
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse)

# get things rolling
soundtrack.play()
frame.start()