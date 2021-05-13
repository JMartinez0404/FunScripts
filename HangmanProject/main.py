import random
import string
import sqlite3


def main():
    # opens up database and creates a cursor
    con = sqlite3.connect('hangmandb.db')
    cur = con.cursor()
    # creates score table is it doesn't exist yet
    cur.execute('''CREATE TABLE IF NOT EXISTS stats(
                        name text NOT NULL,
                        games_won integer NOT NULL,
                        games_lost integer NOT NULL,
                        total_games integer NOT NULL
                );''')

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
    # check is player is in database or not
    name = ''
    name = input('What is your name? ')
    name = name.lower()
    name_handled = False
    for row in cur.execute('SELECT * FROM stats'):
        if name in row:
            stats_tup = cur.execute(f'''SELECT games_won, games_lost, total_games FROM stats
                                    WHERE name = \'{name}\'''').fetchall()[0]
            print(f'Found your name! Your stats will be saved to {name.upper()}')
            print(f'''      {name.upper()}\'s CURRENT STATS:
            Games Won: {stats_tup[0]}
            Games Lost: {stats_tup[1]}
            Total Games Played: {stats_tup[2]}
            Win Percentage: %{stats_tup[0] / stats_tup[2] * 100}''')
            name_handled = True
            break
    if name_handled is False:
        print(f'No name found. Creating new user {name.upper()}')
        cur.execute(f'INSERT INTO stats VALUES (\'{name}\', 0, 0, 0);')

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
                        if guess.isalpha() and len(guess) == 1:
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
        score = ''
        if all(word_bools):
            print('YOU WIN!!')
            playing = False
            cur.execute(f'''UPDATE stats
                            SET games_won = games_won + 1,
                                total_games = total_games + 1
                            WHERE name = \'{name}\';''')
            stats_tup = cur.execute(f'''SELECT games_won, games_lost, total_games FROM stats
                                                WHERE name = \'{name}\'''').fetchall()[0]
            print(f'''      {name.upper()}\'s NEW STATS:
                        Games Won: {stats_tup[0]}
                        Games Lost: {stats_tup[1]}
                        Total Games Played: {stats_tup[2]}
                        Win Percentage: %{stats_tup[0] / stats_tup[2] * 100}''')
        elif tries >= difficulties[difficulty]:
            print('You\'ve run out of tries. YOU LOSE.')
            print(f'The word was: {word_chars}\n')
            playing = False
            cur.execute(f'''UPDATE stats
                            SET games_lost = games_lost + 1,
                                total_games = total_games + 1
                            WHERE name = \'{name}\';''')
            stats_tup = cur.execute(f'''SELECT games_won, games_lost, total_games FROM stats
                                                WHERE name = \'{name}\'''').fetchall()[0]
            print(f'''      {name.upper()}\'s NEW STATS:
                        Games Won: {stats_tup[0]}
                        Games Lost: {stats_tup[1]}
                        Total Games Played: {stats_tup[2]}
                        Win Percentage: %{stats_tup[0] / stats_tup[2] * 100}''')
    con.commit()
    con.close()


if __name__ == '__main__':
    main()
