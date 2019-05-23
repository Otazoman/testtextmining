from gensim.models import word2vec
import sys

word = sys.argv[1]
model = word2vec.Word2Vec.load("../copas/ja_wiki.model")
results = model.wv.most_similar(positive=[word])
for result in results:
    print(result)
