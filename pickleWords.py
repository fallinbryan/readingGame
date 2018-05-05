import pickle
with open('core-wordnet.txt') as words_file:
    raw_data = words_file.readlines()

word_list = []
for line in raw_data:
    word_list.append(line.split()[2].replace(']','').replace('[',''))

word_list = list(set(word_list))
word_list.sort()

with open('words.pickle','wb') as pf:
    pickle.dump(word_list,pf)
