from gensim.models import word2vec
import sys
import time

word = sys.argv[1]

start_t = time.perf_counter()

model = word2vec.Word2Vec.load("../corpas/ja_wiki.model")
results = model.wv.most_similar(positive=[word])
print('-------------------------------------')
print('word \t\t |distance')
print('-------------------------------------')
for result in results:
    print("{0}\t |{1}".format(result[0],result[1]))

print('-------------------------------------')
end_t = time.perf_counter()
process_time = end_t - start_t
print('処理時間は:{0}秒です。'.format(process_time))
