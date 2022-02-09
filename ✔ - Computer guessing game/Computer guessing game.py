import random
import math

Max = int(10000)
Low = int(1)


def random_game():
    human_number = int(input('Gimme a number BIIIG BOii'))
    counter = 0
    cpu_highest_guess = Max
    cpu_lowest_guess = Low
    cpu_number = random.randint(cpu_lowest_guess, cpu_highest_guess)

    while cpu_number != human_number:

        print(f'The computer geussed the number {cpu_number}')
        if human_number < cpu_number:
            print(f'Je number was kleiner dan wat de computer in gedachten had ')

            cpu_highest_guess = cpu_number - 1
            cpu_number = random.randint(cpu_lowest_guess, cpu_highest_guess)

            print(f'laagste gues mogelijk: {cpu_lowest_guess} de hoogste guess mogelijk {cpu_highest_guess} \n')
        else:
            print(f'Je number was Groter dan wat de computer in gedachten had ')

            cpu_lowest_guess = cpu_number + 1
            cpu_number = random.randint(cpu_lowest_guess, cpu_highest_guess)

            print(f'laagste gues mogelijk: {cpu_lowest_guess} de hoogste guess mogelijk {cpu_highest_guess} \n')

        counter += 1
    else:
        print(f'The computer guessed your number it was {cpu_number}\n'
              f'It took the computer {counter} amount of turns to guess')


def divider_game(Max: int, Low: int):
    human_number = int(input('Gimme a number BIIIG BOii  '))
    counter = 0

    cpu_number = Max / 2
    print(f'I Guess {cpu_number}')
    input()

    while human_number != cpu_number:
        if human_number < cpu_number:
            Max = cpu_number - 1
            print(f'I guessed to high')
            print(f'De range is nu {Low} - {Max}')

            cpu_number = math.floor(Low + ((Max - Low) / 2))

            counter += 1

            print(f'ROUND: {counter}')
            print(f'I Guess {cpu_number}')

            input()

        else:
            Low = cpu_number + 1
            print('I guessed to low')
            print(f'De range is nu {Low} - {Max}')

            cpu_number = math.floor(Low + ((Max - Low) / 2))

            counter += 1

            print(f'ROUND: {counter}')
            print(f'I Guess {cpu_number}')
            input()



random_game()
