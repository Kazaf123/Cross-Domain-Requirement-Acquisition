

import csv


import os
import sys
import numpy as np
import scipy as sp
from sklearn.datasets import load_iris
# 欧式距离函数
import matplotlib.pyplot as plt
import math
import csv

from gensim.models import word2vec
import logging

# 主程序



# 使用word2vec向量化



'''def get_distances(xi, xx):
    dis_list = []
    for i in xx:
        x = abs(i[0]- xi[0])
        y = abs(i[1]- xi[1])
        dis = math.sqrt(x*x + y*y)
        dis_list.append(dis)
    print dis_list
    return dis_list'''


class Group(object):
    """
    定义类簇的类 -- 后续也会使用
    """

    def __init__(self):
        self._name = ""
        self._no = None
        self._members = []
        self._center = None

    @property
    def no(self):
        return self._no

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, no):
        self._no = no
        self._name = "G" + str(self._no)

    @property
    def members(self):
        return self._members

    @members.setter
    def members(self, member):
        if member is None:
            raise TypeError("member is None,please set value")
        if isinstance(member, list):
            self.members.extend(member)
            return
        self._members.append(member)

    def clear_members(self):
        self._members = []

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, c):
        self._center = c


class Dbscan(object):
    """
    dbscan- Density-Based Spatial Clustering of Application with Noise
    基于密度的噪声应用空间聚类
    """
    def __init__(self,epos=0.1,minpts=5):
        self._epos = epos # 邻域半径范围
        self._minpts = minpts # 邻域内最小数据个数
        self._groups = [] #类簇集合
        self._kernel_points = [] #核心对象集合
        self._X = {} # 转化后的数据
        self._counter = 0
        self._model = word2vec.Word2Vec.load('trainWord2vecModel')

    def _get_sim(self, a, b):
        a = a.split()
        b = b.split()
        '''if a == b:
            return 1'''
        #print a[0]
        #print b[0]
        try:
            vs = self._model.wv.similarity(a[0].strip(), b[0].strip())
        except:
            print (a[0])
            print (b[0])
            print ("单词表里不存在")
            return 0
        a.remove(a[0])
        b.remove(b[0])
        ns = 0
        for i in a:
            for j in b:
                try:
                    temp = self._model.wv.similarity(i, j)
                    if temp > ns:
                        ns = temp
                except:
                    print (i)
                    print (j)
                    print ("单词表里不存在")
        s = 0.25 * vs + 0.75 * ns
        return s

    def _get_distances(self, xi, XX):
        # 计算两个词的相似度/相关程度
        dis_list = []
        for i in range(len(XX)):
            if xi != XX[i]:
                temp = 1 - self._get_sim(xi, XX[i])
                # sim = 1 - temp
                # print XX[i] + u"和" + xi + u"相似度为："  + str(sim)
                dis_list.append(temp)
        return dis_list


    def _find_nearbours(self,xi,XX):
        """
        查找满足邻域值大小的数据索引列表
        :param xi:
        :param XX:
        :return:
        """
        if XX.shape[0] == 0:
            return []
        distances = self._get_distances(xi, XX)
        distances = np.array(distances)
        nearst_indexes = np.where(distances <= self._epos)[0].tolist()
        return nearst_indexes

    def _compat_X(self,X):
        """
        转化输入数据格式
        为了方便删除、存取操作
        :param X:
        :return:
        """
        rows = X.shape[0]
        CX = {}
        for row in range(rows):
            CX[row]=[False,X[row]]
        self._X = CX

    def _get_data(self,index):
        """
        获取索引的数据
        :param index:
        :return:
        """
        if isinstance(index,int):
            data = self._X.get(index)[-1]
        if isinstance(index,list):
            data = []
            for i in index:
                data.append(self._X.get(i)[-1])
        return data

    def _delete_data(self,indexes):
        """
        删除索引对应的数据
        :param indexes:
        :return:
        """
        if isinstance(indexes,int):
            self._X.get(indexes)[0] = True
        if isinstance(indexes, list):
            for index in indexes:
                self._X.get(index)[0] = True

    def _get_live_data(self):
        """
        获取未被加入到类簇集合的数据
        :return:
        """
        live_data = {}
        for key,value in self._X.items():
            if value[0]==False:
                live_data[key] = value
        return live_data

    def fit(self,X):
        """
        聚类主体
        :param X:
        :return:
        """
        self._compat_X(X)  # 组合X的记录,记录在self._X中
        # 1.首先遍历数据集 找到所有的核心对象
        rows = X.shape[0]
        for i in range(rows):
            # 找到小于邻域参数的数据
            nearbours = self._find_nearbours(X[i],X)
            if len(nearbours) >= self._minpts:
                self._kernel_points.append(i)
        if len(self._kernel_points) == 0 :
            # 若没有核心对象，那么每个点都为单独的一类
            for i in range(rows):
                g = Group()
                g.name = i+1
                g.members = X[i]
                g.center = X[i]
                self._groups.append(g)
            return
        while(True):
            print ("聚类一次")
            if len(self._kernel_points) == 0:
                break
            # 2.4直到当前核心对象集合为空
            # 2.从核心对象集合中取出一个核心对象，完成对一个类簇的生成
            init_index = int(np.random.randint(0,len(self._kernel_points),size=1).squeeze())
            kernel_points = self._kernel_points[init_index]
            self._kernel_points.remove(kernel_points)
            # 2.1拿取第一个核心对象生成类簇，加入当前核心对象集合
            current_points = set()  # 当前簇的样本集合
            current_kernel_points = set()
            g = Group()
            g.center = X[kernel_points]
            self._delete_data(kernel_points)
            current_kernel_points.add(kernel_points)
            delete_kernel_points = set()
            while len(current_kernel_points)!= 0:
                # 2.2然后当前核心对象集合中取一个核心点 找到该核心对象的所有邻域点，则邻域点即为该类簇的成员数据
                current_point_index = current_kernel_points.pop()
                current_points.add(current_point_index)
                delete_kernel_points.add(current_point_index)
                nearbours_points_indexes = self._find_nearbours(X[current_point_index],X)
                current_points = current_points.union(set(nearbours_points_indexes))
                # 2.3用这些成员与原始核心对象集合做交集，若有重合则将其加入当前核心对象集合中，重复上述查询邻域过程
                union_kernel_points = current_points.intersection(set(self._kernel_points))
                current_kernel_points = current_kernel_points.union(union_kernel_points)
                current_kernel_points = current_kernel_points.difference(delete_kernel_points)
                # 3 重复上述步骤
            current_datas = self._get_data(list(current_points))
            self._delete_data(list(current_points))
            g.members = current_datas
            g.name = len(self._groups) + 1
            self._groups.append(g)
            s = set(self._kernel_points)
            s = s.difference(current_points)
            self._kernel_points = list(s)
            self._counter += len(list(current_points))
            print (self._counter)
        # 查询现有余下的数据 也就是噪声点
        live_datas = self._get_live_data()
        for key, value in live_datas.items():
            g = Group()
            g.name = len(self._groups) + 1
            g.center = value[-1]
            g.members = value[-1]
            self._groups.append(g)
        return self._groups

    def plot_example(self):
        """
        画图
        """
        figure = plt.figure()
        ax = figure.add_subplot(111)
        ax.set_title("Dbscan Iris Example")
        plt.xlabel("first dim")
        plt.ylabel("two dim")
        legends = []
        cxs = []
        cys = []
        for i in range(len(self._groups)):
            group = self._groups[i]
            members = group.members
            x = [member[0] for member in members]
            y = [member[1] for member in members]
            cx = group.center[0]
            cy = group.center[1]
            cxs.append(cx)
            cys.append(cy)
            ax.scatter(x, y, marker='o')
            #ax.scatter(cx,cy,marker='+',c='r')
            legends.append(group.name)
        plt.scatter(cxs,cys,marker='+',c='k')
        plt.legend(legends, loc="best")
        plt.show()


