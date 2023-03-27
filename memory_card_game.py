hidden = [1, 3, 3, 4, 2, 4, 2, 1]
state = ['closed' for x in range(len(hidden)) ]
# other states = open, tmp open
N = len(hidden)
active_game = True
found = 0
score = 0
score_lists = []


while active_game:
    score += 1
    #read 1st card
    first_position = int(input("Give 1st 'closed' position (0-8) : "))
    while first_position < 0 or first_position > N or state[first_position] == 'open':
        if first_position < 0 or first_position > N  :
            print('Out Of Bounds')
        else :
            print('Wrong State')
        first_position = int(input("Dialekse thn 1oh 'closed' 8esh (0-8) : "))

    #read 2nd card
    second_position = int(input("Give 2nd'closed' posistion (0-8) : "))
    while second_position < 0 or second_position > N or state[second_position] == 'open' \
                              or second_position == first_position :
        if second_position < 0 or second_position > N  :
            print('Out Of Bounds')
        elif second_position == first_position :
            print('You choose the same card...')
        else :
            print('Wrong State')
        second_position = int(input("Dialekse thn 2oh 'closed' 8esh (0-8) : "))

    #change the current state
    state[first_position] = 'tmp_open'
    state[second_position] = 'tmp_open'

    #print current_stage
    print('')
    for position in range(N):
        if state[position] == 'closed':
            print('_', end='')
        elif state[position] == 'open':
            print(hidden[position],end = '')

        else : #tmp open
            print(hidden[position],end = '')
    print('')

    if hidden[first_position] != hidden[second_position]:
        state[first_position] = 'closed'
        state[second_position] = 'closed'
        print('Whops.. Wrong')

    #check if positions are the same
    else :
        state[first_position] = 'open'
        state[second_position] = 'open'
        print('Success')
        found += 2
        if found == N :
                print(f'Bravo. Game finished. Your score is :{score}')
                score_lists.append(score)
                active_game = False

    #print current_stage
    print('')
    for position in range(N):
        if state[position] == 'closed':
            print('_', end='')
        elif state[position] == 'open':
            print(hidden[position],end = '')

        else : #tmp open
            print(hidden[position],end = '')
    print('')
