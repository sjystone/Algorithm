import numpy as np
import copy
from draw import draw_square

EDGE = 4
STR = 'a'
LENGTH = EDGE * EDGE
dx = [0, 1, 0, -1]; dy = [1, 0, -1, 0]
a, b = 0.5, 1

pathDict = dict()
depthDict = dict()
searchDict = dict()

def reorder_num(str, strTarget):
    """通过逆序对的数量判断问题是否有解"""
    reorderNumInit, reorderNumTarget = 0, 0
    for i in range(len(str)):
        for j in range(i + 1, len(str)):
            if str[i] != STR and str[j] != STR and str[i] > str[j]:
                reorderNumInit += 1
            if strTarget[i] != STR and strTarget[j] != STR and strTarget[i] > strTarget[j]:
                reorderNumTarget += 1
    return reorderNumInit % 2 == reorderNumTarget % 2

def calc_distance(curr, target):
    """计算目前状态和目标状态的距离(l1城市距离)"""
    distance = 0
    for i in range(LENGTH):
        for j in range(LENGTH):
            if curr[i] == target[j] and i != j:
                distance += abs(i//EDGE - j//EDGE) + abs(i%EDGE - j%EDGE)
                break
    return distance

def A_search(init, target):
    if not reorder_num(init, target):
        print("Unsolvable"); return
    global x, y
    heap = dict()
    heap[init] = a * calc_distance(init, target)
    depthDict[init] = 0

    while len(heap):
        # 对heap按值(损失)从小到大进行排序
        heap = dict(sorted(heap.items(), key=lambda x: x[1]))
        # 取出并删除heap中损失最小的项
        curr = list(heap.items())[0]
        heap.pop(curr[0])

        state = curr[0]
        if state == target: break
        if state in searchDict: continue
        searchDict[state] = True

        stateCopy = copy.deepcopy(state)
        depthCurr = depthDict[state]

        # 找到'0'的位置
        for i in range(len(state)):
            if state[i] == STR:
                x = i // EDGE; y = i % EDGE
                break

        # 向上下左右四个方向拓展
        for direct in range(4):
            xNew, yNew = x + dx[direct], y + dy[direct]
            if xNew >= 0 and xNew < EDGE and yNew >= 0 and yNew < EDGE:
                stateList = list(state)
                stateList[x * EDGE + y], stateList[xNew * EDGE + yNew] = \
                    stateList[xNew * EDGE + yNew], stateList[x * EDGE + y]
                stateNew = "".join(stateList)
                if stateNew not in depthDict or depthDict[stateNew] > depthCurr + 1:
                    # 若拓展的状态能在更浅的层被搜索,或者状态没有被拓展,则更新改节点
                    depthDict[stateNew] = depthCurr + 1
                    pathDict[stateNew] = state
                    heap[stateNew] = a * depthDict[stateNew] + b * calc_distance(stateNew, target)

    pathBackward = []
    pathStr = target
    while pathStr != init:
        pathBackward.append(pathStr)
        pathStr = pathDict[pathStr]
    pathBackward.append(init)

    return pathBackward[::-1]


if __name__ == '__main__':

    # squareInit = '087453621'
    # squareTarget = '123456780'
    squareInit = 'abcdefghipjlmnko'
    squareTarget = 'badcefghijklmnop'

    import time
    time_start = time.time()
    path = A_search(squareInit, squareTarget)
    print('Time spend:', time.time() - time_start)
    for p in path:
        draw_square(p, squareTarget)
    print('Nums of steps:', len(path))
