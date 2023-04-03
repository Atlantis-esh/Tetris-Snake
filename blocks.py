import random
from collections import namedtuple
import copy
# Point = namedtuple('Point', 'X Y')
Shape = namedtuple('Shape', 'X Y Width Height')
Block = namedtuple('Block', 'template start_pos end_pos name next')

# 方块形状的设计，我最初我是做成 4 × 4，因为长宽最长都是4，这样旋转的时候就不考虑怎么转了，就是从一个图形替换成另一个
# 其实要实现这个功能，只需要固定左上角的坐标就可以了

# S形方块
S_BLOCK = [Block(['.OO',
                  'OO.',
                  '...'], [0, 0], [2, 1], 'S', 1),
           Block(['O..',
                  'OO.',
                  '.O.'], [0, 0], [1, 2], 'S', 0)]
# Z形方块
Z_BLOCK = [Block(['OO.',
                  '.OO',
                  '...'], [0, 0], [2, 1], 'Z', 1),
           Block(['.O.',
                  'OO.',
                  'O..'], [0, 0], [1, 2], 'Z', 0)]
# I型方块
I_BLOCK = [Block(['.O..',
                  '.O..',
                  '.O..',
                  '.O..'], [1, 0], [1, 3], 'I', 1),
           Block(['....',
                  'OOOO',
                  '....',
                  '....'], [0, 1], [3, 1], 'I', 0)]
# O型方块
O_BLOCK = [Block(['OO',
                  'OO'], [0, 0], [1, 1], 'O', 0)]
# J型方块
J_BLOCK = [Block(['O..',
                  'OOO',
                  '...'], [0, 0], [2, 1], 'J', 1),
           Block(['.OO',
                  '.O.',
                  '.O.'], [1, 0], [2, 2], 'J', 2),
           Block(['...',
                  'OOO',
                  '..O'], [0, 1], [2, 2], 'J', 3),
           Block(['.O.',
                  '.O.',
                  'OO.'], [0, 0], [1, 2], 'J', 0)]
# L型方块
L_BLOCK = [Block(['..O',
                  'OOO',
                  '...'], [0, 0], [2, 1], 'L', 1),
           Block(['.O.',
                  '.O.',
                  '.OO'], [1, 0], [2, 2], 'L', 2),
           Block(['...',
                  'OOO',
                  'O..'], [0, 1], [2, 2], 'L', 3),
           Block(['OO.',
                  '.O.',
                  '.O.'], [0, 0], [1, 2], 'L', 0)]
# T型方块
T_BLOCK = [Block(['.O.',
                  'OOO',
                  '...'], [0, 0], [2, 1], 'T', 1),
           Block(['.O.',
                  '.OO',
                  '.O.'], [1, 0], [2, 2], 'T', 2),
           Block(['...',
                  'OOO',
                  '.O.'], [0, 1], [2, 2], 'T', 3),
           Block(['.O.',
                  'OO.',
                  '.O.'], [0, 0], [1, 2], 'T', 0)]

BLOCKS = {'O': O_BLOCK,
          'I': I_BLOCK,
          'Z': Z_BLOCK,
          'T': T_BLOCK,
          'L': L_BLOCK,
          'S': S_BLOCK,
          'J': J_BLOCK}


def get_block():
    block_name = random.choice('OIZTLSJ')
    b = copy.deepcopy(BLOCKS[block_name]) #深入复制
    idx = random.randint(0, len(b) - 1)
    return b[idx]

def zhuanzhi(matrix,n):
    # 矩阵倒置，即(r,c)->(c,r)
    for r in range(n):
        for c in range(r, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]

    # 每一行倒转
    for r in range(n):
        # 以下两行相当于：matrix[r] = matrix[r][::-1]
        # 本着不修改matrix内部结构的原则，用下面的方式
        for c in range(n // 2):
            matrix[r][c], matrix[r][n - 1 - c] = matrix[r][n - 1 - c], matrix[r][c]

def block_change_pos(block,matrix,n):
    #求新的start_pos和end_pos,这里有一个很坑爹的东西，就是x和y，矩阵中和计算机绘图中是反的一定要注意，以后遇到这种情况可以像下面这样 for 后面的遍历不要用ij什么的用y和x，不然真的太容易混乱了
    start_x = 0x3f3f3f3f
    start_y = 0x3f3f3f3f
    end_x = 0
    end_y = 0
    for y in range(n):
        for x in range(n):
            if(matrix[y][x] == 'O'):
                if(y<start_y):
                    start_y = y
                if (x < start_x):
                    start_x = x
                if (y > end_y):
                    end_y = y
                if (x > end_x):
                    end_x = x
        block.template[y] = ''.join(matrix[y])
    
    block.start_pos[0] = start_x
    block.start_pos[1] = start_y
    block.end_pos[0]= end_x
    block.end_pos[1] = end_y

def rotate(block):
    n = len(block.template)
    matrix = [list(iter) for iter in block.template]
    zhuanzhi(matrix,n)
    block_change_pos(block,matrix,n)

    

def get_next_block(block,block_color):

    rotate(block)
    zhuanzhi(block_color,len(block_color))
    return block,block_color

# def get_next_block(block):
#     b = BLOCKS[block.name]
#     return b[block.next]