def init_distances():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus("data/text8")  # 加载语料
    model = word2vec.Word2Vec(sentences, size=200)  # 训练skip-gram模型; 默认window=5
    model.save("sim_new.model")


def read_csv(name, a=0.8, b=2.0):
    csv_file = csv.reader(open(name, 'r'))
    temp = []
    for i in csv_file:
        if a < float(i[3]) < b and i[2] == "3":
            temp.append(i)
    return temp


def write_csv(name, list_w):
    with open(name, 'a', newline='') as csvFile:
        writer = csv.writer(csvFile)
        for i in list_w:
            writer.writerow(i)


def read_0(new):
    temp = []
    for i in new:
        temp.append(i[0])
    return temp


def read_1(new):
    temp = []
    for i in new:
        temp.append(i[1])
    return temp


def read_0_dic(new):
    temp = []
    for i in new:
        temp.append([i[0], i[3]])
    return temp


def read_1_dic(new):
    temp = []
    for i in new:
        temp.append([i[0], i[3], i[1]])
    return temp


def delete_repetition(feature):
    temp = []
    a = 0
    b = 0
    for i in feature:
        a += 1
        if i not in temp:
            temp.append(i)
            b += 1
    print ('过滤前：',a)
    print ('过滤后：',b)
    # print temp
    return temp


