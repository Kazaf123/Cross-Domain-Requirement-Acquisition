import csv


def read_csv(filename):
    temp = []
    with open(filename, 'r', newline='') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            for j in i:
                temp.append(j)
    csvFile.close()
    return temp


if __name__ == '__main__':
    name = "feature/dbscan/FoodForHealth.csv"
    a = read_csv(name)
    print(a)
