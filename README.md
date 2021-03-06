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
$ pyenv install 3.7.7  
$ pyenv global 3.7.7   
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
$ cd   
#### MeCabとnltkエラー時
$ pip install unidic-lite    
$ pip install mecab-python3==0.996.5    
$ python    
import nltk    
nltk.download()    
Downloader> d    
Download which package (l=list; x=cancel)?    
  Identifier> all    
Downloader> q    
True    

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
$ python ../../src/modelmake.py data.txt jawiki.model    
 
## Chrome Install   
$ curl https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -    
$ echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list    
$ sudo apt update    
$ sudo apt -y install google-chrome-stable    

## MongoDB Install  
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4  
$ echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list  
$ sudo apt update  
$ sudo apt install -y mongodb-org  
$ mongod --version  
$ mongo --version  
$ sudo systemctl start mongod  
$ sudo systemctl enable mongod  
$ mongo  
>use databasename  
> db.createUser({user: "user",pwd: "password",roles: [{ role: "userAdmin", db: "databasename" },{ role: "dbAdmin", db: "databasename" },{ role: "readWrite", db: "databasename" }]})    
> exit
>  

$ sudo vi /etc/mongod.conf  
*added  
"""  
security:  
  authorization: enabled  
"""  
$ sudo systemctl restart mongod  
$ mongo  

> use databasename  
> db.auth("user", "password")  
### insert  
>db.databasename.insert({new_column1: 'new_value1', new_column2: 'A9991', date_column: ISODate()})
### select  
> db.databasename.find({date_column:{$lte:ISODate()}},{_id:0})  
### update  
> db.databasename.update({new_column2: /.*2$/}, {$set:{flg:'True'}}, false, true)  
> db.databasename.update({new_column2: /.*2$/}, {$set:{new_Column2:'C9992'}})  
### delete  
> db.databasename.remove({date_column:{$gte:ISODate("2019-11-14T00:00:00Z"),$lte:ISODate("2019-11-14T09:00:00Z")}})  
> db.databasename.drop()  

## WordNet  

