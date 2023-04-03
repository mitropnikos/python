"""
A simplified verstion
"""

from random import randrange

score = [
    {
        "ones": -1,
        "twos": -1,
        "threes": -1,
        "fours": -1,
        "fives": -1,
        "sixes": -1
    },
    {
        "ones": -1,
        "twos": -1,
        "threes": -1,
        "fours": -1,
        "fives": -1,
        "sixes": -1
    }
]


def roll_dice(roll):
    dice_rolls = []
    for i in range(roll) :
        dice = randrange(1, 6+1)
        dice_rolls.append(dice)
    return sorted(dice_rolls)


def player_turn():
    dices_rolling = 5
    dices_kept = []

    for roll in range(3):
        dice = roll_dice(dices_rolling)
        print("-" * 15)
        print(f"Roll {roll+1}!")
        if roll in range(2):
            while True:
                print(f"Your Dice is : {dice}")
                choice = input("Keep a die or no? (Type the dice or 'n') : ")
                if choice == 'n':
                    break
                elif int(choice) not in dice:
                    print(f"No {choice} in dice")
                else :
                    dices_rolling -= 1
                    dice.remove(int(choice))
                    dices_kept += [int(choice)]

        else :
            dices_kept += dice

    print(f"Your dice is : {dices_kept}")
    return dices_kept


def text_to_numbers(s):
    if s == "ones":
        return  1
    elif s == "twos":
        return 2
    elif s == "threes":
        return 3
    elif s == "fours":
        return 4
    elif s == "fives":
        return 5
    elif s == "sixes":
        return 6


def player_picks(player, dice):
    print("You can store your dice as : ", end=', ')
    picks = []
    for key, val in score[player].items():
        if val == -1:
            print(key, end=', ')
            picks += [key]

    while True:
        choise = input("Type your choice : ")
        if choise not in picks:
            print("Wrong Choise..")
            continue
        else :
            key_val = text_to_numbers(choise)
            score[player][choise] = dice.count(key_val) * key_val
            return


def print_card(player):
    print(f"Player : {player} Card")
    if score[player]["ones"] == -1:
        print("ones : ")
    else:
        print(f"ones: {score[player]['ones']}")

    if score[player]["twos"] == -1:
        print("twos: ")
    else:
        print(f"twos: {score[player]['twos']}")

    if score[player]["threes"] == -1:
        print("threes: ")
    else:
        print(f"threes: {score[player]['threes']}")

    if score[player]["fours"] == -1:
        print("fours: ")
    else:
        print(f"fours: {score[player]['fours']}")

    if score[player]["fives"] == -1:
        print("fives: ")
    else:
        print(f"fives: {score[player]['fives']}")

    if score[player]["sixes"] == -1:
        print("sixes: ")
    else:
        print(f"sixes: {score[player]['sixes']}")


def calculated_score(player):
    return sum(score[player].values())


def main():

    for round in range(1,6+1):
        print("-" * 20)
        print(f"Round : {round}!")
        print("-" * 20)
        for player in range(2):
            print(f"Player {player + 1} Plays")
            print("-" * 15)
            print_card(player)
            print("-" * 15)
            dice = player_turn()
            player_picks(player, dice)

    print()
    #p1
    print_card(0)
    score1 = calculated_score(0)
    print(f"Score Player1 is {score1}")

    #p2
    print_card(1)
    score2 = calculated_score(1)
    print(f"Score Player2 is {score2}")

    if score1 > score2:
        print('Player1 Winds')
    elif score1 == score2 :
        print('Tie')
    else :
        print("Player2 Wins")



if __name__ == '__main__':
    main()
