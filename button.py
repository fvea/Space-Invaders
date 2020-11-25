import pygame 

class Button(object): 
    def __init__(self,screen): 
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # Load the button image and get its rect.
        self.image = pygame.image.load("images\play-button.png")
        self.rect = self.image.get_rect()
        # Start each button @ center of the screen.
        self.rect.center = self.screen_rect.center


    def blitme(self): 
        """Draw the button at its current location."""
        self.screen.blit(self.image,self.rect)
