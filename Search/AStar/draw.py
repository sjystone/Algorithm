// Code to visualize cube and eight_digit problem

import matplotlib.pyplot as plt
import numpy as np
import cv2


def draw_cube(dataStr):
    # 准备一些坐标
    n_voxels = np.ones((5, 5, 5), dtype=bool)

    # 生成间隙
    size = np.array(n_voxels.shape) * 2
    filled_2 = np.zeros(size - 1, dtype=n_voxels.dtype)
    filled_2[::2, ::2, ::2] = n_voxels

    # 缩小间隙
    # 构建voxels顶点控制网格
    # x, y, z均为6x6x8的矩阵，为voxels的网格，3x3x4个小方块，共有6x6x8个顶点。
    # 这里//2是精髓，把索引范围从[0 1 2 3 4 5]转换为[0 0 1 1 2 2],这样就可以单独设立每个方块的顶点范围
    x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) //2  # 3x6x6x8，其中x,y,z均为6x6x8

    x[1::2, :, :] += 0.95
    y[:, 1::2, :] += 0.95
    z[:, :, 1::2] += 0.95
    # 修改最外面的体素的厚度，作为六个面来使用
    x[0, :, :] += 0.94
    y[:, 0, :] += 0.94
    z[:, :, 0] += 0.94

    x[-1, :, :] -= 0.94
    y[:, -1, :] -= 0.94
    z[:, :, -1] -= 0.94

    # 去除边角料
    filled_2[0, 0, :] = 0
    filled_2[0, -1, :] = 0
    filled_2[-1, 0, :] = 0
    filled_2[-1, -1, :] = 0

    filled_2[:, 0, 0] = 0
    filled_2[:, 0, -1] = 0
    filled_2[:, -1, 0] = 0
    filled_2[:, -1, -1] = 0

    filled_2[0, :, 0] = 0
    filled_2[0, :, -1] = 0
    filled_2[-1, :, 0] = 0
    filled_2[-1, :, -1] = 0

    # 给魔方六个面赋予不同的颜色
    colors = np.array(['#ffd400', "#fffffb", "#f47920", "#d71345", "#145b7d", "#45b97c"])
    facecolors = np.full(filled_2.shape, '#77787b')  # 设一个灰色的基调
    facecolors[:, :, -1] = colors[0]    # 上面
    #facecolors[:, :, 0] = colors[1]
    facecolors[:, 0, :] = colors[2]     # 正面
    #facecolors[:, -1, :] = colors[3]
    #facecolors[0, :, :] = colors[4]
    facecolors[-1, :, :] = colors[5]    # 右面

    facecolors[0:3, 0:3, -1] = colors[int(dataStr[42])]
    facecolors[3:6, 0:3, -1] = colors[int(dataStr[43])]
    facecolors[6:9, 0:3, -1] = colors[int(dataStr[44])]
    facecolors[0:3, 3:6, -1] = colors[int(dataStr[39])]
    facecolors[3:6, 3:6, -1] = colors[int(dataStr[40])]
    facecolors[6:9, 3:6, -1] = colors[int(dataStr[41])]
    facecolors[0:3, 6:9, -1] = colors[int(dataStr[36])]
    facecolors[3:6, 6:9, -1] = colors[int(dataStr[37])]
    facecolors[6:9, 6:9, -1] = colors[int(dataStr[38])]

    facecolors[0:3, 0, 0:3] = colors[int(dataStr[6])]
    facecolors[3:6, 0, 0:3] = colors[int(dataStr[7])]
    facecolors[6:9, 0, 0:3] = colors[int(dataStr[8])]
    facecolors[0:3, 0, 3:6] = colors[int(dataStr[3])]
    facecolors[3:6, 0, 3:6] = colors[int(dataStr[4])]
    facecolors[6:9, 0, 3:6] = colors[int(dataStr[5])]
    facecolors[0:3, 0, 6:9] = colors[int(dataStr[0])]
    facecolors[3:6, 0, 6:9] = colors[int(dataStr[1])]
    facecolors[6:9, 0, 6:9] = colors[int(dataStr[2])]

    facecolors[-1, 0:3, 0:3] = colors[int(dataStr[15])]
    facecolors[-1, 3:6, 0:3] = colors[int(dataStr[16])]
    facecolors[-1, 6:9, 0:3] = colors[int(dataStr[17])]
    facecolors[-1, 0:3, 3:6] = colors[int(dataStr[12])]
    facecolors[-1, 3:6, 3:6] = colors[int(dataStr[13])]
    facecolors[-1, 6:9, 3:6] = colors[int(dataStr[14])]
    facecolors[-1, 0:3, 6:9] = colors[int(dataStr[9])]
    facecolors[-1, 3:6, 6:9] = colors[int(dataStr[10])]
    facecolors[-1, 6:9, 6:9] = colors[int(dataStr[11])]

    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(x, y, z, filled_2, facecolors=facecolors)
    #plt.show()
    plt.ion()
    plt.pause(1)
    plt.close()


def draw_square(dataStr, targetStr='123456780'):
    n = int(np.sqrt(len(dataStr)))
    figure_curr = np.zeros((30 * n, 30 * n))
    for i in range(n):
        for j in range(n):
            figure_curr[i * 30: i * 30 + 30, j * 30: j * 30 + 30] = ord(dataStr[i * n + j])
    figure_target = np.zeros((30 * n, 30 * n))
    for i in range(n):
        for j in range(n):
            figure_target[i * 30: i * 30 + 30, j * 30: j * 30 + 30] = ord(targetStr[i * n + j])

    plt.figure(1)
    plt.subplot(211)
    plt.imshow(figure_curr)
    plt.subplot(212)
    plt.imshow(figure_target)

    plt.ion()
    plt.pause(1)
    plt.close()
