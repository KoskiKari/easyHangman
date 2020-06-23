import time, random, os, string

def menuLayout():
    #game's main menu   
    print(f'HANGMAN GAME ')
    print(f'  ____       ')
    print(f'/     |      ')
    print(f'|     O      ')
    print(f'|    -|-     ')
    print(f'|    / \     ')
    print(f'|            ')
    print(f' _________   ')
    print(f'|         |  ')
    print(f'|         |  ')
    while True:
        print(f'(N)ew game, random word')
        print(f'(E)asy mode, random word')
        print(f'(S)elect word yourself')
        print(f'(Q)uit game')
        option = input('Enter option: ')
        if option.lower() in ['n','s','e','q']:
            return option
        else:
            print('Invalid option')
            time.sleep(1)

def selectWord():
    #allow user to create their own word, require length higher than 2
    os.system('cls')
    while True:
        magic_word = input('Enter word to guess: ')
        #check word is atleast 2 chars, and contains only letters
        if len(magic_word) < 2 or not magic_word.isalpha():
            os.system('cls')
            print('Word needs length of 2 atleast')
            continue
        break
    return magic_word

def wordFromFile():
    #get random word from the textfile
    word_list = []
    with open('commonWords.txt','r') as f:
        for i in f:
            word_list.append(i.strip())
    magic_word = random.choice(word_list)
    return magic_word

def addLetters(current,magic_word):
    #easy_mode letter addition, random.sample half the length of the word
    #this has some problems with words that have many duplicate letters
    letters = random.sample(magic_word,len(magic_word)//2)
    for letter in letters:
        indices = [pos for pos, char in enumerate(magic_word) if char == letter]
        for position in indices:
                current[position] = letter.lower()
    return current

def drawHangman(count,figure):
    #after initial draw, start adding body parts
    if count > 0:
        parts = ['O','|','-','-','/','\\']
        figure[count-1] = parts[count-1]
    print(f'  ____                                 ')
    print(f'/     |                                ')
    print(f'|     {figure[0]}                      ')
    print(f'|    {figure[2]}{figure[1]}{figure[3]} ')
    print(f'|    {figure[4]} {figure[5]}           ')
    print(f'|                                      ')
    print(f' _________                             ')
    print(f'|         |                            ')
    print(f'|         |                            ')
    return figure

def game(magic_word,easy_mode):
    #create variables needed for game, add letters to word if easy mode
    count = 0
    figure =['', ' ' , ' ', '', '' ,'']
    current = ['*' for i in range(len(magic_word))]
    already_guessed = []
    if easy_mode:
        current = addLetters(current,magic_word)

    #game loop
    while True:

        #input loop 
        while True:
            os.system('cls')
            drawHangman(count,figure)

            #print current status with list comprehension
            [print(char,end='') for char in current]

            #user input handling
            print(f'\nPrevious guesses: {already_guessed}')
            letter = input('Enter letter to guess:')
            if letter and letter not in already_guessed:
                already_guessed.append(letter)
                break

        #check if letter present in magic_word, fill correct positions
        if letter in magic_word:
            indices = [pos for pos, char in enumerate(magic_word) if char == letter]
            for position in indices:
                current[position] = letter.lower()

        #incorrect guess, add 1 count
        else:
            count += 1
            if count > 5:
                break

        #check if all letters have been guessed
        if '*' not in current:
            print(f'\n***** {magic_word} *****\n')
            print('Congratulations! You have won!')
            input('Press enter to continue.')
            return

    #after all guesses are used, loop breaks -> defeat message
    drawHangman(count,figure)
    print('\nOut of guesses!')
    print(f'Word was: {magic_word}')
    input('Press enter to continue.')

#main
while True:
    easy_mode = False
    os.system('cls')
    option = menuLayout()
    
    #set easy_mode flag and change to normal mode
    #TODO: easy flag in user selected word
    if option == 'e':
        option = 'n'
        easy_mode = True

    #run correct mode
    if option.lower() == 's':
        magic_word = selectWord()
    elif option.lower() == 'n':
        magic_word = wordFromFile()
    elif option.lower() == 'q':
        print('Thanks for playing')
        break

    #if somehow option other than predetermined is introduced, end loop
    else:
        print('Unexpected error')
        break

    game(magic_word,easy_mode)