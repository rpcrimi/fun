import re

with open("A-small-practice.in", "r") as f:
	inputData = f.read().splitlines()

L = int(inputData[0].split(" ")[0])
D = int(inputData[0].split(" ")[1])
N = int(inputData[0].split(" ")[2])

corpus = inputData[1:D+1]
testCases = [el.replace("(", "[").replace(")", "]") for el in inputData[D+1:]]

for X, testCase in enumerate(testCases):
	r = re.compile(testCase)
	K = 0
	for word in corpus:
		if re.match(r, word):
			K += 1
	print "Case #%i: %i" % (X+1, K)