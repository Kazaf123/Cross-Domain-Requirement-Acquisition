# coding: utf-8

import csv
from nltk.tokenize import WordPunctTokenizer
from gensim.models import word2vec


def read_csv_feature(file):
    feature = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            for n1, n2 in enumerate(i):
                if n1 == 5:
                    temp = n2.split(",")
                    for k in temp:
                        feature.append(k)
    return feature


def sim_phrase(f1, f2, model):
    temp1 = f1.split(" ")
    temp2 = f2.split(" ")
    try:
        vs = model.wv.similarity(temp1[0], temp2[0])
    except:
        return 0
    counter = 0
    sum = 0.00
    del temp1[0]
    del temp2[0]
    for i in temp1:
        for j in temp2:
            counter += 1
            try:
                sum += model.wv.similarity(i, j)
            except:
                return 0
    try:
        ns = sum/counter
    except:
        return 0
    s = 0.25 * vs + 0.75 * ns
    return s


def length(feature):
    temp = 0
    for i in feature:
        temp += 1
    return temp


def load_model(saveDir):
    model = word2vec.Word2Vec.load(saveDir)
    return model


def write_csv(file, info):
    with open(file, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        print(info)
        writer.writerows([info])
    csvFile.close()


def relationship(f1, f2, model, filename):
    a = len(f1)
    b = len(f2)
    sum = a * b
    counter = 0
    for i in f1:
        for j in f2:
            counter += 1
            print("当前进度：" + str(counter) + "/" + str(sum))
            sim = sim_phrase(i, j, model)
            # print(i, j, sim)
            if sim > 0.7:
                temp = [i, j, str(sim)]
                write_csv(filename, temp)


if __name__ == '__main__':
    name1 = "health"
    name2 = "food"
    model_name = "trainWord2vecModel"
    model = load_model(model_name)
    file1 = "feature/"+name1+"_1000_new.csv"
    file2 = "feature/"+name2+"_1000_new.csv"
    file3 = "feature/high_sim/"+name1+"&"+name2+".csv"
    feature1 = read_csv_feature(file1)
    feature2 = read_csv_feature(file2)
    relationship(feature1, feature2, model, file3)





