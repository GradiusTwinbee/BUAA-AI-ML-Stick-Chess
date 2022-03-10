#先手玩家为False，后手玩家为True
import Function as f
import pickle as pk
import math as m
import random

tree = pk.load(open("tree_withrule.pkl","rb"))#加载蒙特卡洛树
print("读取完成")
train_times = int(input())#输入总训练次数                                                     
output = int(train_times*0.1)
t = 0#记录当前训练次数
score={False:0,True:0}#记录双方得分
choice = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]#可选下棋位置
state = '0'*24#棋局状态
box = [
    [0,3,4,7],[1,4,5,8],[2,5,6,9],[7,10,11,14],[8,11,12,15],
    [9,12,13,16],[14,17,18,21],[15,18,19,22],[16,19,20,23]
    ]#记录每个格子未放木棍边，用于判断一个格子是否已被围住
state_record = []#依次记录一局棋的所有状态
com_record = []#依次记录一局棋每一手的位置
cheat = True#用于一个实现防对称下法规则的bool量
player = False#当前拥有操作权的玩家
c=0.1#置信区间上限算法中的可选参数
n = 0#置信区间上限算法中的N(所有备选状态的已出现次数之和)
state_choice = []#备选状态
com = 0#当前所选下棋位置

def value(x):#实现置信区间上限算法
    if x not in tree.keys():
        tree[x] = [0,0]
        return float('inf')
    vec = tree[x]
    if vec[1] == 0:
        return float('inf')
    return vec[0]/vec[1] + c * m.sqrt(m.log(n)/vec[1])
    
    
    

def state_choose():#AI选择下棋位置
    global state,cheat,com,n,state_record
    flag2 = False
    n = 0
    state_choice = []
    state_score = 0
    best_state = 0
    list_state = list(state)
    for i in choice:
        if cheat and player and f.group_map[com_record[0]]==f.group_map[i]:
            flag2 = True
            continue
        x = list_state[:]
        x[i] = '1'
        x = ''.join(x)
        state_choice.append(x)
        if x in tree.keys():
            vec = tree[x]
            n = n + vec[1]
    if flag2:
        cheat = False
    for s in state_choice:
        now_score = value(s)
        if now_score>=state_score:
            state_score = now_score
            best_state = s
    for i in range(24):
        if best_state[i] != state[i]:
            com = i
            break
    state_record.append(best_state)
    com_record.append(com)
    state = best_state
        
def search():#寻找棋局中是否有可以立即得分的下法，以实现“有分必得”策略
    for i in range(9):
        if len(box[i])==1:
            return i
    return -1

def chpop(com):#将本轮下棋的位置弹出可选下棋位置的集合
    com_record.append(choice.pop(choice.index(com)))

while t<train_times:#训练代码
    if t%output==0:
        print(t/train_times)
        print(com_record)
    choice = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    score={False:0,True:0}
    state = '0'*24
    box = [
    [0,3,4,7],[1,4,5,8],[2,5,6,9],[7,10,11,14],[8,11,12,15],
    [9,12,13,16],[14,17,18,21],[15,18,19,22],[16,19,20,23]
    ]
    cheat = True
    player = False
    state_record = []
    com_record = []
    flag = False#用于判断一局棋是否已经结束
    while True:
        #实现有分必得策略
        ready = search()
        while ready>=0:
            com = box[ready][0]
            chpop(com)
            state = list(state)
            state[com] = '1'
            state = ''.join(state)
            for i in f.box_map[com]:
                box[i].pop(box[i].index(com))
                if box[i] == []:
                    score[player] = score[player]+1
            if score[player] >=5:
                flag = True
                break
            ready = search()
        #当前不可得分时，AI下棋的代码
        if flag:
            break
        state_choose()
        choice.pop(choice.index(com))
        for i in f.box_map[com]:
            box[i].pop(box[i].index(com))
        player = not player
    #判断胜负与更新蒙特卡洛树
    if score[False] > score[True]:
        win = False
    else:
        win = True
    while state_record != []:
        player = not player
        state = state_record.pop()
        tree[state][1] = tree[state][1] + 1
        if player == win:
            tree[state][0] = tree[state][0] + 1
    t = t + 1
print(com_record)
pk.dump(tree,open("tree_withrule.pkl","wb"))#保存蒙特卡洛树

