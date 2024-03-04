import random

def get_total_chars(data):
    return len(data[0])


def get_characters(data):
    characters = {}
    for c in data[0]:
        if c not in characters:
            characters.update({c: 1})
        else:
            characters[c] += 1
    total_chars = get_total_chars(data)
    for elem in characters:
        characters[elem]=characters[elem]/total_chars
    characters = dict(sorted(characters.items(), key=lambda item: item[1], reverse=True))
    #print("Characters prob: ")
    #print(characters)
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
    #print("Markov: ")
    #print(markov)
    return markov

def third_markov(text):
    markov = {}
    for i in range(len(text)-3):
        if text[i:i+3] not in markov:
            markov.update({text[i:i+3]: {text[i+3]: 1}})
        else:
            if text[i+3] not in markov[text[i:i+3]]:
                markov[text[i:i+3]].update({text[i+3]: 1})
            else:
                markov[text[i:i+3]][text[i+3]] += 1
    for elem in markov:
        total = sum(markov[elem].values())
        for elem2 in markov[elem]:
            markov[elem][elem2] = markov[elem][elem2]/total
    # print("Markov: ")
    # print(markov)
    return markov

def fith_markov(text):
    markov = {}
    for i in range(len(text)-5):
        if text[i:i+5] not in markov:
            markov.update({text[i:i+5]: {text[i+5]: 1}})
        else:
            if text[i+5] not in markov[text[i:i+5]]:
                markov[text[i:i+5]].update({text[i+5]: 1})
            else:
                markov[text[i:i+5]][text[i+5]] += 1
    for elem in markov:
        total = sum(markov[elem].values())
        for elem2 in markov[elem]:
            markov[elem][elem2] = markov[elem][elem2]/total
    #print("Markov: ")
    #print(markov)
    return markov

def generate(length, character_set, starting_set, first_markov, third_markov, fith_markov):
    result = ''
    previous = ''
    last_word = ''
    for i in range(length):
        last_word = result.split(' ')[-1]
        if previous == '':
            result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
        else:
            if len(last_word) < 3:
                try:
                    result += random.choices(list(first_markov[previous].keys()), list(first_markov[previous].values()))[0]
                except:
                     result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
            elif len(last_word) < 5:
                try:
                    result += random.choices(list(third_markov[last_word[-3::1]].keys()), list(third_markov[last_word[-3::1]].values()))[0]
                except:
                    result += random.choices(list(first_markov[previous].keys()), list(first_markov[previous].values()))[0]
            elif len(last_word) >= 5:
                try:
                    result += random.choices(list(fith_markov[last_word[-5::1]].keys()), list(fith_markov[last_word[-5::1]].values()))[0]
                except:
                    try:
                        result += random.choices(list(third_markov[last_word[-3::1]].keys()), list(third_markov[last_word[-3::1]].values()))[0]
                    except:
                        try:
                            result += random.choices(list(first_markov[previous].keys()), list(first_markov[previous].values()))[0]
                        except:
                            result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
        previous = result[-1]
    return result

def main():
    with open(file='resources/norm_hamlet.txt', mode='r') as f:
        text = f.readlines()
    f.close()
    characters_set = get_characters(text)
    starting_chars_set = starting_chars(text[0])
    first_markov_set = first_markov(text[0])
    third_markov_set = third_markov(text[0])
    fith_markov_set = fith_markov(text[0])
    print(generate(1000, characters_set, starting_chars_set, first_markov_set, third_markov_set, fith_markov_set))

if __name__ == '__main__':
    main()