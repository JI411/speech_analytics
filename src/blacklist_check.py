# -*- coding: utf-8 -*-
"""blacklist_check.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bARxzuGyad2iKuKP4zYQnPl80g9QVJcB
"""

# !pip install nltk
# !pip install pymorphy2

import numpy as np
import pandas as pd


import re 
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import json

from google.colab import drive
drive.mount('/content/drive')
link = '/content/drive/My Drive/Colab Notebooks/data/bl/'

class Blacklist:
  """
  На вход получает строку, метод bad_words выдаёт словаь с подсчётом слов из ЧС, 
  есть методы для обновления списка ругательств и угроз, есть метод для удаления ругательств
  """

  def __init__(self, obscene_corpus:str, threats_corpus:str, return_badwords=False):
    """
    obscene_corpus, threats_corpus - ссылки на файлы с матом и угрозами, return_badwords=True возвращает какие именно ругательства и угрозы были в речи
    """

    with open(obscene_corpus, "r", encoding='utf-8') as f:
            self.obs = set(json.load(f))
    with open(threats_corpus, "r", encoding='utf-8') as f:
            self.threats = set(json.load(f))

    self.return_badwords = return_badwords
    self.obs_link = obscene_corpus
    self.threats_link = threats_corpus

  @staticmethod
  def lemmatize(text):
      """
      Приведение слов в нормальню форму
      """
      patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
      stopwords_ru = set(stopwords.words("russian")) - set(['ты'])
      morph = MorphAnalyzer()
      tokens = []
      for token in re.sub(patterns, ' ', text.lower()).split():
        if token and token not in stopwords_ru:
          token = token.strip()
          token = morph.normal_forms(token)[0]
          tokens.append(token)
      return tokens
  

  def bad_words(self, text):
    """
    Принимает строку, возвращает словарь.
    Подсчёт слов из blacklist, obs - мат, threats - угрозы, you - обращение на "ты", cho - чо/че/чё
    """
    words = self.lemmatize(text)
    count_obs = [w for w in words if w in self.obs]
    count_threats = [w for w in words if w in self.threats]
    count_you = [w for w in words if w in set(['ты', 'твой'])]
    count_cho = [w for w in text.lower().split() if w in set(['че', 'чё', 'чо'])]

    if self.return_badwords:
      return {'obs': len(count_obs), 'threats': len(count_threats), 'you': len(count_you ), 'cho': len(count_cho)}, count_obs, count_threats
    else:
      return {'obs': len(count_obs), 'threats': len(count_threats), 'you': len(count_you ), 'cho': len(count_cho)}


  def update_obscene(self, new_text):
    """
    Добавление новых слов в мат, на вход подавать строку слов через пробел
    """
    obscene = set(self.lemmatize(new_text)) | set(new_text.split())
    self.obs |= obscene

    assert len(self.obs) != 0
    with open(self.obs_link, "w", encoding='utf-8') as f:
            json.dump(list(self.obs), f, ensure_ascii=False)

          
  def update_threats(self, new_text):
    """
    Добавление новых слов в угрозы, на вход подавать строку слов через пробел
    """
    threats = set(self.lemmatize(new_text)) | set(new_text.split())
    self.threats |= threats

    assert len(self.threats) != 0
    with open(self.threats_link, "w", encoding='utf-8') as f:
            json.dump(list(self.threats), f, ensure_ascii=False)


  def del_obscene(self, del_text):
    """
    Удаление слов из мата, на вход подавать строку слов через пробел
    """
    good = set(del_text.split())
    self.obs -= good

    assert len(self.obs) != 0
    with open(self.obs_link, "w", encoding='utf-8') as f:
            json.dump(list(self.obs), f, ensure_ascii=False)

  def del_threats(self, del_text):
    """
    Удаление слов из угроз, на вход подавать строку слов через пробел
    """
    good =  set(self.lemmatize(del_text)) | set(del_text.split())
    self.threats -= good

    assert len(self.threats) != 0
    with open(self.threats_link, "w", encoding='utf-8') as f:
            json.dump(list(self.threats), f, ensure_ascii=False)

bl = Blacklist(link + 'normal_forms_obscene_corpus.json', link + 'normal_forms_threats_corpus.json')
bl.bad_words('qewew')