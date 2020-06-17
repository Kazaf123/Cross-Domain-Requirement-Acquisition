import csv


def read_csv(file):
    feature = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            feature.append(i)
    csvFile.close()
    return feature


def write_csv(name, list_w):
    with open(name, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in list_w:
            writer.writerow(i)


def cre_dict(f1, f2):
    word = []
    d = []
    for i in f1:
        for j in i and j not in word:
            word.append(j)
    for i in f2:
        for j in word:
            if j in i[5]:
                d.append((j, [i[0], i[1], i[2], i[3], i[4]]))
    return d


if __name__ == '__main__':
    file1 = "feature/dbscan/FoodForHealth.csv"
    file2 = "feature/food_1000_new.csv"
    file3 = "feature/food_dict"
    f1 = read_csv(file1)
    f2 = read_csv(file2)
    dict = cre_dict(f1, f2)
    write_csv(file3, d)
