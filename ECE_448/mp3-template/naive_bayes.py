# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP3. You should only modify code
within this file and the last two arguments of line 34 in mp3.py
and if you want-- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import math

from nltk.stem import PorterStemmer 

def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter=1.0, pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter --laplace (1.0 by default)
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # train_set_cpy = train_set.copy()
    # dev_set_cpy = dev_set.copy()
    # ps = PorterStemmer() 

    # # handle stemming
    # for x in range(len(train_set_cpy)):
    #     for y in range(len(train_set_cpy[x])):
    #         train_set_cpy[x][y] = ps.stem(train_set_cpy[x][y])

    # for x in range(len(dev_set_cpy)):
    #     for y in range(len(dev_set_cpy[x])):
    #         dev_set_cpy[x][y] = ps.stem(dev_set_cpy[x][y])    

    # return predicted labels of development set

    pos_train_word_occur = {}

    neg_train_word_occur = {}

    train_words_pos = set()
    
    train_words_neg = set()

    pos_train = []

    neg_train = []

    pos_log = {}

    neg_log = {}

    # seperate positive and negative reviews together

    for x in range(len(train_set)):
        if train_labels[x] == 1:
            pos_train.append(train_set[x])
        else:
            neg_train.append(train_set[x])

    
    #count the occurances of the different types of words for the reviews

    for x in range(len(pos_train)):
        for y in range(len(pos_train[x])):
            #print(pos_train[x][y])
            if pos_train[x][y] in pos_train_word_occur:
                pos_train_word_occur[pos_train[x][y]] += 1
            else: 
                pos_train_word_occur[pos_train[x][y]] = 1
            if pos_train[x][y] not in train_words_pos:
                #print(pos_train[x][y])
                train_words_pos.add(pos_train[x][y])

    for x in range(len(neg_train)):
        for y in range(len(neg_train[x])):
            if neg_train[x][y] in neg_train_word_occur:
                neg_train_word_occur[neg_train[x][y]] += 1
            else: 
                neg_train_word_occur[neg_train[x][y]] = 1
            if neg_train[x][y] not in train_words_neg:
                train_words_neg.add(neg_train[x][y])

    # print(len(pos_train), " ", len(train_words_pos))

    n_pos = 0
    n_neg = 0
    for x in pos_train_word_occur:
        n_pos += pos_train_word_occur[x]
        # print(pos_train_word_occur[x]," ")

    for x in neg_train_word_occur:
        n_neg += neg_train_word_occur[x]

    # print(n_pos, " ", n_neg, "\n")
    # print(len(pos_train_word_occur), " ", len(neg_train_word_occur))

    # cacluate the log probability of each word plus the laplace smoothing
    
    for x in pos_train_word_occur:
        word_count = pos_train_word_occur[x]
        pos_tot_words = len(train_words_pos)
        laplace_num = (smoothing_parameter + word_count)
        # print(tot_words, " TOT_WORDS")
        laplace_denom = n_pos + smoothing_parameter * (pos_tot_words + 1)
        pos_log[x] = math.log(laplace_num/laplace_denom)

    for x in neg_train_word_occur:
        word_count = neg_train_word_occur[x]
        neg_tot_words = len(train_words_neg)
        laplace_num = (smoothing_parameter + word_count)
        laplace_denom = n_neg + smoothing_parameter * (neg_tot_words + 1)
        neg_log[x] = math.log(laplace_num/laplace_denom)


    pos_dev_MAP = math.log(pos_prior)

    neg_dev_MAP = math.log(1 - pos_prior)

    MAP_ret_list = []

    #laplace smoothing for unknown cases
    pos_tot_words = len(train_words_pos)
    laplace_num_pos = smoothing_parameter
    laplace_denom_pos = n_pos+ smoothing_parameter * (pos_tot_words + 1)

    neg_tot_words = len(train_words_neg)
    laplace_num_neg = smoothing_parameter
    laplace_denom_neg =  n_neg + smoothing_parameter * (neg_tot_words + 1)


    for review in range(len(dev_set)):
        pos_dev_MAP = math.log(pos_prior)
        neg_dev_MAP = math.log(1 - pos_prior)

        for word in range(len(dev_set[review])):
            if dev_set[review][word] in pos_train_word_occur:
                pos_dev_MAP += pos_log[dev_set[review][word]]
            else:
                pos_dev_MAP += math.log(laplace_num_pos/laplace_denom_pos)
            if dev_set[review][word] in neg_train_word_occur:
                neg_dev_MAP += neg_log[dev_set[review][word]]
            else:
                neg_dev_MAP += math.log(laplace_num_neg/laplace_denom_neg)
        # print(pos_dev_MAP," ",neg_dev_MAP)
        if pos_dev_MAP > neg_dev_MAP:
            MAP_ret_list.append(1)
        else:
            MAP_ret_list.append(0)



    # for review in range(len(dev_set)):
    #     for word in range(len(dev_set[review])):

    return MAP_ret_list

