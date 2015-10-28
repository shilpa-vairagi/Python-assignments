# Implementation of classic arcade game Pong

#Left paddle keys: 'w' ans 's'
#Right paddle keys: 'up arrow' ans 'down arrow'

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = []
ball_vel = []
score1,score2  = 0,0
paddle1_vel = 40
paddle2_vel = 40
paddle1_pos = [[0, HEIGHT/2-HALF_PAD_HEIGHT], #Top Left
               [0, HEIGHT/2+HALF_PAD_HEIGHT], #Bottom Left
               [PAD_WIDTH, HEIGHT/2+HALF_PAD_HEIGHT],# Bottom Right
               [PAD_WIDTH, HEIGHT/2-HALF_PAD_HEIGHT]] # Top Right

paddle2_pos = [[WIDTH-PAD_WIDTH, HEIGHT/2-HALF_PAD_HEIGHT], 
               [WIDTH-PAD_WIDTH, HEIGHT/2+HALF_PAD_HEIGHT], 
               [WIDTH, HEIGHT/2+HALF_PAD_HEIGHT], 
               [WIDTH, HEIGHT/2-HALF_PAD_HEIGHT]]


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [ WIDTH / 2, HEIGHT / 2 ]    
    
    if direction == RIGHT:
        ball_vel = [2,-2]
    if direction == LEFT:
        ball_vel = [-2,-2]
      

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(LEFT)
    
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    if ball_at_top_edge():
        ball_vel[1] = - ball_vel[1]
    if ball_at_bottom_edge():
        ball_vel[1] = - ball_vel[1]
        
        
    #print "left_at else condn"
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
        
        

    # determine whether paddle and ball collide  
    if left_pad_and_ball_collide():
        ball_vel[0] =  1.1 * (-ball_vel[0])
        #print "in fun: left_pad_and_ball_collide"
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif ball_at_left_gutter():
        #print "in fun: ball_at_left_gutter"
        score2 += 1 
        spawn_ball(RIGHT)
    elif right_pad_and_ball_collide():
        ball_vel[0] = 1.1 * (-ball_vel[0])
        #print "left_at else condn"
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif ball_at_right_gutter():     
        #rint "in fun: ball_at_right_gutter"
        score1 += 1
        spawn_ball(LEFT)

        

     # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red","White")  
          
    # draw paddles
    canvas.draw_polygon(paddle1_pos, 1, 'Yellow', 'Orange')
    canvas.draw_polygon(paddle2_pos, 1, 'Yellow', 'Orange')
       
    # draw scores
    canvas.draw_text(str(score1), (WIDTH/2-PAD_HEIGHT, 40),24, 'Red')
    canvas.draw_text(str(score2), (WIDTH/2+PAD_HEIGHT, 40),24, 'Red') 
 


def ball_at_top_edge():
    if (ball_pos[1] <= BALL_RADIUS) :
        return True
    return False
        
    
def ball_at_bottom_edge():
    if (ball_pos[1] >= HEIGHT - BALL_RADIUS):
        return True
    return False

def ball_at_left_gutter():
    if (ball_pos[0] <= BALL_RADIUS+PAD_WIDTH):
        return True
    return False
    
def ball_at_right_gutter():
    if (ball_pos[0] >= WIDTH - (BALL_RADIUS+PAD_WIDTH)):
        return True
    return False

def left_pad_and_ball_collide():
    if ball_at_left_gutter():
        #print "ball_pos : ",ball_pos
        #print "pad1_pos : ",paddle1_pos[0][1],paddle1_pos[1][1]
        if (ball_pos[1] >= paddle1_pos[0][1]) and (ball_pos[1] <= paddle1_pos[1][1]):
            return True
    return False
    
        
def right_pad_and_ball_collide():
    if ball_at_right_gutter():
        if (ball_pos[1] >= paddle2_pos[0][1]) and (ball_pos[1] <= paddle2_pos[1][1]):
            return True
    return False
        
    
def paddle1_top_edge():
    if paddle1_pos[0][1] == 0:
        return True
    return False
   
    
def paddle1_bottom_edge():
    if paddle1_pos[1][1] == HEIGHT:    
        return True
    return False
        
def paddle2_top_edge():
     if paddle2_pos[0][1] == 0:
        return True
     return False
    
def paddle2_bottom_edge():
    if paddle2_pos[1][1] == HEIGHT:    
        return True
    return False

def keydown(key):
    global paddle1_vel, paddle2_vel,vel
       
    if key == simplegui.KEY_MAP["w"]:
        if paddle1_top_edge():
            return
        paddle1_pos[0][1] -= paddle1_vel
        paddle1_pos[1][1] -= paddle1_vel
        paddle1_pos[2][1] -= paddle1_vel
        paddle1_pos[3][1] -= paddle1_vel
    
    elif key == simplegui.KEY_MAP["up"]:
        if paddle2_top_edge():
            return
        paddle2_pos[0][1] -= paddle2_vel
        paddle2_pos[1][1] -= paddle2_vel
        paddle2_pos[2][1] -= paddle2_vel
        paddle2_pos[3][1] -= paddle2_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel,vel
    
    if key == simplegui.KEY_MAP["s"]:
        if paddle1_bottom_edge():
            return
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        paddle1_pos[2][1] += paddle1_vel
        paddle1_pos[3][1] += paddle1_vel
    elif key == simplegui.KEY_MAP["down"]:
        if paddle2_bottom_edge():
            return
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
        paddle2_pos[2][1] += paddle2_vel
        paddle2_pos[3][1] += paddle2_vel

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
