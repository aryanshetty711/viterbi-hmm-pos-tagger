from __future__ import division
from collections import defaultdict
import math
import sys
import string

uncharted = ['UNK_adj','UNK_adv','UNK_cap_noun','UNK_digit', 'UNK','UNK_noun','UNK_verb','UNK_punct',]
end_ver = ['ize',  'ate',  'ify','ise','fy']

end_adj = ['ible', 'ous',    'lly', 'ly', 'ive', 'sy', 'ish', 'esque', 'i','ian', 'able','ful', 'al']
end_adv = ['ily', 'ly', 'wards', 'wise',  'ward','ally']

end_nou = ['hood', 'er', 'dom', 'ism', 'ance', 'ence', 'or', 'scape','ity', 'ment', 'ling', 'ure','ery', 'ation', 'ship',  'ry', 'action',  'cy', 'ist','ion', 'al', 'age', ]
PUNCT = set(string.punctuation)

def viterbi_impl(num_prov, notice, main_space, emi_p, choice):
    first_notif = {}
    total_s = len(notice)

    for (index, val) in enumerate(main_space):
        first_notif[val] = index



    v_arr = []
    for i in range(num_prov):
        v_arr.append([0]*total_s)
    for j in range(num_prov):

        if us_all[beg_find][j] != 0:
            ob_part = math.log(int_arr[j][one_occur])
            bru_part = math.log(us_all[beg_find][j])
            final_val = ob_part + bru_part
            v_arr[j][0] = final_val
        else:
            v_arr[j][0] = -sys.maxsize
    b_arr = []
    for i in range(num_prov):
        b_arr.append([None]*total_s)
    for j in range (num_prov):
        b_arr[j][0] = 0

    for l in range(1, total_s):
        notif_val = first_notif[notice[l]]
        for mp in range(num_prov):
            high_road = None
            max_prob = -sys.maxsize

            for pm in range(num_prov):
                log_part = math.log(int_arr[mp][notif_val])
                viterbi_part = v_arr[pm][l - 1]
                us_all_bit = math.log(us_all[pm][mp])
                bwean_prob = log_part + viterbi_part + us_all_bit

                if bwean_prob > max_prob:
                    max_prob = bwean_prob
                    high_road = pm

                b_arr[mp][l] = high_road
                v_arr[mp][l] = max_prob
    if choice =='v':
        return v_arr
    elif choice == 'b':
        return b_arr

def final_step(v_arr, b_arr, total_s, num_prov):
    s_processor = total_s * [None]
    prob_arr = v_arr[0][total_s - 1]
    ans = total_s * [None]



    for i in range(1, num_prov):
        s_processor[total_s - 1] = i
        if v_arr[i][total_s - 1] <= prob_arr:
            flag = True
        else:
            prob_arr = v_arr[i][total_s - 1]


    ans[total_s - 1] = scene_kya[s_processor[total_s - 1]]

    for j in range(total_s - 1, 0, -1):
        s_processor[j - 1] = b_arr[s_processor[j]][j]
        ans[j - 1] = scene_kya[s_processor[j - 1]]
    return ans

def assign_UNK(text):

    for i in end_nou:
        if text.endswith(i):
            return 'UNK_noun'

    for i in end_adv:
        if text.endswith(i):
            return 'UNK_adv'


    for i in text:
        if i in PUNCT:
            return 'UNK_punct'


    for i in text:
        if i.isdigit()==True:
            return 'UNK_digit'


    for i in text:
        if i.isupper()==True:
            return 'UNK_cap_noun'

    if text[0].isupper == True:
        if '-' in text:
            return 'UNK_cap_noun'


    for i in end_adj:
        if text.endswith(i):
            return 'UNK_adj'

    for i in end_ver:
        if text.endswith(i):
            return 'UNK_verb'

    return 'UNK'

def processor(keys, dictionary, t_e, seshu, choice):
    key_l = len(keys)
    d_l = len(dictionary)
    if choice == "match":

        us_all = [key_l * [0] for i in range(key_l)]

        for i in range(len(keys)):
            for j in range(len(keys)):
                back = keys[i]
                val = keys[j]
                track = 0
                if back in t_e:
                    if tag in t_e[back]:
                        track = t_e[back][val]
                num = track + seshu
                div = (num_hits[back] + (key_l * seshu)  )
                final_val = num / div

                us_all[i][j] = final_val
        return us_all

    elif choice == 'lexicon':
        int_arr = [d_l * [0] for i in range(key_l)]
        for i in range(key_l):
            for j in range(d_l):
                val = keys[i]
                wrd = dictionary[j]
                track = 0
                if wrd not in t_e[val]:
                    flag = False
                else:
                    track = t_e[val][wrd]
                num = track + seshu
                div = ( num_hits[val]+(d_l * seshu))
                final_val = num / div
                int_arr[i][j] = final_val

        return int_arr

num_words = defaultdict(int)
num_hits = defaultdict(int)

switch = defaultdict(lambda : defaultdict(int))
j_s = defaultdict(lambda : defaultdict(int))

with open(sys.argv[1], 'r') as input:
    for sentence in input:
        if sentence.split():
            (word, tag) = sentence.split()
            num_words[word] += 1

    input.seek(0)
    word_list = []
    for (hash, inside) in num_words.items():
        if inside<=1:
            continue
        else:
            word_list.append(hash)


    word_list.extend(uncharted)
    word_list.append('<n>')
    word_list = sorted(word_list)
    dictionary = word_list
    word_set = set(dictionary)

    old = '<s>'
    for sentence in input:
        if not sentence.split():
            info = '<n>'
            hit = '<s>'
        else:
            (info, hit) = sentence.split()
            num_words[info] += 1
            if info in word_set:
                flag = True
            else:
                word = assign_UNK(info)
        switch[old][hit] += 1
        old = hit
        num_hits[hit] += 1
        j_s[hit][info] += 1


keys = sorted(num_hits.keys())
key_l = len(keys)


us_all = processor(keys, [],switch,0.001,"match")


d_l = len(dictionary)
int_arr = processor(keys, dictionary, j_s, 0.001, "lexicon")


input.close()

flag = False
done_checking = []
bwean = []
with open(sys.argv[2], 'r') as test_material:

    for sentence in test_material:
        word = sentence.strip()
        bwean.append(sentence.strip())
        if sentence.split():
            if sentence.strip() in word_set:
                flag = True
            else:
                word = assign_UNK(sentence.strip())
            done_checking.append(word)

        else:
            done_checking.append('<n>')

test_material.close()

main_space = dictionary
scene_kya = keys
num_prov = len(scene_kya)
first_notif = {}
notice = done_checking
us_all = us_all
int_arr = int_arr



for (j, k) in enumerate(main_space):
    the_obs = k
    index = j
    first_notif[the_obs] = index

beg_find = scene_kya.index('<s>')
one_occur = first_notif[notice[0]]
total_s = len(notice)




v_arr = viterbi_impl(num_prov, notice,main_space, int_arr, 'v' )
b_arr = viterbi_impl(num_prov, notice,main_space, int_arr, 'b' )



ans = final_step(v_arr, b_arr, total_s, num_prov)

with open('submission.pos', 'w') as final:
    for (info, hit) in zip(bwean, ans):
        if info:
            final.write('{0}\t{1}\n'.format(info, hit))

        elif not word:
            final.write('\n')
