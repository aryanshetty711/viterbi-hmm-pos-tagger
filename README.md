combined.pos = WSJ_02-21.pos + WSJ_24.pos

How to run the code:
In the terminal, type the following,

	python3 hmm_tagger.py train_data.pos test_data.words

The python file will automatically output a file called "submission.pos"

I create unknown words for noun, adj, adv, and verb to deal with OOV, they have to appeare more than once to avoid being considered as unknown words.

The program uses bigram hidden markov model and viterbi algorithm to decode and tag the test data.
