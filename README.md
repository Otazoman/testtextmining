TextMining test tool(mecab and Cabocha)
====

Japanese Text Mining Test

## Description
このツールはテキストマイニングのサンプルとして作成したツールです。
RSSフィードを取得して、形態素解析して出力するという様な内容を想定しています。

python初心者な上にGitやプログラムそのものも初心者なので至らぬ点が
多いかと思いますがその場合はご指摘いただけると幸いです。

## Requirement
mecab  
mecab-ipadic-utf8  
libmecab-dev python-mecab  
python-pip   
python3-pip  
CRF++-0.58  
swig  
cabocha-0.69  
fonts-ipaexfont  
nkf

pip  
mecab-python3  
feedparser  
neologdn  
numpy  
matplotlib  
pandas  
scipy  
scikit_learn  
tensorflow  
wordcloud  
pillow  
gensim
wikipedia2vec
emoji


## Usage
$ python3 mecabsample.py inputfilename outputname  
$ python3 wordcloudsample.py inputfilename outputname   
$ python3 getrssfeed.py feedlistfilename outputfilename  
$ python3 word2vecsample1.py word

## Environment Setup
$ sudo apt-get -y install mecab mecab-ipadic-utf8 libmecab-dev python-mecab  
$ sudo apt-get -y install python-pip python3-pip  
$ sudo apt -y install swig  
$ sudo pip3 install mecab-python3  
$ wget -O CRF++-0.58.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ"  
$ tar xvzf CRF++-0.58.tar.gz  
$ cd CRF++-0.58  
$ vim node.cpp   
	#include <stdlib.h>  
	#include <cmath>  
	#include <time.h>	←Added  
	#include "node.h"  
	#include "common.h"    
$ ./configure  
$ make  
$ make check  
$ sudo make install  
$ wget "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" -O cabocha.tar.bz2  
$ bzip2 -dc cabocha.tar.bz2 | tar xvf -  
$ cd cabocha-0.69/  
$ ./configure --with-mecab-config=`which mecab-config` --with-charset=utf8 --enable-utf8-only  
$ sudo ldconfig  
$ make  
$ make check  
$ sudo make install  
$ sudo ldconfig  
$ cd python/  
$ sudo python3 setup.py install  
$ cd  
$ rm -Rf CRF*  
$ rm -Rf cabocha*  
$ sudo apt -y install fonts-ipaexfont  
$ sudo apt-get -y install nkf
$ mkdir corpas
$ cd corpas
$ curl https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 -o jawiki-latest-pages-articles.xml.bz2
$ git clone https://github.com/attardi/wikiextractor
$ python3 wikiextractor/WikiExtractor.py jawiki-latest-pages-articles.xml.bz2
$ python3 ../src/datacleaning.py text
$ cat text/*/* > jawiki.txt
$ mecab -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd -Owakati jawiki.txt -o data.txt -b 16384
$ nkf -w --overwrite data.txt
$ python3 ../src/modelmake.py



## Library Install
$ pip3 install neologdn  
$ pip3 install numpy  
$ pip3 install matplotlib  
$ pip3 install pandas  
$ pip3 install scipy  
$ pip3 install scikit_learn  
$ pip3 install tensorflow  
$ pip3 install wordcloud  
$ pip3 install pillow  
$ pip3 install feedparser 
$ pip3 install gensim
$ pip3 install wikipedia2vec
$ pip3 install neologdn
$ pip3 install emoji 
