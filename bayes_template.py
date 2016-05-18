# Name: 
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
      self.poswordsfreq = dict()
      self.negwordsfreq = dict()

      if os.path.isFile('positive_words.txt') == False:
         self.train()
         self.save(poswordsfreq,"positive_words.txt")
      else:
         poswordsfreq = load("positive_words")

      if os.path.isFile('negative_words.txt') == False:
         self.train()
         self.save(negwordsfreq,"negative_words")
      else:
         negwordsfreq = load("negative_words.txt") 

   def loop_files(self):
      lFileList = []
      for fFileObj in os.walk("reviews/"):
         lFileList = fFileObj[2]
         break
      return lFileList

   def train(self):   
      """Trains the Naive Bayes Sentiment Classifier."""

      lFileList = self.loop_files(self)
      #flag will be -1 for a negative word
      #flag will be 1 for a positive word
      for sFilename in lFileList:
         if sFilename[7] == '5':
            for w in self.tokenize(sFilename):
               poswordsfreq[w]+= 1

         elif sFilename[7] == '1':
            for w in self.tokenize(sFilename):
               negwordsfreq[w]+= 1

      print poswordsfreq
      print negwordsfreq

    
   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """

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