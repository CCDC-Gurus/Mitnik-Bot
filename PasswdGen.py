## PasswdGen
## Password generator for CCDC. Should be good enough.
## Gavin Lewis - 2019

import random



def gen_password(num_words = 3):
    """Generate the password
    
    num_words: The number of words to use in the password
    """
    SPECIALS = ['!','@','#','$','%','&','*']
    
    passwd = ""
    
    # Randomly grab num_words number of words
    with open("words.txt", "r") as word_file:
        word_list = word_file.readlines()
        random.shuffle(word_list)
        words = word_list[0:num_words]

    # Prepend special character
    passwd += SPECIALS[random.randint(0,len(SPECIALS)-1)]
    
    for word in words:
        # Add each word, capitalize first letter, lower the rest, strip the newline
        passwd += word[0].upper() + word[1:].strip().lower()
    
    # Append random 2 digit number
    passwd += str(random.randint(10,100))
    
    return passwd


if __name__ == "__main__":
    print(gen_password())

