# coding=utf-8
# 介词将来需要提取，将allow等词对设为假词对（人工辨认）

from nltk.parse import stanford
import os
import Rulers
from stanfordcorenlp import StanfordCoreNLP
from nltk.parse.stanford import StanfordParser



def after_process(j):  #后处理，将无意义的特征结果过滤掉
    # (thing) Because Wabbitemu is an emulator, the calculator it creates will act exactly like the real thing.
    # (enable) It s also needed to enable offline support.
    # (have) Fast and convenient, Wabbitemu allows you to always have your trusty calculator with you.
    # (数字) Wabbitemu supports the TI-73, TI-81, TI-82, TI-83, TI-83 Plus, TI-83 Plus Silver Edition, TI-84 Plus, TI-84 Plus Silver Edition, TI-85, and TI-86.

    if j != []:
        if 'fun' == j[-1]:
            return 0

    for i in j:
        if type(i) != type(1):
            if i.lower() in ['near', 'the', 'up', 'airport', 'included', 'whats', 'at', 'was', 've', 'doesnt', 'isnt',
                             'thats', 'year', 'everything', 'whos', 'i', 't', 'things', 'being', 'him', 'hours', 'i',
                             'any', 'like', 'likes', 'anything', 'only', 'way', 'ways', 'you', 'your', 'we', 'yours',
                             'it', 'allow', 'allows', 'is', 'are', 'It', 'enable', 'have', 'has', 'thing', 'us', 'You',
                             'I', 'were', 'Were', 'app', 'come', 'comes', 'be', '\'s', 'they', 'we', 'does', 'do',
                             'don', 'include', 'one', 'ones', 'include', 'includes', 'including', 'yourself', 'days',
                             'day', 'week', 'weeks', 'range', 'let', 'lets', 'secs', 'and', 'just', 'easy', 'etc', 'a']:
                # print '删了：',i
                return 0

    for i in j:
        for k in ['1', '2', '3', '4', '5', '6', '7' '8', '9', '0']:
            if k in i:
                return 0
    return 1


def preProcess(sent):  # 预处理，删除句子中不重要或者可能影响特征提取的单词，返回的是含有2个值的list
    sent = sent.replace('’', '\'')
    sent = sent.replace('﻿"', ' ')
    sent = sent.replace('：', '')
    sent = sent.replace('%', '')
    sent = sent.strip()
    sent = sent.strip('*')
    sent = sent.strip('-')
    sent = sent.strip('(')
    sent = sent.strip(')')
    sent = sent.strip('（')
    sent = sent.strip('）')
    if sent[-1] not in ['.', '?', '!', ':']:
        sent += '.'
    s = sent

    # 将冒号前后的句子算成两个句子
    if ':' not in s:
        s1 = s
        s2 = ''
    else:
        s1 = ''
        s2 = ''
        a = 1
        for i in s:
            if i == ':':
                a = 0
                s1 += '.'
            if a:
                s1 += i
            else:
                if ':' not in i:
                    s2 += i
    sent = []

    for s in [s1, s2]:
        if s != '':
            # 减 （)
            temp = ''
            a = 1
            for i in s:
                if i == '(':
                    a = 0
                if a:
                    temp += i
                if i == ')':
                    a = 1
            s = temp

            # 删除all、 all of

            s = s.replace('all of ', '')
            s = s.replace('always ', '')
            s = s.replace('Always ', '')
            s = s.replace(' all ', ' ')
            s = s.replace('thousands of', '')
            s = s.replace('Thousands of', '')
            s = s.replace('millions of', '')
            s = s.replace('part of', '')
            s = s.replace('today', '')
            s = s.replace('=', '')
            s = s.replace('+', '')
            s = s.replace('the most', '')
            s = s.replace(' s ', '\'s ')
            s = s.replace('dozens of', '')
            s = s.replace('Dozens of', '')
            s = s.replace('a wide range of', '')
            s = s.replace('a range of', '')
            s = s.replace('a total of', '')
            s = s.replace('every week', '')
            s = s.replace('every day', '')
            s = s.replace('every year', '')
            s = s.replace('every month', '')
            s = s.replace('would do', '')
            s = s.replace('lots of', '')
            s = s.replace('Lots of', '')
            s = s.replace('a lots of', '')
            s = s.replace('a lot of', '')
            s = s.replace('all kinds of', '')
            s = s.replace('and so on', '')
            s = s.replace('and more', '')
            s = s.replace('tons of', '')
            s = s.replace('hundreds of', '')
            s = s.replace('Millions of', '')
            s = s.replace('millions of', '')
            s = s.replace('a burst of', '')
            s = s.replace('a set of', '')
            s = s.replace('set of', '')
            s = s.replace('aspect of', '')
            s = s.replace('a series of', '')
            s = s.replace('every time', '')
            # s = s.replace('plenty', '')
            s = s.replace('all types of', '')
            # 删除副词(需要测试)

            # s = levelTraverse(s)  # Join the most daring chase!(错误)
            # print 's:',s

            nlp = getStanfordParser_py2()
            try:
                temp = nlp.raw_parse(s)
            except:
                print('注意：此处有不能构成树的句子--' + s)
                return ['', '']
            tree = temp.__next__()
            # tree.draw()
            t = 0
            for i in tree:
                t += 1
                if t == 1 and i.label() == 'NP':
                    # print '+I'
                    s = s.strip()
                    c = s[0]
                    if c.isupper():
                        s = c.lower() * 1 + s[1:]
                        s = 'I ' + s
                    else:
                        s = 'I ' + s
            s = s.strip(',')
            sent.append(s)
        else:
            s = s.strip(',')
            sent.append(s)

    return sent


