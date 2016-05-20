# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re
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
      if os.path.isfile('positive_words.txt') == False:
         self.train()
         self.save(self.poswordsfreq,"positive_words.txt")
         self.save(self.negwordsfreq,"negative_words.txt")
      else:
         self.poswordsfreq = self.load("positive_words.txt")
         self.negwordsfreq = self.load("negative_words.txt") 
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

   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      # set prior probability to 1 because corpus is biased
      pos_cond_prob = math.log10(11129.0/(2735.0 + 11129.0))
      neg_cond_prob = math.log10(2735.0/(2735.0 + 11129.0))
      #number of negative files is 2735
      #number of positive files is 11129

      for w in self.tokenize(sText):
         if w.lower() not in punctuation_stopwords and w.lower() in self.poswordsfreq:
            pos_prob_word = float(self.poswordsfreq[w.lower()] + 1)/self.total_positive
            pos_cond_prob = pos_cond_prob + math.log10(pos_prob_word)
         else:
            pos_cond_prob += math.log10(1.0/self.total_positive)

      for w in self.tokenize(sText):
         print self.negwordsfreq
         print sText
         if w.lower() not in punctuation_stopwords and w.lower() in self.negwordsfreq:
            neg_prob_word = float(self.negwordsfreq[w.lower()] + 1)/self.total_negative
            neg_cond_prob = neg_cond_prob + math.log10(neg_prob_word)
         else:
            neg_cond_prob += math.log10(1.0/self.total_negative)


      print pos_cond_prob
      print neg_cond_prob
      if abs((pos_cond_prob-neg_cond_prob) < .5):
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
