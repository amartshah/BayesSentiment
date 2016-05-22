# Name: asf408 (Armaan Shah), snk088 (Sonia Nigam), ats545 (Amar Shah)
# Date: 5/22/16
# Description: Assignment 4
# 
# All group members were present and contributing during all work on this project.

import math, os, pickle, re, nltk,copy
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
         lFileList = []
         for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break
         self.train(lFileList)
         self.save(self.poswordsfreq,"positive_words_best.txt")
         self.save(self.negwordsfreq,"negative_words_best.txt")
      else:
         self.poswordsfreq = self.load("positive_words_best.txt")
         self.negwordsfreq = self.load("negative_words_best.txt") 
         self.total_negative = self.total_negative_words()
         self.total_positive = self.total_positive_words()

   def loop_files(self):
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      #print len(lFileList)
      #print "all files list length ^"
      return lFileList

   def train(self, lFileList):   
      """Trains the Naive Bayes Sentiment Classifier."""
      # lFileList = self.loop_files()
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
            #print file
            tokens = self.tokenize(file)
            bigrams_text = nltk.bigrams(tokens)
            #print bigrams_text
            for (w,x) in bigrams_text:
               if w.lower() not in punctuation_stopwords and x.lower() not in punctuation_stopwords:
                  #print sFilename
                  if (w.lower(), x.lower()) not in self.negwordsfreq:
                     self.negwordsfreq[(w.lower(), x.lower())] = 1
                     self.total_negative = 1
                  else:
                     self.negwordsfreq[(w.lower(), x.lower())]+= 1
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

   def cross_validation(self):
      all_files = self.loop_files()
      #print "length" + str(len(all_files))
      portion = len(all_files)/10 #finding a tenth (or n-th) of the data to keep as testing
      #portion is the size of each faction
      starting_index = 0
      false_positive = 0
      false_negative = 0
      true_positive = 0
      true_negative = 0
      print portion

      for i in range(0,10):
         test_set = []
         training_set = copy.deepcopy(all_files)
         print len(all_files)

         for j in range(0, portion):
            print starting_index
            print j
            print len(all_files)
            test_set.append(all_files[starting_index + j])
         
         starting_index = starting_index + portion
         for file in test_set:
            training_set.remove(file)

         self.train(training_set)

         for sFilename in test_set:
            file = self.loadFile('movies_reviews/' + sFilename)
            verdict = self.classify(file)

            if verdict == 'negative':
               if sFilename[7] == '1':
                  true_negative = true_negative + 1
               else:
                  false_negative = false_negative + 1

            if verdict == 'positive':
               if sFilename[7] == '1':
                  true_positive = true_positive + 1
               else:
                  false_positive = false_positive + 1


      precision = float(true_positive)/float(true_positive+false_positive)
      recall = float(true_positive)/float(true_positive+ false_negative)
   
      f_measure = float(2*precision*recall)/(precision+recall)

      print "precision: " + str(precision)
      print "recall: " + str(recall)
      print "f_measure: " + str(f_measure)
      return precision, recall, f_measure

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
      

      if (abs(pos_cond_prob-neg_cond_prob) < .5):
         # print "neutral"
         return "neutral"
      elif pos_cond_prob > neg_cond_prob:
         # print "positive"
         return "positive"
      elif neg_cond_prob > pos_cond_prob:
         # print "negative"
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
