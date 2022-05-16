class Settings:
	"""save all class Settings in Alien Invasion"""

	def __init__(self):
		"""initial game setting"""
		#screen setting
		self.screen_width=1200
		self.screen_height=720
		self.bg_color=(230,230,230)

		#ship setting
		self.ship_limit=3

		#bullet setting
		self.bullet_width=3
		self.bullet_height=15
		self.bullet_color=(60,60,60)
		self.bullets_allowed=3

		#alien setting
		self.fleet_drop_speed=10

		#increase game speed
		self.speed_up_scale=1.1
		#increase score rate
		self.score_scale=1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""initialize setting variation while running game"""
		self.ship_speed=1.5
		self.bullet_speed=1.5
		self.alien_speed=1.0

		#fleet_direction is 1,then move right,or -1 to move right
		self.fleet_direction=1

		#score recording
		self.alien_points=50

	def increase_speed(self):
		"""increase spped settings"""
		self.ship_speed*=self.speed_up_scale
		self.bullet_speed*=self.speed_up_scale
		self.alien_speed*=self.speed_up_scale

		self.alien_points=int(self.alien_points*self.score_scale)
		print(self.alien_points)