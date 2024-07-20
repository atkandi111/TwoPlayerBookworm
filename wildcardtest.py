"""import nltk

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
dictionary = set(word.lower() for word in nltk.FreqDist(nltk.corpus.brown.words()))

def new_match_wildcard(word):
    for i in range(word.count("?")):
        for letter in alphabet:
            temp = word.replace("?", letter, 1)

            if (i + 1 == word.count("?")):
                if temp in dictionary:
                    return temp
    return word

def match_wildcard(word):
    if "?" in word:
        for letter in alphabet:
            temp = word.replace("?", letter, 1)
            temp = match_wildcard(temp)
            
            if temp in dictionary:
                return temp
    return word

def match_wildcard2(word):
    for letter in alphabet:
        temp = word.replace("?", letter, 1)
        if "?" in temp:
            temp = match_wildcard2(temp)
        
        if temp in dictionary:
            return temp
    return word


print(match_wildcard("mitigate"))
print(match_wildcard("mitiggte"))
print(match_wildcard("miti?ate"))
print(match_wildcard("miti??te"))"""

import hashlib, random, string

for _ in range(100):
    data1 = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    data2 = ''.join(random.choice(string.ascii_letters) for _ in range(10))

    hash1 = int(hashlib.sha256(data1.encode('utf-8')).hexdigest(), base=16)
    hash2 = int(hashlib.sha256(data2.encode('utf-8')).hexdigest(), base=16)

    if hash1 == hash2:
        print(hash1)
        print(hash2)
        break
else:
    print("No collisions")

str = "Word::::"
key, val, data = str.split("::", 2)
print(key, val)
if val == None:
    print("hi")
else:
    print('ehllo')
