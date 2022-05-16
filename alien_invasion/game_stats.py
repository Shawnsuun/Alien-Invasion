class GameStats:
	"""Follow game stats info"""

	def __init__(self,ai_game):
		"""initialize stats info"""
		self.settings=ai_game.settings
		self.reset_stats()

		#game inactive while start
		self.game_active=False
		#never reset highscore
		self.high_score=0

	def reset_stats(self):
		"""initialize possible changing stats info"""
		self.ship_left=self.settings.ship_limit
		self.score=0
		self.level=1