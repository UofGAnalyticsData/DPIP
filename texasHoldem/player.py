

class playerBase:
    """
    This is the base player class. It implements many of the required methods
    which allows the simple construction of simple strategies.
    """
    # Player id number (useful to compute profit)
    id_number = 0

    def __init__(self, name=None):
        """
        Basic player class
        """
        self.cards = []
        self.id_number = playerBase.id_number
        playerBase.id_number += 1
        if name is not None:
            self.name = name

    def takeCard(self, card):
        """
        Take a card method, basic implementation takes a card and adds it to
        the cards in a players hand
        """
        self.cards.append(card)

    def getCards(self):
        """
        Returns the current list of cards the player has
        """
        return self.cards[:]

    def reset(self):
        """
        Reset the  player
        This method should reset the player for the start of a hand
        """
        self.cards = []


class player_bet1(playerBase):
    def chooseBet(self, minBetToStay, curComCards, curBets, idx):
        """
        This method decides how much your agent would like to bet in every
        circumstance.

        It takes the following arguments:

        minBetToStay - Minumum bet required to stay in the game (if you bet
                       below this the player will fold)
        curComCards  - Current Community Cards which are card objects from the
                       class above
        curBets      - The current bets of each of the players (ordered by
                       playing position)
        idx          - Your playing position - useful to interpret the current
                       bets

        In this case it is a simple agent agent that tries to stay in
        and thus bets the larger of 1 and the min bet
        """
        return max(1, minBetToStay)


class player_onlyHighCard(playerBase):
    def chooseBet(self, *args):
        """
        This method decides how much your agent would like to bet in every
        circumstance.

        It takes the following arguments:

        minBetToStay - Minumum bet required to stay in the game (if you bet
                       below this the player will fold)
        curComCards  - Current Community Cards which are card objects from the
                       class above
        curBets      - The current bets of each of the players (ordered by
                       playing position)
        idx          - Your playing position - useful to interpret the current
                       bets

        In this case it will only bet when it has high cards,
        and bets the larger of 1 and the min bet
        """
        nums = [x.getNumber() for x in self.cards]
        highCards = ['10', 'Jack', 'Queen', 'King', 'Ace']
        if nums[0] in highCards or nums[1] in highCards:
            return max(1, minBetToStay)
        return 0
