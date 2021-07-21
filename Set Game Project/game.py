
'''
Set Game Project main file
'''
 
import re
import time
 
#importing functions from other files
from card import Card
from stack_of_cards import StackOfCards
from player import Player
 
class SetStack(StackOfCards): #class that sets the value, color, count, and shape of the cards
 def isSet(self):
   if int(super().size() == 3):
     #For each property, check that they are all the same or all different. Otherwise, return False.
     properties = [[], [], [], []] #[ [values of each card], [counts of each], [colors], [shapes] ]
     for card in self.cards:
       properties[0].append(card.getValueOf('VALUE'))
       properties[1].append(card.getValueOf('COUNT'))
       properties[2].append(card.getValueOf('COLOR'))
       properties[3].append(card.getValueOf('SHAPE'))
     for property in properties:
       #If it is not the case that all the cards have the same value for this property and it is also not the case that all the cards have a different value for this property, then we don't need to search anymore. Return False.
       if not (property[0] == property[1] == property[2]) and not (property[0] != property[1] and property[1] != property[2] and property[2] != property[0]):
         return False
     #If there was a property that didn't safisfy the above condition, we would have exited this function already. So, if we have gotten here, return True.
     return True
   #if there are more than 3 cards, it automatically isn't a set.
   else:
     return False
 
 def displayInRows(self, full=True):
   #If we are displaying in the form of a deck (such as upCards), use this way
   if full:
     #Create the 1 2 3 4 ... at the top
     for x in range(int(super().size() / 3)):
       print("        {}".format(x + 1), end="")
     print()
     #Display the A:, B:, etc. along with the cards
     letters = ["A:", "B:", "C:"]
     for y in range (3):
       #Going across each row, the index of the card being displayed increases by 3 each time. We start with -3 since we need to display
       #the letters first.
       for x in range(-3, len(self.cards), 3):
         if x == -3:
           print(letters[y], end="")
         else:
           print("    {}".format(super().getCard(y + x)), end="")
       print()
   #if we're just printing the cards by themselves in one line (such as when a player guesses a set or asks for a hint), use this way
   else:
     print()
     for card in self.cards:
       print("\t{}".format(str(card)), end=" ")
 
 
def createDeck(): #Create a full new deck
 deck = SetStack()
 #One card of each type (3^4 = 81)
 for value in range(3):
   for color in range(3):
     for count in range(3):
       for shape in range(3):
         deck.add(Card(value, color, count, shape))
 return deck
 
 
