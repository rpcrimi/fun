import math
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'myNewDatabase'
app.config['MONGO_HOST'] = '192.168.99.100'
mongo = PyMongo(app)

@app.route('/words.json', methods=['POST'])
def postWords():
    data = request.get_json()

    # Add anagrams to dictionary
    dictionary = {''.join(sorted(word.lower())): [] for word in data['words']}
    for word in data['words']:
        dictionary[''.join(sorted(word.lower()))].append(word)

    # Copy dictionary to mongodb
    for i,sortedLetters in enumerate(dictionary):
        queryResult = mongo.db.anagrams.find_one({sortedLetters: {'$exists': True}})
        if queryResult:
            # Already have document for sortedLetters => only save distinct words 
            queryResult[sortedLetters] = list(set(queryResult[sortedLetters] + dictionary[sortedLetters]))
            mongo.db.anagrams.save(queryResult)
        else:
            # No document for sortedLetters => create new document in database
            mongo.db.anagrams.insert({sortedLetters: dictionary[sortedLetters]})

    return '', 201

@app.route('/anagrams/<word>.json', methods=['GET'])
def getAnagrams(word):
    # Find document in mongo for requested word
    sortedLetters = ''.join(sorted(word.lower()))
    queryResult = mongo.db.anagrams.find_one({sortedLetters: {'$exists': True}})
    if queryResult:
        # Get list of anagrams and remove requested word
        anagrams = queryResult[sortedLetters]
        anagrams.remove(word)
        # Check for query parameters
        if request.args.to_dict():
            if 'includeProper' in request.args.to_dict():
                includeProper = request.args.to_dict()['includeProper']
                if includeProper.lower() == 'false':
                    # Check each word for capital first letter
                    anagrams = [anagram for anagram in anagrams if not anagram.istitle()]
            if 'limit' in request.args.to_dict():
                # Truncate list to requested limit
                limit = int(request.args.to_dict()['limit'])
                anagrams = anagrams[:limit]

        response = {'anagrams': anagrams}
    else:
        # No match => empty response
        response = {'anagrams': []}
    return jsonify(response), 200

@app.route('/words/<word>.json', methods=['DELETE'])
def deleteWord(word):
    # Find document in mongo for requested word
    sortedLetters = ''.join(sorted(word.lower()))
    queryResult = mongo.db.anagrams.find_one({sortedLetters: {'$exists': True}})
    notFound = False
    if queryResult:
        # Get list of anagrams and try to remove requested word
        anagrams = queryResult[sortedLetters]
        try:
            anagrams.remove(word)
        except ValueError:
            notFound = True
        # Save new list of anagrams to mongo
        queryResult[sortedLetters] = anagrams
        mongo.db.anagrams.save(queryResult)
    else:
        notFound = True
    if notFound:
        # Return message noting word was not in corpus
        return jsonify({'Response': '(%s) not in corpus' % word}), 200
    else:
        return '', 200

@app.route('/words.json', methods=['DELETE'])
def deleteAllWords():
    mongo.db.anagrams.remove({})
    return '', 204

# Helper function to find median string length in list of strings
def median(l):            
    l.sort(key=len)
    if len(l)%2 == 0:
        i = len(l)/2
        median = (len(l[i]) + len(l[i-1]))/2.0
    else:
        i = len(l)/2
        median = len(l[i]) 
    return median

# Helper function to find average string length in list of strings
def average(l):
    lengths = [len(i) for i in l]
    return 0 if len(lengths) == 0 else (float(sum(lengths))/len(lengths)) 


@app.route('/wordCount.json', methods=['GET'])
def getWordCount():
    # Get all documents
    queryResult = mongo.db.anagrams.find({})
    # Create list of all words in collection
    words = []
    for entry in queryResult:
        for key in entry:
            if key != '_id':
                for word in entry[key]:
                    words.append(word)
    response = {}
    if words:
        # Compute statistics about corpus
        response['wordCount'] = len(words)
        response['minLen'] = len(min(words, key=len))
        response['maxLen'] = len(max(words, key=len))
        response['medianLen'] = median(words)
        response['averageLen'] = average(words)
    else:
        response['Response'] = 'No words in the corpus'
    return jsonify(response), 200

@app.route('/mostAnagrams.json', methods=['GET'])
def mostAnagrams():
    # Get all documents
    queryResult = mongo.db.anagrams.find({})
    longestListLen = 0
    longestList = 'No words in the corpus'
    # Find longest list length in corpus
    for anagramSet in queryResult:
        for key in anagramSet:
            if key != '_id':
                if len(anagramSet[key]) > longestListLen:
                    # Update longest list of anagrams
                    longestListLen = len(anagramSet[key])
                    longestList = anagramSet[key]

    response = {'Most Anagrams': longestList}
    return jsonify(response), 200

@app.route('/allAnagrams.json', methods=['POST'])
def allAnagrams():
    # Get list of requested words
    words = request.get_json()['words']
    sortedWords = set([''.join(sorted(word)) for word in words])
    response = {}
    if len(sortedWords) == 1:
        # All sorted words are the same => they are all anagrams
        response['All Anagrams'] = True
    else:
        response['All Anagrams'] = False
    return jsonify(response), 200

@app.route('/deleteAllGroups/<size>.json', methods=['DELETE'])
def deleteAllGroups(size):
    size = int(size)
    # Get all documents
    queryResult = mongo.db.anagrams.find({})
    for anagramSet in queryResult:
        for key in anagramSet:
            if key != '_id':
                if len(anagramSet[key]) >= size:
                    mongo.db.anagrams.remove(anagramSet)
    return '', 204

@app.route('/deleteAllAnagrams/<word>.json', methods=['DELETE'])
def deleteAllAnagrams(word):
    sortedLetters = ''.join(sorted(word.lower()))
    mongo.db.anagrams.remove({sortedLetters: {'$exists': True}})
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)


