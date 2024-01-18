#   Implementing the Viterbi algorithm for HMM sequence labelling
#   Implementation with log probabilities instead of raw probabilities

from hidden_markov_model import set_of_states_Q as Q 
from hidden_markov_model import A_transition_probability_matrix as A
from hidden_markov_model import B_emission_probability_matrix as B

def VITERBI_algorithm(O,Q,A,B):     #   parameters: observations, states, transition probabilities, emission probabilities

    viterbi = {}        #   the path probability matrix, represented as a dictionnary
    backpointer = {}    #   backpointer, represented as a dictionnary
    T = len(O)          #   number of observations

    for state in Q:     #  initialization step
        viterbi[state,0] = A['<s>',state] + B[state,O[0]] 
        backpointer[state,0] = 0        #  backpointer values set to zero

    #iterating over the time steps and states

    for time_step in range(1, T):   #recursion step
        for state in Q:
            max_prob = float('-inf')
            best_prev_state = None
            for prev_state in Q:
                prob = viterbi[(prev_state, time_step-1)] + A[prev_state, state] + B[state, O[time_step]]    #  retrieves log-probability, sums to the transmission log prob and the emission log prob
                if prob > max_prob:
                    max_prob = prob
                    best_prev_state = prev_state
            viterbi[(state, time_step)] = max_prob   #  will look something like this: {('SCONJ', 1): -16.553503032866555, ('PRON', 1): -inf, ('VERB', 1): -inf, ('NOUN', 1): -15.824465801020077, ('ADP', 1): -inf...}
            backpointer[(state, time_step)] = best_prev_state # will look something like this: {('SCONJ', 1): 'PRON', ('PRON', 1): None, ('VERB', 1): None, ('NOUN', 1): 'PRON'...}


    #saving the the most likely states in 'best_path', the probability of this state-sequence will be assigned to 'bestpathprob' (using addition due  to log-space):

    best_path = []
    threshold = float("-inf")
    bestpathprob = 0.0

    #   First, adding the last state in our best_path-list:

    for state in Q:
        prob = viterbi[state, T-1]          #   considering that for example 6 tokens == len(T) == 7. Gets the log probability from Viterbi dictionnary
        if prob > threshold:
            threshold = prob
            prev_state = state
            best_path.append(prev_state)     # appending the last state of O into best_path, in our examples it is always 'PUNCT', at this point 'best_path' only holds 'PUNCT'

    #   Iterating over the time_steps (lenght of observations):

    for time_step in range(T-1,0,-1):   #   negative step size since we go from the end to the start 6,5,4,3,2,1...(0 not needed bc that index doesn't have a previous state?)
        path_prob = viterbi[(prev_state, time_step)]
        bestpathprob = bestpathprob + path_prob
        prev_state = backpointer[(prev_state, time_step)]     # retrieving the value for this key from backpointer (i.e. ('PUNCT', 6) retrieves the value 'NOUN')
        best_path.append(prev_state)
    best_path.reverse()


    return best_path,bestpathprob


if __name__ == '__main__':

    O1 = ['they', 'will', 'hopefully', 'back', 'the', 'bill', '.']
    O2 = ['morning', 'coffee', 'warms', 'my', 'tired', 'soul','.']
    O3 = ['this', 'time',',', 'she', 'might', 'win', '.']

    print(VITERBI_algorithm(O1,Q,A,B))          
    print(VITERBI_algorithm(O2,Q,A,B))          #with these example sentences POS-tagging accuracy is 95%
    print(VITERBI_algorithm(O3,Q,A,B))

