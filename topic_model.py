
import csv
import re
import numpy as np
import matplotlib.pyplot as plt

#Note some of this code was also used by Sydney Smith in her fall 2017 thesis submitted to CMC

def dictionary(subject_list):
  stopWords = open("stop-word-list.txt").read()
  unique_words = list(set("".join(subject_list).split(" ")))
  unique_words =[unique_words for unique_words in unique_words if unique_words not in stopWords]
  return sorted(unique_words)

def wordCount(matrix, paragraphs, unique_words):
  for x in range(0,(len(paragraphs)-1)):
    paragraphs[x] = re.sub('\n',' ',paragraphs[x])
    paragraphs[x] = re.sub('\r',' ',paragraphs[x])
    paragraphx = paragraphs[x].split()
    for z in range(0,(len(unique_words)-1)):
      for words in paragraphx:
       if unique_words[z] in words:
        matrix[z,x] = matrix[z,x]+1
  return matrix

def matmult(a,b):
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]

def topic_mtrx(wordnum, topicsnum):
  temp_list = []
  for x in xrange(0,topicsnum):
   temp_list.append([ ])
   for i in range(0,wordnum):
    temp_list[x].append((0,"Filler"+str(x)))
  return temp_list  

def topicList(words_topics,num_words, num_topics, toprint):
 countmtrx = topic_mtrx(num_words,num_topics)
 for x in xrange(0,num_topics):
  for (word, count) in words_topics:
    L = countmtrx[x][0]
    if (abs(count[x])>=L[0]):
      countmtrx[x][0] = (count[x],word)
      countmtrx[x] = sorted(countmtrx[x])
 if (toprint):     
  for x in xrange(0,num_topics):
   print("Topic: "+ str(x+1))
   print("Word, Frequency")
   for y in range(0,num_words):
    (number, word) = countmtrx[x][num_words-1-y]
    print("{text: '"+str(word)+"', count: '"+str(round(number,3))+"'},")
   # {text: "Alice", count: "15.1"},
 return countmtrx

def svd(frequency_mtrx, num_topics):
  U, S, V = np.linalg.svd(frequency_mtrx, full_matrices=True)
  s = np.diag(S)
  snt = s[:num_topics,:num_topics]
  unt = U[:,:num_topics]
  vnt = V[:num_topics]
  svd_topics_time = matmult((snt),(vnt))
  svd_words_topics = matmult((unt),(snt))
  svd_topics_time = [0 if i < 0 else i for i in svd_topics_time]
  [0 if i < 0 else i for i in svd_words_topics]
  return (svd_words_topics,svd_topics_time)

def plotting(thing_one, title, xlab, ylab):
  plt.plot()
  plt.plot(thing_one)
  plt.title(title)
  plt.ylabel(ylab)
  plt.xlabel(xlab)
  plt.show()

   
def main(genre_string, t): #the genre to partion by and the number of topics (t)
    input_file = open('cleaned_data.csv', 'r')
    csv_input_file = csv.reader(input_file)
    csv_input_file.next() #skip header
    subject_matrix = [] #creating a place to store the subject descriptions
    for line in csv_input_file:
    	genre = line[5]
    	subject = line[6]
        if (genre == genre_string):
          subject = re.sub(r'[^\w\s]','',subject)
          subject_matrix.append(subject)
    unique_words = dictionary(subject_matrix)
    matrix = np.zeros((len(unique_words),len(subject_matrix)))
    X = wordCount(matrix, subject_matrix,unique_words)
    (svd_words_topics,svd_topics_time) = svd(X, t)
    z_svd_words_topics = zip(unique_words,svd_words_topics)
    topicList(z_svd_words_topics,10,t,True)
    plotting(svd_topics_time[2],"Topic 3 Over Time", "Publishing Order","Topic Intensity")

main("History ", 4)