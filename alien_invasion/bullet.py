import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	"""a class to manage bullet shot by ship"""

	def __init__(self,ai_game):
		"""create a bullet in current ship location"""
		super().__init__()
		self.screen=ai_game.screen
		self.settings=ai_game.settings
		self.color=self.settings.bullet_color

		#create a bullet retangle in (0,0),put it in the right place.
		self.rect=pygame.Rect(0,0,self.settings.bullet_width,
			self.settings.bullet_height)
		self.rect.midtop=ai_game.ship.rect.midtop

		#save bullet position by float
		self.y=float(self.rect.y)

	def update(self):
		"""bullets moving up"""
		#updating float which save bullet position
		self.y-=self.settings.bullet_speed
		#updating bullet position
		self.rect.y=self.y

	def draw_bullet(self):
		"""draw bullet on screen"""
		pygame.draw.rect(self.screen,self.color,self.rect)