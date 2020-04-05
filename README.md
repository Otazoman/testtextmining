TextMining sample tool(mecab and Cabocha)
====

Japanese Text Mining sample

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
$ python3 wordcloudsample.py   
$ python3 getrssfeed.py  
$ python3 word2vecsample1.py word

## Environment Setup
### pythonインストール
$ sudo apt -y install python-pip python3-pipi  
$ sudo apt -y install zlib1g-dev libssl-dev libffi-dev jq bzip2 libbz2-dev libreadline-dev libsqlite3-dev jq  
$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv  
$ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc  
$ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc  
$ echo 'eval "$(pyenv init -)"' >> ~/.bashrc  
$ source ~/.bashrc  
$ pyenv install --list  
$ pyenv install 3.7.3  
$ pyenv install 2.7.16  
$ pyenv global 3.7.3   
$ pip install --upgrade pip  

### MeCabインストール
$ sudo apt -y install mecab libmecab-dev mecab-ipadic-utf8 mecab-jumandic-utf8 python-mecab  
$ sudo apt -y install swig fonts-ipaexfont nkf  
$ pip install mecab-python3  
$ git clone https://github.com/neologd/mecab-ipadic-neologd.git
$ cd mecab-ipadic-neologd  
$ chmod -R +x bin build diff libexec misc seed   
$ sudo bin/install-mecab-ipadic-neologd  
$ echo `mecab-config --dicdir`"/mecab-ipadic-neologd"  
/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd  
$ cd ../  

### Cabochaインストール
$ wget -O CRF++-0.58.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ"  
$ tar xvzf CRF++-0.58.tar.gz  
$ cd CRF++-0.58  
$ vim node.cpp  
  
#include <stdlib.h>  
#include   
#include <time.h>	←Added  
#include "node.h"  
#include "common.h"  
  
$ ./configure  
$ make  
$ make check  
$ sudo make install  
$ cd ../  
$ FILE_ID=0B4y35FiV1wh7SDd1Q1dUQkZQaUU  
$ FILE_NAME=cabocha-0.69.tar.bz2  
$ curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=${FILE_ID}" > /dev/null  
$ CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"    
$ curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=${FILE_ID}" -o ${FILE_NAME}  
$ bzip2 -dc cabocha-0.69.tar.bz2 | tar xvf -  
$ cd cabocha-0.69/  
$ ./configure --with-charset=utf8 --enable-utf8-only --with-mecab-config=/usr/bin/mecab-config  
$ sudo ldconfig  
$ make  
$ make check  
$ sudo make install  
$ sudo ldconfig  
$ cd python/  
$ sudo python3 setup.py install  
$ cd  
$ rm -Rf CRF*  
$ sudo rm -Rf cabocha*  

## Library Install
$ pip install --upgrade build  
$ pip install --upgrade neologdn numpy  
$ pip install --upgrade matplotlib pandas  
$ pip install --upgrade scipy scikit_learn   
$ pip install --upgrade wordcloud pillow feedparser  
$ pip install --upgrade gensim wikipedia2vec neologdn emoji  
$ pip install --upgrade tensorflow  
$ pip install --upgrade requests_oauthlib twitter requests  
$ pip install --upgrade flask furl Werkzeug Jinja2 oauth2  
$ pip install --upgrade google-api-python-client gdata  
$ pip install --upgrade tlslite oauth2client  
$ pip install --upgrade pyyaml   
$ pip install --upgrade pytrends  
$ pip install --upgrade xlwt openpyxl xlsxwriter   
$ pip install --upgrade mongo   
$ pip install --upgrade nltk     
$ pip install --upgrade TextBlob   
$ pip install --upgrade Environment    
$ pip install --upgrade sumy    
$ pip install --upgrade tinysegmenter      
$ pip install --upgrade selenium      
$ pip install --upgrade chromedriver-binary      
$ pip install --upgrade pyvirtualdisplay      



## Word2vec Pre operation  
$ sudo apt-get -y install nkf   
$ mkdir models   
$ cd models   
$ mkdir corpasdatamake   
$ cd corpasdatamake/   
$ git clone https://github.com/attardi/wikiextractor   
$ curl https://dumps.wikimedia.org/jawiki/latest/jawiki-latest-pages-articles.xml.bz2 -o jawiki-latest-pages-articles.xml.bz2   
$ python wikiextractor/WikiExtractor.py jawiki-latest-pages-articles.xml.bz2   
$ python ../../src/datacleaning.py text  
$ cat text/*/* > jawiki.txt   
$ sudo ../../mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n  
$ mecab -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd -Owakati jawiki.txt -o data.txt -b 16384   
$ nkf -w --overwrite data.txt   
$ python ../../src/modelmake.py   
 
## Chrome Install   
$ curl https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -    
$ echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list    
$ sudo apt update    
$ sudo apt -y install google-chrome-stable    

