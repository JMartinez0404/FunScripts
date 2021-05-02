import random
import string
# THINGS TO DO
# - keep track of guess ratio using people's name

def main():
    # opens file and checks length
    file = open('hangmanwords.txt', 'rt')
    file_length = 0
    for line in file:
        file_length += 1
    file.close()

    # reopens file to reset line position and chooses random word
    file = open('hangmanwords.txt', 'rt')
    r = random.randint(1, file_length)
    word_chars = ''
    cnt = 1
    while cnt <= r:
        word_chars = next(file).rstrip()
        cnt += 1

    # fills boolean list
    word_bools = []
    for i in word_chars:
        word_bools.append(False)

    # creates list of alphas
    letters = tuple(string.ascii_lowercase)
    # creates boolean list for alpha list
    letters_used = []
    for i in letters:
        letters_used.append(False)

    '''start of the game'''
    playing = True
    tries = 0
    print('_______Welcome to HANGMAN!_______')
    difficulties = {'1': 20, '2': 15, '3': 10, '4': 5}
    difficulty = input('''
        1 - EASY (20 tries)
        2 - NORMAL (15 tries)
        3 - HARD (10 tries)
        4 - MASTER (5 tries)
        Select a difficulty: 
        ''')
    while playing:
        tries += 1
        print(f'Number of tries: {tries}/{difficulties[difficulty]}')
        # print out which letters have been guessed correctly
        for i, b in enumerate(word_bools):
            if b:
                print(word_chars[i], end=' ')
            else:
                print('_', end=' ')
        print()

        print('''
        1 - Guess a letter
        2 - Guess the word (counts as 1 try)
        3 - Show letters that have been used
        ''')

        # selection loop
        selection_not_valid = True
        guess = ''
        while selection_not_valid:
            selection = input('What would you like to do? ')
            if selection.isnumeric():
                if int(selection) == 1:
                    selection_not_valid = False

                    # check if guess is valid
                    not_valid_guess = True
                    while not_valid_guess:
                        guess = input('Guess a letter: ')
                        if guess.isalpha():
                            if letters_used[letters.index(guess)] is False:
                                not_valid_guess = False
                            else:
                                print('That letter has been used already :(')
                        else:
                            print('You did not enter a letter :(')
                elif int(selection) == 2:
                    selection_not_valid = False
                    guess_word = input('What do you think the word is: ')
                    if guess_word == word_chars:
                        for i, b in enumerate(word_bools):
                            word_bools[i] = True
                    else:
                        print('Sorry that wasn\'t the word')
                elif int(selection) == 3:
                    # shows letters or not
                    for i, b in enumerate(letters_used):
                        if b:
                            print(letters[i], end=' ')
                        else:
                            print('_', end=' ')
                    print('\n')
                else:
                    print('You did not choose a valid option.')
            else:
                print('You did not enter a number :(')

        # changes boolean to True if guess is in the word
        for i, char in enumerate(word_chars):
            if char == guess:
                word_bools[i] = True

        # marks which letters have been used already
        for i, l in enumerate(letters):
            if guess == l:
                letters_used[i] = True

        # check if all letters have been guess correctly or if no tries are left
        if all(word_bools):
            print('YOU WIN!!')
            playing = False
        elif tries >= difficulties[difficulty]:
            print('You\'ve run out of tries. YOU LOSE.')
            print(f'The word was: {word_chars}\n')
            playing = False


if __name__ == '__main__':
    main()
