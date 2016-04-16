import re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet_ic


def tagger(sentence):
    text = sentence.split()
    taggedText = nltk.pos_tag(text)
    #print(taggedText)
    return taggedText

def similarityInAList(sameTaggedList, tag):
    if len(sameTaggedList) < 2: #if list contains only 0 or 1
        return 0
    else:
        for i in range(len(sameTaggedList)-1):
            newSimilarity(sameTaggedList[i], sameTaggedList[i+1], tag)

    return

def sentiScores(word):      #takes input as string, return bith +&- values
    word = swn.senti_synset(word)[0]
    values = []
    values.append(word.pos_score())      #positive value
    values.append(word.neg_score())     #negative value
    return values


def similarity(word1, word2, tag):
    obj1 = wn.synset(word1 + "."+ tag+".01")
    obj2 = wn.synset(word2 + "."+ tag+".01")
    #print(obj1)
    brown_ic = wordnet_ic.ic('ic-brown.dat') 	# Information content
    semcor_ic = wordnet_ic.ic('ic-brown.dat')
    value = obj1.res_similarity(obj2, brown_ic)
    return value

def removingCommonWords(taggedData):
    finalList = list(set(taggedData))
    return finalList

def newSimilarity(word1, word2, tag):
    obj1 = wn.synsets(word1)
    obj2 = wn.synsets(word2)
    #print(obj1, obj2)
    listOfSameTaggedSynsets1 = synsetToString(obj1, tag)
    print(listOfSameTaggedSynsets1)
    listOfSameTaggedSynsets2 = synsetToString(obj2, tag)
    print(listOfSameTaggedSynsets2)

    pass
    
l=[]
def synsetToString(obj, tag):
    for i in obj:
        l.append(str(i)[8:-2])
    for i in l:
        if i[-4] != tag:
            l.remove(i)

    return l

def findingResnikSimilarity(synset1, synset2):
	return (max (wn.synset(synset1).path_similarity(wn.synset(synset2)), wn.synset(synset2).path_similarity(wn.synset(synset1))))

#input starts from here
text = input()
text = text.lower()
Taggedtext = tagger(text)


print(Taggedtext)


#converting tags into simpler ones as used in the paper
# use this to see all possible tags nltk.help.upenn_tagset()
# also determinants, conjuctions are not taken care of
countV, countN, countA, countR = 0, 0, 0, 0 #for similarity measures
listV, listN, listA, listR = [], [], [], []

for i in range(len(Taggedtext)):
    old = Taggedtext[i][1]
#for verb
    match = re.match(r'VB*', old)
    if match:
        Taggedtext[i] = (Taggedtext[i][0],'VB')
        listV.append(Taggedtext[i][0])
        
#for noun
    match = re.match(r'NN*', old)
    if match:
        Taggedtext[i] = (Taggedtext[i][0],'NN')
        listN.append(Taggedtext[i][0])

#for adjectives
    match = re.match(r'JJ*', old)
    if match:
        Taggedtext[i] = (Taggedtext[i][0],'JJ')
        listA.append(Taggedtext[i][0])


#for adverb
    match = re.match(r'RB*', old)
    if match:
        Taggedtext[i] = (Taggedtext[i][0],'RB')
        listR.append(Taggedtext[i][0])

listA = removingCommonWords(listA)
listR = removingCommonWords(listR)
listV = removingCommonWords(listV)


#getting the sentiscore for all tagged words
similarityInAList(listA, 'a')
similarityInAList(listR, 'r')
similarityInAList(listV, 'v')
