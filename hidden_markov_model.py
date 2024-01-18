# Code that estimates the transition probability matrix(A)
# and emission probabilities (called B) and gets the set of states (Q) from the annotated corpus given in the materials.

# Starting with getting the set of states(Q) (these will be the POS-tags from the corpus)
# We are also creating a list with all the POS-tags from the corpus in order to 
# calculate the transition probability matrix(A). We also need their counts, which is why we initialize "all_tags_n_counts".

from working_version_prob_distr_class import LogCondPr
from math import log

set_of_states_Q = []
all_tags = []
all_tags_n_counts = {}

with open ('pos_training_data.toks_tags', encoding="utf8") as ann_corpus:
    for line in ann_corpus:
        line = list(line.split())
        final_line = ['<s>'] + line + ['<\s>']    #   adding start-of-sequence and end-of-sequence symbols to each line (each list) 
        for word_tag in final_line:
            if word_tag not in ['<s>','<\s>']:
                word_tag = word_tag.split('|')
                if word_tag[1] not in set_of_states_Q:      #   putting all the possible pos-tags in a list, excluding <s> and <\s>
                    set_of_states_Q.append(word_tag[1])
                if word_tag[1] not in all_tags_n_counts:    #   putting all the possible pos-tags in a dictionary, their frequencies as the value
                    all_tags_n_counts[word_tag[1]] = 0
                all_tags_n_counts[word_tag[1]] = all_tags_n_counts[word_tag[1]] + 1
                all_tags.append(word_tag[1])            #   putting all of the pos-tags in a list, including all of the duplicates
            elif word_tag in ['<s>','<\s>']:
                all_tags.append(word_tag)
                if word_tag not in all_tags_n_counts:
                    all_tags_n_counts[word_tag] = 0
                all_tags_n_counts[word_tag] = all_tags_n_counts[word_tag] + 1


#   Creating the transition probability matrix (A):
#   Calculating the probability of a certain tag occurring after another tag, 
#   For instance, Pr(VERB|NOUN) (basically, calculating bigram probabilities).


pos_tag_bigrams = {}    #   will hold raw counts of pos-bigrams

for i in range(len(all_tags)-1):
    pos_bigram = all_tags[i],all_tags[i+1]
    if pos_bigram not in pos_tag_bigrams:
        pos_tag_bigrams[pos_bigram] = 0
    pos_tag_bigrams[pos_bigram] = pos_tag_bigrams[pos_bigram] + 1


#   Calculating the emission probabilities (B):
#   Starting by getting the counts of all the word-tags in the corpus.
#   Then, we can calculate the emission probabilities, for example Pr('you|PRON') 


word_tags_n_counts = {}         #   raw counts of the word-tag frequencies in the corpus

with open ('pos_training_data.toks_tags', encoding="utf8") as ann_corpus:
    for sentence in ann_corpus:
        sentence = list(sentence.split())
        for word_tag in sentence:
            word,tag = word_tag.split('|')
            word = word.lower()             #   lowercasing the corpus words but leaving the tags as they are (capital letters)
            word_tag = (tag,word)   
            if word_tag not in word_tags_n_counts:      #   adding the word-tag-instances in our raw count dictionary 
                word_tags_n_counts[word_tag] = 0
            word_tags_n_counts[word_tag] = word_tags_n_counts[word_tag] + 1

#instantiation of the objects

A_transition_probability_matrix = LogCondPr(pos_tag_bigrams)
B_emission_probability_matrix = LogCondPr(word_tags_n_counts)

if __name__ == '__main__':

#   Running the code and providing the five examples:
            
#   for POS-tag-POS-tags (transitions):
            
    test1 = A_transition_probability_matrix[('NOUN', 'VERB')]   #   the log prob of VERB given NOUN, notice the inversed order in 'logic notation'
    test2 = A_transition_probability_matrix[('VERB', 'NOUN')]   #   the log prob of NOUN given VERB, notice the inversed order in 'logic notation'
    test3 = A_transition_probability_matrix[('NOUN', 'PRON')]   #   the log prob of PRON given NOUN, notice the inversed order in 'logic notation'
    test4 = A_transition_probability_matrix[('NOUN', 'NOUN')]   #   the log prob of NOUN given NOUN, notice the inversed order in 'logic notation'
    test5 = A_transition_probability_matrix[('DET', 'NOUN')]    #   the log prob of NOUN given DET, notice the inversed order in 'logic notation'
    print("the log prob of VERB given NOUN",test1)
    print("the log prob of NOUN given VERB",test2)
    print("the log prob of PRON given NOUN",test3)
    print("the log prob of NOUN given NOUN", test4)
    print("the log prob of NOUN given DET",test5)

#   for word-POS-tags (emissions):

    test6 = B_emission_probability_matrix[('VERB', 'sandwich')]           #   the log prob of 'sandwich' given VERB, notice the inversed order in 'logic notation'
    test7 = B_emission_probability_matrix[('VERB', 'said')]            #   the log prob of 'said' given VERB, notice the inversed order in 'logic notation'
    test8 = B_emission_probability_matrix[('DET', 'the')]          #   the log prob of 'the' given DET, notice the inversed order in 'logic notation'
    test9 = B_emission_probability_matrix[('VERB', 'showing')]            #   the log prob of 'showing' given VERB, notice the inversed order in 'logic notation'
    test10 = B_emission_probability_matrix[('PRON', 'you')]          #   the log prob of 'you' given PRON, notice the inversed order in 'logic notation'
    print("the log prob of 'sandwich' given VERB", test6)
    print("the log prob of 'said' given VERB", test7)
    print("the log prob of 'the' given DET", test8)
    print("the log prob of 'showing' given VERB", test9)
    print("the log prob of 'you' given PRON", test10)

