# coding=utf-8

import extract_feature


class Stack:
    """模拟栈"""

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return len(self.items) == 0

    def isNotEmpty(self):
        return len(self.items) != 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        if not self.isEmpty():
            return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)

    def show(self):
        temp = []
        while self.isNotEmpty():
            temp.insert(0, self.pop())
        for i in temp:
            self.push(i)
        return temp

    def Empty(self):
        while self.isNotEmpty():
            temp = self.pop()
        return self


def first_two(word):
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


def is_NN(t):
    if "NN" in t.label():
        return 1


def is_PRP(t):
    if t.label() == 'PRP':
        return 1


'''def is_IN(t):
    if "IN" in t.label():
        return 1 '''


def is_VB(t):
    if "VB" in t.label():
        return 1


def is_Action(i, t):
    if type(i) == t:
        return 0
    return 1


def ruleSet(t, t_label, ed, PP_sign):
    if t.label() == 'VP':
        return rule_VP(t, t_label, ed)
    if t.label() == 'NP':
        return rule_NP(t, t_label)
    if t.label() == 'PP':
        if PP_sign.isEmpty():
            temp = []
            for i in t:
                temp.append(i)
            return temp
        else:
            notSearch = []
            notSearch.append('PP_sign')
            for i in t:
                notSearch.append(i)
            notSearch.append('PP_cancel')
            temp = extract_feature.deepTraverse(notSearch)
            return temp
    if first_two(t.label()) == 'SB':
        return rule_SB(t, t_label)

    temp = []
    for i in t:
        temp.append(i)
    return temp


def rule_SB(t,t_label):

    if t_label == ['WH', 'S']:  # VB+AD+PP 为特殊形式 提取PP中的名词
        temp_wh = []
        for i in t:
            temp_wh.append(i)
        if temp_wh[0].label == ['WP', 'NN']:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter == 1:
                    temp.append(i)
            return temp
        else:
            temp = []
            for i in t:
                temp.append(i)
            return temp

    temp = []
    for i in t:
        temp.append(i)
    return temp


def rule_PP(t, t_label):
    '''if t_label == ['IN', 'NP']:
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_1_merga')
        temp.append('action_merga_PP')
        return temp

    if t_label == ['TO','NP']:
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_1_merga')
        temp.append('action_merga_PP')
        return temp'''


