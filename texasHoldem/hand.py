import itertools as it
from collections import Counter


class Hand:
    def __init__(self, cards):
        """
        """
        assert len(cards) == 5
        self.cards = cards[:]
        self.__quality__ = None
        self.card2rank = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 11,
            'Queen': 12,
            'King': 13,
            'Ace': 14}

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
        if self.__quality__ is not None:
            return

        # Is this a flush 
        curSuit = self.cards[0].getSuit()
        flush = True
        for card in self.cards:
            if curSuit != card.getSuit():
                flush = False
                break

        # Get number distribution
        numbersIdx = [x.getNumberIdx() for x in self.cards]
        numbersIdx.sort(reverse=True)
        # count numbers for pairs/three of a kind etc
        numbersC = [0,]*15
        for x in numbersIdx:
            numbersC[x] += 1
        numbers = [(y,x) for x,y in zip(range(15), numbersC) if y>0]
        numbers.sort(reverse=True)

        straight = False
        straightLowest = False
        if numbers[0][0]>2:
            if numbers[0][0] == 4:
                # Four of a kind
                numberState = 5
            else:
                if numbers[1][0] == 2:
                    # Full House
                    numberState = 4
                else:
                    # Three of a kind
                    numberState = 3
        else:
            if numbers[0][0] == 2:
                if numbers[1][0] == 2:
                    # Two pair
                    numberState = 2
                else:
                    # One pair
                    numberState = 1
            else:
                numberState = 0
                # Could be a straight
                diff = numbersIdx[0] - numbersIdx[-1]
                if diff == 4:
                    straight = True
                else:
                    if numbersIdx == [14,5,4,3,2]:
                        straight = True
                        straightLowest = True

        # Lets walk down the cats to construct a hand quality vector
        # Structure of the vector is as follows:
        # 0th: hand id from list above
        # 1st: Quality measure of hand (i.e. card of pair)
        # 2nd: Quality measure of hand (i.e. second card of 2 pair)
        # 3-8: Other cards in order

        # Make a simple list of the card (for high card comparisons)
        if flush and straight:
            if straightLowest:
                quality = [8, 0, 0] + numbersIdx
            else:
                quality = [8, numbersIdx[0], 0] + numbersIdx
        elif numberState == 5:
            quality = [7, numbers[0][1], 0] + numbersIdx
        elif numberState == 4:
            quality = [6, numbers[0][1], numbers[1][1]] + numbersIdx
        elif flush:
            quality = [5, 0, 0] + numbersIdx
        elif straight:
            if straightLowest:
                quality = [4, 0, 0] + numbersIdx
            else:
                quality = [4, numbersIdx[0], 0] + numbersIdx
        elif numberState == 3:
            quality = [3, numbers[0][1], 0] + numbersIdx
        elif numberState == 2:
            quality = [2, numbers[0][1], numbers[1][1]] + numbersIdx
        elif numberState == 1:
            quality = [1, numbers[0][1], 0] + numbersIdx
        else:
            quality = [0, 0, 0] + numbersIdx
        self.__quality__ = quality

    def __setupQuality__(self, other):
        """
        Wrapper around setting up the quality
        for each hand
        """
        if not hasattr(other, 'setQuality'):
            assert False
            return NotImplemented

        # Set quality
            # If quality already set dont set again.
        if other.__quality__ is None:
            other.setQuality()
        if self.__quality__ is None:
            self.setQuality()

    def __lt__(self, other):
        self.__setupQuality__(other)
        return other.__quality__ > self.__quality__

    def __eq__(self, other):
        self.__setupQuality__(other)
        return other.__quality__ == self.__quality__

    def __str__(self):
        """
            Create a simple string summerising the hand
        """
        idx2name = {}
        idx2name[8] = 'Straight Flush'
        idx2name[7] = 'Four of a kind'
        idx2name[6] = 'Full House'
        idx2name[5] = 'Flush'
        idx2name[4] = 'Straight'
        idx2name[3] = 'Three of a kind'
        idx2name[2] = 'Two pair'
        idx2name[1] = 'Pair'
        idx2name[0] = 'High card'
        self.setQuality()
        res = 'Hand: '
        res += idx2name[self.__quality__[0]]
        res += ' using '
        res += ', '.join(str(x) for x in sorted(self.cards))
        return res

    def __repr__(self):
        return self.__str__()


class WrongNumberOfCards(Exception):
    pass




def findBestHands(community_cards, players):
    """
        This function find who has the best hand, using the object orientated
        Note that this function is could be made substantially more efficient
        this is mostly a demonstration of object orientated programming rather
        than
    """
    bestHands = []
    for player in players:
        player_cards = player.getCards()
        if len(player_cards) != 2:
            print('Player has too many cards - look at the reset function')
            raise WrongNumberOfCards
        listOfCards = community_cards + player_cards
        temp1 = (Hand(item) for item in it.combinations(listOfCards, 5))
        bestHand = max(temp1)
        bestHands.append([bestHand, player])
    overallBest = max(bestHands, key=lambda x: x[0])[0]
    result = [(x, y) for x, y in bestHands if x == overallBest]

    return result
