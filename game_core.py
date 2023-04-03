#cur_pos_x,y是俄罗斯方块block在地图上的位置，而snake_direction是小蛇的走位方向而不是位置;本项目参考俄罗斯方块，没有特别表明snake的变量一般就是blocks（俄罗斯方块）的变量
import sys
import time
import pygame
from pygame.locals import *
import blocks
from blocks import Block
import math
import random
import time
from collections import deque


SIZE = 24  # 每个小方格大小
BLOCK_HEIGHT = 30  # 游戏区高度 25
BLOCK_WIDTH = 30   # 游戏区宽度 10
BORDER_WIDTH =  4  # 游戏区边框宽度 4
READ_ME_WIDTH = 10
screen_width = SIZE * (BLOCK_WIDTH + READ_ME_WIDTH)  # 游戏屏幕的宽
SCREEN_WIDTH = screen_width
screen_height = SIZE * BLOCK_HEIGHT      # 游戏屏幕的高

BORDER_COLOR = (40, 40, 200)  # 游戏区边框颜色
BG_COLOR = (255,255,204)  # 背景色(40, 40, 60)  (80, 80, 100) 和(100, 100, 120)好！
BLOCK_COLOR = (20, 128, 200)  #
LINE_COLOR = (230, 230, 230)
RED = (200, 30, 30)      # GAME OVER 的字体颜色
GREEN = (0,255,0)
LINE_WIDTH = 1
DARK = (64,64,64)  # 蛇的颜色(240,240,240) 
DARK_HEAD = (0,0,0)    #蛇头颜色



# 食物的分值及颜色
FOOD_STYLE_LIST = [(10, (135,206,250)), (20, (0,191,255)), (30, (0,0,255)),(40, (153,0,153))]
SNAKE_EAT_INTERVAL =  30
BLOCK_REV_INERNAL= 90


def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 3)]

