import numpy as np
import copy
from draw import draw_cube

N = 3                  # 阶数
n = (N * N - 1)        # 每个面除了中心点的元素数量

pathDict = dict()
depthDict = dict()
searchDict = dict()

# 旋转方式
def rot(cube_, face, direction='CW'):
    cube = copy.deepcopy(cube_)
    # 由于可以通过顺时针旋转达到逆时针旋转的效果，此处只用顺时针旋转
    if direction == 'CW':
        if face == 0:
            cube[0] = np.rot90(cube[0], -1); tmp = copy.deepcopy(cube[3][:, -1])
            cube[3][:, -1] = cube[5][0, :]; cube[5][0, :] = cube[1][:, 0]
            cube[1][:, 0] = cube[4][-1, :]; cube[4][-1, :] = tmp
        elif face == 1:
            cube[1] = np.rot90(cube[1], -1); tmp = copy.deepcopy(cube[0][:, -1])
            cube[0][:, -1] = cube[5][:, -1]; cube[5][:, -1] = cube[2][:, 0]
            cube[2][:, 0] = cube[4][:, -1]; cube[4][:, -1] = tmp
        elif face == 2:
            cube[2] = np.rot90(cube[2], -1); tmp = copy.deepcopy(cube[4][0, :])
            cube[4][0, :] = cube[1][:, -1]; cube[1][:, -1] = cube[5][-1, :]
            cube[5][-1, :] = cube[3][:, 0]; cube[3][:, 0] = tmp
        elif face == 3:
            cube[3] = np.rot90(cube[3], -1); tmp = copy.deepcopy(cube[0][:, 0])
            cube[0][:, 0] = cube[4][:, 0]; cube[4][:, 0] = cube[2][:, -1]
            cube[2][:, -1] = cube[5][:, 0]; cube[5][:, 0] = tmp
        elif face == 4:
            cube[4] = np.rot90(cube[4], -1); tmp = copy.deepcopy(cube[0][0, :])
            cube[0][0, :] = cube[1][0, :]; cube[1][0, :] = cube[2][0, :]
            cube[2][0, :] = cube[3][0, :]; cube[3][0, :] = tmp
        elif face == 5:
            cube[5] = np.rot90(cube[5], -1); tmp = copy.deepcopy(cube[0][-1, :])
            cube[0][-1, :] = cube[1][-1, :]; cube[1][-1, :] = cube[2][-1, :]
            cube[2][-1, :] = cube[3][-1, :]; cube[3][-1, :] = tmp
        return cube

def matching(cubeCurr, cubeTarget):
    """判断是否匹配"""
    return (cubeCurr == cubeTarget).all()

def calc_distance(cubeCurr, cubeTarget, method='cnt'):
    """计算当前状态与最终状态的距离"""
    if method == 'cnt':
        return np.sum(cubeCurr != cubeTarget)
    elif method == 'l1':
        return np.sum(np.abs(cubeCurr - cubeTarget))
    elif method == 'l2':
        return np.sqrt(np.sum(np.power(cubeCurr - cubeTarget, 2)))

def array_2_str(cube):
    """数组[6x3x3]变为字符串"""
    cubeStr = ""
    for i in list(cube.reshape(-1)):
        cubeStr += str(i)[0]
    return cubeStr

def str_2_array(cubeStr):
    """字符串变为数组[6x3x3]"""
    cube = list()
    for i in cubeStr:
        cube.append(int(i))
    return np.array(cube).reshape((6, N, N))

def IDA(magicCube, magicCubeTarget):
    """IDA*法搜索解，返回还原过程"""
    heap = dict()
    magicCubeStr = array_2_str(magicCube)
    heap[magicCubeStr] = [calc_distance(magicCube, magicCubeTarget)]
    depthDict[magicCubeStr] = 0

    while len(heap):
        heap = dict(sorted(heap.items(), key=lambda x: x[1]))
        # 取出并删除heap中损失最小的项
        curr = list(heap.items())[0]
        heap.pop(curr[0])
        # 当前状态
        state = str_2_array(curr[0])
        stateStr = array_2_str(state)
        # 该状态与最终状态是否匹配
        if matching(state, magicCubeTarget): break
        # 该状态是否被搜索过
        if stateStr in searchDict: continue
        searchDict[stateStr] = True

        # 当前的深度
        depthCurr = depthDict[array_2_str(state)]

        for i in range(6):
            stateNew = rot(state, i, 'CW')
            stateNewStr = array_2_str(stateNew)
            # 若拓展的状态能在更浅层被搜到，或者状态没有被拓展，则更新
            if stateNewStr not in depthDict or depthDict[stateNewStr] > depthCurr + 1:
                depthDict[stateNewStr] = depthCurr + 1
                pathDict[stateNewStr] = stateStr
                heap[stateNewStr] = depthCurr + 1 + calc_distance(stateNew, magicCubeTarget)
    # 找魔方还原的路径并倒叙返回，为正序
    InitStr = array_2_str(magicCube)
    pathStr = array_2_str(magicCubeTarget)
    pathBackward = []
    while pathStr != InitStr:
        pathBackward.append(pathStr)
        pathStr = pathDict[pathStr]
    pathBackward.append(InitStr)

    return pathBackward[::-1]


if __name__ == '__main__':

    # 构造魔方的最终状态
    magicCubeTarget = np.zeros((6, N, N))
    magicCubeTarget += np.array([0, 1, 2, 3, 4, 5]).reshape((-1, 1, 1))

    # 待还原的魔方
    magicCubeTest = np.array([[[3, 3, 3], [0, 0, 5], [0, 0, 5]],
                              [[4, 2, 5], [1, 1, 5], [1, 1, 2]],
                              [[5, 4, 3], [2, 2, 3], [2, 2, 1]],
                              [[5, 0, 4], [4, 3, 1], [4, 3, 1]],
                              [[2, 1, 1], [5, 4, 4], [0, 0, 0]],
                              [[4, 4, 2], [5, 5, 2], [0, 3, 3]]])

    path = IDA(magicCubeTest, magicCubeTarget)

    # 画出魔方还原过程
    for p in path:
        draw_cube(p)


