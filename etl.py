import re
import string
special = {
    '&nbsp;' : ' ', '&amp;' : '&', '&quot;' : '"',
    '&lt;'   : '<', '&gt;'  : '>'
}
def cleanText(raw_html):
  cleanweb = re.compile('<.*?>')
  cleanhashtag = re.compile('#')
  cleantext = re.sub(cleanweb, '', raw_html) ##remove HTML
  for (k,v) in special.items(): ## remove spacial Char
    cleantext = cleantext.replace(k,v)
  cleantext = re.sub(cleanhashtag,'',cleantext) ## remove hashtag
  for c in string.punctuation:
    cleantext = re.sub(r'\{}'.format(c),'',cleantext) # clean punctuation char
  cleantext = ' '.join(cleantext.split())

  # Remove EMOJI
  RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
  cleantext = RE_EMOJI.sub(r'', cleantext)
  return cleantext

import pythainlp
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.corpus import wordnet
from nltk.stem.porter import PorterStemmer #lovis
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from stop_words import get_stop_words
en_stop = tuple(get_stop_words('en'))
import nltk

from attacut import tokenize, Tokenizer

def tokenization2(text,engine="attacut"):
  tokens = word_tokenize(text,engine=engine, keep_whitespace=False)
  tokens = [i for i in tokens if not i in thai_stopwords() and not i in en_stop]
  # Thai
  tokens_temp=[]
  for i in tokens:
      w_syn = wordnet.synsets(i)
      if (len(w_syn)>0) and (len(w_syn[0].lemma_names('tha'))>0):
          tokens_temp.append(w_syn[0].lemma_names('tha')[0])
      else:
          tokens_temp.append(i)
    
  tokens = tokens_temp
  # ลบตัวเลข
  tokens = [i for i in tokens if not i.isnumeric()]
  # ลบช่องว่าง
  tokens = [i for i in tokens if not ' ' in i]
  # print(tokens)
  return tokens
