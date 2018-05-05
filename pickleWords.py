import pickle
with open('core-wordnet.txt') as words_file:
    raw_data = words_file.readlines()

blockWords = ['sex','rape','faggot','shit','fuck','damn','pussy','penis','vagina','hell','cock',
             'piss','nigger','penetrate','penetration','sexual','pervert','breast','kill','murder',
             'boob','boobie','tit','titty','dick','ass','asshole','ass-hole','bitch','hot']

word_list = []
for line in raw_data:
    word = line.split()[2].replace(']','').replace('[','')
    if word not in blockWords:
        word_list.append(word)

word_list = list(set(word_list))
word_list.sort()

with open('words.pickle','wb') as pf:
    pickle.dump(word_list,pf)
