# "Stopwatch: The Game"
#To earn points player should press the stop button when seconds count is 0

import simplegui

# define global variables
flag = 1
interval = 100  # 0.1 sec
A,BC,D = 0, 0,0
cur_time = 0
no_of_wins = 0
no_of_attempts = 0
update = False
stop_press = False
message = "Win / Attempts"

# in tenths of seconds into formatted string A:BC.D
def format(t):
    global A,BC,D
    A = 0
    BC = 0
    D = 0
    if (t == 0):
        return "0 : 00 . 0"
    D = t % 10
    t = t / 10
    if (t > 60):
        A = t / 60
        t = t % 60
        
    if(t > 9):
        BC = t
    else:
        BC = "0"+ str(t)

    return (str(A)+" : "+str(BC)+" . "+str(D))

#Keep track of number of attempts and number of wins
def update_score():
    global D,no_of_wins,no_of_attempts,update,flag
    if flag == 1:
        no_of_wins  = 0
        no_of_attempts = 0
        return "0 / 0"
    if update == True:
        update = False
        if D == 0:
            no_of_wins  += 1
        no_of_attempts += 1
    
    return (str(no_of_wins )+" / "+str(no_of_attempts))
        
       
   
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    timer.start()
    global flag,stop_press
    flag = 0
    stop_press = True
    
    
    
def stop_button_handler():
    global flag,update,stop_press
    timer.stop()
    flag = 0
    if (stop_press == True):
        update = True
    stop_press = False
    
    
def reset_button_handler():
    global flag,cur_time,update
    cur_time = 0 
    flag = 1
        

# define event handler for timer with 0.1 sec interval

def timer_handler():
    global cur_time,flag,update
    update = False
    if (flag == 1):
        cur_time  = 0
    else:
        cur_time  += 1
    
    
    
    
# define draw handler
def draw_handler(canvas):
    global cur_time
    canvas.draw_circle((200, 200), 100, 20, 'Orange','Orange')
    canvas.draw_text(format(cur_time), (130, 200), 40, 'Black')
    canvas.draw_text(message, (280, 20), 15, 'White')
    canvas.draw_text(update_score(), (290, 50), 24, 'White')
    
    


# create frame
frame = simplegui.create_frame("StopWatch",400,400)
timer = simplegui.create_timer(interval, timer_handler)

# register event handlers
start = frame.add_button('Start', start_button_handler,200)
stop = frame.add_button('Stop', stop_button_handler,200)
reset = frame.add_button('Reset', reset_button_handler,200)
frame.set_draw_handler(draw_handler)
frame.set_canvas_background('Purple')

# start frame, start timer
frame.start()
timer.start()
