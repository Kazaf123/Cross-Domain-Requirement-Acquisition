# coding = utf-8
import csv
from nltk.stem import WordNetLemmatizer


def read_csv(file, dict):
    info = []
    feature_set = []
    wnl = WordNetLemmatizer()
    with open(file, 'r', newline='') as csvFile:
        csv_reader = csv.reader(csvFile)

        for i, j in enumerate(csv_reader):
            part = []
            features = ""
            if i % 2 == 0:
                sign = 0
                for k, l in enumerate(j):
                    if k < 5:
                        part.append(l.split("'")[1].strip())
                    else:
                        temp = ''
                        l = l.split("'")
                        for n1, n2 in enumerate(l):
                            if n1 % 2 == 1 and n1 == 1:
                                n2 = wnl.lemmatize(n2, 'v')  # 词形还原
                                temp += n2
                                temp += " "
                                if n2 not in dict:
                                    sign = 1
                            elif n1 % 2 == 1 and n1 != 1:
                                n2 = wnl.lemmatize(n2, 'n')  # 词形还原
                                temp += n2
                                temp += " "
                                if n2 not in dict:
                                    sign = 1
                        temp = temp.strip()
                        features += temp
                        features += ","
                if features.strip(",") not in feature_set:  # 去重
                    feature_set.append(features.strip(","))
                else:
                    sign = 1
                part.append(features.strip(","))
                if sign == 0:
                    info.append(part)
    csvFile.close()
    return info


def write_csv(file, info):
    with open(file, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(info)
    csvFile.close()


def read_csv_dict():
    csv_file = csv.reader(open('EnWords.csv', 'r', encoding='UTF-8'))
    temp = []
    for i in csv_file:
        temp.append(i[0])
    return temp


if __name__ == '__main__':
    file = "feature/video_1000.csv"
    file_new = "feature/video_1000_new.csv"
    eng_dict = read_csv_dict()
    info = read_csv(file, eng_dict)
    write_csv(file_new, info)

