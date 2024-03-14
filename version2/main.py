import random
import codecs

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
    markov_sorted = {}
    for elem in sorted(markov):
        markov_sorted.update({elem: sorted(markov[elem].items(), key=lambda item: item[1], reverse=True)})

    #print("Markov: ")
    #print(markov_sorted)
    return markov_sorted

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
    markov_sorted = {}
    for elem in sorted(markov):
        markov_sorted.update({elem: sorted(markov[elem].items(), key=lambda item: item[1], reverse=True)})
    # print("Markov: ")
    # print(markov)
    return markov_sorted

def fifth_markov(text):
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
    markov_sorted = {}
    for elem in sorted(markov):
        markov_sorted.update({elem: sorted(markov[elem].items(), key=lambda item: item[1], reverse=True)})
    #print("Markov: ")
    #print(markov)
    return markov_sorted

def generate(length, character_set, starting_set, first_markov, third_markov, fifth_markov):
    result = 'you'
    previous = ''
    last_word = ''
    for i in range(length):
        previous = result[-1]
        last_word = result[-5:]
        if previous == '':
            result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
        else:
            if len(last_word) < 3:
                try:
                    result += first_markov[previous][0][random.randint(0, 2)]
                except:
                    result += random.choices(list(character_set.keys()), list(character_set.values()))[0]
            elif len(last_word) < 5:
                try:
                    result += third_markov[last_word][0][random.randint(0, 2)]
                except:
                    try:
                        result += first_markov[last_word][0][random.randint(0, 2)]
                    except:
                        result += random.choices(list(character_set.keys()), list(character_set.values()))[0]
            else:
                try:
                    result += fifth_markov[last_word][0][random.randint(0, 2)]
                except:
                    try:
                        result += third_markov[last_word][0][random.randint(0, 2)]
                    except:
                        try:
                            result += first_markov[last_word][0][random.randint(0, 2)]
                        except:
                            result += random.choices(list(character_set.keys()), list(character_set.values()))[0]
        #print('Word: ', last_word, ' Letter: ', previous)
    return result

def generate5(length, character_set, starting_set, first_markov, third_markov, fifth_markov):
    result = 'pan '
    previous = ''
    last_word = ''
    for i in range(length):
        previous = result[-1]
        last_word = result[-5:]
        if previous == '':
            result += random.choices(list(starting_set.keys()), list(starting_set.values()))[0]
        elif last_word not in fifth_markov.keys():
            if len(first_markov[previous]) > 1:
                next_word = first_markov[previous][random.randint(0, 1)][0]
            else:
                next_word = first_markov[previous][0][0]
            result += next_word
        elif last_word in fifth_markov.keys():
            if len(fifth_markov[last_word]) > 1:
                next_word = fifth_markov[last_word][random.randint(0, 1)][0]
            else:
                next_word = fifth_markov[last_word][0][0]
            result += next_word
        #print('Word: ', last_word, ' Letter: ', previous)
    return result

def main():
    text = ''
    with open('resources/pan-tadeusz.txt', mode='r', encoding='ANSI') as f:
        for line in f.readlines():
            text += line
    f.close()
    #print(text)
    text = [text]
    characters_set = get_characters(text)
    print(characters_set)
    starting_chars_set = starting_chars(text[0])
    first_markov_set = first_markov(text[0])
    #print(first_markov_set)
    third_markov_set = third_markov(text[0])
    fifth_markov_set = fifth_markov(text[0])
    print(generate5(300, characters_set, starting_chars_set, first_markov_set, third_markov_set, fifth_markov_set))

if __name__ == '__main__':
    main()