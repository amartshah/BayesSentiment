# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re, nltk
punctuation_stopwords = [" ", ".", '"', ",", "?", "!", "/", "'", "-", "_", ";", ":", "&","<",">", ',"', '",', ")", "(", "://", "/"]

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      self.poswordsfreq = dict()
      self.negwordsfreq = dict()
      self.total_negative = 0
      self.total_positive = 0
      if os.path.isfile('positive_words_best.txt') == False:
         self.train()
         self.save(self.poswordsfreq,"positive_words_best.txt")
         self.save(self.negwordsfreq,"negative_words_best.txt")
      else:
         self.poswordsfreq = self.load("positive_words_best.txt")
         self.negwordsfreq = self.load("negative_words_best.txt")
         self.total_negative = self.total_negative_words()
         self.total_positive = self.total_positive_words()

      # if os.path.isfile('negative_words.txt') == False:
      #    print "training"
      #    self.train()
      #    self.save(self.negwordsfreq,"negative_words.txt")
      # else:
      #    self.negwordsfreq = self.load("negative_words.txt") 

   def loop_files(self):
      lFileList = []
      for fFileObj in os.walk("reviews/"):
         lFileList = fFileObj[2]
         break
      return lFileList

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""
      # lFileList = self.loop_files()

      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break

      #flag will be -1 for a negative word
      #flag will be 1 for a positive word
      for sFilename in lFileList:
         if sFilename[7] == '5':
            file = self.loadFile('movies_reviews/' + sFilename)
            tokens = self.tokenize(file)
            bigrams_text = nltk.bigrams(tokens)
            
            for (w,x) in bigrams_text:
               if w.lower() not in punctuation_stopwords and x.lower() not in punctuation_stopwords:
                  if (w.lower(), x.lower()) not in self.poswordsfreq:
                     self.poswordsfreq[(w.lower(), x.lower())] = 1
                     self.total_positive = 1
                  else:
                     self.poswordsfreq[(w.lower(), x.lower())]+= 1
                     self.total_positive += 1

         elif sFilename[7] == '1':
            file = self.loadFile('movies_reviews/' + sFilename)
            print file
            tokens = self.tokenize(file)
            bigrams_text = nltk.bigrams(tokens)
            print bigrams_text
            for (w,x) in bigrams_text:
               if w.lower() not in punctuation_stopwords and x.lower() not in punctuation_stopwords:
                  print sFilename
                  if (w.lower(), x.lower()) not in self.negwordsfreq:
                     self.negwordsfreq[(w.lower(), x.lower())] = 1
                     self.total_negative = 1
                  else:
                     self.negwordsfreq[(w.lower(), x.lower())]+= 1
                     self.total_negative += 1
      
   def train2(self, lFileList):   
      """Trains the Naive Bayes Sentiment Classifier."""


      #flag will be -1 for a negative word
      #flag will be 1 for a positive word
      for sFilename in lFileList:
         if sFilename[7] == '5':
            for w in self.tokenize(self.loadFile('movies_reviews/' + sFilename)):
               if w.lower() not in punctuation_stopwords:
                  if w.lower() not in self.poswordsfreq:
                     self.poswordsfreq[w.lower()] = 1
                     self.total_positive = 1
                  else:
                     self.poswordsfreq[w.lower()]+= 1
                     self.total_positive += 1

         elif sFilename[7] == '1':
            for w in self.tokenize(self.loadFile('movies_reviews/' + sFilename)):
               if w.lower() not in punctuation_stopwords:
                  print sFilename
                  if w.lower() not in self.negwordsfreq:
                     self.negwordsfreq[w.lower()] = 1
                     self.total_negative = 1
                  else:
                     self.negwordsfreq[w.lower()]+= 1
                     self.total_negative += 1
   

   def total_positive_words(self):
      counter = 0
      for key in self.poswordsfreq:
         counter = counter + self.poswordsfreq[key]
      self.total_positive = counter
      return self.total_positive

   def total_negative_words(self):
      counter = 0
      for key in self.negwordsfreq:
         counter = counter + self.negwordsfreq[key]
      self.total_negative = counter
      return self.total_negative

   def cross_validation(self, nfold):
      all_files = self.loop_files()
      portion = len(all_files)/nfold #finding a tenth (or n-th) of the data to keep as testing



      #still need to account for the remainder when divided by 10

      for i in range(nfold):
         if i == nfold-1:
            test = all_files[i*portion:] # test files from the last set, ranging from starting position of the portion to the end of the set
                                         # this absorbs the remainder
            train = all_files[:i*portion] # train files all files before the test set

         elif i == 0:
            test = all_files[i*portion:(i+1)*portion] #setting the test portion from next set of length portion
            train = all_files[portion+1:] # setting train set to be everything after the first portion test set

         else:
            test = all_files[i*portion:(i+1)*portion] #setting the test portion from next set of length portion
            train = all_files[:i*portion] + all_files[(i+1)*portion:]

         self.validate(test,train)


###REALIZED THAT WE PROBABLY DONT NEED THIS
   def separate_pos_neg_files(self, test, train):
      pos_train = []
      neg_train = []
      neutral_train = []

      ## Separate files into positive negative and neutral train sets

      for i in train:
         if self.classify(self.loadFile(i)) == 'positive':
            pos_train.append(i)

         elif self.classify(self.loadFile(i)) == 'negative':
            neg_train.append(i)

         else:
            neutral_train.append(i)

      validate(self, test, pos_train, neg_train, neutral_train) #validate test set against train sets

   def validate(self, test, train):
      self.train2(train)
      sentiments =[]
      for i in test:
         file_text = self.loadFile(i)
         sentiments.append(self.classify(file_text))

      # compare the sentiments of those files to what we already had them classified as!!


   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      # set prior probability to
      pos_cond_prob = math.log10(11129.0/(2735.0 + 11129.0))
      neg_cond_prob = math.log10(2735.0/(2735.0 + 11129.0))
      #number of negative files is 2735
      #number of positive files is 11129
      file_words = self.tokenize(sText)
      bigrams_text = nltk.bigrams(file_words)
    
      for w, v in bigrams_text:
         if w.lower() not in punctuation_stopwords and v.lower() not in punctuation_stopwords and (w.lower(), v.lower()) in self.poswordsfreq:
            pos_prob_word = float(self.poswordsfreq[(w.lower(), v.lower())] + 1)/self.total_positive
            pos_cond_prob = pos_cond_prob + math.log10(pos_prob_word)
         else:
            pos_cond_prob += math.log10(1.0/self.total_positive)

      for w,v in bigrams_text:
         if w.lower() not in punctuation_stopwords and v.lower() not in self.negwordsfreq and (w.lower(), v.lower()) in self.negwordsfreq:
            neg_prob_word = float(self.negwordsfreq[(w.lower(), v.lower())] + 1)/self.total_negative
            neg_cond_prob = neg_cond_prob + math.log10(neg_prob_word)
         else:
            neg_cond_prob += math.log10(1.0/self.total_negative)
      

      print pos_cond_prob
      print neg_cond_prob
      print abs(pos_cond_prob-neg_cond_prob)
      if (abs(pos_cond_prob-neg_cond_prob) < .5):
         print "neutral"
         return "neutral"
      elif pos_cond_prob > neg_cond_prob:
         print "positive"
         return "positive"
      elif neg_cond_prob > pos_cond_prob:
         print "negative"
         return "negative"


   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      """Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens



b = Bayes_Classifier()