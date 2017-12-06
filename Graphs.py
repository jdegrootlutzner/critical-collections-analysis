import csv
import numpy as np
import pandas
import matplotlib.pyplot as plt

my_file = 'genre.csv'


def import_data(delimited_file):
    with open(delimited_file, 'rb') as csvfile:
        all_data = list(csv.reader(csvfile, delimiter=','))
    return all_data

def seperate_headings_from_data(data):
    headings = data[0]
    data.pop(0)
    print pandas.DataFrame(data, columns=headings)

def get_basic_statistics(data):
    gc = []
    for genre in data:
        gc.append(float(genre[1]))
    return gc

def get_gen(data):
    gen = []
    for genre in data:
        gen.append(str(genre[0]))
    return gen

def calculate_min_and_max(genre):
    return np.min(genre), np.max(genre)

def get_genre(count, min_max, data):
    genre=[]
    min_index = count.index(min_max[0])
    max_index = count.index(min_max[1])
    for count in data:
        genre.append(count[0])
    return genre[min_index], genre[max_index]

def create_frequency_dist(index):
    hist,bin_edges = np.histogram(index,bins=10)
    return hist,bin_edges

def create_histogram(index):
    plt.hist(index, facecolor='red', label='Count')
    plt.title('Count of the entries by Genre')
    plt.xlabel("Genre")
    plt.ylabel("Count")
    plt.legend()
    plt.show()

def create_bar(index):
    width = 0.2
    a=(len(index))
    ind = np.arange(a)
    plt.bar(ind, index, width, color='b')
    plt.xticks(ind, gen, rotation = 90)
    plt.show()
    
data = import_data(my_file)
seperate_headings_from_data(data)
gc = get_basic_statistics(data)
gen = get_gen(data)
min_max = calculate_min_and_max(gc)
genre = get_genre(gc,min_max,data)
print "Genre with the greatest volume in the Claremont Colleges Library: {} at {}".format(
   (genre)[0], (min_max)[1])
print "Genre with the smallest volume in the Claremont Colleges Library: {} at {}".format(
    (genre)[1], (min_max)[0])
print create_frequency_dist(gc)
create_bar(gc)
