print('Importing libraries...')
import os
import datetime
import time
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from progressbar import ProgressBar, Bar, ETA, Percentage
from textblob import TextBlob
dir = os.path.dirname(os.path.realpath(__file__))
content_dir = dir + '/../data/texts'
es = Elasticsearch('http://localhost:9200')
es.indices.delete(index='words', ignore=[404,400])
es.indices.delete(index='sentences', ignore=[404,400])
request_body = {
    'settings' : {
        'number_of_shards': 1,
        'number_of_replicas': 0
    },
    'mappings' : {
        '_default_':{
            '_timestamp':{
                 'enabled':'true',
                 'store':'true',
                 'path':'plugins.time_stamp.string',
                 'format':'yyyy-MM-dd HH:m:ss'
             }
         }
    }
}
es.indices.create(index='words', ignore=[400], body=request_body)
es.indices.create(index='sentences', ignore=[400], body=request_body)
from textblob_aptagger import PerceptronTagger
files = os.listdir(content_dir)
tagger = PerceptronTagger()
print('Reading files...')

for i, file in enumerate(files):
  with open(content_dir+'/'+file) as f:
    text = f.read()
    sections = text.split('SECTION ')
    pbar = ProgressBar(widgets=['  Processing book ' + str(i+1) + ' of ' + str(len(files)),' ', Bar(), ' ', Percentage(), ' ', ETA()], maxval=len(sections)).start()
    for j, section in enumerate(sections):
      s = TextBlob(section, pos_tagger=tagger)
      tags = s.tags
      sentences = s.sentences
      wordcount = 0
      sixs = []
      wixs = []
      for k, sentence in enumerate(sentences):
        words = sentence.words
        polarity = sentence.sentiment[0]
        subjectivity = sentence.sentiment[1]
        phrases = sentence.noun_phrases
        ix = {
          'book':i+1,
          'section':j+1,
          'sentence':k+1,
          'text': str(sentence),
          'polarity':polarity,
          'subjectivity':subjectivity,
          'phrases':phrases
        }
        sixs.append({
          '_id': str(i)+'.'+str(j)+'.'+str(k),
          '_index': 'sentences',
          '_type': 'sentence',
          '_source': ix
        })
        for l, word in enumerate(words):
          tag = None
          if len(tags[wordcount]) > 1 and tags[wordcount][0] == str(word):
            tag = tags[wordcount][1]
            wordcount+=1
          wix = {
            'book':i+1,
            'section':j+1,
            'sentence':k+1,
            'wordnum': l+1,
            'word': str(word),
            'tag': tag
          }
          wixs.append({
            '_id': str(i)+'.'+str(j)+'.'+str(k)+'.'+str(l),
            '_index': 'words',
            '_type': 'word',
            '_source': wix
          })
      bulk(es, sixs)
      bulk(es, wixs)
      pbar.update(j+1)
    pbar.finish()
