
import random
import time 
import numpy as np


Deck     = [ 'A', 2, 3, 4, 5, 6, 7, 8, 9, 10 , 10, 10, 10 ]



def Hit():      
    card = random.randint(0, 12)
    return Deck[ card ]

def usable_Ace( hand ):
    card_sum = 0
    if 'A' in hand: 
        #If the hand has an ace 
        for card in hand:
            if card != 'A':
                card_sum += card
        
        i = 0
        if card_sum + 11 <= 21:
            #check if the ace can be 11
            for card in hand:
                if card == 'A':
                   hand[i] = 11
                i += 1
                ace = True
        else:
            #else it must be 1
            for card in hand:
                if card == 'A':
                   hand[i] = 1
                i += 1
                ace = False
        return hand , ace
    
    else:
        #If there is no ace the hadn returns as is
        ace = False
        return hand , ace
    
def dealer_Policy( dHand ):
    while True:
        if   sum( dHand ) < 17:
            #if the sum of the dealers hand is < 17 -> Hit
            dHand.append( Hit(  ) )
            print("    Dealer hits!: " , dHand)
            dHand , dont_Care_Flag  = usable_Ace( dHand )
            
        elif sum( dHand ) >= 17 and sum( dHand ) <= 21:
            #if its >= 17 and <= 21 -> Stick
            return dHand
        
        elif sum( dHand ) > 21:
            #else he gets burned 
            return dHand
        
def Stick( aHand, dHand ):
    
    #After deciding to stick comes the dealers turn 
    dHand = dealer_Policy(  dHand  )
    
    if sum( dHand ) <= 21:
        #if the dealers hadn is <= 21 -> compare hands
        
        print("  Stick!")
        print("~Agent:  ", aHand  )
        print("~Dealer: ", dHand  )
        
        if  sum( aHand ) == sum( dHand ):
            # Agent Hand == Dealer Hand -> Tie  
            print("    Tie!")
            return 0
        
        if  sum( aHand )  >  sum( dHand ):
            #Agent hand > Dealer Hand -> Win
            print("    Win!")
            return 1
        
        if  sum( aHand )  <  sum( dHand ):
            #Agent hand < Dealer Hand -> Loss 
            print("    Loss!")
            return -1
    else:
        #else the agent Wins
            print("~Dealer:", dHand)
            print("    Win!")
            return 1

def generate_Episode( p ):
    #New game
    #List of memory to keep the States, Actions and Rewards
    memory = []
    
    #Lists to represent the agent hand and the dealer hand
    aHand  = []
    dHand  = []
    
    #Hitting the agent with 2 cards
    for i in range( 2 ):
        aHand.append( Hit(  ) )
   
    #Hitting the dealer with 2 cards
    for i in range( 2 ):
        dHand.append( Hit(  ) )
    #Checking to see if theres a usable ace
    aHand , u_Ace           =   usable_Ace( aHand )
    dHand , dont_Care_Flag  =   usable_Ace( dHand )

    print("~Agent:"   ,   aHand   , "  " )
    print("~Dealer:[" ,  dHand[0] , ",?]" )
    #Beginning the playing phase
    while True:
       
        if  ( 10 == aHand[0] or 10 == aHand[1]) and (11 == aHand[0] or 11 == aHand[1] ):
            #If there is a natural the agent wins or draw -> Stick!
            #Stick functions dictates reward
            print("    NATURAL !")
            memory.append( ( sum( aHand ) , dHand[0] , u_Ace , 1 , Stick(aHand, dHand) ) )
            return memory
    
        elif  sum( aHand ) >= p and sum( aHand ) <= 21:
            #If we reach the policy threshold -> Stick!            #Stick functions dictates reward
            memory.append( ( sum( aHand ) , dHand[0] , u_Ace , 1 , Stick(aHand, dHand) ) )
            return memory
        
        elif  sum( aHand ) > 21:
            #If we have total > 21 -> Lost!             
            #Reward for loss: -1
            print("    BURNED")
            memory.append( ( sum( aHand ) , dHand[0] , u_Ace , 1 , -1 ) )
            return memory
        
        elif  sum( aHand ) < 21:
            #IFwe can draw more cards -> Hit!
            #but first we sava it to the memory
            memory.append( ( sum( aHand ) , dHand[0] , u_Ace , 0 , 0 ) )
            aHand.append( Hit(  ) )
            aHand , u_Ace  = usable_Ace( aHand )
            print("    Agent Hits!:", aHand )
            
 
    
 
    
