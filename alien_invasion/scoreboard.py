import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
	"""a class showing score info"""

	def __init__(self,ai_game):
		"""initialize property of shown score"""
		self.ai_game=ai_game
		self.screen=ai_game.screen
		self.screen_rect=self.screen.get_rect()
		self.settings=ai_game.settings
		self.stats=ai_game.stats

		#show font settings of score info
		self.text_color=(30,30,30)
		self.font=pygame.font.SysFont(None,36)
		#prepare initial score image
		self.prep_score()
		#prepare high score
		self.prep_high_score()
		#prepare level
		self.prep_level()
		#prepare ship left
		self.prep_ships()

	def prep_score(self):
		"""render score to image"""
		rounded_score=round(self.stats.score,-1)
		score_str="{:,}".format(rounded_score)
		self.score_image=self.font.render("Score:"+score_str,True,
			self.text_color,self.settings.bg_color)

		#show score on upper right corner
		self.score_rect=self.score_image.get_rect()
		self.score_rect.right=self.screen_rect.right-20
		self.score_rect.top=20

	def prep_high_score(self):
		"""render high score to image"""
		high_score=round(self.stats.high_score,-1)
		high_score_str="{:,}".format(high_score)
		self.high_score_image=self.font.render("HighScore:"+high_score_str,True,
			self.text_color,self.settings.bg_color)

		#show score on upper right corner
		self.high_score_rect=self.high_score_image.get_rect()
		self.high_score_rect.centerx=self.screen_rect.centerx
		self.high_score_rect.top=5

	def check_high_score(self):
		if self.stats.score>self.stats.high_score:
			self.stats.high_score=self.stats.score
			self.prep_high_score()

	def prep_level(self):
		"""render level to image"""
		level_str=str(self.stats.level)
		self.level_image=self.font.render("Level:"+level_str,True,
			self.text_color,self.settings.bg_color)

		#show level on upper right corner
		self.level_rect=self.level_image.get_rect()
		self.level_rect.right=self.score_rect.right
		self.level_rect.top=self.score_rect.bottom+10		

	def prep_ships(self):
		"""show ship left"""
		self.ships=Group()
		for ship_number in range(self.stats.ship_left):
			ship=Ship(self.ai_game)
			ship.rect.x=10+ship.rect.width*ship_number
			ship.rect.y=10
			self.ships.add(ship)

	def show_score(self):
		"""show score on screen"""
		self.screen.blit(self.score_image,self.score_rect)
		self.screen.blit(self.high_score_image,self.high_score_rect)
		self.screen.blit(self.level_image,self.level_rect)
		self.ships.draw(self.screen)