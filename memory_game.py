# implementation of card game - Memory

import simplegui
import random

CAN_WIDTH = 800
CAN_HEIGHT = 100
REC_WIDTH = 50
REC_HEIGHT = 100
NUM_OF_CARDS = CAN_WIDTH//REC_WIDTH
rectangle_list = []
p = [0,0,0,100,50,100,50,0,"Green"]
click_count = 0	#evry mouse click it gets incremented
numbers = []
paired_visible_cards = []
unpaired_visible_cards = []
last_card_value = -1
current_card_value = -1
click_count = 0
turns = 0
# helper function to initialize globals

def draw_rectangle():
    for i in range(NUM_OF_CARDS):
        rectangle_list.append([p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],"Green"])
        p[0] = p[0] + REC_WIDTH
        p[2] = p[2] + REC_WIDTH
        p[4] = p[4] + REC_WIDTH
        p[6] = p[6] + REC_WIDTH
        
         
def new_game():
    global click_count,unpaired_visible_cards,turns,paired_visible_cards
    unpaired_visible_cards = []
    paired_visible_cards = []
    turns = 0
    click_count = 0
    label.set_text("Turns = 0")
    for i in range(2):
        for num in range(8):
            numbers.append(num) 
    random.shuffle(numbers)
    print numbers
    
def map_mouse_click_to_index(pos):
    '''
    returns the index of rectangle where the mouse clicked
    '''
    rec_index = 0
    rec_index = pos[0]//REC_WIDTH		
    return rec_index
         
# define event handlers
def mouseclick(pos):
    global click_count,unpaired_visible_cards,last_card_value,paired_visible_cards,current_card_value,turns
    index = map_mouse_click_to_index(pos)
    if (index in unpaired_visible_cards) or (index in paired_visible_cards):
        return
    
    if click_count == 0:
        unpaired_visible_cards.append(index)
        last_card_value = numbers[index]
        click_count += 1
        
    elif click_count == 1:
        unpaired_visible_cards.append(index)
        current_card_value = numbers[index]
        click_count += 1
        turns += 1
        label.set_text("Turns = "+str(turns))
        if(last_card_value == current_card_value):
            paired_visible_cards.extend(unpaired_visible_cards)
            unpaired_visible_cards = []
            click_count = 0
        
    elif click_count == 2:	#if the previous two values not equal
        unpaired_visible_cards = []
        unpaired_visible_cards.append(index)
        last_card_value = numbers[index]
        click_count = 1
        
        
            

def draw(canvas):
    all_visible_cards = []
    all_visible_cards.extend(unpaired_visible_cards)
    all_visible_cards.extend(paired_visible_cards)
    for p in rectangle_list:
        index = rectangle_list.index(p)
        
        if index in all_visible_cards:
            canvas.draw_polygon([[p[0],p[1]],[p[2],p[3]],[p[4],p[5]],[p[6],p[7]]], 1, 'Black', "Black")
            canvas.draw_text(str(numbers[index]), (p[0]+18, 50), 24, 'White', 'sans-serif')
        else:
            canvas.draw_polygon([[p[0],p[1]],[p[2],p[3]],[p[4],p[5]],[p[6],p[7]]], 1, 'Black', p[8])
        
    
    
    
   
        
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", CAN_WIDTH, CAN_HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
draw_rectangle()
new_game()
frame.start()


# Always remember to review the grading rubric
