'''
Date: 2023-04-01 21:30:00
LastEditors: Atlantis
LastEditTime: 2023-04-03 11:23:50
FilePath: \AllFileAboutPythonProject\本机项目跑（复现）\游戏制作\GITHUB_python_Games-master\俄罗斯方块\pygame-button-interface-switch-main\Tetris Snake\Tetris_Snake_init.py
'''

import pygame
from pygame.locals import *
display_width = 540
display_height = 720

WHITE = (255, 255, 255)
RED = (200, 30, 30)
ORENGE = (255,250, 205)
bg_location = 'background.jpg'

pygame.init()

class Button(object):
	def __init__(self, text, color, x=None, y=None, **kwargs):
		self.surface = font.render(text, True, color)

		self.WIDTH = self.surface.get_width()
		self.HEIGHT = self.surface.get_height()

		if 'centered_x' in kwargs and kwargs['centered_x']:
			self.x = display_width // 2 - self.WIDTH // 2
		else:
			self.x = x

		if 'centered_y' in kwargs and kwargs['cenntered_y']:
			self.y = display_height // 2 - self.HEIGHT // 2
		else:
			self.y = y

	def display(self):
		screen.blit(self.surface, (self.x, self.y))

	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

		if x_match and y_match:
			return True
		else:
			return False


def starting_screen():
	screen = pygame.display.set_mode((display_width, display_height))
	font_title = pygame.font.Font(font_addr, 50)
	game_title = font_title.render('Tetris Snake', True, WHITE)
	screen.blit(game_title, (display_width//2 - game_title.get_width()//2, 150))


	font_title = pygame.font.Font(font_addr, 15)
	snake_operation_str = "'w, a, s, d': Snake Operation"
	tetris_operation_str = "'i, j, k, l, space': Tetris Operation"
	pause_operation_str = "'p': Pause"	
	archive_operation_str = "'r': Archive"	
	exit_operation_str = "'y': Exit"

	snake_operation_display = font_title.render(snake_operation_str, True, ORENGE)
	tetris_operation_display = font_title.render(tetris_operation_str, True, ORENGE)
	pause_operation_display = font_title.render(pause_operation_str, True, ORENGE)
	archive_operation_display = font_title.render(archive_operation_str, True, ORENGE)
	exit_operation_display = font_title.render(exit_operation_str, True, ORENGE)

	screen.blit(snake_operation_display, (display_width//2 - snake_operation_display.get_width()//2, 575))
	screen.blit(tetris_operation_display, (display_width//2 - tetris_operation_display.get_width()//2, 600))
	screen.blit(pause_operation_display, (display_width//2 - pause_operation_display.get_width()//2, 625))
	screen.blit(archive_operation_display, (display_width//2 - archive_operation_display.get_width()//2, 650))
	screen.blit(exit_operation_display, (display_width//2 - exit_operation_display.get_width()//2, 675))

	Easy_button = Button('Easy', WHITE, None, 350, centered_x=True)
	Medium_button = Button('Medium', WHITE, None, 400, centered_x=True)
	hard_button = Button('Hard', WHITE, None, 450, centered_x=True)
	Load_button = Button('Keep on Playing', WHITE, None, 500, centered_x=True)
	Easy_button.display()
	Medium_button.display()
	hard_button.display()
	Load_button.display()
	pygame.display.update()
	while True:
		screen.blit(bg, (0,0))
		screen.blit(game_title, (display_width//2 - game_title.get_width()//2, 150))
		screen.blit(snake_operation_display, (display_width//2 - snake_operation_display.get_width()//2, 575))
		screen.blit(tetris_operation_display, (display_width//2 - tetris_operation_display.get_width()//2, 600))
		screen.blit(pause_operation_display, (display_width//2 - pause_operation_display.get_width()//2, 625))
		screen.blit(archive_operation_display, (display_width//2 - archive_operation_display.get_width()//2, 650))
		screen.blit(exit_operation_display, (display_width//2 - exit_operation_display.get_width()//2, 675))

		if Easy_button.check_click(pygame.mouse.get_pos()):
			Easy_button = Button('Easy', RED, None, 350, centered_x=True)
		else:
			Easy_button = Button('Easy', WHITE, None, 350, centered_x=True)

		if Medium_button.check_click(pygame.mouse.get_pos()):
			Medium_button = Button('Medium', RED, None, 400, centered_x=True)
		else:
			Medium_button = Button('Medium', WHITE, None, 400, centered_x=True)

		if hard_button.check_click(pygame.mouse.get_pos()):
			hard_button = Button('Hard', RED, None, 450, centered_x=True)
		else:
			hard_button = Button('Hard', WHITE, None, 450, centered_x=True)
		
		if Load_button.check_click(pygame.mouse.get_pos()):
			Load_button = Button('Keep on Playing', RED, None, 500, centered_x=True)
		else:
			Load_button = Button('Keep on Playing', WHITE, None, 500, centered_x=True)

		Easy_button.display()
		Medium_button.display()
		hard_button.display()
		Load_button.display()
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				raise SystemExit
		if pygame.mouse.get_pressed()[0]:
			if Easy_button.check_click(pygame.mouse.get_pos()):
				game_core.main(14,30,False)
				screen = pygame.display.set_mode((display_width, display_height))
			if Medium_button.check_click(pygame.mouse.get_pos()):
				game_core.main(24,30,False)
				screen = pygame.display.set_mode((display_width, display_height))
			if hard_button.check_click(pygame.mouse.get_pos()):
				game_core.main(34,30,False)
				screen = pygame.display.set_mode((display_width, display_height))
			with open('save_parameter.txt','r',encoding='utf-8') as f:
				block_width =  eval(f.readline())
				block_height =  eval(f.readline())
			if Load_button.check_click(pygame.mouse.get_pos()):
				game_core.main(block_width,block_height,True)
				screen = pygame.display.set_mode((display_width, display_height))
		pygame.display.flip()

import game_core
screen = pygame.display.set_mode((display_width, display_height))
bg = pygame.image.load(bg_location)
font_addr = pygame.font.get_default_font()
font = pygame.font.Font(font_addr, 36)
# font = pygame.font.SysFont('SimHei', 50)
starting_screen()