def getStanfordParser_py2():  # 获取parser库
    java_path = 'C:/Program Files/Java/jdk1.8.0_201/bin/java.exe'
    # java_path = 'C:/Program Files/Java/jdk1.8.0_161/bin/java.exe'
    os.environ['JAVAHOME'] = java_path
    parser = stanford.StanfordParser(path_to_jar="G:/NLP/stanford_parser/stanford-parser.jar",
                                     path_to_models_jar="G:/NLP/stanford_parser/stanford-parser-3.5.2-models.jar",
                                     model_path="G:/NLP/stanford_parser/stanford-parser-3.5.2-models/edu/stanford/"
                                                "nlp/models/lexparser/englishPCFG.ser.gz")
    return parser


def getStanfordNLP_py3():  # 没用
    zh_model = StanfordCoreNLP('G:/stanfordNLP')
    return zh_model


def first_two(word):  # 取一个str的前两位
    if len(word) < 2:
        return word
    temp = 0
    temp_label = []
    for ch in word:
        temp += 1
        if temp < 3:
            temp_label.append(ch)
    temp = ''.join(temp_label)
    return temp


def lower_out(out):  # 小写str
    if out == []:
        return out
    temp_out = []
    for i in out:
        temp = []
        for j in i:
            # print j
            temp.append(j.lower())
        temp_out.append(temp)
    out = temp_out
    return out


def levelTraverse(sent):  # 预处理中用于删除副词，后来不用了

    nlp = getStanfordParser_py2()
    temp = nlp.raw_parse(sent)
    tree = temp.__next__()

    # tree.draw()
    notSearch = []
    notSearch.append(tree)
    temp = []
    while len(notSearch) > 0:
        i = notSearch.pop(0)

        print(i)

        if len(i) == 1 and isinstance(i[0], str):
            if first_two(i.label()) != 'RB':
                temp.append(i[0])
        else:
            t = []
            for j in i:
                t.append(j)
            t.extend(notSearch)
            notSearch = t
    temp_s = ''
    for i in temp:
        temp_s = temp_s + i
        temp_s = temp_s + ' '

    return temp_s


