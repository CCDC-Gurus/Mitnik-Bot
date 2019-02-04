## PasswdGen
## Password generator for CCDC. Should be good enough.
## Gavin Lewis - 2019

import random



def get_rand_arr(num,MAX):
    num_list = []
    cnt = 0
    for x in range(num):
        flag = True
        while flag:
            new_rand = random.randint(0,MAX-1)
            if not (new_rand in num_list):
                num_list.append(new_rand)
                flag = False
                
    return num_list

def count_words():
    with open("words.txt","r") as file:
        cnt = 0
        for line in file:
            cnt += 1
            
    return cnt

def gen_password(num_words = 3):
    SPECIALS = ['!','@','#','$','%','&','*']
    MAX_WORDS = count_words()
    
    passwd = ""
    #num_words = 3 # Num words in password
    
    num_list = get_rand_arr(num_words, MAX_WORDS) # Decide words to use
    
    passwd += SPECIALS[random.randint(0,len(SPECIALS)-1)] # Prepend symbol
    
    with open("words.txt","r") as file:
        cnt = 0
        while cnt < MAX_WORDS:
            line = file.readline()
            if cnt in num_list:
                passwd += line[0].upper() + line[1:-1].lower()
            cnt += 1
    
    passwd += str(random.randint(10,100))
    
    return passwd


if __name__ == "__main__":
    print(gen_password())

