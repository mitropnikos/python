from random import randrange

species = ('heart', 'diamond', 'spade', 'club')
numbers = (2,3,4,5,6,7,8,9,10,'jack', 'queen', 'king', 'ace')
deck = {(kind, number) for kind in species for number in numbers}

def player_hands(name, cnt):
    numbers_sum = 0
    cards = set()
    #hand
    for _ in range(cnt):
        card = deck.pop()
        cards.add(card)

    #cards number convertion
    for figure, card in cards:
        number = card

        if number == 'king' or number == 'queen' or number == 'jack':
            numbers_sum += 10
        elif number == 'ace':
            choise = input("Convert Ace to 1 or 11 : ")
            while choise not in ["1", "11"]:
                choise = input("Convert Ace to 1 or 11 : ")
            numbers_sum += int(choise)
        else :
            numbers_sum += number

    print()
    return cards, numbers_sum



def pick_card(name):
    count = []
    cards, numbers_sum = player_hands(name, 2)
    print(f"{name} initial hand is {cards} and the sum of them is {numbers_sum}")
    count.append(numbers_sum)

    active_game = True
    while active_game:
        card_choise = input("Pick a card? [y/n] : ").lower().strip()
        while card_choise not in ["y", "n"]:
            card_choise = input("Please choose [y/n] : ")

        if card_choise == "y":
            cards, number = player_hands(name, 1)
            print(f"{name} drew {cards} and got {number}")
            count.append(number)
            print(f"{name} has a sum of {sum(count)}")

            if sum(count) == 21:
                active_game = False
                print(f"{name} won")
                break
            elif sum(count) >= 22:
                active_game = False
                print(f"{name} lost")
            else :
                continue

        elif card_choise == "n":
            active_game = False
            break

    if not active_game:
        print(f"{name} total count is {sum(count)}")
        return {sum(count)}


def reset():
    global deck
    global p1
    global p2
    p1 = []
    p2 = []

    deck = {(kind, number) for kind in species for number in numbers}
    p1, _ = player_hands('player', 2)
    p2, _ = player_hands('pc', 2)

def turn():

    global score
    print(f"Player Score : {score[0]}. PC Score : {score[1]}")

    p1 = pick_card('player')
    p1 = list(p1) # returned sum
    if p1[0] > 22 :
        print('You lose')
        score[1] += 1

    else :
        p2 = pick_card('pc')
        p2 = list(p2)

        if p2[0] == 21:
            print('PC won')
            score[1] += 1

        elif p2[0] >= p1[0]:
            print('PC won')
            score[1] += 1
        else:
            print('Player won')
            score[0] += 1

def main():
    global score
    score = [0,0]
    while True:

        turn()
        choice = input("Do you want to continue playing? [y/n]: ").lower()
        while choice not in ["y", "n"]:
            choice = input("Please choose [y/n] : ").lower()

        if choice == "y":
            print("Dealing a new Round\n")
            reset()
        if choice == "n":
            print('Game Stoped')
            break

if __name__ == '__main__':
    main()