def delete_repetition_dic(feature):
    temp = []
    temp_dic = []
    for i in feature:
        if i[0] not in temp:
            temp.append(i[0])
    for i in temp:
        temp_sim = 0
        for j in feature:
            if j[0] == i:
                if j[1] > temp_sim:
                    temp_sim = j[1]
        temp_dic.append((i, temp_sim))
    dic = dict(temp_dic)
    return dic


def feature_dict(file):  #返回两个字典，通过相似领域的feature查询
    temp1 = []
    temp2 = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            temp1.append((i[1], i[0]))
            temp2.append((i[1], i[2]))
    dict1 = dict(temp1)
    dict2 = dict(temp2)
    return dict1, dict2


def max_count(lt):
    # 定义一个字典，用于存放元素及出现的次数
    d = {}
    # 记录最大的次数的元素
    max_key = None
    # 遍历列表，统计每个元素出现的次数，然后保存到字典中
    for i in lt:
        if i not in d:
            # 计算元素出现的次数
            count = lt.count(i)
            # 保存到字典中
            d[i] = count
            # 记录次数最大的元素
            if count > d.get(max_key, 0):
                max_key = i
    return max_key


def get_sim(model, a, b):
    a = a.split()
    b = b.split()
    '''if a == b:
        return 1'''
    # print a[0]
    # print b[0]
    try:
        vs = model.wv.similarity(a[0].strip(), b[0].strip())
    except:
        print (a[0])
        print (b[0])
        print ("单词表里不存在")
        return 0
    a.remove(a[0])
    b.remove(b[0])
    ns = 0
    for i in a:
        for j in b:
            try:
                temp = model.wv.similarity(i, j)
                if temp > ns:
                    ns = temp
            except:
                print (i)
                print (j)
                print ("单词表里不存在")
    s = 0.25 * vs + 0.75 * ns
    return s


def centre(words):
    dic = []
    model = word2vec.Word2Vec.load('trainWord2vecModel')
    for i in words:
        num = 0.00
        distances = 0
        for j in words:
            distances += get_sim(model, i, j)
            num += 1
        distances = distances / num
        dic.append([i, distances])
    dis = 0
    key = ""
    for i in dic:
        if i[1] > dis:
            dis = i[1]
            key = i[0]
    return key

def read_sim(file):
    part2 = []
    with open(file, "r", encoding='UTF-8') as csvFile:
        csv_reader = csv.reader(csvFile)
        for i in csv_reader:
            if i[1] not in part2:
                part2.append(i[1])
    csvFile.close()
    return part2


if __name__ == '__main__':
    file1 = "feature/high_sim/health&food.csv"
    write_name = "feature/dbscan/FoodForHealth.csv"
    print(type(file1))
    food_feature = read_sim(file1)
    X = np.array(food_feature)
    dbscan = Dbscan(0.2, 5)
    g = dbscan.fit(X)
    group = []
    for i in g:
        temp = []
        if len(i.members) > 1:
            for j in i.members:
                s = str(j)
                temp.append(s)
        group.append(temp)
    write_csv(write_name, group)



