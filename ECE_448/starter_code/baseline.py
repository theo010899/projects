"""
Part 1: Simple baseline that only uses word statistics to predict tags
"""

def baseline(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    words = {}

    # record the all the different occurance a given word and its associated tags
    for sen in range(len(train)):
        for word in range(len(train[sen])):
            pair = train[sen][word]
            if pair[0] not in words:
                words[pair[0]] = {}
            if pair[1] not in words[pair[0]]:
                words[pair[0]][pair[1]] = 1
            else:
                words[pair[0]][pair[1]] += 1

    # for word in words:
    #     if len(words[word]) > 1:
    #         print(word ," = ", words[word])
    
    # record the tag with the most occurances for a given word
    best_tag = {}
    for word in words:
        best_val = max(words[word].values())
        for tag in words[word]:
            if words[word][tag] == best_val and word not in best_tag:
                # if len(words[word]) > 1:
                #     print(word ," = ", words[word], " : ", best_val, " = ", tag)
                    # print(tag)
                best_tag[word] = tag

    # UKN case: find words that only occur once and calcuate the most popular tag
    UKN = {}

    for word in words:
        best_val = max(words[word])
        for tag in words[word]:
            if len(words[word]) == 1 and words[word][tag] == 1:
                if tag not in UKN:
                    UKN[tag]  = words[word][tag]
                else:
                    UKN[tag]  += words[word][tag]

    best_UKN_tag = max(UKN, key = lambda k: UKN[k])

    print(best_UKN_tag)
    output_list = []

    for sen in range(len(test)):
        sentence = []
        for word in range(len(test[sen])):
            # print(" word is: ", test[sen][word])
            if test[sen][word] not in words:
                pair = (test[sen][word],best_UKN_tag)
                sentence.append(pair)
            else:
                pair = (test[sen][word], best_tag[test[sen][word]])
                sentence.append(pair)
        output_list.append(sentence)

    # print("test = ", test, '\n', "output = ", output_list)
    
    return output_list