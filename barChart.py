import csv
import numpy as np
import pandas
import matplotlib.pyplot as plt

my_file = 'BarChart.csv'


def import_data(delimited_file):
    with open(delimited_file, 'r') as csvfile:
        all_data1 = list(csv.reader(csvfile, delimiter=','))
        all_data = np.array(all_data1).astype(np.float)
    return all_data


def get_basic_statistics(data):
    gc = []
    for pub_date in data:
        gc.append(float(pub_date[0]))
    return gc

def get_gen(data):
    gen = []
    for genre in data:
        gen.append(str(genre[0]))
    return gen

def calculate_min_and_max(pub_date):
    return np.min(pub_date), np.max(pub_date)

def get_pub_date(count, min_max, data):
    pub_date=[]
    min_index = count.index(min_max[0])
    max_index = count.index(min_max[1])
    for count in data:
        pub_date.append(count[0])
    return pub_date[min_index], pub_date[max_index]

def create_frequency_dist(index):
    hist,bin_edges = np.histogram(index,bins=10)
    return hist,bin_edges


data = import_data(my_file)

gc = get_basic_statistics(data)
min_max = calculate_min_and_max(gc)
pub_date = get_pub_date(gc,min_max,data)
print ('Year with the most books published in the Claremont Colleges Library: {} at {}'.format((pub_date)[1], str((min_max)[1])))
print ('Year with the least books published in the Claremont Colleges Library: {} at {}'.format((pub_date)[0], str((min_max)[0])))


plt.figure(figsize=(12,9))

ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.xlabel("Year Published", fontsize=16)
plt.ylabel("Count", fontsize=16)
plt.hist(data, bins=1000)

print (create_frequency_dist(gc))

plt.show()

plt.savefig("Histogram.png", bbox_inches="tight");