import pygame
import random

# 初始化 Pygame 库
pygame.init()

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# 定义游戏界面的尺寸和贪吃蛇方块的大小
screen_width = 600
screen_height = 400
block_size = 10

# 设置游戏帧率
FPS = 15

# 定义字体和字体大小
font_style = pygame.font.SysFont(None, 30)


def message(msg, color):
    """
    在屏幕上显示消息
    """
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [screen_width / 6, screen_height / 3])


def your_score(score):
    """
    显示得分
    """
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])


def our_snake(block_size, snake_List):
    """
    绘制贪吃蛇
    """
    for x in snake_List:
        pygame.draw.rect(screen, black, [x[0], x[1], block_size, block_size])


def gameLoop():
    """
    游戏循环
    """
    # 创建窗口
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))

    # 设置窗口标题
    pygame.display.set_caption('贪吃蛇')

    # 初始化游戏变量
    game_over = False
    x1 = screen_width / 2
    y1 = screen_height / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    score = 0

    # 随机生成食物和障碍物的位置
    foodx = round(random.randrange(0, screen_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, screen_height - block_size) / 10.0) * 10.0
    obstacle_list = []
    for i in range(4):
        obstacle_x = round(random.randrange(0, screen_width - block_size) / 10.0) * 10.0
        obstacle_y = round(random.randrange(0, screen_height - block_size) / 10.0) * 10.0
        while [obstacle_x, obstacle_y] in obstacle_list or [obstacle_x, obstacle_y] == [foodx, foody]:
            obstacle_x = round(random.randrange(0, screen_width - block_size) / 10.0) * 10.0
            obstacle_y = round(random.randrange(0, screen_height - block_size) / 10.0) * 10.0
        obstacle_list.append([obstacle_x, obstacle_y])
    direction = ''
    # 游戏循环
    while not game_over:
        for event in pygame.event.get():
            # 监听事件
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                    y1_change = block_size
                    x1_change = 0

        # 判断贪吃蛇是否撞墙
        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_over = True

        # 更新贪吃蛇的位置
        x1 += x1_change
        y1 += y1_change

        # 绘制背景和障碍物
        screen.fill(green)
        for obstacle in obstacle_list:
            pygame.draw.rect(screen, blue, [obstacle[0], obstacle[1], block_size, block_size])

        # 绘制食物
        pygame.draw.rect(screen, red, [foodx, foody, block_size, block_size])

        # 更新贪吃蛇列表
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 判断贪吃蛇是否碰到了食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, screen_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, screen_height - block_size) / 10.0) * 10.0
            Length_of_snake += 1

            # 更新障碍物列表
            new_obstacle_list = []
            for obstacle in obstacle_list:
                if [foodx, foody] != obstacle:
                    new_obstacle_list.append(obstacle)
            obstacle_list = new_obstacle_list

        # 绘制贪吃蛇和显示分数
        our_snake(block_size, snake_List)
        your_score(score)

        # 判断贪吃蛇是否碰到了障碍物
        for obstacle in obstacle_list:
            if [x1, y1] == obstacle:
                game_over = True

        # 更新分数
        score = (Length_of_snake - 1) * 10

        # 更新屏幕
        pygame.display.update()

        # 设置游戏的帧率
        clock = pygame.time.Clock()
        clock.tick(FPS)

    # 在游戏结束时显示消息和分数
    screen.fill(green)
    message("You lost! Press Q-Quit or C-Play Again", red)
    your_score(score)
    pygame.display.update()

    # 等待用户按下 Q 或 C
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    gameLoop()
        pygame.display.update()
        
gameLoop()