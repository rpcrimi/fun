import nltk
import math
import numpy as np

def hash_function(inpt, N):
	xlength = len(inpt)
	s = 0
	for i in range(xlength):
		s += ord(inpt[i])
	return s % N

def main():
	hashTable = np.empty([10000, 1], dtype="S10")
	words = list(set(nltk.corpus.gutenberg.words('austen-emma.txt')))
	for word in words:
		hashTable[hash_function(word, 10000)] = word

	testword = words[1500]
	testindex = hash_function(testword, 10000)
	print hashTable[testindex], testword
if __name__ == "__main__":
	main()