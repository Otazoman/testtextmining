from gensim.models import word2vec
import sys
import time
import traceback


def comp_words(model,word1,word2):
    """
    与えられた複数の言葉の近似値を比較する
    """
    try:
         r = model.similarity(word1, word2)
         if r:
            return r
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def get_similor_word(model,word):
    """
    与えられた単語の類義語を調べる
    """
    try:
        r = model.wv.most_similar(positive=[word])
        if r:
           return r
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

def main():
    """
    主処理
    引数が1つの場合は類義語とベクトル値表示
    引数が複数の場合は比較単語と数値を表示

    """
    try:
        argvs = sys.argv
        num = len(argvs)
        model = word2vec.Word2Vec.load("../corpas/ja_wiki.model")
        
        start_t = time.perf_counter()

        if num == 2: 
           words = get_similor_word(model,sys.argv[1])
           print('-------------------------------------')
           print('word \t\t |cos_distance')
           print('-------------------------------------')
           for w in words:
               print("{0}\t |{1}".format(w[0],w[1]))
           print('-------------------------------------')
        else:
           print('-------------------------------------')
           print('word1\t|word2\t|cos_distance')
           print('-------------------------------------')
           for i in range(2,num):
               rcos =comp_words(model,sys.argv[1],sys.argv[i])
               print("{0}\t|{1}\t|{2}".format(sys.argv[1],sys.argv[i],rcos))
           print('-------------------------------------')

        end_t = time.perf_counter()
        process_time = end_t - start_t
        print('処理時間は:{0}秒です。'.format(process_time))
    except Exception as e:
        t, v, tb = sys.exc_info()
        print(traceback.format_exception(t,v,tb))
        print(traceback.format_tb(e.__traceback__))

if __name__ == '__main__':
   main()