def rule_VP(t, t_label, ed):
    # 从PP中提取特征型（特殊）

    if t_label == ['VB', 'AD', 'PP']:  # VB+AD+PP 为特殊形式 提取PP中的名词
        temp = []
        for i in t:
            temp.append(i)
        temp.append('VP_1')
        temp.append('action_merga')
        return temp

    if t_label == ['VB', 'AD', 'S']:
        temp = []
        for i in t:
            if i.label() != 'S':
                temp.append(i)
        temp.append('VP_1')
        temp.append('action_merga')
        return temp

    if t_label == ['VB', ',', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
            temp.append('action_merga')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter != 3:
                    temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', ',', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        print ('进入1')
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            print ('进入2')
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter != 3:
                    temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PR', 'PP', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter != 3:
                    temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'SB', ',', 'SB']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter < 3:
                    temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'NP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                if temp_counter == 1:
                    temp.append(i)
                    temp.append('Vi')
                    temp.append('VP_1')
                if temp_counter == 2:
                    temp.append(i)
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'S']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
                if temp_counter == 2:
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'SB']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
                if temp_counter == 2:
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', ',', 'SB']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
                if temp_counter == 2:
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PP', 'AD']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if 'VB' in i.label():
                    temp.append(i)
                    temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                    temp.append('VP_1')
        return temp

    if t_label == ['VB', 'VP']:  # 被动语态处理方法
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter == 1:
                temp.append('ED')
            else:
                temp.append(i)
        return temp

    if t_label == ['RB', 'VB', 'PP']:
        temp = []
        for i in t:
            if 'VB' not in i.label():
                temp.append(i)
        # temp.append('VP_1')
        # temp.append('action_merga')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'PP']:  # 不及物动词及被动语态剪枝处理方法
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'PP':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp_counter += 1
                temp.append(i)
                if temp_counter == 1:
                    temp.append('Vi')
                if temp_counter == 3:
                    temp.append('Vi')
                    temp.append('VP_2')
            temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PR', 'PP']:  # 不及物动词处理方法（1）
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            temp.append(i)
            if temp_counter == 1:
                temp.append('Vi')
                temp.append('VP_1')
        temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'PP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
                    temp.append('PP_sign')
        temp.append('PP_cancel')
        return temp

    if t_label == ['VB', 'NP', 'PP', 'PP']:
        temp = []
        temp_counter = 0
        temp_counter2 = 0
        for i in t:
            if first_two(i.label()) == 'VB':
                temp.append(i)
            if first_two(i.label()) == 'NP':
                temp.append(i)
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
            if first_two(i.label()) == 'PP':
                temp_counter2 += 1
                if temp_counter2 == 1:
                    temp.append('PP_sign')
                    temp.append(i)
                    temp.append('PP_cancel')
                if temp_counter2 == 2:
                    temp.append('PP_sign')
                    temp.append(i)
                    temp.append('PP_cancel')
        return temp

    if t_label == ['VB', 'NP', 'NP', 'PP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('VP_1')
                    temp.append('NP_2_merga')
                    temp.append('action_merga')
                    temp.append('PP_sign')
        temp.append('PP_cancel')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'NP', 'PP']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            if 'PP' not in i.label():
                print ('在进入')
                temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_2')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'NP', 'PP', 'PP']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            if 'PP' not in i.label():
                print ('在进入')
                temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_2')
                    temp.append('action_merga')
        return temp

    if t_label == ['AD', 'VP', 'CC', 'VP']:
        temp = []
        for i in t:
            temp.append(i)
        return temp

    # 预处理 去除AD : . PP ,

    temp_t = []
    t_label = []
    for temp in t:
        # FR Now, instantly monitor changes to grades and attendance with push notifications!
        if first_two(temp.label()) not in ['AD', ':', '.', 'FR', 'PP', 'RB']:  # 去掉了一个逗号，
            temp_t.append(temp)
            t_label.append(first_two(temp.label()))
    t = temp_t

    # 直接在后面加动词数和动作型

    if t_label == ['VB', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PR', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PR', ',', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', ',', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'VP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'S':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'S', ',']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'S':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'SB']:
        if ed:
            temp = []
            temp.append('ED_C')
            for i in t:
                if i.label() != 'SB':
                    temp.append(i)
            temp.append('VP_1')
        else:
            temp = []
            temp_counter = 0
            for i in t:
                temp.append(i)
                if first_two(i.label()) == 'SB':
                    temp_counter += 1
                    if temp_counter == 1:
                        temp.append('VP_1')
                        temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('VP_1')
                    temp.append('NP_2_merga')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', ',', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('VP_1')
                    temp.append('NP_2_merga')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'PR', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'PR']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'SB']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', 'VP', '.']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'NP', ',']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_1')
                    temp.append('action_merga')
        return temp

    # 多VB型

    if t_label == ['VB', ',', 'VB', 'CC', 'VB', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_3')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', ',', 'VB', 'CC', 'VB', 'NP', ',']:

        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_3')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'NP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_2')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'NP', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_2')
                    temp.append('action_merga')
        return temp

    if t_label == ['VB', 'CC', 'VB', 'NP', 'PP']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NP':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('VP_2')
                    temp.append('action_merga')
        return temp

    temp = []
    for i in t:
        temp.append(i)
    return temp


