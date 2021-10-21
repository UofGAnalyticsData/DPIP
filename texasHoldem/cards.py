import random as rd

class Card:
    """
    This is a simple class which represents a single card
    """
    def __init__(self,suit,number):
        self.suit = suit
        self.number = number
    def getSuit(self):
        return self.suit
    def getNumber(self):
        return self.number
    def __str__(self):
        return f"{self.number} of {self.suit}" 
    def display(self):
        pass

class Deck:
    """
    This class stores the current deck state and allows shuffing and drawing of cards 
    """
    def __init__(self):
        """
        Set up the deck
        """

        # Set up the suits and numbers 
        self.suits = suits = ['Spades','Clubs','Hearts','Diamonds']
        self.numbers = ['2','3','4','5','6','7','8','9','10','Jack','Queen','King','Ace']
        
        # Set up the cards
        self.cardStore = [Card(x,y) for x in self.suits for y in self.numbers]
        # Make a current deck so we can pop
        self.curDeck = self.cardStore[:]
    def shuffle(self):
        # In place shuffle
        rd.shuffle(self.curDeck)
    def resetDeck(self):
        # make a new deck copy
        self.curDeck = self.cardStore[:]
        # shuffle 
        self.shuffle()
    def burnCard(self):
        # Burn - draw a card without looking at it
        self.curDeck.pop()
    def drawCard(self):
        # Deal - draw a card and return 
        return self.curDeck.pop()