Q = {}
                      #Agent sum ranges from 4 to 21
agent_Sum           = [ i   for i in range(4, 22) ]
                      #Dealer card has 10 states
dealer_Card         = [ i for i in range(12)  ]
                      #has(n't) a usable ace
u_Ace           = [ True , False ]
                      # stick or hit
actions         = [  1   ,   0   ] 


states = []
returns = {}
pairs_Visited = {}

#Initializing returns, Q(s,a) function, 
#a list of visited states and actions, a states list
for total in agent_Sum:
    #for each possible agent_sum 
    for card in dealer_Card:
        #for each possible dealer card
        for ace in u_Ace:
            #for the the both sates of the ace
            for action in actions:
                #for stick or hit
                Q            [ ( (total, card, ace)  , action ) ] = 0
                returns      [ ( (total, card, ace)  , action ) ] = 0
                pairs_Visited[ ( (total, card, ace)  , action ) ] = 0
            states.append      ( (total, card, ace) )


policy = {}
for state in states:
    #Initializing a random policy for each possible sate -> π(s,a)
    policy[ state ] = np.random.choice( actions )

#setting number of episodes 
episodes = 100000
#setting explore rate 
EPS      = 0.05

for i in range( episodes ):

    #Retruns(s,a)
    sa_Returns = []
    
    #The memory list holds all "played"
    #rewards states and actions
    memory = []
    memory = generate_Episode( 20 )
    print(memory)


    #G stores all the rewards 
    #coming from (S,A) of the episode
    #plus some discount which in this case 
    #is 1 sicne win, loos or tie are deterministic states
    G = 0
    last = True
    
    
    for agent_Sum , dealer_Card , Ace , action , reward in reversed( memory ):
    #Reading (S,A) and rewards from most recent to least recent in the episodes memory
        if last:
            last = False
        else:
            sa_Returns.append( (agent_Sum, dealer_Card, Ace , action, G) )
        G = (1 * G) + reward
        
        #reversing the Returns(S,A)
        sa_Returns.reverse()
        #making a lsit to mark visited (S,A)
        sa_Visited = []
       
        
        for agent_Sum, dealer_Card, Ace, action , G in sa_Returns:
        #Same loop now adding G and pulling form Returns
            
            #making and (S,A) index as we see in the documentation
            sa = ( (agent_Sum, dealer_Card , Ace ) , action )
         
            if sa not in sa_Visited:
             
                pairs_Visited[sa] += 1
             
                #Using incremental implementation to average returns
                returns[ (sa) ]   += ( 1 / pairs_Visited [ (sa) ]) * ( G - returns[ (sa) ] )
                Q[ sa ] = returns[ sa ]
                
                rand = np.random.random()
                if rand < 1 - EPS:
                    #picking the most efficient policy ( EXPLOIT )
                    #base on epsilon greedy approach                    
                    
                    state  = ( agent_Sum , dealer_Card, Ace )
                    values = np.array( [ Q[ ( state, a ) ] for a in actions ] )
                    
                    #pick the argmax where our values get maxed out
                    best   = np.random.choice( np.where( values==values.max() ) [0] )
                    
                    #Updating policy 
                    policy[state] = actions[best]
                    
                else:
                    
                    #There is a small chance to explore other policies 
                    policy[state] = np.random.choice( actions )
                    sa_Visited.append(sa)
            
            #Ensuring our policy wont be absolute greedy
            if EPS - 1e-7 > 0:
                
                EPS -= 1e-7
                
            else:
                
                EPS = 0    

        
        
print( policy  )    
    
    