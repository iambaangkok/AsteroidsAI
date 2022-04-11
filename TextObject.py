import pygame

import Colors

class TextObject:
    
    def __init__(self,text, x = 0, y = 0, fontName = "UbuntuMono", fontSize = 24, color = Colors.WHITE, align = "left", baseline = "bottom"):
        self.text = text
        self.font = pygame.font.SysFont(fontName, fontSize)
        self.color = color
        self.x = x
        self.y = y
        self.align = align
        self.baseline = baseline

    def draw(self, window):
        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect()

        if self.align == "left":
            text_rect.left = self.x
        elif self.align == "center":
            text_rect.centerx = self.x
        elif self.align == "right":
            text_rect.right = self.x

        if self.baseline == "top":
            text_rect.top = self.y
        elif self.baseline == "middle":
            text_rect.centery = self.y
        elif self.baseline == "bottom":
            text_rect.bottom = self.y

        window.blit(text, text_rect)
