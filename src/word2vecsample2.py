from gensim.models import word2vec
import logging
import sys
import time


"""
http://swdrsker.hatenablog.com/entry/2017/02/23/193137
"""
model = word2vec.Word2Vec.load("../models/ja_wiki.model")

def neighbor_word(posi, nega=[], n=10):
    count = 1
    result = model.most_similar(positive = posi, negative = nega, topn = n)
    print('--------------------------------------')
    print('NO\t|word\t|distance\t')
    print('--------------------------------------')
    for r in result:
        print(str(count)+"\t|"+str(r[0])+"\t|"+str(r[1]))
        count += 1
    print('--------------------------------------')

def calc(equation):
    if "+" not in equation or "-" not in equation:
        neighbor_word([equation])
    else:
        posi,nega = [],[]
        positives = equation.split("+")
        for positive in positives:
            negatives = positive.split("-")
            posi.append(negatives[0])
            nega = nega + negatives[1:]
        neighbor_word(posi = posi, nega = nega)

if __name__=="__main__":
    start_t = time.perf_counter()

    equation = sys.argv[1]
    calc(equation)

    end_t = time.perf_counter()
    process_time = end_t - start_t
    print('処理時間は:{0}秒です。'.format(process_time))
