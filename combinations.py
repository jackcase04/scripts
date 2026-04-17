# This program calculates the total possible permutations of a 8 char password
# if the length of the word is the key of the word_dict and the key is the possible words it could be

import math

combinations = [
    [1,1,1,1,1,1,1,1],
    [2,1,1,1,1,1,1],
    [2,2,1,1,1,1],
    [2,2,2,1,1],
    [2,2,2,2],
    [4,1,1,1,1],
    [4,2,1,1],
    [4,2,2],
    [4,4],
    [5,1,1,1],
    [5,2,1]
]

word_dict = {
    1: 5,
    2: 32,
    4: 103,
    5: 402
}

total_result = 0

for combination in combinations:
    # num = len!
    # denom = for each duplicate, dup! x dup!
    dict = {}

    for num in combination:
        dict[num] = dict.get(num, 0) + 1

    numer = math.factorial(len(combination))
    denom = 1

    word_choices = 1 

    print(f"For combination: {combination}: ", end=" ")

    for x in dict:
        denom *= math.factorial(dict[x])
        print(f"{word_dict[x]}^{dict[x]} x", end=" ")
        word_choices *= pow(word_dict[x], dict[x]) 

    print(f"{numer / denom} = {(numer / denom) * word_choices}")
    total_result += (numer / denom) * word_choices

print(f"Sum of all totals: {total_result}")
