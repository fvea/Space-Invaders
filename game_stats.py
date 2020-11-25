class GameStats(object): 
    """Track statistics for Alien Invasion."""
    def __init__(self,ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        # Start Alien Invasion in an active state.
        self.game_active = False
        # High score should never be reset.
        with open('highscore.txt') as f_obj: 
            current_highScore = f_obj.read()
        self.high_score = int(current_highScore)
        self.reset_stats()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
