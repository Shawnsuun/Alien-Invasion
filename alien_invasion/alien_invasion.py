import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
	"""class to manage game resource and act"""

	def __init__(self):
		"""initial game and create game resource"""
		pygame.init()
		self.settings=Settings()

		self.screen=pygame.display.set_mode(
			(self.settings.screen_width,self.settings.screen_height))

		"""full screen mode
		self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
		self.settings.screen_width=self.screen.get_rect().width
		self.settings.screen_height=self.screen.get_rect().height"""

		pygame.display.set_caption("Alien Invasion")

		#create an example to save game stats
		#create scoreboard
		self.stats=GameStats(self)
		self.sb=Scoreboard(self)

		self.ship=Ship(self)
		self.bullets=pygame.sprite.Group()
		self.aliens=pygame.sprite.Group()
		self._create_fleet()

		#create play button
		self.play_button=Button(self,"Play")

	def run_game(self):
		"""start main game loop"""
		while True:
			self._check_events()
			
			if self.stats.game_active==True:
				self.ship.update()
				self._update_bullets()
				self._update_aliens()

			self._update_screen() 

	def _check_events(self):
		#monitoring keyboard and mouse event
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				sys.exit()
			elif event.type==pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type==pygame.KEYUP:
				self._check_keyup_events(event)	
			elif event.type==pygame.MOUSEBUTTONDOWN:
				mouse_pos=pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)

	def _check_keydown_events(self,event):
		"""respond to key press"""
		if event.key==pygame.K_RIGHT:
			#ship move right
			self.ship.moving_right=True
		elif event.key==pygame.K_LEFT:
			#ship move left
			self.ship.moving_left=True
		elif event.key==pygame.K_SPACE:
			self._fire_bullet()
		elif event.key==pygame.K_q:
			sys.exit()		

	def _check_keyup_events(self,event):	
		"""respond to key release"""	
		if event.key==pygame.K_RIGHT:	
			self.ship.moving_right=False
		elif event.key==pygame.K_LEFT:	
			self.ship.moving_left=False					
	 
	def _check_play_button(self,mouse_pos):
		"""start new game while click play"""
		button_clicked=self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active:
			#reset game settings
			self.settings.initialize_dynamic_settings()

			#reset game stats info
			self.stats.reset_stats()
			self.stats.game_active=True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#clear bullets and aliens
			self.aliens.empty()
			self.bullets.empty()

			#reset fleet and ship
			self._create_fleet()
			self.ship.center_ship()

			#hide mouse
			pygame.mouse.set_visible(False)

	def _fire_bullet(self):
		"""create a bullet,add it in groups bullets"""
		if len(self.bullets)<self.settings.bullets_allowed:
			new_bullet=Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		#update bullets position and disappearance
		self.bullets.update()
		
		#delete diappearing bullet
		for bullet in self.bullets.copy():
			if bullet.rect.bottom<=0:
				self.bullets.remove(bullet)
		print(len(self.bullets))

		self._check_bullet_alien_collisions()

	def _check_bullet_alien_collisions(self):
		#check if bullets hits aliens
		#if yes,delete bullet and alien
		collisions=pygame.sprite.groupcollide(
			self.bullets,self.aliens,True,True)		
		
		if collisions:
			for aliens in collisions.values():
				self.stats.score+=self.settings.alien_points
				self.sb.prep_score()
				self.sb. check_high_score()

		if not self.aliens:
			#delete all bullets and create new aliens
			self.bullets.empty()
			self._create_fleet()
			self.settings.increase_speed()

			#level up!
			self.stats.level+=1
			self.sb.prep_level()

	def _create_fleet(self):
		"""create alien fleet!"""
		#calculate number of aliens in a line
		alien=Alien(self)
		alien_width,alien_height=alien.rect.size
		available_space_x=self.settings.screen_width-(2*alien_width)
		number_aliens_x=available_space_x//(2*alien_width)

		#calculate number of lines in screen
		ship_height=self.ship.rect.height
		available_space_y=(self.settings.screen_height-
								(3*alien_height)-ship_height)
		number_rows=available_space_y//(2*alien_height)

		#create alien fleet
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number,row_number)

	def _create_alien(self,alien_number,row_number):
		"""create an alien in the certain position"""
		alien=Alien(self)
		alien_width,alien_height=alien.rect.size
		alien.x=alien_width+2*alien_width*alien_number
		alien.rect.x=alien.x
		alien.y=alien_height+2*alien_height*row_number
		alien.rect.y=alien.y
		self.aliens.add(alien)

	def _check_fleet_edges(self):
		"""do sth if the fleet meet the edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""move down whole group of aliens,change direction"""
		for alien in self.aliens.sprites():
			alien.rect.y+=self.settings.fleet_drop_speed
		self.settings.fleet_direction*=-1

	def _ship_hit(self):
		"""respond to collision from alien"""

		#ship_left minus 1
		if self.stats.ship_left>0:
			self.stats.ship_left-=1
			self.sb.prep_ships()

			#clear all bullets and aliens
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet,reset ship into middle
			self._create_fleet()
			self.ship.center_ship()

			#pause
			sleep(0.5)
		else:
			self.stats.game_active=False

			#show mouse
			pygame.mouse.set_visible(True)

	def _check_aliens_bottom(self):
		"""check if any aliens reach bottom"""
		screen_rect=self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom>=screen_rect.bottom:
				self._ship_hit()
				break

	def _update_aliens(self):
		self._check_fleet_edges()
		self.aliens.update()

		#check collisions between alien and ship
		if pygame.sprite.spritecollideany(self.ship,self.aliens):
			print("Ship hit!!!")
			self._ship_hit()

		#check if any aliens meet the bottom
		self._check_aliens_bottom()

	def _update_screen(self):
		#screen refresh in each loop
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()
		self.aliens.draw(self.screen)

		#show score
		self.sb.show_score()

		#if game inactive, draw play button
		if not self.stats.game_active:
			self.play_button.draw_button()

		#keep recently drawn screen visible
		pygame.display.flip()

if __name__=='__main__':
	#create game example and run game
	ai=AlienInvasion()
	ai.run_game()