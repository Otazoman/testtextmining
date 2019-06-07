from gensim.models import word2vec
import logging
import sys

"""
第一引数に対象のテキストファイルを指定し第2引数に出力モデルファイルを指定
"""
inputfile = sys.argv[1]
outputmodel = sys.argv[2]

try:
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                        level=logging.INFO)
    sentences = word2vec.Text8Corpus(inputfile)

    #model = word2vec.Word2Vec(sentences, size=200, min_count=20, window=15)
    model = word2vec.Word2Vec(sentences, size=200, min_count=2, window=5, 
                              iter=4000)
    model.save(outputmodel)
except Exception as e:
       t, v, tb = sys.exc_info()
       print(traceback.format_exception(t,v,tb))
       print(traceback.format_tb(e.__traceback__))
