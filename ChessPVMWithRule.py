#先手玩家为False，后手玩家为True
import turtle as tt
import Function as f
import pickle as pk
import math as m
#初始化
print("加载AI需要十几秒，请稍候~")
tree = pk.load(open("tree_withrule.pkl","rb"))#加载蒙特卡洛树
state = '0'*24#棋局状态
box = [
    [0,3,4,7],[1,4,5,8],[2,5,6,9],[7,10,11,14],[8,11,12,15],
    [9,12,13,16],[14,17,18,21],[15,18,19,22],[16,19,20,23]
    ]#记录每个格子未放木棍边，用于判断一个格子是否已被围住
color = {False:'red',True:'blue'}#用于绘图区别双方的颜色
score={False:0,True:0}#记录双方得分
cheat = True#用于一个实现防对称下法规则的bool量
player = False#当前拥有操作权的玩家
state_record = []#依次记录一局棋的所有状态
com_record = []#依次记录一局棋每一手的位置
choice = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]#可选下棋位置
c=0.1#置信区间上限算法中的可选参数
q = 0#用于一个实现防对称下法规则的数量
learn = False#决定是否在退出时保存更新的蒙特卡洛树


    

def value(x):#实现置信区间上限算法
    if x not in tree.keys():
        tree[x] = [0,0]
        return float('inf')
    vec = tree[x]
    if vec[1] == 0:
        return float('inf')
    return vec[0]/vec[1] + c * m.sqrt(m.log(n)/vec[1])



def state_choose():#AI选择下棋位置
    global state,q,n,state_record
    n = 0
    state_choice = []
    state_score = 0
    best_state = 0
    list_state = list(state)
    for i in choice:
        if q==1 and f.group_map[com_record[0]]==f.group_map[i]:
            continue
        x = list_state[:]
        x[i] = '1'
        x = ''.join(x)
        state_choice.append(x)
        if x in tree.keys():
            vec = tree[x]
            n = n + vec[1]
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
    state = best_state
    return com

def chpop(com):#将本轮下棋的位置弹出可选下棋位置的集合
    com_record.append(choice.pop(choice.index(com)))

def draw_line(com):#图形界面下棋时画线
    tt.color(color[player])
    start = f.key_map1[com]
    end = f.key_map2[com]
    tt.up()
    tt.goto(start[0],start[1])
    tt.down()
    tt.goto(end[0],end[1])

def draw_circle(x):#图形界面得分时画圆
    tt.begin_fill()
    tt.color(color[player],color[player])
    tt.up()
    x = f.circle_map[x]
    tt.goto(x[0]-25,x[1]-25)
    tt.down()
    tt.circle(25)
    tt.end_fill()
    
def search():#寻找棋局中是否有可以立即得分的下法，以实现“有分必得”策略
    for i in range(9):
        if len(box[i])==1:
            return i
    return -1


#游戏开始
while True:
    people = False
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
    end_flag = False
    q = 0
    f.init_draw()#初始化棋局
    while True:
        if player == people:#玩家操作
            while True:
                people_flag = True
                com = int(input("轮到你了："))
                if (com not in choice) or (q==1 and f.group_map[com_record[0]]==f.group_map[com]):
                    print("输入非法，请重下！")
                    continue
                chpop(com)
                state = list(state)
                state[com] = '1'
                state = ''.join(state)
                draw_line(com)
                for i in f.box_map[com]:
                    box[i].pop(box[i].index(com))
                    if box[i] == []:
                        people_flag = False
                        score[player] = score[player] + 1
                        draw_circle(i)
                        if score[player] >= 5:
                            end_flag = True
                            people_flag = True
                            break
                if people_flag:
                    if not end_flag:
                        state_record.append(state)
                    break
        else:#AI操作
            ready = search()
            while ready>=0:
                com = box[ready][0]
                chpop(com)
                state = list(state)
                state[com] = '1'
                state = ''.join(state)
                draw_line(com)
                for i in f.box_map[com]:
                    box[i].pop(box[i].index(com))
                    if box[i] == []:
                        score[player] = score[player]+1
                        draw_circle(i)
                    if score[player] >=5:
                        end_flag = True
                        break
                if end_flag:
                    break
                ready = search()   
            if end_flag:
                break
            com = state_choose()
            chpop(com)
            draw_line(com)
            for i in f.box_map[com]:
                box[i].pop(box[i].index(com))

        if end_flag:
            break
        q = q + 1
        player = not player

        
    #判断胜负
    if score[False] > score[True]:
        win = False
    else:
        win = True
    if win == people:
        print('恭喜，你赢了！')
    else:
        print('很遗憾，你输了！')
    #是否重玩
    x = 1
    try:
        x = int(input("重玩一局：输入0后回车\n退出：直接回车\n"))
    except ValueError:
        print("已退出")

    if x==0:
        continue
    #更新蒙特卡洛树
    if learn:
        print('AI资料保存中，请等待至程序自动结束，勿强行退出')
        while state_record != []:
            player = not player
            state = state_record.pop()
            if state not in tree.keys():
                continue
            tree[state][1] = tree[state][1] + 1
            if player == win:
                tree[state][0] = tree[state][0] + 1  
    break

if learn:
    pk.dump(tree,open("tree_withrule.pkl","wb"))#保存蒙特卡洛树