# Input:
#   deck - SetStack which is the deck to draw new cards from
#   upCards - SetStack that are face up
#   players - list of Player
# Return boolean: True to continue game, False to end game
def playRound(deck, upCards, players, timed = False, playerTimes = [], challengeMode=[False], startOfGameTime=0, extraTime=[0], numberOfHints=[0]):
 #End game immediately if no more sets on the table and deck is empty
 if deck.size() == 0:
   foundSet = False
   for card1 in range(0, upCards.size() - 2):
     for card2 in range(card1 + 1, upCards.size() - 1):
       for card3 in range(card2 + 1, upCards.size()):
         testing = SetStack()
         testing.add(upCards.getCard(card1))
         testing.add(upCards.getCard(card2))
         testing.add(upCards.getCard(card3))
         if testing.isSet():
           foundSet = True
           break
       if foundSet:
         break
     if foundSet:
       break
   if not foundSet: #if no sets found
     print("\nThere are no more sets.\n")
     return False
  #If there are no more cards, end the game immediately
 if upCards.size() == 0:
   return False
 
 #If we just startd a new round and the timer is up, end the game immediately
 if challengeMode[0]:
   if time.time() - startOfGameTime > challengeMode[1] + extraTime[0]:
     return False
 
 #The time at the start of the game, used to figure out how long it took for a player to guess a set (is reset at the start of every
 # new round, for example it is reset when the player asks for a hint)
 roundTimer = time.time()
 #Display the upCards
 upCards.displayInRows(True)
 
 #Player input for each round below
 response = ""
 #Keep asking the user until he gives a valid input(Input Validation)
 while response != 'y' and response != 'n' and response != 'q' and response != '?' and response != "???" and response != "extra time":
   response = input("Can you find a set (y/n/?/???/q/extra time) : ")
 print()
 
 if response == "extra time": #if user requests extra time
   if challengeMode[0]: #checks if user is in challenge mode, since extra time is only available in timed mode
     extraTime[0] += 15
     print("You got some extra time: {} seconds remaining now".format(round(time.time() - startOfGameTime + extraTime[0])))
     print()
   else: #Does nothing if the user is in normal mode
     print("Extra time is for challenge mode only.")
     print()
   return True
 
 if response == 'y':
   #Ask which player has found a set so we can change the points for that specific player
   name = ""
   player = 0
   playerIndex = 0
   nameList = []
   #Get a list of names, used for figuring out if the player the user enters is valid and (since the index of each player is the same
   #in both players and nameList) to actually get the Player object that corresponds to the name the player enters
   for person in players:
     nameList.append(person.getName())
   #If there is only one player, we already know what player found the set. Only ask which player if there are multiple players.
   if len(nameList) > 1:
     while not (name in nameList):
       #figuring out which player has found the set
       name = str((input("Which player thinks they have found a set? (enter the name): ")))
       if name in nameList:
         if timed == True:
           #Get how long it took for that player to find a set
           roundTimer = time.time() - roundTimer
         playerIndex = nameList.index(name)
         player = players[playerIndex]
     print()
   #If there is only one player, get that player into the variable "player".
   else:
     roundTimer = time.time() - roundTimer
     playerIndex = 0
     player = players[playerIndex]
 
   #Check if there are actually any sets on the board. If not, automatically subtract a point from the player that called Set.
   foundSet = False
   for card1 in range(0, upCards.size() - 2):
     for card2 in range(card1 + 1, upCards.size() - 1):
       for card3 in range(card2 + 1, upCards.size()):
         testing = SetStack()
         testing.add(upCards.getCard(card1))
         testing.add(upCards.getCard(card2))
         testing.add(upCards.getCard(card3))
         if testing.isSet():
           foundSet = True
           break
       if foundSet:
         break
     if foundSet:
       break
   if not foundSet: #if no sets found
     print("\nThere actually aren't any sets on the board right now.  ", end="")
     player.addScore(-1)
     print(str(player))
     return True
 
   #Add the time to the player's time
   if timed:
     playerTimes[playerIndex] = roundTimer
 
   #Ask what the user thinks is a set (Input Validation while loop)
   inputValid = False
   while not inputValid:
     answer = input("What is the set? Type out the 3 coordinates in this format(ex: A3 B1 C2): ") #where now equals = "A3 B1 C2"
     where = answer.split(" ") #where = ["A3", "B1", "C2"]
     #Sets inputValid boolean to True(which means the input is valid)
     if answer != "" and len(where) == 3: #input validation for answer
       inputValid = True
       for x in where: # Run through each coordinate and find if it doesn't match the specified format
         if not (x[0] in "ABCabc" and x[1].isnumeric() and int(x[1]) in range((upCards.size() // 3) + 1)): #line causing error
           inputValid = False #Set variable to false if doesn't match format, which will make the loop run and ask for coordinates again
   print()
  
   #Convert the coordinates to numbers.
   for card in range(len(where)):
     sum = 0
     if where[card][0] == "B" or where[card][0] == "b":
       sum += 1
     elif where[card][0] == "C" or where[card][0] == "c":
       sum += 2
     sum += 3 * (int(where[card][1]) - 1)
     where[card] = sum
   check = SetStack()
  
   #check that all the cards are different and valid. Otherwise the player could get a set by typing one card 3 times, for example
   allDifferent = True
   for i in range(len(where)):
     if where.index(where[i]) < i:
       allDifferent = False
   if allDifferent == False:
     player.addScore(-1)
     print("\t Oops, it looks like you used a card more than once or typed a card that doesn't exist.", str(player))
     return True
  
   #add the guessed cards to a new setStack so we can call isSet()
   for i in range(len(where)):
     check.add(upCards.getCard(where[i]))
   check.displayInRows(False)
   if check.isSet():
     #Add 1 point to the player that guessed correctly
     player.addScore(1)
     if timed:
       playerTimes[playerIndex] += roundTimer
     print("\t - Yes, this is a set! {}: {} points".format(player.getName(), player.getScore()))
     if deck.size() > 0 and upCards.size() == 12:
       for i in range(3):
         upCards.replaceCard(where[i], deck.deal())
     else:
       where.sort()
       where.reverse()
       for i in range(3):
         upCards.remove(where[i])
   else:
     #Subtract 1 point from the player that guessed incorrectly
     player.addScore(-1)
     print("\t - Whoops, that isn't a set. {}: {} points".format(player.getName(), player.getScore()))
   print()
   return True
 
 if response == 'n': #means user cannot find a set
   #If there are already 21 cards, display message
   if upCards.size() == 21:
     print("In 21 cards, there is a 100% probability that there is a set. So, no more cards for you.")
   #Otherwise, add 3 cards and start another round.
   else:
     #Only add cards if there are any in the deck, if the deck is empty and we call cards there will be an error
     if deck.size() > 0:
       for i in range(3):
         upCards.add(deck.deal())
     else:
       print("The deck is empty.")
       return True
   return True
 
 #See if there is a set. If so, return the first one found. If no sets are found, tell the player that there are no sets currently
 # on the board and that the player needs to add 3 cards.   
 if response == '?': #means user wants 1 hint
   print()
   #Search through all possibilities of 3 cards. If no sets are found, tell the player.
   foundSet = False
   #Search through all combinations of 3 cards (order doesn't matter)
   for card1 in range(0, upCards.size() - 2):
     for card2 in range(card1 + 1, upCards.size() - 1):
       for card3 in range(card2 + 1, upCards.size()):
         testing = SetStack()
         testing.add(upCards.getCard(card1))
         testing.add(upCards.getCard(card2))
         testing.add(upCards.getCard(card3))
         if testing.isSet():
           foundSet = True
           print("Here's a set") #If a set is found, display it in the proper format
           testing.displayInRows(False)
           print()
           numberOfHints[0] += 1
           return True
   if not foundSet: #If a set is not found, add 3 cards
     print("There are currently no sets. Add 3 cards. (type n)")
   print("\n")
   return True
 
 if response == "???": #means user wants all available hints (Super Hint)
   print()
   #Search through all combinations of 3 cards. If no sets are found, tell the player.
   foundSet = False
   for card1 in range(0, upCards.size() - 2):
     for card2 in range(card1 + 1, upCards.size() - 1):
       for card3 in range(card2 + 1, upCards.size()):
         testing = SetStack()
         testing.add(upCards.getCard(card1))
         testing.add(upCards.getCard(card2))
         testing.add(upCards.getCard(card3))
         if testing.isSet():
           foundSet = True
           print("Here's a set") #If a set is found, display it in the proper format
           testing.displayInRows(False)
           numberOfHints[0] += 1
           print()
   if not foundSet: #If a set is not found, add 3 cards
     print("There are currently no sets. Add 3 cards. (type n)")
   print("\n")
   return True
  
 if response == 'q': #means user wants to end the game
   #exit the round and return False.
   return False
  
 
# Input:
#   deck - SetStack which is the deck to draw new cards from
#   players - list of Player
# No return value
def playSetGame(deck, players, timed = False, playerTimes = [], challengeMode=[False]):
 numHints = [0]
 extraTime = [0]
 upCards = SetStack()
  # deal the necessary amount cards from the deck (all cards in deck if deck.size() < 12, else 12)
 if deck.size() < 12:
   for x in range (deck.size()):
     upCards.add(deck.deal())
 else:
   for x in range(12):
     upCards.add(deck.deal())
 
 if challengeMode[0]: #timer for challenge mode(different from normal game timer)
   startOfGameTime = time.time()
 else:
   startOfGameTime = 0
  
 # repeatedly call playRound until the game is over. Since playRound returns a boolean, we can just do this:
 while playRound(deck, upCards, players, timed, playerTimes, challengeMode, startOfGameTime, extraTime, numHints):
   continue
 
 #If we have gotten here, the game is over. Display the end message.
 print("\nGreat game!")
 print()
 print("Game Stats:")
 print()
 if not challengeMode[0]:
   #print out the scores for each player
   for player in players:
     print(str(player))
   print()
 
   #Print out the number of hints that were used throughout the entire game
   if numHints[0] == 1:
     print("1 hint was used in total")
   else:
     print("{} hints were used in total".format(numHints[0]))
   print()
 
   #Print out the timed scores for each player if we're in timed mode
   if timed:
     print("Timed scores for each player (in points per second): ")
     for i in range(len(players)):
       if players[i].getScore() == 0:
         print("{}: 0 (didn't find a set)".format(players[i].getName()))
       else:
         print("{}: {} points/second".format(players[i].getName(), round(players[i].getScore() / round(playerTimes[i]), 3)))
 #Challenge mode has a custom print message.
 else:
   print("You were able to get {} point(s) in {} seconds.".format(players[0].getScore(), challengeMode[1] + extraTime[0]))
   if numHints[0] == 1:
     print("1 hint was used in total")
   else:
     print("{} hints were used in total".format(numHints[0]))
   print()
 
def play(): #Function to start the game and initialize everything
 players = []
 name = "something"
 num = 1
 nameList = []
 playerTimes = []
 timed = False
 print("Welcome to the game of Set!")
 print
 Help = ""
 
 while not (Help == "y" or Help == "n"): #input validation for y/n
   Help = input("Do you know how to play the game? (y/n): ")
   if Help == "n": #give rules for the game if user does not know how to play
    print("\nHere is the help menu for the game of set:")
    print("The object of the game is to identify a 'Set' of three cards from 12 cards laid out on the table. Each card has a variation of the following four features:\n1) COLOR: Each card is red, green, or blue.\n2) SYMBOL: Each card has an X, Y, or Z.\n3) NUMBER: Each card has one, two, or three letters.\n4) PATTERN: Each card is lowercase, uppercase, or underlined.\n\nA 'Set' consists of three cards in which each feature is either the same on each card OR is different on each card. That is to say, any feature in the 'Set' of three cards is either common to all three cards or is different on each card")
    print("\n Examples of sets:\n1) color: different on each card, symbol: the same on each card, number: the same on each, pattern: the same on each card\n2) color: different on each card, symbol: different on each card, number: different on each card, pattern: different on each card\n3) color: the same on each card, symbol: the same on each card,number: different on each card, pattern: different on each card")
    input("\nwhen you are done reading the rules and ready to play, press enter: ")
  #Input validation combined with calling playSetGame() over and over again until the user wants to stop
 again = "y"
 while again == "y":
   challengeMode = ""
   while challengeMode != "y" and challengeMode != "n": #input validation for y/n
     challengeMode = input("\nDo you want to play Challenge Mode?\n(Challenge mode is single player only and will allow you to choose a time limit for yourself) (y/n): ")
   if challengeMode == "y":
     timeLimit = "something"
     players.append(Player("Player 1")) #This name is actually irrelevant since we never display or ask for the player's name at all
     # while in Challenge Mode
     print()
     while not timeLimit.isnumeric():
       timeLimit = input("Enter how much time you would like in seconds: ")
     challengeMode = [True, int(timeLimit)]
   else:
     challengeMode = [False]
    
   #We only ask for the names of all the players if we're not doing Challenge Mode (Challenge Mode only allows for 1 player)
   if not challengeMode[0]:
     #Keep asking for names until the player gives an empty string(presses enter)(input validation)
     #Multiplayer Support(as many players as you like!)
     players = []
     while name != "" :
       print()
       name = input("What is player {}'s name? Players with the same name will count as one player. (Press enter to start):".format(num))
       if name != "" and not (name in nameList):
         players.append(Player(name))
         nameList.append(name)
       num += 1
     #If no actual names are given, automatically create a player with the name "Player 1"
     if len(players) == 0:
       players.append(Player("Player 1"))
     for player in players:
       playerTimes.append(0)
  
   #Timer code below
   timed = ""
   print()
   if not challengeMode[0]:
     while not (timed == "y" or timed == "n"): #input validation for timed mode input
       timed = input("Do you want to play with a timer? (y/n): ")
     if timed == "y":
       timed = True
     else:
       timed = False
   #If we're in Challenge Mode, set timed to False. Challenge Mode has its own timer
   else:
     timed = False
   print()
  
   deck = createDeck()
   deck.shuffle()
   startTime = time.time() #Used to figure out how long the entire game took
  
   playSetGame(deck, players, timed, playerTimes, challengeMode)
  
   #Input validation for if the player wants to play another game
   again = ""
   if timed: #calculates the game time if timed = true by subtracting the start time from the current time and rounds to 2 decimal points
     print("\nGame time: {} seconds".format(round(time.time() - startTime, 2)))
     print()
   while again != "y" and again != "n":
     again = input("\nDo you want to play another game? (y/n): ") #if play another game equals true, it keeps the player names and starts a new game
   if again == 'n':
     print("\nThanks for playing!\nBye!")
   else:
     if timed: #if timed mode was on, lists out the player times one by one
       for i in range(len(players)):
         playerTimes[i] = 0
 
 
def main():
   play()
  
  
if __name__ == "__main__":
   main()