def print_text(screen, font, x, y, text, fcolor=(0,0,0)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))
# 画背景
def _draw_background(screen):
    # 填充背景色
    screen.fill(BG_COLOR)
    # 画游戏区域分隔线
    pygame.draw.line(screen, BORDER_COLOR,
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, 0),
                     (SIZE * BLOCK_WIDTH + BORDER_WIDTH // 2, screen_height), BORDER_WIDTH)
# 画网格线
def _draw_gridlines(screen):
    # 画网格线 竖线
    for x in range(BLOCK_WIDTH):
        pygame.draw.line(screen, LINE_COLOR, (x * SIZE, 0), (x * SIZE, screen_height), 1)
    # 画网格线 横线
    for y in range(BLOCK_HEIGHT):
        pygame.draw.line(screen, LINE_COLOR, (0, y * SIZE), (BLOCK_WIDTH * SIZE, y * SIZE), 1)
        
# 画已经落下的方块
def _draw_game_area(screen, game_area):
    if game_area:
        for i, row in enumerate(game_area):
            for j, cell in enumerate(row):
                if cell != '.':
                    pygame.draw.rect(screen, BLOCK_COLOR, (j * SIZE, i * SIZE, SIZE, SIZE), 0)

# 初始化蛇
def init_snake():
    snake = deque()
    snake.append((2, 10))
    snake.append((1, 10))
    snake.append((0, 10))
    return snake

def main(block_width,block_height,from_load = False):
    global SIZE, screen_width, screen_height ,LINE_WIDTH, BLOCK_WIDTH, BLOCK_HEIGHT,SCREEN_WIDTH
    BLOCK_WIDTH = block_width
    BLOCK_HEIGHT = block_height
    #这里逻辑可能不是最好的，screenheight都不用考虑，但是喔不想管了，能跑就行============
    screen_width = SIZE * (BLOCK_WIDTH + READ_ME_WIDTH)  # 游戏屏幕的宽
    SCREEN_WIDTH = screen_width
    # 游戏区域的坐标范围
    SCOPE_X = (0, BLOCK_WIDTH - 1)
    SCOPE_Y = (0, BLOCK_HEIGHT  - 1)
    #==============================================================================
    EXIT = False
    pygame.init()
    # pygame.key.set_repeat(100, 100)
    screen = pygame.display.set_mode((screen_width, screen_height),flags=pygame.RESIZABLE)
    pygame.display.set_caption('Tetris Snake')

    cur_block = None   # 当前下落方块
    next_block = None  # 下一个方块
    cur_block_color = []
    next_block_color = []
    cur_pos_x, cur_pos_y = 0, 0

    game_area = None    # 整个游戏区域
    game_over = True    # 初始假设 就已经是失败的情况￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
    start = False       # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    score = 0           # 得分
    orispeed = 1      # 原始速度
    speed = orispeed    # 当前速度
    pause = False       # 暂停
    last_drop_time = None   # 上次下落时间
    last_press_time = None  # 上次按键时间
    cur_block = None   #正在下落的方块
    snake_last_eat_time  =time.time()
    block_last_remove_time = time.time()
    pause_flag = True  #判断是否暂停过，计时用
    snake_eat_interval = SNAKE_EAT_INTERVAL   #实时记录的剩余时间，下同
    block_rev_interval =  BLOCK_REV_INERNAL   
    daxiao_rate = screen_width/SCREEN_WIDTH #大小比例
    Game_over_result = None
    press_key = False  #为了如果之前已经按过键位了，就不用自动走了，增加蛇的可控性
    block_num = 0  #消除方块或食物的数量，这里我们用消除的方块计速度，而不是用score，从而可以使得玩家可有策略的在消灭相同方块或食物的情况下速度增长相同，却有可能有更高的分数

    # 如果蛇正在向右移动，那么快速点击向下向左，由于程序刷新没那么快，向下事件会被向左覆盖掉，导致蛇后退，直接GAME OVER
    # b 变量就是用于防止这种情况的发生
    b = True
    snake = init_snake()
    snake_diretion = [1, 0]  # 蛇的初始方向
    jiafen_time = None       #加分用
    save_success_time = None #存档用
    speed_refresh_frequency = 0.1
    snake_freq_faster = False
    # 画得分等信息
    def _draw_info(screen, font, pos_x, font_height, score):
        print_text(screen, font, pos_x, 10, f'得分: ',fcolor=BORDER_COLOR)
        print_text(screen, font, pos_x + font_height*3, font1_interval, f'{score}',fcolor=BORDER_COLOR)
        print_text(screen, font, pos_x                , font1_interval+(font_height)+font1_interval, f'速度: ',fcolor=BORDER_COLOR)
        print_text(screen, font, pos_x + font_height*3, font1_interval+(font_height)+font1_interval, f'{block_num // 3}',fcolor=BORDER_COLOR)
        print_text(screen, font, pos_x                , font1_interval+2*((font_height)+font1_interval), f'下一个：',fcolor=BORDER_COLOR)
        print_text(screen, font, pos_x                , font1_interval*2+3*((font_height)+font1_interval) + 3 *SIZE, f'食物块分值')
    
    # 画单个方块,这里必须注意一下，offset_x和offset_y是针对readme区的下一个方块准备的，当画那个的时候，pos_x和pos_y都为0
    # 而pos_x pos_y是为了画图中正在下落的方块的，所以在画它们的时候offset_x和y都为0
    def _draw_block(screen, block, offset_x, offset_y, pos_x, pos_y,block_color):
        if block:
            for i in range(block.start_pos[1], block.end_pos[1] + 1):
                for j in range(block.start_pos[0], block.end_pos[0] + 1):
                    if block.template[i][j] != '.':
                        pygame.draw.rect(screen, block_color[i][j][1],
                                        (offset_x + (pos_x + j) * SIZE, offset_y + (pos_y + i) * SIZE, SIZE, SIZE), 0)

    def _dock():
        nonlocal cur_block, next_block, game_area, cur_pos_x, cur_pos_y, game_over, score, speed,cur_block_color,next_block_color,block_last_remove_time,remaining,Game_over_result,block_num
        for _i in range(cur_block.start_pos[1], cur_block.end_pos[1] + 1):
            for _j in range(cur_block.start_pos[0], cur_block.end_pos[0] + 1):
                if cur_block.template[_i][_j] != '.':
                    game_area[cur_pos_y + _i][cur_pos_x + _j] = '0'
        if cur_pos_y + cur_block.start_pos[1] <= 0:
            game_over = True
            Game_over_result = '由于俄罗斯食物顶天了，游戏结束'
        else:
            # 计算消除
            remove_idxs = []
            for _i in range(cur_block.start_pos[1], cur_block.end_pos[1] + 1):
                if all(_x == '0' for _x in game_area[cur_pos_y + _i]):
                    remove_idxs.append(cur_pos_y + _i)
            if remove_idxs:
                # 计算得分
                remove_count = len(remove_idxs)
                if remove_count == 1:
                    score += 25*BLOCK_WIDTH
                elif remove_count == 2:
                    score += 25*(BLOCK_WIDTH*2)*1.2
                elif remove_count == 3:
                    score += 25*(BLOCK_WIDTH*3)*1.4
                elif remove_count == 4:
                    score += 25*(BLOCK_WIDTH*4)*1.6

                block_num = block_num + remove_count * BLOCK_WIDTH  #增添新加的方块数
                speed = max(0.05, orispeed - 0.1 * (block_num / 1000))
                # 消除
                _i = _j = remove_idxs[-1]
                while _i >= 0:
                    while _j in remove_idxs:
                        _j -= 1
                    if _j < 0:
                        game_area[_i] = ['.'] * BLOCK_WIDTH
                    else:
                        game_area[_i] = game_area[_j]
                    _i -= 1
                    _j -= 1
                block_last_remove_time = time.time()
                remaining[1] = BLOCK_REV_INERNAL
            cur_block = next_block
            cur_block_color = next_block_color

            next_block,next_block_color = block_begin()

            cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos[0] - 1) // 2, -1 - cur_block.end_pos[1]

    def _judge(pos_x, pos_y, block):
        nonlocal game_area
        for _i in range(block.start_pos[1], block.end_pos[1] + 1):
            if pos_y + block.end_pos[1] >= BLOCK_HEIGHT:
                return False
            for _j in range(block.start_pos[0], block.end_pos[0] + 1):
                if pos_y + _i >= 0 and block.template[_i][_j] != '.' and game_area[pos_y + _i][pos_x + _j] != '.':
                    return False
        return True

    #蛇相关变量*********************************************
    def _change_snake_pop_append(snake,snake_direction,block,block_pos_x,block_pos_y):
        nonlocal game_over,speed,cur_block_color,score,snake_last_eat_time,remaining,Game_over_result,block_num
        
        next_s = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        flag = 0
        if block:
            for i in range(block.start_pos[1], block.end_pos[1] + 1):
                temp_str = block.template[i]
                for j in range(block.start_pos[0], block.end_pos[0] + 1):
                    if temp_str[j] != '.':
                        if(next_s == (block_pos_x + j,(block_pos_y + i))): #进食中===================
                            snake.appendleft(next_s)
                            flag = flag+1
                            block.template[i] = temp_str[:j] + '.' +temp_str[j+1:]
                            score = score + cur_block_color[i][j][0]
                            block_num = block_num + 1
                            speed = max(0.05,orispeed - 0.1 * (block_num / 1000))
                            snake_last_eat_time = time.time()
                            remaining[0] = SNAKE_EAT_INTERVAL
                blocks.block_change_pos(block,block.template,len(block.template))
        if(not flag): #没有吃东西的话就自己往下走一格
            if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] and next_s not in snake:
                
                    snake.appendleft(next_s)
                    snake.pop()
            else:
                game_over = True
                Game_over_result = '由于小蛇越过边界或者咬到身体，游戏结束'
            
    # 蛇相关变量*********************************************
    def block_begin():
        block = blocks.get_block()
        block_color = []
        #设置初始值颜色==============
        block_n = len(block.template)
        for i in range(block_n):
            block_color.append([])
            for j in range(block_n):
                block_color[i].append( get_food_style())
        
        return block,block_color

    def load_parameter():
        load_parameters = []
        with open ('save_parameter.txt','r',encoding='utf-8') as f:
            for line in f.readlines():
                load_parameters.append(eval(line))
        return tuple(load_parameters[2:])   #前两行是block_width ,block_height

    if(from_load == True):
        cur_block,next_block,      cur_block_color,next_block_color,game_area,snake_diretion,remaining,     snake,    snake_freq_faster  ,cur_pos_x,cur_pos_y,speed,block_num,score      = load_parameter()
        # print(cur_block,next_block,      cur_block_color,next_block_color,game_area,snake_diretion,remaining,     snake,    snake_freq_faster  ,cur_pos_x,cur_pos_y,speed,block_num,score)
    while True:
        if(speed<0.2):
            snake_freq_faster = True
        daxiao_rate = screen_width/SCREEN_WIDTH
        font1_interval = int(10*daxiao_rate)
        font1_daxiao = 20 * daxiao_rate
        font1 = pygame.font.SysFont('SimHei', int(font1_daxiao))  # 黑体24
        font2_daxiao = 72 * daxiao_rate
        font2 = pygame.font.Font(None, int(font2_daxiao))  # GAME OVER 的字体
        font_pos_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 10  # 右侧信息显示区域字体位置的X坐标
        gameover_size = font2.size('GAME OVER')
        font1_height = int(font1.size('得分')[1])



        if start and not game_over:
            #断尾==========================================
            row_width2score = 5 #蛇蛇断尾要什么时候断？的值
            if(len(snake) >=row_width2score * BLOCK_WIDTH): #蛇长度达到到一定加分
                for i in range(row_width2score*BLOCK_WIDTH-3):
                    snake.pop()
                score = score + 10*row_width2score*BLOCK_WIDTH
                jiafen_str = f'小蛇长度达到{row_width2score*BLOCK_WIDTH},小蛇断尾缩减为3,分数增加{10*(row_width2score*BLOCK_WIDTH-3)}分！'
                jiafen_size = font1.size(jiafen_str)
                jiafen_time = time.time()
        
            #碰到game_area ,游戏结束========================
            if(  game_area[snake[0][1]][snake[0][0]] != '.'): 
                game_over = True
                Game_over_result = '小蛇越过方块区域边界，游戏结束'
            O_list = []
            for y,str_iter in enumerate(cur_block.template):
                for x,iter in enumerate(str_iter):
                    if(iter == 'O'):
                        O_list.append((x,y))
            for iter in O_list:
                if((cur_pos_x + iter[0],cur_pos_y+iter[1]) in list(snake)[1:]):
                    game_over = True
                    Game_over_result = '可能是食物把蛇砸死了or蛇的身体碰到了食物，游戏结束'

            # ============================================
            #cur_block全被吃力，重新启动
            if(sum(['O' in iter for iter in cur_block.template])==0):
                cur_block = next_block
                cur_block_color = next_block_color
                next_block,next_block_color = block_begin()
                cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos[0] - 1) // 2, -1 - cur_block.end_pos[1]
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:        # 获取新窗体宽高,调整窗口大小及各个参数
                gao1 = math.floor(event.h/BLOCK_HEIGHT) * BLOCK_HEIGHT
                kuan1 = (BLOCK_WIDTH+READ_ME_WIDTH)/BLOCK_HEIGHT * gao1
                if(kuan1 >event.w):
                    kuan1 = 0x3f3f3f3f
                    gao1 = 0x3f3f3f3f
                kuan2 = math.floor(event.w/BLOCK_WIDTH) * BLOCK_WIDTH
                gao2 = BLOCK_HEIGHT/(BLOCK_WIDTH+READ_ME_WIDTH) * kuan2
                if(gao2 >event.h):
                    kuan2 = 0x3f3f3f3f
                    gao2 = 0x3f3f3f3f
                screen_width,screen_height =min(kuan1,kuan2),min(gao1,gao2)
                print(f'screen_width{screen_width}')
                screen = pygame.display.set_mode((screen_width,screen_height),pygame.RESIZABLE)   # 赋值回去
                old_size = SIZE
                SIZE = screen_height/BLOCK_HEIGHT
                font_pos_x = BLOCK_WIDTH * SIZE + BORDER_WIDTH + 10  # 右侧信息显示区域字体位置的X坐标
                LINE_WIDTH = SIZE/old_size * LINE_WIDTH
            # print('cesssssssssssssssssssssssssssss')
            #定义开始回车，空格暂停，按上变换===============================
            elif event.type == KEYDOWN:
                if(event.key == K_y) :#退出游戏
                    EXIT = True
                if event.key == K_RETURN:
                    if game_over:
                        if(from_load==False):
                            speed = orispeed
                            remaining = [SNAKE_EAT_INTERVAL,BLOCK_REV_INERNAL] #记录暂停时snake和block各自的时间
                            start = True
                            game_over = False
                            score = 0
                            last_drop_time = time.time()
                            last_press_time = time.time()
                            last_press_time_snake = time.time()
                            game_area = [['.'] * BLOCK_WIDTH for _ in range(BLOCK_HEIGHT)]

                            cur_block,cur_block_color = block_begin()
                            next_block,next_block_color = block_begin()

                            cur_pos_x, cur_pos_y = (BLOCK_WIDTH - cur_block.end_pos[0] - 1) // 2, -1 - cur_block.end_pos[1]
                            # 蛇相关变量*********************************************
                            snake = init_snake()
                            snake_diretion = [1, 0]
                            last_move_time = time.time()
                            snake_freq_faster = False
                            # 蛇相关变量*********************************************
                            block_last_remove_time = time.time()
                            snake_last_eat_time = time.time()
                            block_num = 0
                        else:  #载入存档========================================================================
                            from_load = False
                            start = True
                            game_over = False
                            last_drop_time = time.time()
                            last_press_time = time.time()
                            last_press_time_snake = time.time()
                            last_move_time = time.time()
                            # 蛇相关变量*********************************************
                            block_last_remove_time = time.time()
                            snake_last_eat_time = time.time()
                if(event.key == K_r) and start == True:#存档！！！！
                    save_list = [block_width,block_height,cur_block,next_block,      cur_block_color,next_block_color,game_area,snake_diretion,[snake_eat_interval,block_rev_interval],     snake,    snake_freq_faster  ,cur_pos_x,cur_pos_y,speed,block_num,score]
                    with open('save_parameter.txt','w',encoding='utf-8') as f:
                        for iter in save_list:
                            f.write(str(iter) + '\n')
                    #显示存档成功============
                    save_success_str = f'Archive Succeeded'
                    save_success_size = font2.size(save_success_str)
                    save_success_time = time.time() 
                    if not game_over:# 也要暂停！！！！！！！！！！！！！！！！！！！！！！！！！！
                        pause = not pause
                        pause_flag = True  #判断是否暂停过，计时用
                        remaining = [snake_eat_interval,block_rev_interval] 
                
                if (event.key == K_p) and not game_over:
                    pause = not pause
                    pause_flag = True  #判断是否暂停过，计时用
                    remaining = [snake_eat_interval,block_rev_interval]
                if not game_over and not pause and event.key == K_i:
                    # 旋转
                    # 其实记得不是很清楚了，比如
                    # .0.
                    # .00
                    # ..0
                    # 这个在最右边靠边的情况下是否可以旋转，我试完了网上的俄罗斯方块，是不能旋转的，这里我们就按不能旋转来做
                    # 我们在形状设计的时候做了很多的空白，这样只需要规定整个形状包括空白部分全部在游戏区域内时才可以旋转
                    if 0 <= cur_pos_x <= BLOCK_WIDTH - len(cur_block.template[0]):
                        _next_block,_next_block_color = blocks.get_next_block(cur_block,cur_block_color)
                        # print('-------------')
                        # print(_next_block)
                        # print('-------------')
                        if _judge(cur_pos_x, cur_pos_y, _next_block):
                            cur_block = _next_block
                            cur_block_color = _next_block_color


                if not game_over and not pause and event.key == K_SPACE: #骤降=======================================================================
                    snake_pos_x = [iter for iter in snake]
                    # snake_pos_y_with_blockposx = set()
                    for iter in snake:
                        if(iter[0] in list(range(cur_pos_x + cur_block.start_pos[0], cur_pos_x + cur_block.end_pos[0]+1))):
                            if(iter[1]>cur_pos_y+cur_block.end_pos[1]):   #在方块下方
                                game_over = True
                                Game_over_result = '食物骤降，砸死了小蛇'
                                cur_pos_y = iter[1]-1 -cur_block.end_pos[1]  #小方块坠落到小蛇上方
                                break                     
                    if not game_over:
                        while _judge(cur_pos_x, cur_pos_y + 1, cur_block): #cs : judge判断是否能继续下落
                            cur_pos_y += 1
                        _dock()

        
        #按键按下时，上下左右俄罗斯方块和蛇都一起判断
        key_pressed = pygame.key.get_pressed()
        if not game_over and not pause:
        # 蛇相关变量****************************************************************
            if key_pressed[pygame.K_w]:
                if(snake_diretion[1]!=1):   #snake_diretion[1]!=1 是为了防止向右然后按左键直接挂
                    press_key = True
                    if time.time() - last_press_time_snake > speed_refresh_frequency * (1-snake_freq_faster*1/2):   
                        last_press_time_snake = time.time()
                        snake_diretion = [0,-1]
                        _change_snake_pop_append(snake,snake_diretion,cur_block,cur_pos_x,cur_pos_y)
            if key_pressed[pygame.K_s]:
                if(snake_diretion[1]!=-1):
                    press_key = True
                    if time.time() - last_press_time_snake > speed_refresh_frequency * (1-snake_freq_faster*1/2) :
                        last_press_time_snake = time.time()
                        snake_diretion = [0,1]
                        _change_snake_pop_append(snake,snake_diretion,cur_block,cur_pos_x,cur_pos_y)
            if key_pressed[pygame.K_a]:
                if(snake_diretion[0]!=1):
                    press_key = True
                    if time.time() - last_press_time_snake > speed_refresh_frequency * (1-snake_freq_faster*1/2):
                        last_press_time_snake = time.time()
                        snake_diretion = [-1,0]
                        _change_snake_pop_append(snake,snake_diretion,cur_block,cur_pos_x,cur_pos_y)
            if key_pressed[pygame.K_d]:
                if(snake_diretion[0]!=-1):
                    press_key = True
                    if time.time() - last_press_time_snake > speed_refresh_frequency * (1-snake_freq_faster*1/2) :
                        last_press_time_snake = time.time()
                        snake_diretion = [1,0]
                        _change_snake_pop_append(snake,snake_diretion,cur_block,cur_pos_x,cur_pos_y)
        # 蛇相关变量****************************************************************
        # 俄罗斯方块相关变量&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
            if key_pressed[pygame.K_j]:
                            if time.time() - last_press_time > speed_refresh_frequency:
                                last_press_time = time.time()
                                if cur_pos_x > - cur_block.start_pos[0]:
                                    if _judge(cur_pos_x - 1, cur_pos_y, cur_block):
                                        cur_pos_x -= 1
            if key_pressed[pygame.K_l]:
                if time.time() - last_press_time > speed_refresh_frequency:
                    last_press_time = time.time()
                    # 不能移除右边框
                    if cur_pos_x + cur_block.end_pos[0] + 1 < BLOCK_WIDTH:
                        if _judge(cur_pos_x + 1, cur_pos_y, cur_block):
                            cur_pos_x += 1
            if key_pressed[pygame.K_k]:
                if time.time() - last_press_time > speed_refresh_frequency:
                    last_press_time = time.time()
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block): #cs : judge判断是否能继续下落
                        _dock()
                    else:
                        last_drop_time = time.time()
                        cur_pos_y += 1
        # 俄罗斯方块相关变量&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        if not game_over:
            #方块每隔一段时间下落=======================================
            cur_drop_time = time.time()
            if cur_drop_time - last_drop_time > speed:
                if not pause:
                    # 不应该在下落的时候来判断到底没，我们玩俄罗斯方块的时候，方块落到底的瞬间是可以进行左右移动
                    if not _judge(cur_pos_x, cur_pos_y + 1, cur_block):
                        _dock()
                    else:
                        last_drop_time = cur_drop_time
                        cur_pos_y += 1
            #蛇每隔一段时间走路=======================================
            if(press_key == True):
                press_key = False
                last_move_time = time.time() #上面已经按过键位了，所以下面就不用自动走了
            else:
                curTime = time.time()
                if curTime - last_move_time > speed:
                    if not pause:
                        b = True
                        last_move_time = curTime
                        _change_snake_pop_append(snake,snake_diretion,cur_block,cur_pos_x,cur_pos_y)
        # print(f'speed={speed}        speed_refresh_frequency= {speed_refresh_frequency}, block_num = {block_num}')
        if not game_over:
            if not pause:
                if(pause_flag):
                    pause_flag = False
                    snake_last_eat_time = block_last_remove_time =  time.time()
                snake_eat_interval = remaining[0] - math.floor(time.time() - snake_last_eat_time)
                block_rev_interval =  remaining[1] - math.floor(time.time() - block_last_remove_time)
            if(snake_eat_interval==0 or block_rev_interval==0):
                game_over = True
                Game_over_result = '蛇饿死了or俄罗斯食物太久没有被至少消除一行,游戏结束'
            # print(f'snake_eat_interval = {snake_eat_interval}; block_rev_interval = {block_rev_interval}')

        #画图==========================================================================================================================================================================================================
        _draw_background(screen)
        # screen.blit(background,(0,0))  #对齐的坐标
        _draw_game_area(screen, game_area)

        _draw_gridlines(screen)
        # 画当前下落方块
        _draw_block(screen, cur_block, 0, 0, cur_pos_x, cur_pos_y,cur_block_color)

        #readme绘画===============================================================
        _draw_info(screen, font1, font_pos_x, font1_height, score)
        # 画显示信息中的下一个方块
        _draw_block(screen, next_block, font_pos_x + 5*font1_height, 10+2*(font1_height+10), 0, 0,next_block_color)
        # 画出四个小方框，注释！！！==============================================
        shiwukuai_pos_y = font1_interval * 2+3*((font1_height)+font1_interval) + 3 *SIZE
        for index,iter in enumerate(FOOD_STYLE_LIST):
            if(index == 0):
                pygame.draw.rect(screen, iter[1],
                                (font_pos_x , shiwukuai_pos_y + font1_height + font1_interval, SIZE, SIZE), 0)
            if(index == 1):
                pygame.draw.rect(screen, iter[1],
                                (font_pos_x + READ_ME_WIDTH*0.4 * SIZE, shiwukuai_pos_y + font1_height + font1_interval, SIZE, SIZE), 0)
            if(index == 2):
                pygame.draw.rect(screen, iter[1],
                                (font_pos_x , shiwukuai_pos_y + 2*(font1_height + font1_interval), SIZE, SIZE), 0)
            if(index == 3):
                pygame.draw.rect(screen, iter[1],
                                (font_pos_x + READ_ME_WIDTH*0.4 * SIZE, shiwukuai_pos_y + 2*(font1_height + font1_interval), SIZE, SIZE), 0)

        print_text(screen,font1,font_pos_x + SIZE + 5 ,shiwukuai_pos_y + font1_height + font1_interval,":10")
        print_text(screen,font1,font_pos_x + READ_ME_WIDTH*0.4 * SIZE + SIZE + 5 ,shiwukuai_pos_y + font1_height + font1_interval,":20")
        print_text(screen,font1,font_pos_x + SIZE + 5 ,shiwukuai_pos_y + 2*(font1_height + font1_interval),":30")
        print_text(screen,font1,font_pos_x + READ_ME_WIDTH*0.4 * SIZE + SIZE + 5 ,shiwukuai_pos_y + 2*(font1_height + font1_interval),":40")
        #画食物值分值上方的线：
        pygame.draw.line(screen, LINE_COLOR, (BLOCK_WIDTH*SIZE+6,shiwukuai_pos_y-font1_interval), ((BLOCK_WIDTH+READ_ME_WIDTH)*SIZE,shiwukuai_pos_y-font1_interval), 1)
        #食物值分值下方的线：
        shiwukuai_lower_pos_y = shiwukuai_pos_y + 2*(font1_height + font1_interval)+SIZE+font1_interval
        pygame.draw.line(screen, LINE_COLOR, (BLOCK_WIDTH*SIZE+6,shiwukuai_lower_pos_y), ((BLOCK_WIDTH+READ_ME_WIDTH)*SIZE,shiwukuai_lower_pos_y), 1)
        # 写剩余时间
        print_text(screen,font1,font_pos_x ,shiwukuai_lower_pos_y+font1_interval,f"小蛇捕食剩余：{snake_eat_interval} 秒")
        print_text(screen,font1,font_pos_x ,shiwukuai_lower_pos_y+2*font1_interval + font1_height,f"方块消除剩余：{block_rev_interval} 秒")
        #任务下方的线：
        renwu_lower_pos_y = shiwukuai_lower_pos_y+2*font1_interval + font1_height+font1_height+font1_interval
        pygame.draw.line(screen, LINE_COLOR, (BLOCK_WIDTH*SIZE+6,renwu_lower_pos_y), ((BLOCK_WIDTH+READ_ME_WIDTH)*SIZE,renwu_lower_pos_y), 1)
        #写说明
        text = [
             '游戏基本说明：',
            '1.食物落地变成方块，玩家需要',
            '在相应规定时间内完成消除方块',
            '与小蛇捕食两项任务',
            '2.不让除蛇头外的身体触碰食物',
            '3.小蛇不可越过边界和方块',
            '4.方块不可越过上界',
            '温馨提示：',
            '  食物具有重量，请尽量让小蛇',
            '从上方、左方、右方进食。小蛇',
            '从下方进食，容易被食物砸死。']
        font_small_daxiao = 15 * daxiao_rate
        font_small_interval = int(7.5* daxiao_rate)
        font_small = pygame.font.SysFont('SimHei', int(font_small_daxiao)) 
        font_small_height = int(font_small.size('得分')[1])
        for index,iter in enumerate(text):
            if(iter =='游戏基本说明：'):
                print_text(screen,font1,font_pos_x ,renwu_lower_pos_y+2*font1_interval+index*(font_small_height+\
                                font1_interval),text[index],fcolor=(128,128,128))
            if(iter =='温馨提示：'):
                print_text(screen,font1,font_pos_x ,renwu_lower_pos_y+4*font1_interval+(font1_height+font1_interval)+(index-1)*(font_small_height+\
                                font1_interval),text[index],fcolor=(128,128,128))
            else:
                if(index>0 and index<=6):
                    print_text(screen,font_small,font_pos_x ,renwu_lower_pos_y+2*font1_interval+(font1_height+font1_interval)+(index-1)*(font_small_height+\
                                font1_interval),text[index],fcolor=(128,128,128))
                if(index>=8):
                    print_text(screen,font_small,font_pos_x ,renwu_lower_pos_y+4*font1_interval+(font1_height+font1_interval)*2+(index-2)*(font_small_height+\
                                font1_interval),text[index],fcolor=(128,128,128))
        # 画蛇        
        for index,s in enumerate(snake):
            if(index == 0):
                dark = DARK_HEAD
            else:
                dark = DARK
            pygame.draw.rect(screen, dark, (s[0] * SIZE, s[1] * SIZE , SIZE, SIZE), 0)
            
 
            
        if(jiafen_time): #呈现超过3秒的效果
            if(time.time()-jiafen_time<3):
                print_text(screen, font1,
                        (screen_width// 2 - jiafen_size[0]// 2) , (screen_height - jiafen_size[1]) // 2 ,jiafen_str, GREEN)
            else:
                jiafen_time = None
        

        if(save_success_time): 
            if(time.time()-save_success_time<1):
                pause = True
                print_text(screen, font2,
                        (screen_width// 2 - save_success_size[0]// 2) , (screen_height - save_success_size[1]) // 2 ,save_success_str, GREEN)
            else:
                pause = False
                save_success_time = None
        if(speed == 0.05):
            fontGETIT_daxiao = 40 * daxiao_rate
            fontGETIT = pygame.font.Font(None, int(fontGETIT_daxiao))  # GAME OVER 的字体
            getit_str = 'YOU GET IT, MY MASTER!'
            GETIT_size = fontGETIT.size(getit_str)
            print_text(screen, fontGETIT,
                        (screen_width - GETIT_size[0]) // 2, (screen_height - GETIT_size[1]) // 2,
                        'YOU GET IT, MY MASTER!', GREEN)
            game_over = True  
               

        
        # 游戏结束的判定，任何时候都要放在最后
        if start and game_over and speed!=0.05:
            print_text(screen, font2,
                        (screen_width - gameover_size[0]) // 2, (screen_height - gameover_size[1]) // 2,
                        'GAME OVER', RED)
            # if(Game_over_result!=None):
            #     print(Game_over_result)
            Game_over_result_size = font1.size(Game_over_result)
            print_text(screen, font1,
                        (screen_width// 2 - Game_over_result_size[0]// 2) , (screen_height - gameover_size[1]) // 2 + font1_interval*3+gameover_size[1],
                        Game_over_result, RED)
        pygame.display.flip()
        if(EXIT ):
            # pygame.quit()
            return
            
            
        
        


if __name__ == '__main__':
    
    main(10,30)
