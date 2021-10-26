import random as rd


class BadlySpecifiedCard(Exception):
    pass


class Card:
    """
    This is a simple class which represents a single card
    """

    def __init__(self, suit, number):
        """
        Create a card with the following suit and number

        Suit -   Should be one of 'Spades','Clubs','Hearts','Diamonds'
        Number - Should be one of '2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'
        """
        suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        numbers = [
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            'Jack',
            'Queen',
            'King',
            'Ace']
        if number not in numbers:
            raise BadlySpecifiedCard
        if suit not in suits:
            raise BadlySpecifiedCard

        self.suit = suit
        self.number = number
        # Add 2 so a '2' is a 2
        self.numberIdx = numbers.index(number) + 2

    def getSuit(self):
        """
        Returns the suit of the card
        """
        return self.suit

    def getNumber(self):
        """
        Returns the number of the card
        """
        return self.number

    def getNumberIdx(self):
        """
        Returns the number of the card i.e. 2 is 2 and Jack is 11 etc
        Aces are high.
        """
        return self.numberIdx

    def __str__(self):
        """
        Simple string implementation
        """
        return f"{self.number} of {self.suit}"
    def __repr__(self):
        """
        Simple string implementation
        """
        return self.__str__()

    def __lt__(self,x):
        """
        Simple card ordering
        """
        return self.getNumberIdx() < x.getNumberIdx()

class Deck:
    """
        This class stores the current deck state and allows shuffling and
        drawing of cards
    """

    def __init__(self):
        """
            Set up the deck
        """

        # Set up the suits and numbers
        self.suits = ['Spades', 'Clubs', 'Hearts', 'Diamonds']
        self.numbers = [
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            'Jack',
            'Queen',
            'King',
            'Ace']

        # Set up the cards
        self.cardStore = [Card(x, y) for x in self.suits for y in self.numbers]
        # Make a current deck so we can pop
        self.curDeck = self.cardStore[:]

    def shuffle(self):
        """
            In place shuffle
        """
        rd.shuffle(self.curDeck)

    def resetDeck(self):
        """
            Resets the deck and shuffles it
        """
        # Reset the deck from the store 
        self.curDeck = self.cardStore[:]
        # shuffle the cards
        self.shuffle()

    def burnCard(self):
        """
            Burn a card i.e. - draw a card without looking at it
        """
        self.curDeck.pop()

    def drawCard(self):
        """
            Deal - draw a card and return it
        """
        return self.curDeck.pop()

