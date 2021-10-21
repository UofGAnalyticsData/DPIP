

class playerBase:
    id_number = 0
    def __init__(self,name=None):
        self.cards = []
        self.id_number = playerBase.id_number
        playerBase.id_number += 1
        if name!=None:
            self.name = name
    def takeCard(self,card):
        self.cards.append(card)
    def getCards(self):
        return self.cards[:]
    def reset(self):
        self.cards = []

class player_bet1(playerBase):
    def chooseBet(self,minBetToStay,curComCards,curBets,idx):
        return max(1,minBetToStay)


class player_onlyHighCard(playerBase):
    def chooseBet(self,*args):
        nums = [x.getNumber() for x in self.cards]
        if nums[0] in ['10','Jack','Queen','King','Ace'] or nums[1] in ['10','Jack','Queen','King','Ace']:
                return max(1,minBetToStay)
        return 0
