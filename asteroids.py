# Rice Rocks Project
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
time = 0
rotate_vel = 0
rock_group = set([])
remove = set([])
missile_group = set([])
count = 0
num_of_rocks  = 12
lives = 3
gameStarted = False
restartGame = False




class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = 1000, animated = False):
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
#             	debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
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
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 100)
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
        self.friction = 0.05	# friction constant
    
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def fire_missile(self):
        missile_sound.play()
        forward = angle_to_vector(self.angle)
        
        mx = self.pos[0] + forward[0] * self.radius
        my = self.pos[1] + forward[1] * self.radius
        
        mx_vel = forward[0] * 5
        my_vel = forward[1] * 5
        
        missile_group.add(Sprite("Missile",[mx, my], [mx_vel , my_vel], 
                          self.angle,self.angle_vel, missile_image, missile_info))
        
    def draw(self,canvas):
        control_pos(self)     
        if self.thrust:   			#thrusters on		 
            ship_thrust_sound.play()
            canvas.draw_image(self.image, [self.image_center[0]+90,self.image_center[1]],
                        self.image_size, self.pos, self.image_size, self.angle)
       
        else:   					#thrusters off			 
            ship_thrust_sound.rewind()	
            canvas.draw_image(self.image, self.image_center,
                        self.image_size, self.pos, self.image_size, self.angle)
            
          
    def update_angle_vel(self,vel):
        self.angle_vel = vel
                     
    def update_thrust(self,thrust):
        self.thrust = thrust
        
    def reset(self,pos,vel,angle):
        self.pos[0] = pos[0]
        self.pos[1] = pos[1]
        self.vel[0] = vel[0]
        self.vel[0] = vel[1]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        
    def update(self):
        #position update
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
     
        #add friction and update velocity
        self.vel[0] *=  (1 - self.friction)
        self.vel[1] *=  (1 - self.friction)
     
        forward = angle_to_vector(self.angle)
        
        #update acceleration
        if self.thrust :
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]

        self.angle += self.angle_vel
        
    
                 
    
# Sprite class
class Sprite:
    def __init__(self, name, pos, vel, ang, ang_vel, image, info, sound = None):
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
        self.name = name
        
        if sound:
            sound.rewind()
            sound.play()
            
    def get_lifespan(self):
        return self.lifespan
    
    def get_age(self):
        return self.age
    
    def draw(self, canvas):
        control_pos(self)   
        canvas.draw_image(self.image, self.image_center,
                        self.image_size, self.pos, self.image_size, self.angle)
    
      
    def update(self):
        if self.name == "Missile":
            self.age += 1
             
        self.angle += self.angle_vel
     
        self.pos[0] += self.vel[0] 
        self.pos[1] += self.vel[1] 
        
    def get_radius(self):
        return self.radius
        
    def get_position(self):
        return self.pos
    
    #To check whether ship and a sprite collide
    def collide(self, other_object):
        d1 = self.get_position()
        r1 = self.get_radius()
        
        d2 = other_object.get_position()
        r2 = other_object.get_radius()
        
        if dist(d1, d2) < r1+r2:	
            return True
        return False
        
      
    
#When rock/ship goes out of screen
def control_pos(self):
        if self.pos[1] > HEIGHT:
            self.pos[1] = 0
        elif self.pos[1] < 0:
            self.pos[1] = HEIGHT
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] < 0:
            self.pos[0] = WIDTH

              
def process_sprite_group(sprite_group, canvas, is_missile_group):
    for sprite in list(sprite_group):
        sprite.update()
        if is_missile_group and sprite.get_age() > sprite.get_lifespan():
            sprite_group.remove(sprite)
        else:
            sprite.draw(canvas)

   
            
def group_object_collide(my_set,other_obj):
    for obj in list(my_set):
        if obj.collide(other_obj):
            my_set.remove(obj)
            return True
    return False
 
def group_group_collide(my_set,other_set):
    global score
    for obj in list(other_set):
        if group_object_collide(my_set,obj):
            score += 1
    
           
         
def draw(canvas):
    global time,my_ship,lives,count,gameStarted,restartGame, rock_group
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    canvas.draw_text(('SCORE : '+str(score)), (WIDTH-150, 30),25, 'Yellow')
    canvas.draw_text(('ASTEROIDS : '+str(len(rock_group))), (WIDTH/2-50, 30),25, 'Yellow')
    canvas.draw_text(('Lives Remaining : '+str(lives)), (5, 30),25, 'Yellow')
    
    # draw ship 
    my_ship.draw(canvas)
    process_sprite_group(missile_group,canvas,True)
    my_ship.update()
    
    #draw and update rock group(asteroids)
    process_sprite_group(rock_group,canvas,False)
    
    if group_object_collide(rock_group, my_ship):
        lives -= 1
        if lives > -1:
            my_ship.reset([WIDTH/2, HEIGHT/2],[0.01, 0.01],1)
        
    if (lives < 0) or (restartGame == True):
        gameStarted = False
        soundtrack.rewind()
        restart_game() 
        
    
    group_group_collide(rock_group, missile_group)
    if not gameStarted:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

def rock_spawner():
    global gameStarted,count ,num_of_rocks,my_ship,restartGame
    
    distance = 0
    if (count == num_of_rocks) and len(rock_group) == 0:     
        gameStarted = False
        restartGame = True 
        soundtrack.pause()
        
    if count < num_of_rocks and (gameStarted == True):
        while distance == 0 :
            rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
            distance = dist(rock_pos, my_ship.pos)
            #to avoid rocks which spawn close to ship
            if distance < (asteroid_info.get_radius() + my_ship.get_radius() + 50):
                distance = 0
                
        #random velocity
        vel_x = random.random()
        vel_y = random.random() 

        #random angle
        angle = random.random() - 0.5
        angle_vel = random.random() * 0.5
        if angle_vel > 0.3:
            angle_vel -= 0.4

        rock_group.add(Sprite("Rock",rock_pos, [vel_x, vel_y], angle,angle_vel, asteroid_image, asteroid_info))
        count += 1
     
def restart_game():
    global lives,count,score,gameStarted,my_ship,restartGame,rock_group
    if lives < 0:
        lives = 3
        score = 0
    count = 0
    rock_group = set([])
    missile_group = set([])
    my_ship.reset([WIDTH/2, HEIGHT/2],[0.01, 0.01],1)
    restartGame = False
    gameStarted = False
   
def keypress(key):
    global rotate_vel,gameStarted
    if not gameStarted:
        return
    if key == simplegui.KEY_MAP["left"]:
        rotate_vel -= 0.05
        my_ship.update_angle_vel(rotate_vel)
     
    elif key == simplegui.KEY_MAP["right"]:
        rotate_vel += 0.05
        my_ship.update_angle_vel(rotate_vel)
     
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(True)
        
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.fire_missile()

def key_up(key):	#when pressed key is released or not presssed
    global rotate_vel,gameStarted

    if key == simplegui.KEY_MAP["left"]:
        rotate_vel = 0
        my_ship.update_angle_vel(rotate_vel)
     
    elif key == simplegui.KEY_MAP["right"]:
        rotate_vel = 0
        my_ship.update_angle_vel(rotate_vel)
     
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(False)

def click(pos):
    global gameStarted,spawn
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not gameStarted) and inwidth and inheight:
        gameStarted = True 
    my_ship.reset([WIDTH/2, HEIGHT/2],[0.01, 0.01],1)
    soundtrack.play()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship 
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0.01, 0.01], 1, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keypress)
frame.set_keyup_handler(key_up)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(click)
frame.start()
timer.start()
