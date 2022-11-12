import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
XMIN, XMAX = 0, 1500
YMIN, YMAX = 0, 800
VXMIN, VXMAX = -5, 5
VYMIN, VYMAX = -5, 5
RMIN, RMAX = 10, 30
screen = pygame.display.set_mode((1500, 800))
font_score = pygame.font.SysFont('Comic Sans MS', 50, True)
font_plus_score = pygame.font.SysFont('Comic Sans MS', 30, True)
font_stage = pygame.font.SysFont('Comic Sans MS', 100)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Balls():
	'''
	Содержит шесть итерируемых объектов для каждого цвета шаров
	Каждый итерируемый объект содержит все шары своего цвета
	'''
	def __init__(self):
		self.colors_balls = {0: set(), 1: set(), 2: set(), 3: set(), 4: set(), 5: set()}
	
	def generate_new(self):  # Генерирует новый шар с некоторой вероятностью
		rnd = randint(0, 100)
		if rnd >= 95:
			ball = Ball()
			self.colors_balls[ball.color].add(ball)
	
	def draw(self):  # Рисует все шары
		for color_balls in self.colors_balls.values():
			for ball in color_balls:
				ball.draw()
	
	def remove_old(self):  # Удаляет старые шары с истёкшим временем жизни
		for i in range(len(COLORS)):
			self.colors_balls[i] = set(filter(lambda x: x.t > 0, self.colors_balls[i]))


class Ball():
    '''
    x, y - координаты шара
    vx, vy - проекции скорости на координаты
    r - радиус шара
    score - количество очков, которое даёт шар
    t - время жизни шара (в кадрах), используется для реализации плавного удаления шара
    r_up - возрастаюая переменная, связанная с радиусом шара, позволяет реализовать плавное появление шара
    color - цвет шара
    burst - булевая переменная, содержащая в себе информацию, было ли попадание в этот шарик
    is_second_type - булевая переменная, содержащая в себе информацию, какого типа шарик (True, если второго)
    '''
    def __init__(self, is_second_type=False):
        self.is_second_type = is_second_type
        if self.is_second_type:
            self.vx = (2*randint(0, 1)-1) * (2*VXMAX)
            self.vy = (2*randint(0, 1)-1) * (2*VYMAX)
            self.r = RMIN
            self.score = 10
        else:
            self.vx = randint(int(VXMIN), int(VXMAX))
            self.vy = randint(int(VYMIN), int(VYMAX))
            self.r = randint(RMIN, RMAX)
            self.score = round(40 / self.r)
        self.t = randint(FPS, 10*FPS)
        self.x = randint(XMIN, XMAX)
        self.y = randint(YMIN, YMAX)
        self.r_up = 0
        self.color = randint(0, 5)
        self.burst = False

    def draw(self):  # рисует шар
        if self.is_second_type:
            self.color = (self.color+0.5) % 5.5
        self.r_up += 1
        if self.burst:
            circle(screen, COLORS[round(self.color)], (self.x, self.y), min(self.r, self.r_up), self.t)
        else:
            self.r = min(self.r, self.t)
            circle(screen, COLORS[round(self.color)], (self.x, self.y), min(self.r, self.r_up))
        self.move()

    def move(self):  # рассчёт перемещения центра масс
        self.t -= 1
        self.x += self.vx
        self.y += self.vy
        if self.x < self.r:
            self.x = 2*self.r - self.x
            self.vx = -self.vx
        elif self.x > XMAX - self.r:
            self.x = 2*(XMAX-self.r) - self.x
            self.vx = -self.vx
        if self.y < self.r:
            self.y = 2*self.r - self.y
            self.vy = -self.vy
        elif self.y > YMAX - self.r:
            self.y = 2*(YMAX-self.r) - self.y
            self.vy = -self.vy
        if self.t <= 0:
            if self.is_second_type:
                flag_second_type = False
            del self


class Plus_Scores():
    '''
    Содержит итерируемый объект, элементами которого являются объекты класса Plus_Score
    '''
    def __init__(self):
        self.plus_scores = set()

    def print_scores(self):  # вывод сообщения о количестве очков за пойманные шарики в местах щелчков
        for plus_score in self.plus_scores:
            plus_score.print_score()
	
    def remove_old(self):  # удаление старых сообщений
        self.plus_scores = set(filter(lambda x: x.t > 0, self.plus_scores))


class Plus_Score():
    '''
    x, y - координаты сообщения о количестве начисленных очков
    score - количество начисленных очков
    t - время жизни сообщения
    '''
    def __init__(self, x, y, score):
        self.x = x + randint(-40, 0)
        self.y = y + randint(-40, 0)
        self.score = score
        self.t = FPS // 2
	
    def print_score(self):  # вывод сообщения о количестве очков за пойманный шарик в месте щелчка
        screen.blit(font_plus_score.render('+' + str(self.score), True, WHITE), (self.x, self.y))
        self.t -= 1
        if self.t <= 0:
            del self


class Stage():
	def __init__(self):
		self.stage = 0
		self.t = 0
	
	def print_if_need(self, count):
		if self.t == 0 and count >= 100*self.stage:
			self.stage += 1
			self.t = 2 * FPS
		if self.t > 0:
			self.t -= 1
			screen.blit(font_stage.render('Stage ' + str(self.stage), True, WHITE), (600, 300))


def count_if_hit_ball(pos):
    '''
    Проверка попадания места щелчка в шарик и обновление суммы очков
    '''
    global VXMAX, VXMIN, VYMAX, VYMIN
    score = 0
    x_click, y_click = pos
    for color_balls in balls.colors_balls.values():
        for ball in color_balls:
            if not ball.burst and (x_click-ball.x)**2 + (y_click-ball.y)**2 <= ball.r**2:
                ball.burst = True
                ball.t = ball.r
                plus_scores.plus_scores.add(Plus_Score(ball.x, ball.y, ball.score))
                score = ball.score
    if not special_ball.burst and (x_click-special_ball.x)**2 + (y_click-special_ball.y)**2 <= special_ball.r**2:
        special_ball.burst = True
        special_ball.t = special_ball.r
        plus_scores.plus_scores.add(Plus_Score(special_ball.x, special_ball.y, special_ball.score))
        score = special_ball.score
    VXMAX += score / 10
    VXMIN -= score / 10
    VYMAX += score / 10
    VYMIN -= score / 10
    return score


def print_count():
    '''
    Вывод сообщения о текущем количестве очков в левый верхний угол экрана
    '''
    screen.blit(font_score.render('Score: ' + str(count), True, WHITE), (randint(0, max(0, count - 100) // 10), randint(0, max(0, count - 100) // 10)))
    screen.blit(font_score.render('Stage: ' + str(stage.stage), True, WHITE), (1280 - randint(0, max(0, count - 100) // 10), randint(0, max(0, count - 100) // 10)))


pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = Balls()
special_ball = Ball(True)
plus_scores = Plus_Scores()
count = 0
stage = Stage()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            count += count_if_hit_ball(event.pos)
    balls.generate_new()
    balls.draw()
    special_ball.draw()
    balls.remove_old()
    print_count()
    plus_scores.print_scores()
    plus_scores.remove_old()
    stage.print_if_need(count)
    pygame.display.update()
    screen.fill(BLACK)
    if special_ball.t <= 0:
        special_ball = Ball(True)

pygame.quit()
