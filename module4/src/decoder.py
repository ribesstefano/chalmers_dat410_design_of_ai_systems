from language_model import language_model
from translation_model import train_language_model, get_prob
from warmup import get_word_counter, get_bigram_counter

import os
import re
from math import log
import codecs
import operator

from operator import itemgetter

def decoder(src_sentence, target_word_cnt, src_word_cnt, target_bigram_cnt,
        src_bigram_cnt, beam_size=3, prob_table=None, alpha=0.7, verbose=0):
    # NOTE: Since we are dealing with log probabilities, the beam search
    # will favour shorter sentence. Because of that, we introduce a
    # normalization factor over the length of the candidate sentence.
    def get_len(sentence):
        length = 0
        for word in sentence:
            if word != 'EOS' and word != 'NULL':
                length += 1
            else:
                break
        return length

    candidate_sentences = []

    target_dict = list(target_word_cnt)
    src_dict = list(src_word_cnt)

    if prob_table is None:
        prob_table = train_language_model(target_dict, src_dict, verbose=verbose-1)

    # NOTE: Assuming target sentence length <= source sentence length.
    for i, src_word in enumerate(src_sentence):
        p_fe = [0] * beam_size
        prob = {}
        for j in range(beam_size):
            # For each candidate sentence, calculate its translation probability
            # for the translated words so far.
            if i != 0:
                for k, target_word in enumerate(candidate_sentences[j]):
                    p_fe[j] += log(get_prob(prob_table, src_sentence[k], target_word))
            # Now loop over all possible target words and calculate the new prob
            for target_word in target_dict:
                if i == 0:
                    # NOTE: candidate_sentences is still empty
                    word_list = [target_word]
                    sentence = target_word
                else:
                    word_list = candidate_sentences[j] + [target_word]
                    sentence = ''.join([w + ' ' for w in word_list])[:-1]
                # Get probabilities from the models.
                p_e = language_model(word_list, target_word_cnt, target_bigram_cnt)
                p_fe_curr = p_fe[j] + log(get_prob(prob_table, src_word, target_word))
                # Update the database of candidate sentences and their prob.
                prob[sentence] = (p_e + p_fe_curr) / (get_len(word_list)**alpha)
        # Sort the sentences according to the highest probabilities.
        best_sentences = dict(sorted(prob.items(), key=lambda item: item[1], reverse=True))
        best_sentences = list(best_sentences.keys())[:beam_size]
        # Create a list of sentences, i.e. list of words, for the updated
        # candidate translated senteces.
        candidate_sentences = [[w for w in s.split(' ')] for s in best_sentences]
    return candidate_sentences

def main():
    lang = 'sv'
    lang = 'de'
    lang = 'fr'
    src_sentence = {}
    src_sentence['sv'] = 'Jag vill säga någonting'.lower()
    src_sentence['fr'] = 'je veux dire quelque chose'.lower()
    src_sentence['de'] = 'Ich möchte etwas sagen'.lower()

    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    e_path = os.path.join(data_dir, 'europarl-v7.' + lang + '-en.lc.en')
    f_path = os.path.join(data_dir, 'europarl-v7.' + lang + '-en.lc.' + lang)

    e_word_cnt = get_word_counter(e_path)
    f_word_cnt = get_word_counter(f_path)

    e_bigram_cnt = get_bigram_counter(e_path)
    f_bigram_cnt = get_bigram_counter(f_path)

    candidate_sentences = decoder(src_sentence[lang].split(' '), e_word_cnt,
                                  f_word_cnt, e_bigram_cnt, f_bigram_cnt,
                                  beam_size=5, alpha=0.9, verbose=0)

    print(f'INFO. Original sentence: "{src_sentence[lang]}"')
    for i, sentence in enumerate(candidate_sentences):
        s = ''.join([w + ' ' for w in sentence if w != 'NULL'])[:-1]
        print(f'INFO. Translated candidate sentence n.{i}: "{s}"')

if __name__ == '__main__':
    main()