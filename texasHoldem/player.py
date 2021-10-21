

class playerBase:
    id_number = 0
    def __init__(self):
        self.cards = []
        self.id_number = playerBase.id_number
        playerBase.id_number += 1
    def takeCard(self,card):
        self.cards.append(card)
    def getCards(self):
        return self.cards[:]
    def reset(self):
        self.cards = []

class player_bet1(playerBase):
    def chooseBet(self,*args):
        return 1


class player_onlyHighCard(playerBase):
    def chooseBet(self,*args):
        nums = [x.getNumber() for x in self.cards]
        if nums[0] in ['10','Jack','Queen','King','Ace'] or nums[1] in ['10','Jack','Queen','King','Ace']:
                return 1
        return 0
