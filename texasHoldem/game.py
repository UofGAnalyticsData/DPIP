from DPIP.texasHoldem import cards
from DPIP.texasHoldem import hand 
import random as rd


class Game:
    def __init__(self,players):
        self.players = players[:]
        self.playersOrig = players[:]
        self.Deck = cards.Deck()
        self.profit = {x.id_number:0 for x in players}
        self.__cleanup__()
    def getProfitByPlayer(self):
        id2player = {x.id_number:x for x in self.players}
        return {id2player[x]:y for x,y in self.profit}
        
    def getProfitByName(self):
        id2name = {}
        for x in self.players:
            if hasattr(x,'name'):
                id2name[x.id_number] = x.name 
            else:
                id2name[x.id_number] = x.id_number 
        return {id2name[x]:y for x,y in self.profit}
        
    def __cleanup__(self):
        self.communityCards = []
        self.curBets = [None for x in self.players]
        self.stillIn = [None for x in self.players]
        self.Deck.resetDeck()
        for player in self.players:
            player.reset()
        
    def runBettingRound(self):
        curComCards = tuple(self.communityCards)
        curMax = max(self.curBets)
        noRaise = True
        roundCount = 0
        while noRaise and roundCount<6:
            roundCount += 1

            noRaise = False
            for idx,player in enumerate(self.players):
                if self.stillIn[idx] == False:
                    continue
                minBetToStay = curMax - self.curBets[idx]
                bet = player.chooseBet(minBetToStay,curComCards,tuple(self.curBets),idx)
                if bet < minBetToStay:
                    # They have not bet enough to stay in
                    self.stillIn[idx] = False
                else:
                    if minBetToStay > bet:
                        noRaise = False
                    self.curBets[idx] += bet
                    curMax = self.curBets[idx]
        return 
    def runEarlyEndGame(self):
        ## all but one player is out then give all of the cash
        idx = 0
        for player,stillin,bet in zip(self.players,self.stillIn,self.curBets):
            if stillin:
                self.profit[player.id_number] = sum(self.curBets) - self.curBets[idx]
            else:
                self.profit[player.id_number] -= self.curBets[idx]
            idx += 1
            
    def runEndGame(self):
        players = [x for x,y in zip(self.players,self.stillIn) if y]
        result = hand.findBestHands(self.communityCards,players)
        # Remove bets
        idx = 0
        for player,bet in zip(self.players,self.curBets):
            self.profit[player.id_number] -= self.curBets[idx]
            idx += 1
        # add profits
        toAdd = sum(self.curBets)/len(result)
        for item in result:
            self.profit[item.id_number] += toAdd
        
        # run cleanup
        self.__cleanup__()
        
    def runHand(self):
        # Lets run some set up
        self.curBets = [1 for x in self.players]
        self.stillIn = [True for x in self.players]
        
        # reorder the players
        self.players = [self.players[-1],] + self.players[:-1]


        # Reset the deck
        self.Deck.resetDeck()
        
        # Deal cards
        
        # first card
        for player in self.players:
            player.takeCard(self.Deck.drawCard())
        # Second card
        for player in self.players:
            player.takeCard(self.Deck.drawCard())
        
        # Run inital betting round
        # No Big Blind as that is hard
        self.runBettingRound()
        if sum(1 for x in self.stillIn if x)==1:
            self.runEarlyEndGame()
        
        # First 3 cards
        self.Deck.burnCard()
        for _ in range(3):
            self.communityCards.append(self.Deck.drawCard())
        
        self.runBettingRound()
        if sum(1 for x in self.stillIn if x)==1:
            self.runEarlyEndGame()
            return
            
        # Next card  
        self.Deck.burnCard()
        self.communityCards.append(self.Deck.drawCard())
        self.runBettingRound()
        if sum(1 for x in self.stillIn if x)==1:
            self.runEarlyEndGame()
            return

            
        # Final card  
        self.Deck.burnCard()
        self.communityCards.append(self.Deck.drawCard())
        self.runBettingRound()
        if sum(1 for x in self.stillIn if x)==1:
            self.runEarlyEndGame()
            return
        
        self.runEndGame()

    def runGame(self,num):
        for idx in range(num):
            self.runHand()
        return
        
        
        
