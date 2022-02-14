from language_model import language_model
from translation_model import train, get_prob
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
            if word != 'EOS':
                length += 1
            else:
                break
        return length

    candidate_sentences = []

    target_dict = list(target_word_cnt)
    src_dict = list(src_word_cnt)

    if prob_table is None:
        prob_table = train(target_dict, src_dict, verbose=verbose-1)

    # NOTE: Assuming target sentence length <= source sentence length.
    for i, src_word in enumerate(src_sentence):

        p_fe = [0] * beam_size
        prob = {}
        for j in range(beam_size):
            # For each candidate sentence, calculate its translation probability
            if i != 0:
                for k, target_word in enumerate(candidate_sentences[j]):
                    p_fe[j] += log(get_prob(prob_table, src_sentence[k], target_word))
            # Now loop over all possible target words and calculate the new prob
            for target_word in target_dict:
                if i == 0:
                    # NOTE: The assumption is that 'candidate_sentences' is empty
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

        # Version n.1
        # probs = get_best_words(prob_table, src_word)
        # if probs != []:
        #     for j in range(min(len(probs), beam_size)):
        #         # Get probability and word from the translation model.
        #         (_, word), p_fe = probs[j]
        #         # print(f'P({src_word}|{word}) = {best_prob}')
        #         if i == 0:
        #             word_list = [word]
        #             sentence = word
        #         else:
        #             word_list = candidate_sentences[j] + [word]
        #             sentence = ''.join([w + ' ' for w in word_list])[:-1]

        #         p_e = language_model(word_list, target_word_cnt, target_bigram_cnt, use_log=False)
        #         # Update the database of candidate sentences and their prob.
        #         beam_probs[sentence] = (p_e * p_fe) / (get_len(word_list)**alpha)

        #     # Sort the sentences according to the highest probabilities.
        #     best_sentences = dict(sorted(beam_probs.items(), key=lambda item: item[1], reverse=True))
        #     best_sentences = list(best_sentences.keys())[:beam_size]
        #     # Create a list of sentences, i.e. list of words, for the updated
        #     # candidate translated senteces.
        #     candidate_sentences = [[w for w in s.split(' ')] for s in best_sentences]
        #     if verbose > 0:
        #         for j in range(beam_size):
        #             print(f'DEBUG. Candidate n.{j} at step n.{i}: {candidate_sentences[j]}')
        # else:
        #     word, best_prob = '', []

        # Version n.0
        # prob = {}
        # for j in range(beam_size):
        #     for word in target_dict:
        #         if word != 'EOS' or i != 0:
        #             # NOTE: The assumption is that we are ignoring EOS at the
        #             # firststep, and so 'candidate_sentences' is empty
        #             if i == 0:
        #                 word_list = [word]
        #                 sentence = word
        #             else:
        #                 word_list = candidate_sentences[j] + [word]
        #                 sentence = ''.join([w + ' ' for w in word_list])[:-1]
        #             # Get probabilities from the models.
        #             p_e = language_model(word_list, target_word_cnt, target_bigram_cnt, use_log=False)
        #             p_fe = translation_model()
        #             # Update the database of candidate sentences and their prob.
        #             prob[sentence] = (p_e * p_fe) / (get_len(word_list)**alpha)
        # # Sort the sentences according to the highest probabilities.
        # best_sentences = dict(sorted(prob.items(), key=lambda item: item[1], reverse=True))
        # best_sentences = list(best_sentences.keys())[:beam_size]
        # # Create a list of sentences, i.e. list of words, for the updated
        # # candidate translated senteces.
        # candidate_sentences = [[w for w in s.split(' ')] for s in best_sentences]
        # if verbose > 0:
        #     for j in range(beam_size):
        #         print(f'DEBUG. Candidate n.{j} at step n.{i}: {candidate_sentences[j]}')

    return candidate_sentences

def main():
    data_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
    en_path = os.path.join(data_dir, 'europarl-v7.sv-en.lc.en')
    sv_path = os.path.join(data_dir, 'europarl-v7.sv-en.lc.sv')

    en_word_cnt = get_word_counter(en_path)
    sv_word_cnt = get_word_counter(sv_path)

    en_bigram_cnt = get_bigram_counter(en_path)
    sv_bigram_cnt = get_bigram_counter(sv_path)

    src_sentence = 'Jag vet inte om det'.lower()

    candidate_sentences = decoder(src_sentence.split(' '), en_word_cnt,
                                  sv_word_cnt, en_bigram_cnt, sv_bigram_cnt,
                                  beam_size=5, alpha=0.9999, verbose=0)

    print(f'INFO. Original sentence: "{src_sentence}"')
    for i, sentence in enumerate(candidate_sentences):
        s = ''.join([w + ' ' for w in sentence if w != 'NULL'])[:-1]
        print(f'INFO. Translated candidate sentence n.{i}: "{s}"')

if __name__ == '__main__':
    main()