def bigramBayes(train_set, train_labels, dev_set, unigram_smoothing_parameter=1.0, bigram_smoothing_parameter= 0.005, bigram_lambda=0.5,pos_prior=0.8):
    """
    train_set - List of list of words corresponding with each movie review
    example: suppose I had two reviews 'like this movie' and 'i fall asleep' in my training set
    Then train_set := [['like','this','movie'], ['i','fall','asleep']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two reviews, first one was positive and second one was negative.
    Then train_labels := [1, 0]

    dev_set - List of list of words corresponding with each review that we are testing on
              It follows the same format as train_set

    unigram_smoothing_parameter - The smoothing parameter for unigram model (same as above) --laplace (1.0 by default)
    bigram_smoothing_parameter - The smoothing parameter for bigram model (1.0 by default)
    bigram_lambda - Determines what fraction of your prediction is from the bigram model and what fraction is from the unigram model. Default is 0.5
    pos_prior - The prior probability that a word is positive. You do not need to change this value.
    """
    # TODO: Write your code here
    # return predicted labels of development set using a bigram model

    pos_train_word_occur = {}

    neg_train_word_occur = {}

    train_words_pos = set()
    
    train_words_neg = set()

    pos_train = []

    neg_train = []

    pos_log = {}

    neg_log = {}

    # seperate positive and negative reviews together

    for x in range(len(train_set)):
        if train_labels[x] == 1:
            pos_train.append(train_set[x])
        else:
            neg_train.append(train_set[x])

    #count the occurances of the different types of words for the reviews

    for x in range(len(pos_train)):
        for y in range(len(pos_train[x])):
            #print(pos_train[x][y])
            if pos_train[x][y] in pos_train_word_occur:
                pos_train_word_occur[pos_train[x][y]] += 1
            else: 
                pos_train_word_occur[pos_train[x][y]] = 1
            if pos_train[x][y] not in train_words_pos:
                #print(pos_train[x][y])
                train_words_pos.add(pos_train[x][y])

    for x in range(len(neg_train)):
        for y in range(len(neg_train[x])):
            if neg_train[x][y] in neg_train_word_occur:
                neg_train_word_occur[neg_train[x][y]] += 1
            else: 
                neg_train_word_occur[neg_train[x][y]] = 1
            if neg_train[x][y] not in train_words_neg:
                train_words_neg.add(neg_train[x][y])

    # print(len(pos_train), " ", len(train_words_pos))

    n_pos = 0
    n_neg = 0
    for x in pos_train_word_occur:
        n_pos += pos_train_word_occur[x]
        # print(pos_train_word_occur[x]," ")

    for x in neg_train_word_occur:
        n_neg += neg_train_word_occur[x]

    # cacluate the log probability of each word plus the laplace smoothing
    
    for x in pos_train_word_occur:
        word_count = pos_train_word_occur[x]
        pos_tot_words = len(train_words_pos)
        laplace_num = (unigram_smoothing_parameter + word_count)
        # print(tot_words, " TOT_WORDS")
        laplace_denom = n_pos + unigram_smoothing_parameter * (pos_tot_words + 1)
        pos_log[x] = math.log(laplace_num/laplace_denom)

    for x in neg_train_word_occur:
        word_count = neg_train_word_occur[x]
        neg_tot_words = len(train_words_neg)
        laplace_num = (unigram_smoothing_parameter + word_count)
        laplace_denom = n_neg + unigram_smoothing_parameter * (neg_tot_words + 1)
        neg_log[x] = math.log(laplace_num/laplace_denom)


######################## END of UNIGRAM PART ########################


    pos_tuple_occur = {}

    neg_tuple_occur = {}

