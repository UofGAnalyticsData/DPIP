import itertools as it

class Hand:
    def __init__(self,cards):
        self.cards = cards[:]
        self.__quality__ = None
        self.card2rank = {'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack':11,'Queen':12,'King':13,'Ace':14}

    def setQuality(self):
        """
        This method finds and sets the quality of the hand
        Quality is measured as follows:
        8 Straight Flush
        7 Four of a kind
        6 Full House
        5 Flush
        4 Straight
        3 Three of a kind
        2 Two pair
        1 Pair
        0 High card
        """
        if self.__quality__!=None:
            return

        # Get suit distribution
        suits = set(x.getSuit() for x in self.cards)
        
        if len(suits)==1:
            flush = True
        else:
            flush = False
        
        # Get number distribution
        numbersC = Counter(x.getNumber() for x in self.cards)
        numbers = numbersC.most_common()

        straight = False
        straightLowest = False
        if numbers[0][-1] == 4:
            # Four of a kind
            numberState = 5 
        elif numbers[0][-1] == 3 and numbers[1][-1] == 2:
            # Full House
            numberState = 4
        elif numbers[0][-1] == 3:
            # Three of a kind 
            numberState = 3
        elif numbers[0][-1] == 2 and numbers[1][-1] == 2:
            # Two pair
            numberState = 2
        elif numbers[0][-1] == 2:
            # One pair
            numberState = 1
        else:
            numberState = 0
            # Could be a straight
            tempRang = [self.card2rank[x] for x in numbersC]
            diff = max(tempRang) - min(tempRang)
            if diff==4:
                straight = True
            else:
                tempRang.sort()
                if tempRang == [2,3,4,5,14]:
                    straight = True
                    straightLowest = True
        # lets walk down the cats
        numbersQual = [self.card2rank[x.getNumber()] for x in self.cards]
        numbersQual.sort(reverse=True)
        if flush and straight:
            if straightLowest:
                quality = [8,0,0] + numbersQual

            else:
                quality = [8,numbersQual[0],0] + numbersQual
        elif numberState == 5:
            quality = [7,self.card2rank[numbers[0][0]],0] + numbersQual
        elif numberState == 4:
            quality = [6,self.card2rank[numbers[0][0]],self.card2rank[numbers[1][0]]] + numbersQual
        elif flush:
            quality = [5,0,0] + numbersQual
        elif straight:
            if straightLowest:
                quality = [4,0,0] + numbersQual

            else:
                quality = [4,numbersQual[0],0] + numbersQual
        elif numberState == 3:
            quality = [3,self.card2rank[numbers[0][0]],0] + numbersQual
        elif numberState == 2:
            quality = [2,self.card2rank[numbers[0][0]],self.card2rank[numbers[1][0]]] + numbersQual
        elif numberState == 1:
            quality = [1,self.card2rank[numbers[0][0]],0] + numbersQual
        else:
            quality = [0,0,0] + numbersQual
        self.__quality__ = quality




            




        
        
    def __setupQuality__(self,other):
        """
        Wrapper around setting up the quality 
        for each hand
        """
        if not hasattr(other,'setQuality'):
            assert False
            return NotImplemented
        
        # Set quality
                # If quality already set dont set again.
        if other.__quality__==None:
            other.setQuality()
        if self.__quality__==None:
            self.setQuality()
        
    def __lt__(self,other):
        self.__setupQuality__(other)
        return other.__quality__ > self.__quality__

    def __eq__(self,other):
        self.__setupQuality__(other)        
        return other.__quality__ == self.__quality__


        

def findBestHands(community_cards,players):
    """
    This function find who has the best hand, using the object orientated 
    Note that this function is could be made substansially more efficient
    this is mostly a demonstration of object orientated programming rather th
    """
    bestHands = []
    count = 0
    for player in players:
        listOfCards = community_cards + player.getCards()
        temp1 = [Hand(item) for item in it.combinations(listOfCards,5)]
        count += len(temp1)

        bestHand = max(temp1)
        bestHands.append([bestHand,player])
    overallBest = max(bestHands,key=lambda x:x[0])[0]
    temp1 = [y for x,y in bestHands if x==overallBest]

    return temp1
    
        
