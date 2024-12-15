class Button:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def checkForInput(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        return False