# count the occurences of pairs

    for x in range(len(pos_train)):
        for y in range(len(pos_train[x])):
            if y == len(pos_train[x]) -1:
                pair1 = (pos_train[x][y], None)
            else:
                pair1 = (pos_train[x][y],pos_train[x][y+1])
            if pair1 in pos_tuple_occur:
                pos_tuple_occur[pair1] += 1
            else: 
                # print(pair1, " False")
                pos_tuple_occur[pair1] = 1

    for x in range(len(neg_train)):
        for y in range(len(neg_train[x])):
            if y == len(neg_train[x]) -1:
                pair1 = (neg_train[x][y], None)
            else:
                pair1 = (neg_train[x][y],neg_train[x][y+1])
            if pair1 in neg_tuple_occur:
                neg_tuple_occur[pair1] += 1
            else: 
                neg_tuple_occur[pair1] = 1
    

    n_pos_pair = 0
    n_neg_pair = 0
    for x in pos_tuple_occur:
        n_pos_pair += pos_tuple_occur[x]
        # print(pos_train_word_occur[x]," ")

    for x in neg_tuple_occur:
        n_neg_pair += neg_tuple_occur[x]
 
 #calculate the log for the pairs
    pos_pair_log = {}
    neg_pair_log = {}

    for x in pos_tuple_occur:
        pair_count = pos_tuple_occur[x]
        pos_tot_pairs = len(pos_tuple_occur)
        laplace_num = (bigram_smoothing_parameter + pair_count)
        # print(tot_pairs, " TOT_pairs")
        laplace_denom = n_pos_pair + bigram_smoothing_parameter * (pos_tot_pairs + 1)
        pos_pair_log[x] = math.log(laplace_num/laplace_denom)
    
    for x in neg_tuple_occur:
        pair_count = neg_tuple_occur[x]
        neg_tot_pairs = len(neg_tuple_occur)
        laplace_num = (bigram_smoothing_parameter + pair_count)
        # print(tot_pairs, " TOT_pairs")
        laplace_denom = n_neg_pair + bigram_smoothing_parameter * (neg_tot_pairs + 1)
        neg_pair_log[x] = math.log(laplace_num/laplace_denom)


    pos_dev_MAP = math.log(pos_prior)

    neg_dev_MAP = math.log(1 - pos_prior)

    MAP_pos = []

    MAP_neg = []

    #laplace smoothing for unknown cases
    pos_tot_pairs = len(pos_tuple_occur)
    laplace_num_pos = bigram_smoothing_parameter
    laplace_denom_pos = n_pos_pair+ bigram_smoothing_parameter * (pos_tot_pairs + 1)

    neg_tot_pairs = len(neg_tuple_occur)
    laplace_num_neg = bigram_smoothing_parameter
    laplace_denom_neg =  n_neg_pair + bigram_smoothing_parameter * (neg_tot_pairs + 1)


    for review in range(len(dev_set)):
        pos_dev_MAP = math.log(pos_prior)
        neg_dev_MAP = math.log(1 - pos_prior)

        for word in range(len(dev_set[review])):
            if word == len(dev_set[review]) -1:
                pair1 = (dev_set[review][word], None)
            else:
                pair1 = (dev_set[review][word],dev_set[review][word+1])
            if pair1 in pos_train_word_occur:
                pos_dev_MAP += pos_log[pair1]
            else:
                pos_dev_MAP += math.log(laplace_num_pos/laplace_denom_pos)
            if pair1 in neg_train_word_occur:
                neg_dev_MAP += neg_log[pair1]
            else:
                neg_dev_MAP += math.log(laplace_num_neg/laplace_denom_neg)
        
        MAP_pos.append(pos_dev_MAP)

        MAP_neg.append(neg_dev_MAP)
        # print(pos_dev_MAP," ",neg_dev_MAP)
        
        # if pos_dev_MAP > neg_dev_MAP:
        #     MAP_ret_list.append(1)
        # else:
        #     MAP_ret_list.append(0)


######## UKN unigram #####
    pos_dev_MAP_uni = math.log(pos_prior)

    neg_dev_MAP_uni = math.log(1 - pos_prior)

    MAP_pos_uni = []

    MAP_neg_uni = []

    #laplace smoothing for unknown cases
    pos_tot_words = len(train_words_pos)
    laplace_num_pos = unigram_smoothing_parameter
    laplace_denom_pos = n_pos+ unigram_smoothing_parameter * (pos_tot_words + 1)

    neg_tot_words = len(train_words_neg)
    laplace_num_neg = unigram_smoothing_parameter
    laplace_denom_neg =  n_neg + unigram_smoothing_parameter * (neg_tot_words + 1)


    for review in range(len(dev_set)):
        pos_dev_MAP_uni = math.log(pos_prior)
        neg_dev_MAP_uni = math.log(1 - pos_prior)

        for word in range(len(dev_set[review])):
            if dev_set[review][word] in pos_train_word_occur:
                pos_dev_MAP_uni += pos_log[dev_set[review][word]]
            else:
                pos_dev_MAP_uni += math.log(laplace_num_pos/laplace_denom_pos)
            if dev_set[review][word] in neg_train_word_occur:
                neg_dev_MAP_uni += neg_log[dev_set[review][word]]
            else:
                neg_dev_MAP_uni += math.log(laplace_num_neg/laplace_denom_neg)
        # print(pos_dev_MAP_uni," ",neg_dev_MAP_uni)
        MAP_pos_uni.append(pos_dev_MAP_uni)

        MAP_neg_uni.append(neg_dev_MAP_uni)
        # if pos_dev_MAP_uni > neg_dev_MAP_uni:
        #     MAP_ret_list_uni.append(1)
        # else:
        #     MAP_ret_list_uni.append(0)

##### MIXED COMAPARE #####
    MAP_ret_list_final = []

    for x in range(len(dev_set)):
        pos_dev_MAP = (1-bigram_smoothing_parameter) * MAP_pos_uni[x] + bigram_smoothing_parameter * MAP_pos[x]
        neg_dev_MAP = (1-bigram_smoothing_parameter) * MAP_neg_uni[x] + bigram_smoothing_parameter * MAP_neg[x]
        if pos_dev_MAP > neg_dev_MAP:
            MAP_ret_list_final.append(1)
        else:
            MAP_ret_list_final.append(0)


    return MAP_ret_list_final