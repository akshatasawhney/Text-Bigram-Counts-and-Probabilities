import ujson
import math
import sys

def preprocess(sentence):
	print("Preprocessing...")
	text = []
	tmp = sentence.split(" ")
	for word in tmp:
		w = word.split("_")[0]
		text.append(w.lower())
	return text

def getFile(fileName):
	with open(fileName, 'r') as file:
		x = ujson.load(file)
		return x

def getKey(bigram):
	return "('" + bigram[0] +"', '" + bigram[1] + "')"

def NoSmoothingProbability(unigramFreq,bigramFreq,bigramKeyDict):
    probability = 1.0
    for key in bigramKeyDict:
        bigramProbsNoSmoothing = float(bigramFreq[key])/unigramFreq[bigramKeyDict[key]]
        probability *= bigramProbsNoSmoothing
    print("No Smoothing Probability - ",probability)

def AddOneSmoothingProbability(bigramKeyDict,unigramFreq,bigramFreq,V):
    probability = 1.0
    for key in bigramKeyDict:
        bigramProbsAddOne = float(bigramFreq[key]+1)/(unigramFreq[bigramKeyDict[key]] + V)
        probability *= bigramProbsAddOne
    print("Add 1 Smoothing Probability - ",probability) 

def GoodTuringSmoothingProbability(processed,inputBigramsFreq,bigramFreq,buckets,N):
    probability = 1.0
    for bigram in inputBigramsFreq:
        bigramBucket = buckets[str(inputBigramsFreq[bigram])]
        
        if bigram not in bigramFreq:
            probability *= float(buckets['1'])/N
        elif str(bigramBucket + 1) not in buckets.keys():
            probability = 0.0
        else:
            nNext = float(buckets[str(bigramBucket + 1)])
            nCurrent = buckets[str(bigramBucket)]
            c_star = (bigramBucket + 1) * (nNext/nCurrent)
            probability *= float(c_star)/N
    print("Good Turing Smoothing Probability - ",probability)


def calculateProbabilty(inputText,smoothing,unigramFreq,bigramFreq):
    inputBigramsFreq = {} 
    processed = preprocess(inputText)
    bigramKeyDict = {}
    for i in range(len(processed)-1):
        bigram = (processed[i],processed[i+1])
        key = getKey(bigram)
        bigramKeyDict[key] = processed[i]
        if key not in inputBigramsFreq:
            inputBigramsFreq[key] = 1
        else:
            inputBigramsFreq[key] +=  1 

    if smoothing == "NS" or smoothing == "ns":
        NoSmoothingProbability(unigramFreq,bigramFreq,bigramKeyDict)
    elif smoothing == "AO" or smoothing == "ao":
        AddOneSmoothingProbability(bigramKeyDict,unigramFreq,bigramFreq,len(unigramFreq))
    elif smoothing == "GT" or smoothing == "gt":
        buckets = getFile("GTBuckets.txt")
        GoodTuringSmoothingProbability(processed,inputBigramsFreq,bigramFreq,buckets,66517)
        

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arguments Expected : sentence smoothing(NS/AO/GT)")
        sys.exit()
    inputText = str(sys.argv[1])
    smoothing = str(sys.argv[2])
    unigramFreq = getFile("trainUnigramFreq.txt")
    bigramFreq = getFile("trainBigramFreq.txt")
    calculateProbabilty(inputText,smoothing,unigramFreq,bigramFreq)

