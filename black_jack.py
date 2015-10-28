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
in_stand = False

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}



message = "Hit or Deal?"

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

    def draw(self, canvas, pos, face_up):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        card_loc_back = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        if face_up == True:
            
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_back,card_loc_back,CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self, name):
        self.hand_card_list = []	
        self.name = name

    def join_hand_card_list(self,string_list):
        self.ans = ""
        for i in string_list:
            self.ans += " "+str(i)
        return self.ans
    
    def __str__(self):
        return str(self.name)+ self.join_hand_card_list(self.hand_card_list)	# return a string representation of a hand

    def add_card(self, card):
        self.hand_card_list.append(str(card))
            
    def reset_card_list(self):
        self.hand_card_list = []
        
    def get_value(self):
        num_of_aces = 0
        hand_value = 0
        for i in self.hand_card_list: 
            if i[1] in VALUES:
                if VALUES[i[1]] == 1:
                    num_of_aces += 1
                hand_value += VALUES[i[1]]
                           
        if num_of_aces == 0 or num_of_aces == 2 :
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
                        
   
    def draw(self, canvas, pos):
        global in_stand
        offset =76
        if in_stand == False and self.name == "Dealer":
            c1 = self.hand_card_list[0]
            c2 = self.hand_card_list[1]
            card1 = Card(c1[0],c1[1])
            card2 = Card(c2[0],c2[1])
            card1.draw(canvas, pos,False)
            pos[0]+=76
            card2.draw(canvas, pos,True)
            
        else:
            for c in self.hand_card_list:
                card = Card(c[0],c[1])
                card.draw(canvas, pos,True)
                pos[0] += offset 
                
        
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck_cards = []	# create a Deck object
        self.shuffle()

    def shuffle(self):
        for i in SUITS:
            for j in RANKS:
                self.deck_cards.append(i+j)
        random.shuffle(self.deck_cards)
        return self.deck_cards
        

    def deal_card(self):
        if len(self.deck_cards) >= 1:
            card = self.deck_cards.pop()
            return card
        return None
        
                
    def __str__(self):
        return "Deck contains "+str(self.deck_cards)	# return a string representing the deck


player_hand = Hand("Player")
dealer_hand = Hand("Dealer")


#define event handlers for buttons
def deal():
    global d, in_play,in_stand,message,score
    
    score = 0
    if in_play:
        message = "Player busted!!  New Deal?"
        in_play = False
        score -= 1;
        return
    
    d = Deck()
    message = "Hit or Stand?"
    in_play = False
    in_stand = False   
    dealer_hand.reset_card_list()  
    player_hand.reset_card_list()
    
    for i in range(2):
        player_card = d.deal_card()
        dealer_card = d.deal_card()
        player_hand.add_card(player_card)
        dealer_hand.add_card(dealer_card)
     
    in_play = True
    #print player_hand
    #print dealer_hand
 
        
    
def hit():
    global in_play,score,message
    summ = 0
    if in_play == False:
        return
    
    player_card = d.deal_card()
    player_hand.add_card(player_card)
    summ = player_hand.get_value()	
    
    if summ > 21:
        message = "Player busted!!  New Deal?"
        score -= 1
        in_play = False
 
       
def stand():
    global in_play,in_stand,score,message
    
    if in_play == False:
        return
    in_stand = True
    player_sum = player_hand.get_value()
    if player_sum > 21:
        message = "Player busted!!  New Deal?"
        score -= 1
        
    else:
        while dealer_hand.get_value() < 17:
            dealer_card = d.deal_card()
            dealer_hand.add_card(dealer_card)
            
        dealer_sum = dealer_hand.get_value()
        
        if dealer_sum > 21:
            message = "Dealer busted!!  New Deal?"
            score += 1
        elif dealer_sum >= player_sum:
            message = "Dealer WON!!  New Deal?"
            score -= 1
        else:
            message = "Player WON!!  New Deal?"
            score += 1
     
    in_play = False       
            
            
   
# draw handler    
def draw(canvas):
    global dealer_hand, player_hand,message
    
    canvas.draw_text('BLACKJACK', (10, 40), 40, 'Yellow')
    canvas.draw_text(message, (150, 330),30, 'Yellow')
    canvas.draw_text('Score:'+" "+str(score), (400, 400), 24, 'Black')
    canvas.draw_text('Dealer:', (10, 100), 24, 'Black')
    canvas.draw_text('Player:', (10, 400), 24, 'Black')
    
    dealer_hand.draw(canvas,[150,150])
    player_hand.draw(canvas, [150,450])
    

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

