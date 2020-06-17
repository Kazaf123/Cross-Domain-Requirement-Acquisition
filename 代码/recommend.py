import csv


def read_cluster_csv(file):
    feature = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            for j in i:
                feature.append(j)
    csvFile.close()
    return feature


def write_csv(name, list_w):
    with open(name, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in list_w:
            writer.writerow(i)


def dict_cre(file):
    feature = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            feature.append(i)
    csvFile.close()
    dict = dict(feature)
    return dict


def ce(t):
    a = 0.7*t[2]+0.2*t[3]+0.1*t[4]
    return a


def recommended(feature, dict, file):
    pair = []
    for i in feature:
        result = ce(dict[i])
        pair.append([i, result])
    write_csv(file, pair)


if __name__ == '__main__':
    file_name1 = "feature/dbscan/FoodForHealth.csv"
    file_name2 = "feature/food_dict.csv"
    file_name3 = "feature/recommended/FoodForHealth.csv"
    feature = read_cluster_csv(file_name1)
    dict = dict_cre(file_name2)
    recommended(feature, dict, file_name3)
