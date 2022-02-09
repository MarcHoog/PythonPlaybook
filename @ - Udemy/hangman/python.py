import random
import os
from hangman import hangman_drawing


def cls():
    os.system('cls' if os.name=='nt' else 'clear')
     
def generate_hangman_string(mystery_word,correct_letters):
    hm_string = ''
    
    for l in mystery_word:
        if l in correct_letters:
            hm_string += l
        else:
            hm_string += '_'
    
    return ' '.join(hm_string)

def generate_hangman_drawing(wrong_letters):
    stage = len(wrong_letters) 
    return hangman_drawing.art[stage]

def game(words):
    mystery_word = random.choice(words)
    
    wrong_letters = []
    correct_letters = []
    
    lives = 6
    
    while True:
        cls()
        print(generate_hangman_drawing(wrong_letters))
        print('\n\n\n')
        print(generate_hangman_string(mystery_word,correct_letters))
        print(wrong_letters)
        
        # Checks the input if it's correct or duped
        while True:
            l = input("Give my your letter!...  ")
            if len(l) > 1:
                print("letter cannot be bigger then one!")
                continue
            elif l in wrong_letters or l in correct_letters:
                print("letters cannot be used already")
                continue
            else:
                break
            
        if l in mystery_word:
            correct_letters.append(l)
            if set(mystery_word) == set(correct_letters):
                cls()
                print(f'Concratz you guessed the word was:  {mystery_word}')
                return True
        else:
            wrong_letters.append(l)
            if len(wrong_letters) == 6:
                cls()
                print(f'You have lost the word was {mystery_word}!')
                return False
            
    

if __name__ == "__main__":
    words = ['boner','boobs','bigdick','biggerdick']
    result = game(words)
                
            
        
        
    
    

    
    

        
            

        
        
        
            
        
           
                
                    
                
                
        
        
        
        

                
        
                
        
