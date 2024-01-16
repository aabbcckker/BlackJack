import sys , random

# 花色
Hearts = chr(9829)
Diamonds = chr(9830)
Spades = chr(9824)
Clubs = chr(9827)

BACKSIDE = 'backside'
def getBet(maxBet):
    while True:
        print("确定本轮的赌资：(1-{},or Quit)".format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'Quit':
            sys.exit()

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
    #方便实现摸牌，分牌的操作
    deck =[]
    for suit in (Hearts,Diamonds,Spades,Clubs):
        for rank in range(2,11):
            deck.append((str(rank),suit))
        for rank in ('J','Q','K','A'):
            deck.append((rank,suit))
    #打乱牌堆
    random.shuffle(deck)
    return deck

# 计算手牌大小
def getHandValue(cards):
    value = 0
    numberOfAces = 0   # 'A'的数量，特殊卡特殊对待

    for card in cards:
        rank = card[0]

        if rank == 'A':
            numberOfAces += 1
        elif rank in ('J','Q','K'):
            value += 10
        else:
            value += int(rank)

    value += numberOfAces
    for i in range(numberOfAces):
        if value + 10 <= 21:
            value += 10

    return value

def displayHands(playerhand,dealerhand,showdealerhand):
    print()
    if showdealerhand:
        print('Dealer:',getHandValue(dealerhand))
        displayCards(dealerhand)
    else:
        print('Dealer:???')
        displayCards([BACKSIDE] + dealerhand[1:])

    print('Player:',getHandValue(playerhand))
    displayCards(playerhand)



def displayCards(cards):
    # 通过遍历的方式展示卡牌
    rows = ['','','',''] #牌顶，左上角数，花色，右下角数
    for i,card in enumerate(cards):
        rows[0] += ' ___ '
        if card == BACKSIDE:
            rows[1] += '|## |'
            rows[2] += '|###|'
            rows[3] += '|_##|'
        else:
            rank,suit = card
            rows[1] += '|{} |'.format(rank.ljust(2))
            rows[2] += '| {} |'.format(suit)
            rows[3] += '|_{}|'.format(rank.rjust(2,'_'))

    for row in rows:
        print(row)


def getMove(playerhand,money):
    while True:
        moves = ['(H)it','(S)tand']

        if len(playerhand) == 2 and money > 0:
            moves.append('(D)ouble down')

        movePrompt = ','.join(moves) + '>'
        move = input(movePrompt).upper()

        if move  in ('H','S'):
            return move
        if move == 'D' and '(D)ouble down' in moves:
            return move


def main():
    #初始本金
    money = 5000

    while True:
        if money == 0:
            print('You have lost all the money')
            sys.exit()

        print('Money: ',money)
        # 确定赌资,传入值为最大赌资，不得超过本金
        bet = getBet(money)
        # 获取卡牌
        deck = getDeck()
        #庄家拿牌
        dealerhand = [deck.pop(),deck.pop()]
        #玩家拿牌
        playerhand = [deck.pop(),deck.pop()]


    #   处理Player的操作
        print('Bet:',bet)
        while True:
            displayHands(playerhand,dealerhand,False)
            print()
            # 爆仓
            if getHandValue(playerhand) > 21:
                break

            move = getMove(playerhand,money - bet)

            if move == 'D':
                additionalBet = getBet(min(bet,(money-bet)))
                bet += additionalBet
                print('赌资增加到{}'.format(bet))
                print('Bet:',bet)

            if move in ('H','D'):
                newCard = deck.pop()
                rank,suit = newCard
                print('You drew a {} of {}'.format(rank,suit))
                playerhand.append(newCard)
                # 摸到第三张后重新检测是否爆仓
                if getHandValue(playerhand) > 21:
                    continue

            if move in ('S','D'):
                break
#       处理Dealer操作
        if getHandValue(playerhand) <= 21:
            while getHandValue(dealerhand) < 17:
                print('Dealer hits...')
                dealerhand.append(deck.pop())
                displayHands(playerhand,dealerhand,False)

                if getHandValue(dealerhand) > 21:
                    break
                input('Press Enter to continue...')
                print()
                print()
        displayHands(playerhand,dealerhand,True)

        playerValue = getHandValue(playerhand)
        dealerValue = getHandValue(dealerhand)

        if dealerValue > 21:
            print('Dealer busts! You win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif (playerValue == dealerValue) or ((playerValue > 21) and (dealerValue > 21)):
            print('It\'s a tie')

        print('Press Enter to continue...')
        print()
        print()

if __name__ == '__main__':
    main()