import random
import sys
import os

def get_total_chars(data):
    return len(data)

def get_characters_probability(data):
    characters = {}
    total_chars = get_total_chars(data)
    for i in range(total_chars):
        if data[i] not in characters:
            characters.update({data[i]: 1})
        else:
            characters[data[i]] += 1
    for elem in characters:
        characters[elem] = characters[elem]/total_chars
    characters = dict(sorted(characters.items(), key=lambda item: item[1], reverse=True))
    # print("Characters prob: ")
    # print(characters)
    return characters


def starting_chars(text):
    starting_chars = {}
    for i in range(len(text)):
        if text[i] == ' ':
            try:
                if text[i+1] not in starting_chars:
                    starting_chars.update({text[i+1]: 1})
                else:
                    starting_chars[text[i+1]] += 1
            except:
                pass
    total_chars = sum(starting_chars.values())
    for elem in starting_chars:
        starting_chars[elem]=starting_chars[elem]/total_chars
    starting_chars = dict(sorted(starting_chars.items(), key=lambda item: item[1], reverse=True))
    #print("Starting characters prob: ")
    #print(starting_chars)
    return starting_chars

def first_markov(text):
    markov = {}
    for i in range(len(text)-1):
        if text[i] not in markov:
            markov.update({text[i]: {text[i+1]: 1}})
        else:
            if text[i+1] not in markov[text[i]]:
                markov[text[i]].update({text[i+1]: 1})
            else:
                markov[text[i]][text[i+1]] += 1
    for elem in markov:
        total = sum(markov[elem].values())
        for elem2 in markov[elem]:
            markov[elem][elem2] = markov[elem][elem2]/total
    markov_sorted = {}
    for elem in sorted(markov):
        markov_sorted.update({elem: sorted(markov[elem].items(), key=lambda item: item[1], reverse=True)})

    # print("Markov 1: ")
    # print(markov_sorted)
    return markov_sorted

def n_markov(text, n):
    markov = {}
    for i in range(len(text)-n):
        if text[i:i+n] not in markov:
            markov.update({text[i:i+n]: {text[i+n]: 1}})
        else:
            if text[i+n] not in markov[text[i:i+n]]:
                markov[text[i:i+n]].update({text[i+n]: 1})
            else:
                markov[text[i:i+n]][text[i+n]] += 1
    for elem in markov:
        total = sum(markov[elem].values())
        for elem2 in markov[elem]:
            markov[elem][elem2] = markov[elem][elem2]/total
    markov_sorted = {}
    for elem in sorted(markov):
        markov_sorted.update({elem: sorted(markov[elem].items(), key=lambda item: item[1], reverse=True)})
    # print("Markov: ")
    # print(markov)
    return markov_sorted

def generate(length, starting_set, first_markov, text, n):
    custom_markov = n_markov(text, n)
    result = 'start '
    previous = ''
    last_word = ''

    if n >= 2:
        for i in range(length):
            previous = result[-1]
            last_word = result[-n:]
            if previous == '':
                result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
            elif last_word not in custom_markov.keys():
                if len(first_markov[previous]) > 1:
                    next_word = first_markov[previous][random.randint(0, 1)][0]
                else:
                    next_word = first_markov[previous][0][0]
                result += next_word
            elif last_word in custom_markov.keys():
                if len(custom_markov[last_word]) > 1:
                    next_word = custom_markov[last_word][random.randint(0, 1)][0]
                else:
                    next_word = custom_markov[last_word][0][0]
                result += next_word
    elif n == 0:
        characters = get_characters_probability(text)
        for i in range(length):
            result += random.choice(list(characters.keys()))
    elif n == 1:
        characters = get_characters_probability(text)
        for i in range(length):
            previous = result[-1]
            if previous == '':
                result += random.choices(list(characters.keys()), list(characters.values()))[0]
            elif previous not in characters.keys():
                next_word = random.choices(list(characters.keys()), list(characters.values()))[0]
                result += next_word
            elif previous in characters.keys():
                next_word = random.choices(list(characters.keys()), list(characters.values()))[0]
                result += next_word
    return result

def main():
    n = int(sys.argv[1])
    file = sys.argv[2]
    file_out = sys.argv[3]
    length = int(sys.argv[4])
    text = ''

    with open(str(file), mode='r', encoding='ANSI') as f:
        for line in f.readlines():
            text += line
    f.close()

    starting_chars_set = starting_chars(text)
    first_markov_set = first_markov(text)
    
    result = generate(length, starting_chars_set, first_markov_set, text, n)
    if not os.path.exists('out'):
        os.makedirs('out')

    with open('out/%s' % str(file_out), mode='w', encoding='ANSI') as f:
        f.write(result)

if __name__ == '__main__':
    main()