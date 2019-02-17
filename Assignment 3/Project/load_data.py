from os import listdir
import csv

def find_csv(path):
    return [f for f in listdir(path) if f.split('.')[-1] == "csv"]

def read_csv(path, name):
    file = open(path + name, "r")
    reader = csv.reader(file)
    time, price = [], []
    for entry in reader:
        time.append(int(entry[0]))
        price.append(float(entry[1]))
    file.close()
    return time, price

if __name__ == "__main__":
    print(find_csv('./data/'))