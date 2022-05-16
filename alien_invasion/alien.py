import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""class represent alien"""
	def __init__(self,ai_game):
		"""initialize alien and set original position"""
		super().__init__()
		self.screen=ai_game.screen
		self.settings=ai_game.settings
		
		#load alien bmp and get rect property
		self.image=pygame.image.load('images/alien.bmp')
		self.rect=self.image.get_rect()

		#initially every alien near upperleft side of screen
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height

		#save accurate alien horizonal position
		self.x=float(self.rect.x)

	def check_edges(self):
		"""return True if meet edge"""
		screen_rect=self.screen.get_rect()
		if self.rect.right>=screen_rect.right or self.rect.left<=0:
			return True

	def update(self):
		"""aliens moving right"""
		self.x+=(self.settings.alien_speed*
				self.settings.fleet_direction)
		self.rect.x=self.x