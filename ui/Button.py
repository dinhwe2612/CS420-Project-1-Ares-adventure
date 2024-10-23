import pygame as pg
from .Font import Font

class Button:
    def __init__(self, position = (0, 0), text='', width=100, height=10, command=None, **kwargs):
        
        self.assign_kwargs(kwargs)
        self.label, self.label_rect = self.render_font(text, self.font, self.fontsize)
        self.color = self.bg_color
        self.callback = command
        
        self.image = pg.Surface([width,height]).convert()
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.label_rect.center = self.rect.center
        self.is_hover = False
        
    def assign_kwargs(self, kwargs):
        self.hover_bg_color = kwargs['hover']
        self.bg_color = kwargs['bg']
        self.text_color = kwargs['fg']
        self.font = kwargs['font']
        self.border = kwargs['border']
        self.fontsize = kwargs['fontsize']
        
    def render_font(self, text, filename, size):
        if not filename:
            f = pg.font.SysFont('Arial', size)
        else:
            f = Font.load(self.font, size)
        font = f.render(text, 1, self.text_color)
        rect = font.get_rect()
        return (font, rect)
        
    def render(self, screen):
        pg.draw.rect(screen, self.color, self.rect, self.border)
        screen.blit(self.label, self.label_rect)
        
    def mouse_collision(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.is_hover = True
        else:
            self.is_hover = False
            
        if self.is_hover:
            self.color = self.hover_bg_color
        else:
            self.color = self.bg_color
            
    def update(self):
        self.label_rect.center = self.rect.center
        self.mouse_collision()
            
    def get_event(self, event):
        if self.is_hover:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.callback()