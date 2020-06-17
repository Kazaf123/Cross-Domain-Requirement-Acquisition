import csv
import math


def read_csv_feature_n(file):
    features = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            feature = i[5].split(",")
            print(feature)
            for f in feature:
                '''temp = f.split(" ")
                del temp[0]
                nn = ""
                for j in temp:
                    nn += j
                    nn += " "
                nn = nn.strip(" ")
                features.append(nn)'''
                features.append(f)
    csvFile.close()

    return features


def num(feature, feature_list):
    counter = 0
    for i in feature_list:
        if i == feature:
            counter += 1
    return counter


def num_in_six(feature, f1, f2, f3, f4, f5, f6):
    counter = 0
    temp = [f1, f2, f3, f4, f5, f6]
    for i in temp:
        if feature in i:
           counter += 1
    return counter + 1


def tf_idf(nn, n1, n2, n3, n4, n5, n6):
    feature_n = []
    for i in nn:
        tf = num(i, nn)/len(nn)
        idf = math.log(6.00/num_in_six(i, n1, n2, n3, n4, n5, n6))
        temp = tf * idf
        if [i, str(temp)] not in feature_n:
            feature_n.append([i, str(temp)])
    return feature_n


def write_csv(file, info):
    with open(file, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in info:
            writer.writerows([i])
    csvFile.close()


if __name__ == '__main__':
    file1 = "feature/health_1000_new.csv"
    file2 = "feature/food_1000_new.csv"
    file3 = "feature/social_1000_new.csv"
    file4 = "feature/shopping_1000_new.csv"
    file5 = "feature/sports_1000_new.csv"
    file6 = "feature/video_1000_new.csv"

    food_file = "feature/tf-idf/text.csv"

    n1 = read_csv_feature_n(file1)
    n2 = read_csv_feature_n(file2)
    n3 = read_csv_feature_n(file3)
    n4 = read_csv_feature_n(file4)
    n5 = read_csv_feature_n(file5)
    n6 = read_csv_feature_n(file6)

    f = tf_idf(n2, n1, n2, n3, n4, n5, n6)
    write_csv(food_file, f)