def rule_NP(t, t_label):
    # 此处的为特殊处理型（需剪枝等手段处理特殊的句子）

    if t_label == ['AD', 'JJ', 'NN']:  # 剪枝AD
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter != 1:
                temp.append(i)
        temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN', 'CD']:  # 强行剪支
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter == 2:
                temp.append(i)
                temp.append('action_NNcounter_1')
                temp.append('NP_1')
            if temp_counter == 3:
                temp.append(i)
        return temp

    if t_label == ['NP', 'NN']:  # 强行剪支
        temp = []
        temp_counter = 0
        for i in t:
            if i.label() != 'NP':
                temp.append(i)
        return temp

    if t_label == ['NP', 'NP', ',', 'AD']:  # 强行剪支
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter == 1:
                temp.append(i)
                temp.append('action_NNcounter_1')
                temp.append('NP_1')
            if temp_counter == 4:
                temp.append(i)
        return temp

    '''if t_label == ['DT', 'NN', 'NN', 'VB', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if 'VB' not in i.label():  # 强行剪去一支VB
                temp.append(i)
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
                temp.append('NP_2')
        return temp'''

    # 此处开始预处理（剪掉的包括DT JJ AD CD RB）

    temp_t = []
    t_label = []
    for temp in t:
        # QP PowerSchool is the fastest-growing, most widely used student information system, supporting more than 13 million students across the globe.
        if first_two(temp.label()) not in ['DT', 'JJ', 'AD', 'CD', 'RB', 'PO', 'X', ':']:
            temp_t.append(temp)
            t_label.append(first_two(temp.label()))
    t = temp_t

    # 此处的为NN型（只需在最后的NN后面加入相应的NN数）

    if t_label == ['NN', 'NN', 'VB', 'NN']:  # 特殊处理 Wabbitemu creates a Texas Instruments graphing calculator right
        #  on your Android device.
        temp = []
        for i in t:
            if first_two(i.label()) == 'NN':
                temp.append(i)
        temp.append('action_NNcounter_3')
        temp.append('NP_1')
        return temp

    if t_label == ['NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == [',', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['PR']:  # 错误（将代词都处理）
        temp = []
        for i in t:
            temp.append(i)
        temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                    temp.append('NP_1')
        return temp

    if t_label == ['PR', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['PR', 'NN', 'S']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                    temp.append('NP_1')
        return temp

    if t_label == ['VB', 'NN']:  # DODGE the oncoming trains!
        temp = []
        temp_counter = 0
        for i in t:
            if 'VB' not in i.label():
                temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['VB', 'NN', 'NN', 'NN']:  # DODGE the oncoming trains!
        temp = []
        temp_counter = 0
        for i in t:
            if 'VB' not in i.label():
                temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 3:
                    temp.append('action_NNcounter_3')
        temp.append('NP_1')
        return temp

    if t_label == ['PR', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 3:
                    temp.append('action_NNcounter_3')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 4:
                    temp.append('action_NNcounter_4')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 5:
                    temp.append('action_NNcounter_5')
        temp.append('NP_1')
        return temp

    if t_label == ['PR', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 3:
                    temp.append('action_NNcounter_3')
        temp.append('NP_1')
        return temp

    if t_label == ['NN', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    '''if t_label == ['NN', 'JJ', 'NN']:
        temp = []
        for i in t:
            temp.append(i)
        temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp'''

    # 包含连词或逗号

    if t_label == ['NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['VB', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            if first_two(i.label()) == 'NN':
                temp.append(i)
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', ',', 'NN', ',']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['CC', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'CC', 'NN', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', ',', 'NN', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'NN', 'CC', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['PR', 'NN', 'NN', 'CC', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'NN', 'NN', ',', 'NN', ',', 'NN', 'CC', 'NN']:
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 3:
                    temp.append('action_NNcounter_3')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
                if temp_counter == 6:
                    temp.append('action_NNcounter_1')
        temp.append('NP_4')
        return temp

    if t_label == ['NN', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'NN', 'CC', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 5:
                    temp.append('action_NNcounter_3')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'CC', 'NN', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_3')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
                if temp_counter == 6:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
                if temp_counter == 5:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['PR', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp

    if t_label == ['PR', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', 'CC', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
        temp.append('NP_4')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', ',', 'NN', ',', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
                if temp_counter == 6:
                    temp.append('action_NNcounter_2')
        temp.append('NP_4')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'CC', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', 'CC', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['PR', 'NN', ',', 'NN', 'CC', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['PR', 'NN', ',', 'NN', 'CC', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', ',', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
        temp.append('NP_4')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', ',', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
        temp.append('NP_5')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', ',', 'NN', ',', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
        temp.append('NP_5')
        return temp

    if t_label == ['NN', ',', 'NN', ',', 'NN', ',', 'NN', ',', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 2:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 4:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
                if temp_counter == 6:
                    temp.append('action_NNcounter_1')
        temp.append('NP_6')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', 'NN', ',', 'NN', 'NN', ',', 'NN', 'NN', 'CC', 'NN', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
                if temp_counter == 6:
                    temp.append('action_NNcounter_2')
                if temp_counter == 8:
                    temp.append('action_NNcounter_2')
                if temp_counter == 10:
                    temp.append('action_NNcounter_2')
        temp.append('NP_5')
        return temp

    if t_label == ['NN', 'NN', ',', 'NN', 'NN', ',', 'NN', 'NN', ',', 'NN', 'NN', ',', 'NN', 'CC', 'NN']:
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 4:
                    temp.append('action_NNcounter_2')
                if temp_counter == 6:
                    temp.append('action_NNcounter_2')
                if temp_counter == 8:
                    temp.append('action_NNcounter_2')
                if temp_counter == 9:
                    temp.append('action_NNcounter_1')
                if temp_counter == 10:
                    temp.append('action_NNcounter_1')
        temp.append('NP_6')
        return temp

    if t_label == ['PR', 'NN', 'NN', ',', 'NN', 'CC', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_2')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', 'CC', 'NN', 'NN', 'CC', 'NN', 'NN']:  # 没判断是否是动宾短语
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
                if temp_counter == 5:
                    temp.append('action_NNcounter_1')
        temp.append('NP_3')
        return temp

    if t_label == ['NN', 'NN', ',', 'CC', 'NN']:  # 没判断是否是动宾短语
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 2:
                    temp.append('action_NNcounter_2')
                if temp_counter == 3:
                    temp.append('action_NNcounter_1')
        temp.append('NP_2')
        return temp

    if t_label == ['NP', ',', 'NN', 'CC', 'NN', 'NN']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            if i.label() != 'NP':
                temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                if temp_counter == 3:
                    temp.append('action_NNcounter_2')
        temp.append('NP_2')
        return temp

    if t_label == ['NN', 'NP']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp.append(i)
            if first_two(i.label()) == 'NN':
                temp_counter += 1
                if temp_counter == 1:
                    temp.append('action_NNcounter_1')
                    temp.append('NP_1')
        temp.append('NP_2_merga')
        return temp

    # 此处的为NP型（需在最后的NP后面加入相应的NP_数_merga）

    if t_label == ['NP', 'PP']:
        temp = []
        for i in t:
            if first_two(i.label()) == 'NP':
                temp.append(i)
                temp.append('NP_1_merga')
            if first_two(i.label()) == 'PP':
                temp.append('PP_sign')
                temp.append(i)
                temp.append('PP_cancel')
        return temp

    if t_label == ['NP', ',', 'PP']:
        temp = []
        for i in t:
            if i.label() == 'NP':
                temp.append(i)
                temp.append('NP_1_merga')
        return temp

    if t_label == ['NP', 'PP', 'S']:
        temp = []
        for i in t:
            if i.label() == 'NP':
                temp.append(i)
                temp.append('NP_1_merga')
            if i.label() == 'S':
                temp.append(i)
        return temp

    if t_label == ['NP', 'SB']:
        temp = []
        for i in t:
            if i.label() == 'NP':
                temp.append(i)
                temp.append('NP_1_merga')
        return temp

    if t_label == ['NP', ',', 'SB', ',']:
        print ('进入')
        temp = []
        for i in t:
            temp.append(i)
            if i.label() == 'NP':
                temp.append('NP_1_merga')
        return temp

    if t_label == ['NP', ',', 'VP']:
        temp = []
        for i in t:
            temp.append(i)
            if i.label() == 'NP':
                temp.append('NP_1_merga')
        return temp

    if t_label == ['NP', 'VP']:
        temp = []
        for i in t:
            if i.label() == 'NP':
                temp.append(i)
                temp.append('NP_1_merga')
        return temp

    if t_label == ['NP', 'JJ', 'NN']:
        temp = []
        for i in t:
            temp.append(i)
        temp.append('action_NNcounter_1')
        temp.append('NP_1')
        return temp

    if t_label == ['NP', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', 'CO', 'NP']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter != 2:
                temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', ',', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',']:  # 没判断是否是动宾
        print ('进入hahha')
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', ',', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', ',', 'VP', ',', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        temp_counter = 0
        for i in t:
            temp_counter += 1
            if temp_counter == 1 or temp_counter == 3:
                temp.append(i)
        return temp

    if t_label == ['NP', ',', 'CC', 'NP', ',']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_2_merga')
        return temp

    if t_label == ['NP', ',', 'NP', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_3_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_3_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_4_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_4_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'CC', 'NP']:  # 没判断是否是动宾
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_4_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'CC', 'NP']:  # 没判断是否是动宾
        print ('进入')
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_4_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'NP', 'CC', 'NP']:  # 最后一个NP是more
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_5_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'NP', ',', 'NP']:  # 最后一个NP是more
        print ('进入')
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_5_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'NP', ',', 'PP']:  # 最后一个NP是more
        print ('进入')
        temp = []
        temp_counter = 0
        for i in t:
            if first_two(i.label()) == 'NP':
                temp.append(i)
                temp_counter += 1
                if temp_counter == 4:
                    temp.append('NP_4_merga')
        return temp

    if t_label == ['NP', ',', 'NP', ',', 'NP', ',', 'NP', ',', 'NP', ',', 'NP', 'CC', 'NP']:  # 最后一个NP是more
        print ('进入')
        temp = []
        for i in t:
            temp.append(i)
        temp.append('NP_7_merga')
        return temp

    temp = []
    for i in t:
        temp.append(i)
    return temp


def Action(i, n, v, vi_counter, ed_counter, p, v_counter, n_counter, PP_sign, constant_n_counter, constant_n,
           constant_p_counter):
    temp = []

    if type(i) == type([u'investigate', u'areas']):
        # print '检测到直读词对：',i
        temp.append(i)
        return temp

    PairSet = []
    pair = []
    if i == 'action_merga':
        temp_n = []
        temp_p = []
        try:
            v_c = v_counter.pop()
        except:
            print ('动词计数器pop失败')
            return 0
        try:
            n_c = n_counter.pop()
            # print '名词数为：',n_c
        except:
            print ('名词计数器pop失败')
            return 0
        # print 'v:',v_c
        # print 'n:',n_c

        # print n.peek()
        '''if n.peek() == 'them':
            # print '进入'
            n.pop()
            p.pop()
            try:
                n_c = n_counter.pop()
            except:
                print '名词数pop失败'
                return 0'''

        if v_c > 1:
            for j in range(0, v_c - 1):
                try:
                    V = v.pop()
                except:
                    print ('动词pop失败')
                    return 0
                for k in range(0, n_c):
                    try:
                        P = p.pop()
                    except:
                        print ('词组词数pop失败')
                        return 0
                    temp_p.insert(0, P)
                    pair.append(V)
                    for j in range(0, P):
                        try:
                            N = n.pop()
                        except:
                            print ('名词pop失败')
                            return 0
                        temp_n.insert(0, N)
                        pair.insert(1, N)
                    PairSet.append(pair)
                    pair = []
                for j in temp_n:
                    n.push(j)
                for j in temp_p:
                    p.push(j)
            # 最后一层需要弹栈
            try:
                V = v.pop()
            except:
                print ('动词pop失败')
                return 0
            for k in range(0, n_c):
                try:
                    P = p.pop()
                except:
                    print ('词组词数pop失败')
                    return 0
                pair.append(V)
                for j in range(0, P):
                    try:
                        N = n.pop()
                    except:
                        print ('名词pop失败')
                        return 0
                    pair.insert(1, N)
                PairSet.append(pair)
                pair = []

        if v_c == 1:
            V = v.pop()
            for k in range(0, n_c):
                pair = []
                try:
                    P = p.pop()
                except:
                    print('词组词数pop失败')
                    return 0
                pair.append(V)
                for j in range(0, P):
                    try:
                        N = n.pop()
                    except:
                        print ('名词pop失败')
                        return 0
                    pair.insert(1, N)
                '''if 'them' not in pair:'''
                PairSet.append(pair)
                # print pair
            '''if 'them' in pair:
                try:
                    n_c = n_counter.pop()
                except:
                    print '名词计数器pop失败'
                    return 0
                print n_c
                for k in range(0, n_c):
                    pair = []
                    P = p.pop()
                    pair.append(V)
                    for j in range(0, P):
                        N = n.pop()
                        print N
                        pair.insert(1, N)
                    PairSet.append(pair)'''

    if i == 'NP_1_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 1):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2046')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_2_merga':  # Get younger or older JJR
        temp_counter = 0
        n_c = 0
        for k in range(0, 2):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2058')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_3_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 3):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2070')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_4_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 4):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2082')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_5_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 5):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2094')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_6_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 6):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2106')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'NP_7_merga':
        temp_counter = 0
        n_c = 0
        for k in range(0, 7):
            try:
                n_c = n_counter.pop()
            except:
                print ('error2118')
            temp_counter += n_c
        n_counter.push(temp_counter)
        temp_counter += 100
        return temp_counter

    if i == 'action_NNcounter_1':
        p.push(1)
        return 100

    if i == 'action_NNcounter_2':
        p.push(2)
        return 100

    if i == 'action_NNcounter_3':
        p.push(3)
        return 100

    if i == 'action_NNcounter_4':
        p.push(4)
        return 100

    if i == 'action_NNcounter_5':
        p.push(5)
        return 100

    if i == 'PP_sign':
        PP_sign.push(1)
        return 100

    if i == 'PP_cancel':
        try:
            PP_sign.pop()
        except:
            print ('error2158')
        return 100

    if i == 'NP_1':
        n_counter.push(1)
        return 100

    if i == 'NP_2':
        n_counter.push(2)
        return 100

    if i == 'NP_3':
        n_counter.push(3)
        return 100

    if i == 'NP_4':
        n_counter.push(4)
        return 100

    if i == 'NP_5':
        n_counter.push(5)
        return 100

    if i == 'NP_6':
        n_counter.push(6)
        return 100

    if i == 'NP_7':
        print ('进入')
        n_counter.push(7)
        return 100

    if i == 'NP_8':
        n_counter.push(8)
        return 100

    if i == 'VP_1':
        v_counter.push(1)
        return 100

    if i == 'VP_2':
        v_counter.push(2)
        return 100

    if i == 'VP_3':
        v_counter.push(3)
        return 100

    if i == 'VP_4':
        v_counter.push(4)
        return 100

    if i == 'Vi':
        vi_counter.push(1)
        return 100

    if i == 'ED':
        ed_counter.push(1)
        return 100

    if i == 'ED_C':
        try:
            ed_counter.pop()
        except:
            print ('error2222')
        return 100
    # print '词对为：',PairSet

    temp = []

    for i in PairSet:
        # print 'i:', i
        n_c = constant_n_counter.peek()
        if n_c == None:
            n_c = 0
        if 'them' in i:
            V = i[0]
            for k in range(0, n_c):
                pair = []
                try:
                    P = constant_p_counter.pop()
                except:
                    print('名词pop失败')
                    return 0
                pair.append(V)
                for j in range(0, P):
                    try:
                        N = constant_n.pop()
                        # print 'N：', N
                    except:
                        print('名词pop失败')
                        return 0
                    pair.insert(1, N)
                temp.append(pair)
        else:
            temp.append(i)
    PairSet = temp
    return PairSet