def deepTraverse(sent):  # 使用深度优先遍历的形式对语法树进行处理，是特征提取的核心
    if sent == []:
        return 0
    notSearch = []
    if type(sent) == type(u'hello world') or type(sent) == type('hello world'):  # 判断输入是否是字符串，不是字符串的情况是句子中的句子迭代。
        nlp = getStanfordParser_py2()
        try:
            temp = nlp.raw_parse(sent)
        except:
            print('注意：此处有不能构成树的句子--' + sent)
            return 0
        tree = temp.__next__()
        tree.draw()
        type_1 = type(tree)  # 构建输入的语法树
        notSearch.append(tree)
    else:
        notSearch = sent
        type_1 = type(sent[1])

    #  声明各种变量，用于储存
    n = Rulers.Stack()  # 名词栈
    v = Rulers.Stack()  # 动词栈
    constant_p_counter = Rulers.Stack()
    constant_n = Rulers.Stack()
    constant_n_counter = Rulers.Stack()
    vi_counter = Rulers.Stack()  # 不及物动词计数器
    ed_counter = Rulers.Stack()  # 被动语态计数器
    p_counter = Rulers.Stack()  # 词组计数器
    p_counter.push(0)
    v_counter = Rulers.Stack()  # 动词计数器
    v_counter.push(0)
    n_counter = Rulers.Stack()  # 名词计数器
    n_counter.push(0)
    PP_sign = Rulers.Stack()  # PP标记器
    temp1 = Rulers.Stack()
    temp2 = Rulers.Stack()
    temp3 = Rulers.Stack()
    out = []

    while len(notSearch) > 0:
        # print 'notSearch:', notSearch
        i = notSearch.pop(0)
        while Rulers.is_Action(i, type_1):
            # print '名词栈：',n.show()
            # print '动词栈：',v.show()
            # print '不及物动词栈：',vi_counter.show()
            # print '被动语态栈：',ed_counter.show()
            # print '名词对内次数栈：',p_counter.show()
            # print '动词计数栈：',v_counter.show()
            # print '名词计数栈：',n_counter.show()
            # print '词对内名词计数栈：',constant.show()
            if n.peek() != 'them':
                constant_p_counter.Empty()
                constant_n_counter.Empty()
                constant_n.Empty()
                temp1.Empty()
                temp2.Empty()
                temp3.Empty()
                temp_n = n_counter.peek()
                constant_n_counter.push(temp_n)
                temp_counter = 0

                while temp_n != 0 and temp_n != None:
                    temp_n = temp_n - 1
                    try:
                        t = p_counter.pop()
                        temp_counter += t
                        temp1.push(t)
                        temp2.push(t)
                    except:
                        print ('270pop失败')

                while temp1.isNotEmpty():
                    try:
                        p_counter.push(temp1.pop())
                    except:
                        print ('281pop失败')

                while temp2.isNotEmpty():
                    try:
                        constant_p_counter.push(temp2.pop())
                    except:
                        print ('289pop失败')

                while temp_counter != 0:
                    temp_counter -= 1
                    try:
                        t = n.pop()
                        constant_n.push(t)
                        temp3.push(t)
                    except:
                        print ('298pop失败')



                while temp3.isNotEmpty():
                    try:
                        n.push(temp3.pop())
                    except:
                        print ('307pop失败')



            '''print constant_n.show()
            print constant_p_counter.show()
            print constant_n_counter.show()'''

            temp = Rulers.Action(i, n, v, vi_counter, ed_counter, p_counter, v_counter, n_counter, PP_sign,
                                    constant_n_counter, constant_n, constant_p_counter)
            if type(temp) == type(1)and temp > 99:  # 动作
                if len(notSearch) > 0:
                    i = notSearch.pop(0)
                else:
                    # print 'out1:', out
                    return lower_out(out)
            else:
                if type(temp) == type(1):  # 操作失败，即返回值为0
                    out.append('')
                    if len(notSearch) > 0:
                        i = notSearch.pop(0)
                    else:
                        # print 'out2:', out
                        return lower_out(out)
                else:
                    # print '后处理前：',temp
                    for j in temp:

                        if after_process(j):  # 后处理判断
                            out.append(j)

                            '''else:  # 代词还原
                                for k in j:
                                    if k != 'them':
                                        while constant.isNotEmpty():
                                            t = []
                                            t.append(k)
                                            t.append(constant.pop())
                                            # print t
                                            out.append(t)
                    for j in temp:
                        print j
                        temp_counter = 0
                        for k in j:
                            temp_counter += 1
                            if temp_counter == 2:
                                constant.push(k)'''
                    if len(notSearch) > 0:
                        i = notSearch.pop(0)
                    else:
                        # print 'out3:', out
                        return lower_out(out)
            # print 'i:', i
        if len(i) == 1 and isinstance(i[0], str):  # 叶节点

            if Rulers.is_NN(i):
                n.push(i[0])


            if Rulers.is_PRP(i):
                # print '压入代词'
                if i[0] == 'them':
                    n.push(i[0])

            if Rulers.is_VB(i):
                # print'压入动词'
                v.push(i[0])
            '''if Rulers.is_IN(i):
                #print'压入动词'
                in_Stanford.push(i[0])'''

        else:  # 非叶节点
            if type(i) == type_1:
                '''if i.label() == 'ROOT':   # 单独考虑ROOT下连NP的情况
                    for j in i:
                        if j.label() == 'NP':
                            print levelTraverse(sent)
                            return 0 '''
                t = []
                t_label = []
                for j in i:

                    if type(j) == str:  # 防止数字str类型的j
                        return []
                    if len(j.label()) <= 2:
                        t_label.append(j.label())
                    else:
                        t_label.append(first_two(j.label()))
                ed = 0
                if ed_counter.isEmpty():
                    temp = Rulers.ruleSet(i, t_label, ed, PP_sign)
                else:
                    ed = 1
                    temp = Rulers.ruleSet(i, t_label, ed, PP_sign)
                if temp:
                    t.extend(temp)  # 加动作
                t.extend(notSearch)
                notSearch = t

    return lower_out(out)


def extract(s):
    l = len(s)
    if l > 300 or l < 5:
        return []

    # offline support可以作为特殊处理
    s = preProcess(s)  # 在Root直接连NP时，
    # print s[1]在句首加I;去除句子中的（）以及其中的内容;删除all 、all of;删除副词RB
    #     # print s[0]

    if s[1] == '':
        temp = deepTraverse(s[0])
        print ('提出特征：', temp)

    else:
        temp1 = deepTraverse(s[0])
        temp2 = deepTraverse(s[1])
        temp = temp1 + temp2
        print ('提出特征：', temp)
    result = []
    t = 0
    if temp != [] and temp != [[]]:
        try:
            for i in temp:
                for j in i:
                    # print(j)
                    if j not in "a":
                        t = 1
                if t == 1:
                    result.append(i)
                t = 0

        except:
            print ('不是数组结构error 428')
            if temp == 0:
                return []
            return temp
    if result == 0:
        return []
    return result


if __name__ == '__main__':
    s = ' This app can recognises what goods you are looking for '
    # temp = deepTraverse(s)
    extract(s)




