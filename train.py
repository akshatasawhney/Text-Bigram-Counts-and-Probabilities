import ujson

def preprocess(inputFile):
	print("Preprocessing...")
	with open(inputFile) as f:
		corpus = f.readlines()
		preprocessed_corpus = []
		for x in corpus:
			tmp = x.split(" ")
			sentence = []
			for word in tmp[:-1]:
				w = word.split("_")[0]
				sentence.append(w.lower())
			preprocessed_corpus.append(sentence)
		return preprocessed_corpus

def storeForTesting(content, fileName):
	with open(fileName, 'w') as file:
		file.write(ujson.dumps(content))
	file.close()

def storeBigrams(content, fileName):
	f = open(fileName, "w")
	for tokens in content:
		t = ' '.join(tokens)
		tmp = t + " : " + str(content[tokens])
		f.write(tmp)
		f.write("\n")
	f.close()

def storeUnigrams(content, fileName):
	f = open(fileName, "w")
	for tokens in content:
		tmp = tokens + " : " + str(content[tokens])
		f.write(tmp)
		f.write("\n")
	f.close()	

def noSmoothingProbability(unigrams,bigrams):
	print("Calculating No Smoothing Probability and Counts for Corpus...  ")
	bigramProbsNoSmoothing = {}
	for bigram in bigrams:
		bigramProbsNoSmoothing[bigram] = float(bigrams[bigram])/unigrams[bigram[0]]
	#print(bigramProbsNoSmoothing)
	storeBigrams(bigramProbsNoSmoothing, "trainBigramCounts_noSmoothing.txt") 

def addOneSmoothingProbability(unigrams,bigrams,V,N):
	print("Calculating Add One Smoothing Probability and Counts for Corpus... ")
	bigramProbsAddOne = {}
	bigramCountAddOne = {}
	for bigram in bigrams:
		bigramProbsAddOne[bigram] = float(bigrams[bigram]+1)/(unigrams[bigram[0]] + V) 
		bigramCountAddOne[bigram] = bigramProbsAddOne[bigram] * N 	
	storeBigrams(bigramProbsAddOne, "trainBigramProbs_addOne.txt") 
	storeBigrams(bigramCountAddOne, "trainBigramCounts_addOne.txt")

def goodTuringDiscountProbability(unigrams,bigrams,N):
	print("Calculating Good Turing Discount Probability and Counts for Corpus...")
	buckets = {} 
	for bigram in bigrams:
		if bigrams[bigram] not in buckets:
			buckets[bigrams[bigram]] = 1
		else:
			buckets[bigrams[bigram]] +=  1
	bigramProbsGT = {}
	bigramCountGT = {} 
	for bigram in bigrams:
		bigramBucket = bigrams[bigram]
		if (bigramBucket + 1) not in buckets: 
			bigramCountGT[bigram] = 0
		else:
			bigramCountGT[bigram] = (bigramBucket + 1) * (float(buckets[bigramBucket + 1])/buckets[bigramBucket])
		bigramProbsGT[bigram] = float(bigramCountGT[bigram]) / unigrams[bigram[0]]
	storeForTesting(buckets,"GTBuckets.txt")
	storeBigrams(bigramProbsGT, "trainBigramProbs_GT.txt") 
	storeBigrams(bigramCountGT, "trainBigramCounts_GT.txt")

def calculateUnigramsAndBigrams(corpus):
	print("Calculating Unigrams and Bigrams Counts for Corpus... ")
	unigrams = {}
	bigrams = {} 
	N = 0 # number of tokens in corpus
	NB = 0 # number of bigrams in corpus
	for i in range(len(corpus)):
		sentence = corpus[i]
		for word in range(len(sentence)):
			N = N + 1
			if sentence[word] not in unigrams:
				unigrams[sentence[word]] = 1
			else:
				unigrams[sentence[word]] += 1
			if word != len(sentence) - 1:
				NB = NB + 1
				if (sentence[word],sentence[word+1]) not in bigrams:
					bigrams[(sentence[word],sentence[word+1])] = 1
				else:
					bigrams[(sentence[word],sentence[word+1])] += 1

	storeUnigrams(unigrams,"UnigramFreq.txt") 
	storeBigrams(bigrams,"BigramFreq.txt") 
	storeForTesting(unigrams,"trainUnigramFreq.txt") 
	storeForTesting(bigrams,"trainBigramFreq.txt") 
	return (unigrams,N, bigrams, NB)
	
if __name__ == '__main__':
	inputFile = "NLP6320_POSTaggedTrainingSet-Windows.txt"
	preprocessed = preprocess(inputFile)
	unigramsAndBigrams = calculateUnigramsAndBigrams(preprocessed)

	unigrams = unigramsAndBigrams[0] # unigrams
	N = unigramsAndBigrams[1] # number of tokens in the corpus
	bigrams = unigramsAndBigrams[2] # bigrams
	NB = unigramsAndBigrams[3] # number of bigrams
	V = len(unigrams) # size of vocabulary
	#print(V,NB,N)
	noSmoothingProbability(unigrams,bigrams)
	addOneSmoothingProbability(unigrams,bigrams,V,N)
	goodTuringDiscountProbability(unigrams,bigrams,NB)

	print("---------------------------MODEL GENERATED---------------------------")