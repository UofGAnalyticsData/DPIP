from DPIP.texasHoldem import cards
from DPIP.texasHoldem import hand
import random as rd


class Game:
    """
        Class to store and run the game state

        Class must be initialised with all players

        Parameters
        ----------
        Players - A list of players - Cannot be modified once the game
                  has started
    """

    def __init__(self, players):
        """Initialise the game

            Parameters
            ----------
            Players - A list of players - Cannot be modified once the game
                    has started
        """
        self.players = players[:]
        self.playersOrig = players[:]
        self.Deck = cards.Deck()
        self.profit = {x.id_number: 0 for x in players}
        self.__cleanup__()

    def getProfitByPlayer(self):
        """
            Obtain the profit achieved this game indexed by player
        """
        id2player = {x.id_number: x for x in self.players}
        return {id2player[x]: y for x, y in self.profit.items()}

    def getProfitByName(self):
        """
            Obtain the profit achieved this game indexed by name
        """
        id2name = {}
        for x in self.players:
            if hasattr(x, 'name'):
                id2name[x.id_number] = x.name
            else:
                id2name[x.id_number] = x.id_number
        return {id2name[x]: y for x, y in self.profit.items()}

    def __cleanup__(self):
        """
            Clean up the class to reset the variable to play the next hand
        """
        self.communityCards = []
        self.curBets = [None for x in self.players]
        self.stillIn = [None for x in self.players]
        self.Deck.resetDeck()
        for player in self.players:
            player.reset()

    def runBettingRound(self):
        """
            Run a single betting round (one round of bets, raises checks etc)

            Implementation is simplified to fix the number of betting rounds

            Players are assumed to be out if they bid below the minimum bet
            to stay in
        """

        # Get the current set of community cards
        curComCards = tuple(self.communityCards)

        # Get the current maximum bets
        curMax = max(self.curBets)

        # Make sure that that betting is working correctly
        bets = [x for x, y in zip(self.curBets, self.stillIn) if y]
        assert max(bets) == min(bets)

        # Run a fixed number of round
        Raised = True
        roundCount = 0

        # Run rounds while:
        #       - Someone has raised
        #       - Number of rounds is less than 7
        while Raised and roundCount < 7:
            roundCount += 1

            # Run over each player for betting
            Raised = False
            for idx, player in enumerate(self.players):
                # skip if player not in
                if self.stillIn[idx] is False:
                    continue
                # Compute min bet to stay
                minBetToStay = curMax - self.curBets[idx]

                # get player bet
                bet = player.chooseBet(
                    minBetToStay, curComCards, tuple(
                        self.curBets), idx)

                # If the bet is too small then they fold
                if bet < minBetToStay:
                    # They have not bet enough to stay in
                    self.stillIn[idx] = False
                else:
                    if roundCount == 6:
                        # If this is the final round then just set the bet to
                        # min bet
                        bet = minBetToStay

                    # If this is a raise then set the raised flag
                    if minBetToStay < bet:
                        Raised = True

                    # Update the bet
                    self.curBets[idx] += bet
                    # Set curMax to the new bet
                    curMax = self.curBets[idx]
        return

    def runEarlyEndGame(self):
        """
            Run the end game (cleaning up betting etc) for
            games where all but one player has folded
        """

        # All but one player is out then give all of the cash
        idx = 0
        for player, stillin, bet in zip(
                self.players, self.stillIn, self.curBets):
            if stillin:
                # If this player still in (won) 
                # compute and add profit
                self.profit[player.id_number] += sum(
                    self.curBets) - self.curBets[idx]
            else:
                # If this player not in (lost) 
                # compute and remove losses
                self.profit[player.id_number] -= self.curBets[idx]
            idx += 1

        # run cleanup
        self.__cleanup__()

    def runEndGame(self, run_display=False):
        """
            Run the end game (cleaning up betting etc) for
            games where at least two players are still in,
            need to evaluate the hands
        """
        # Get the list of all players who are still in
        players = [x for x, y in zip(self.players, self.stillIn) if y]

        # Find the best hand/results
        result = hand.findBestHands(self.communityCards, players)

        # Mark non winners as out
        winners = set([x.id_number for x in result])
        for idx, player in enumerate(self.players):
             if player.id_number not in winners:
                 self.stillIn[idx] = False

        if run_display:
            self.__printWinners__()

        # Remove bets
        for player, bet in zip(self.players, self.curBets):
            self.profit[player.id_number] -= bet

        # Add profits divided by number of winners
        toAdd = sum(self.curBets)/len(result)
        for item in result:
            self.profit[item.id_number] += toAdd

        # run cleanup
        self.__cleanup__()

    def __printBetting__(self,title):
        """
            Print the current state of betting
            between the individuals
        """
        print(title)
        for player in self.players:
            print(player.getName(), end=": ")
            print(self.curBets[player.id_number])

    def __printWinners__(self):
        """
            Print who won
        """
        whoWon = [x.getName() for x,y in zip(self.players,self.stillIn) if y]
        print('Game Finished as',whoWon," won")

    def runHand(self, run_display=False):
        """
            Run a single hand of poker

            Compute all of the profits and update all of the counts
        """

        # Lets run some set up
        # Place a 1 unit bet for each player
        self.curBets = [1 for x in self.players]
        self.stillIn = [True for x in self.players]

        # Reorder the players
        self.players = [self.players[-1], ] + self.players[:-1]

        # Reset the deck
        self.Deck.resetDeck()

        if run_display:
            print('Starting a hand:\n')

        # Deal cards

        # First card
        for player in self.players:
            player.takeCard(self.Deck.drawCard())
        # Second card
        for player in self.players:
            player.takeCard(self.Deck.drawCard())

        # Run initial betting round
        # No Small/Big Blind
        self.runBettingRound()


        if run_display:
            # Print Draw
            print('Draw:\n')
            for player in self.players:
                print(player.getName(), end=": ")
                for card in player.getCards():
                    print(card, end =", ")
                print('\n')

            # Print the betting results
            self.__printBetting__("Initial Betting")

        # Leave Game if only 1 player in
        if sum(1 for x in self.stillIn if x) == 1:
            if run_display:
                self.__printWinners__()
            self.runEarlyEndGame()
            return

        # Deal 3 cards (the flop)
        self.Deck.burnCard()
        for _ in range(3):
            self.communityCards.append(self.Deck.drawCard())
        if run_display:
            print('Flop: ',self.communityCards)

        # Run flop betting round
        self.runBettingRound()
        if run_display:
            self.__printBetting__("Flop Betting")

        # Leave Game if only 1 player in
        if sum(1 for x in self.stillIn if x) == 1:
            if run_display:
                self.__printWinners__()
            self.runEarlyEndGame()
            return

        # Deal 1 card (the turn)
        self.Deck.burnCard()
        self.communityCards.append(self.Deck.drawCard())
        if run_display:
            print('Turn: ',self.communityCards)

        # Run Turn betting round
        self.runBettingRound()
        if run_display:
            self.__printBetting__("Turn Betting")

        # Leave Game if only 1 player in
        if sum(1 for x in self.stillIn if x) == 1:
            if run_display:
                self.__printWinners__()
            self.runEarlyEndGame()
            return

        # Run River betting round
        self.Deck.burnCard()
        self.communityCards.append(self.Deck.drawCard())
        if run_display:
            print('River: ',self.communityCards)

        # Run River betting round
        self.runBettingRound()
        if run_display:
            self.__printBetting__("River Betting")

        # Leave Game if only 1 player in
        if sum(1 for x in self.stillIn if x) == 1:
            if run_display:
                self.__printWinners__()
            self.runEarlyEndGame()
            return

        self.runEndGame()

    def runGame(self, num, display=False):
        """
            Run a game i.e. a fixed number of hands
        """
        for idx in range(num):
            self.runHand(display)
        return
