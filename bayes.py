# Name: asf408 (Armaan Shah), snk088 (Sonia Nigam), ats545 (Amar Shah)
# Date: 5/22/16
# Description: Assignment 4
# 
# All group members were present and contributing during all work on this project.

import math, os, pickle, re
#stopword list to filter punctuation
punctuation_stopwords = [" ", ".", '"', ",", "?", "!", "/", "'", "-", "_", ";", ":", "&","<",">", ',"', '",', ")", "(", "://", "/"]

class Bayes_Classifier:

   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text."""
	  #dictionaries that capture the frequency of words associated to positive texts and negative texts
      self.poswordsfreq = dict()
      self.negwordsfreq = dict()
	  #total words in the corresponding negative and positive dicts
      self.total_negative = 0
      self.total_positive = 0
	  #populate an array of all the movie files
      if os.path.isfile('positive_words.txt') == False:
         lFileList = []
         for fFileObj in os.walk("movies_reviews/"):
            lFileList = fFileObj[2]
            break
         #train the system based on all of the movie files
         self.train(lFileList)
         #save the corresponding frequency dicts in txt files
         self.save(self.poswordsfreq,"positive_words.txt")
         self.save(self.negwordsfreq,"negative_words.txt")
      else:
         #load the preexisting frequency dictionaries and total counts
         self.poswordsfreq = self.load("positive_words.txt")
         self.negwordsfreq = self.load("negative_words.txt") 
         self.total_negative = self.total_negative_words()
         self.total_positive = self.total_positive_words()

   def loop_files(self):
      """this method populates an array of all the movie files"""
      lFileList = []
      for fFileObj in os.walk("movies_reviews/"):
         lFileList = fFileObj[2]
         break
      # print len(lFileList)
      # print "all files list length ^"
      return lFileList

   def total_positive_words(self):
      """this method counts all of the words in the positive frequency dict"""
      counter = 0
      #increment counter for each key
      for key in self.poswordsfreq:
         counter = counter + self.poswordsfreq[key]
      self.total_positive = counter
      return self.total_positive

   def total_negative_words(self):
      '''this method counts all of the words in the negative frequency dict'''
      counter = 0
      #increment the counter for each key
      for key in self.negwordsfreq:
         counter = counter + self.negwordsfreq[key]
      self.total_negative = counter
      return self.total_negative

   def train(self, lFileList):   
      """Trains the Naive Bayes Sentiment Classifier."""
      #iterate through each files
      for sFilename in lFileList:
         #checks positive files
         if sFilename[7] == '5':
            #tokenize file name
            for w in self.tokenize(self.loadFile('movies_reviews/' + sFilename)):
               #take the lowercase and make sure it is not punctuation  
               if w.lower() not in punctuation_stopwords:
                  #if the word is not already in the dict
                  if w.lower() not in self.poswordsfreq:
                     self.poswordsfreq[w.lower()] = 1
                     self.total_positive = 1
                     #if the word is already in the dict
                  else:
                     self.poswordsfreq[w.lower()]+= 1
                     self.total_positive += 1

         #checks negative files
         elif sFilename[7] == '1':
            #tokenize the file name
            for w in self.tokenize(self.loadFile('movies_reviews/' + sFilename)):
               #take the lowercase and make sure it is not punctuation
               if w.lower() not in punctuation_stopwords:
                  # if the word is not in the dict
                  if w.lower() not in self.negwordsfreq:
                     self.negwordsfreq[w.lower()] = 1
                     self.total_negative = 1
                     #if the word is already in the dict
                  else:
                     self.negwordsfreq[w.lower()]+= 1
                     self.total_negative += 1
      


   def cross_validation(self):
      '''executes cross_validation test and returns three heuristics: recall, precision, and f measure'''
      #populate an array of all of the files
      all_files = self.loop_files()
      # print "length" + str(len(all_files))
      portion = len(all_files)/10 #finding a tenth (or n-th) of the data to keep as testing
      #portion is the size of each faction
      #initialize varibles to track starting index, aggreate false positive, false negative, true positive, and true negative
      starting_index = 0
      false_positive = 0
      false_negative = 0
      true_positive = 0
      true_negative = 0

      #iterates ten times
      for i in range(0,10):
         #initiate an empty test list
         test_set = []
         #copy all files to initial training set list
         training_set = copy.deepcopy(all_files)

         #iterate through the next tenth of the files
         for j in range(0, portion):
            #populate the test set
            test_set.append(all_files[starting_index + j])

         # print len(test_set)
         #increment the starting index to adjust for the next tenth
         starting_index = starting_index + portion
         #delete the test files from the aggregate file training list
         for file in test_set:
            training_set.remove(file)
         #train the data based on the 9/10 files
         self.train(training_set)
         #iterate through the test files and detect accuracy
         for sFilename in test_set:
            file = self.loadFile('movies_reviews/' + sFilename)
            verdict = self.classify(file)
            #handles negative cases
            if verdict == 'negative':
               #increment true negative
               if sFilename[7] == '1':
                  true_negative = true_negative + 1
               else:
                  #increment false negative
                  false_negative = false_negative + 1

            if verdict == 'positive':
               #increment true positive
               if sFilename[7] == '1':
                  true_positive = true_positive + 1
               else:
                  #increment false positive
                  false_positive = false_positive + 1

            # print false_positive, false_negative, true_positive, true_negative
      #calculate precision, recall, and f-measure heuristics based on formulas and aggregate data
      precision = float(true_positive)/float(true_positive+false_positive)
      recall = float(true_positive)/float(true_positive+ false_negative)
      f_measure = float(2*precision*recall)/(precision+recall)

      print "precision: " + str(precision)
      print "recall: " + str(recall)
      print "f_measure: " + str(f_measure)
      #return results
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
      #iterate through each word in the tokenized text
      for w in self.tokenize(sText):
         #if the word is not punctuation and already in positive frequency dict
         if w.lower() not in punctuation_stopwords and w.lower() in self.poswordsfreq:
            #find probability of word based on relative frequency
            pos_prob_word = float(self.poswordsfreq[w.lower()] + 1)/self.total_positive
            #determine positive conditional probablity
            pos_cond_prob = pos_cond_prob + math.log10(pos_prob_word)
         else:
            #determine positive conditional probablity for words not present in the system
            pos_cond_prob += math.log10(1.0/self.total_positive)

      for w in self.tokenize(sText):
         # print self.negwordsfreq
         # print sText
         #if the word is not punctuation and already in negative frequency dict
         if w.lower() not in punctuation_stopwords and w.lower() in self.negwordsfreq:
            #find probability of word based on relative frequency
            neg_prob_word = float(self.negwordsfreq[w.lower()] + 1)/self.total_negative
            #determine negative conditional probablity
            neg_cond_prob = neg_cond_prob + math.log10(neg_prob_word)
         else:
            #determine negative conditional probablity for words not present in the system
            neg_cond_prob += math.log10(1.0/self.total_negative)


      # print pos_cond_prob
      # print neg_cond_prob
      #determine neutral cases
      if (abs(pos_cond_prob-neg_cond_prob) < .5):
         # print "neutral"
         return "neutral"
      #determine positive cases
      elif pos_cond_prob > neg_cond_prob:
         # print "positive"
         return "positive"
      #determine negative cases
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

