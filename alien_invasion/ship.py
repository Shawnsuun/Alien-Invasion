import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	"""class to manage class Ship"""
	def __init__(self,ai_game):
		"""initialization ship,get game screen retangular to set initial position"""
		super().__init__()

		self.screen=ai_game.screen
		self.screen_rect=ai_game.screen.get_rect()
		self.settings=ai_game.settings

		#load ship image and get outter rectangle
		self.image=pygame.image.load('images/ship.bmp')
		self.rect=self.image.get_rect()

		#for each new ship,put it in the midbottom of the screen
		self.rect.midbottom=self.screen_rect.midbottom

		#float of ship position
		self.x=float(self.rect.x)

		#flag to control moving
		self.moving_right=False
		self.moving_left=False

	def update(self):
		#adjust ship location by flag
		if self.moving_right and self.rect.right<self.screen_rect.right:
			self.x+=self.settings.ship_speed
		if self.moving_left and self.rect.left>self.screen_rect.left:
			self.x-=self.settings.ship_speed
		
		#give back float to self.rect.x
		self.rect.x=self.x

	def blitme(self):
		"""draw ship in certain location"""
		self.screen.blit(self.image,self.rect)

	def center_ship(self):
		"""set ship in the middle center of screen"""
		self.rect.midbottom=self.screen_rect.midbottom
		self.x=float(self.rect.x)