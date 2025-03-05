"""
Part 3: Here you should improve viterbi to use better laplace smoothing for unseen words
This should do better than baseline and your first implementation of viterbi, especially on unseen words
"""
import math
def viterbi_2(train, test):
    '''
    input:  training data (list of sentences, with tags on the words)
            test data (list of sentences, no tags on the words)
    output: list of sentences with tags on the words
            E.g., [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
    '''
    tags = {}

    words = {}

    initial = {}

    tag_pairs = {} # transition

    tag_word = {}  # emmission

    total_e = 0

    total_t = 0

    smoothing_parameter_alpha = 0.000001
    smoothing_parameter = 0.00001

    # record occurances of tags, tag pairs, and tag/word pairs
    for sen in range(len(train)):
        for word in range(len(train[sen])):
            if word == 0:
                tag_word_pair = train[sen][word]
                tag = tag_word_pair[1]
                tag_pair = (tag, None)
            else:
                tag_word_pair = train[sen][word]
                tag_word_pair_prev = train[sen][word-1]
                tag = tag_word_pair[1]
                tag_prev = tag_word_pair_prev[1]
                tag_pair = (tag, tag_prev)

            if tag not in tags:     ### total tags
                tags[tag] = 1
            else: tags[tag] += 1

            if tag_word_pair[1] == "START":     ### initial
                if tag_word_pair[0] not in initial: 
                    initial[tag_word_pair[0]] = 1
                else: initial[tag_word_pair[0]] += 1


            pair = train[sen][word]     ### find out how many tags there are for each word
            if pair[0] not in words:
                words[pair[0]] = {}
            if pair[1] not in words[pair[0]]:
                words[pair[0]][pair[1]] = 1
            else:
                words[pair[0]][pair[1]] += 1



            if tag_pair[1] not in tag_pairs:        #### transition
                tag_pairs[tag_pair[1]] = {}
            if tag_pair[0] not in tag_pairs[tag_pair[1]]:
                tag_pairs[tag_pair[1]][tag_pair[0]] = 1
                total_t += 1
            else:  tag_pairs[tag_pair[1]][tag_pair[0]] += 1

            if tag_word_pair[1] not in tag_word:        ### emmission
                tag_word[tag_word_pair[1]] = {}
            if tag_word_pair[0] not in tag_word[tag_word_pair[1]]:
                tag_word[tag_word_pair[1]][tag_word_pair[0]] = 1
                # total_e += 1
            else: tag_word[tag_word_pair[1]][tag_word_pair[0]] += 1
            
    

        # UKN case: find words that only occur once and calcuate the most popular tag
    UKN = {}

    for word in words:
        # best_val = max(words[word])
        for tag in words[word]:
            if len(words[word]) == 1 and words[word][tag] == 1:
                if tag not in UKN:
                    UKN[tag]  = words[word][tag]
                else:
                    UKN[tag]  += words[word][tag]
    # print(UKN)
    hapax = {}
    for tag in tags:
        if tag in UKN:
            value = UKN[tag]
            laplace_num = (smoothing_parameter + value)
            all_values = UKN.values()
            total = sum(all_values)
            laplace_denom = total + smoothing_parameter * (len(UKN) + 1)
            # print(tag, " ", laplace_num," ", laplace_denom, " ", total)
            hapax[tag] = laplace_num/laplace_denom
        else:
            laplace_num = smoothing_parameter
            all_values = UKN.values()
            total = sum(all_values)
            laplace_denom = total + smoothing_parameter * (len(UKN) + 1)
            hapax[tag] = laplace_num/laplace_denom

    # print(hapax)
    prob_i = {}
    prob_t = {}
    prob_e = {}

    # calculate the log initial probability

    # print(tags['START'])

    for x in initial:
        word_count = initial[x]
        laplace_num = (smoothing_parameter + word_count)
        start_count = tags['START']
        laplace_denom = start_count + smoothing_parameter * (len(initial) + 1)
        prob_i[x] = math.log(laplace_num/laplace_denom)


    # calculate the log transition probability

    for prev_t in tag_pairs:
        for next_t in tag_pairs[prev_t]:
            pair_count = tag_pairs[prev_t][next_t]
            laplace_num = (smoothing_parameter + pair_count)
            pair_values = tag_pairs[prev_t].values()
            prev_count = sum(pair_values)
            # print(tag_pairs[prev_t], "   ", pair_values, "    ", prev_count)
            laplace_denom = prev_count + smoothing_parameter * (len(tag_pairs[prev_t]) + 1)
            prob_t[(prev_t,next_t)] = math.log(laplace_num/laplace_denom)

    # print(prob_t)
     # calculate the log emission probability

    for cur_tag in tag_word:
        # if cur_tag in UKN:
        alpha = hapax[cur_tag] * smoothing_parameter_alpha
        # else:
        #     all_values = UKN.values()
        #     total = sum(all_values)
        #     alpha = smoothing_parameter_alpha/len(UKN)
        for cur_word in tag_word[cur_tag]:
            word_count = tag_word[cur_tag][cur_word]
            laplace_num = (alpha + word_count)
            tag_count = tags[cur_tag]
            laplace_denom = tag_count + alpha * (len(tag_word[cur_tag]) + 1)
            prob_e[(cur_tag,cur_word)] = math.log(laplace_num/laplace_denom)

    # print(prob_e)
    # handle unknown initials
    for x in range(len(test)):
        init_word = test[x][0]
        if init_word not in prob_i:
            laplace_num = smoothing_parameter
            start_count = tags["START"]
            laplace_denom = start_count + smoothing_parameter * (len(initial) + 1)
            prob_i[init_word] = math.log(laplace_num/laplace_denom)

    # handle unknowns transition
    for tag_A in tags:
        for tag_B in tags:
            if tag_A == "END":
                break
            if (tag_A, tag_B) not in prob_t:
                laplace_num = smoothing_parameter
                pair_values = tag_pairs[tag_A].values()
                prev_count = sum(pair_values)
                laplace_denom = prev_count + smoothing_parameter * (len(tag_pairs[tag_A]) + 1)
                prob_t[(tag_A,tag_B)] = math.log(laplace_num/laplace_denom)
                # prob_t[(tag_A, tag_B)] = 0.000001

    # handle unknowns emission
    for cur_tag in tags:
        # if cur_tag in UKN:
        alpha = hapax[cur_tag] * smoothing_parameter_alpha
        # else:
        #     all_values = UKN.values()
        #     total = sum(all_values)
        #     alpha = smoothing_parameter_alpha/len(UKN)
        for x in range(len(test)):
            for y in range(len(test[x])):
                cur_word = test[x][y]
                if (cur_tag, cur_word) not in prob_e:
                    laplace_num = alpha
                    tag_count = tags[cur_tag]
                    laplace_denom = tag_count + alpha * (len(tag_word[cur_tag]) + 1)
                    prob_e[(cur_tag,cur_word)] = math.log(laplace_num/laplace_denom)    


    # construct trellis graph
    return_test = []

    for sent in range(len(test)):
        sentence = [[(-9999999999999999999,None,"") for i in range(len(tags))] for j in range(len(test[sent]))] 
        # sentence = test[sent].copy()
        # print(len(sentence), " ", len(sentence[0]), " ", len(tags))
        best_prob = -9999999999999999999
        for x in range(len(test[sent])):
            best_end = None
            row = 0
            for y in tags:
                # print(x, " ", row)
                if x == 0:  #initialization
                    cur_word = test[sent][x]
                    cur_tag = y
                    tag_word = (cur_tag,cur_word)
                    if cur_tag == "START":
                        v_prob = 0
                    else: v_prob = -9999999999999999999
                    sentence[x][row] = (v_prob, None, cur_tag)
                    # continue

                cur_v = sentence[x][row][0]
                # next_b = None
                cur_tag = y
                # print(len(test[sent]))
                if x != len(test[sent]) - 1:
                    next_word = test[sent][x+1]
                
                next_row = 0
                for tag_b in tags: # iterate through all possible next tags  RECURSION
                    if cur_tag == "END" or x == len(test[sent]) - 1:
                        break
                    next_v = sentence[x+1][next_row][0]

                    next_tag_pair = (cur_tag, tag_b)
                    # print(next_tag_pair)
                    next_tag_word = (tag_b,next_word)
                    # print(next_tag_word)
                    temp_v = cur_v + prob_t[next_tag_pair] + prob_e[next_tag_word]
                    # print(temp_v)
                    if temp_v > next_v:
                        next_v = temp_v
                        next_b = (x,row) # the b_val for the next cell should point to the current cell
                        sentence[x+1][next_row] = (next_v, next_b, tag_b)

                    next_row += 1

                # print(sentence[x][row])
                # print(x, " ",len(test[sent]) - 1," ", sentence[x][row][0], "  ", best_end)
                if x == len(test[sent]) - 1 and sentence[x][row][0] > best_prob: 
                    best_prob = sentence[x][row][0]
                    best_end = sentence[x][row]
                    # print(best_prob, "  ", best_end)
                row += 1
                    # TERMINATION
            if x == len(test[sent]) -1:
                sen_pairs = []
                z = x
                cur_cell = best_end
                # print(cur_cell, " ", z)
                while z >= 0:
                    if z == 0:
                        # print("END")
                        sen_pairs.insert(0,(test[sent][z],cur_cell[2]))
                    else:
                        # print("HELLO")
                        sen_pairs.insert(0,(test[sent][z],cur_cell[2]))
                        prev_b = cur_cell[1]
                        cur_cell = sentence[prev_b[0]][prev_b[1]]
                    z -= 1
                return_test.append(sen_pairs)
            #     break
            # break

    # print(return_test)

    return return_test