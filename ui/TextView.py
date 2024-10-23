from .Font import Font
import pygame

class TextView:
    def __init__(self, position=(0, 0), text='', width=100, height=10, **kwargs):
        # Set up the TextView
        self.assign_kwargs(kwargs)
        self.label, self.label_rect = self.render_font(text, self.font, self.fontsize)
        self.color = self.bg_color
        self.width = width
        self.height = height
        
        # Create the surface for the TextView with the specified width and height
        self.image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()
        self.image.fill(self.bg_color)
        
        # Set the rectangle for the TextView's position
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        
        # Position the label inside the TextView
        self.label_rect.topleft = self.rect.topleft

    def assign_kwargs(self, kwargs):
        # Assign kwargs for customizable properties
        self.bg_color = kwargs['bg']
        self.text_color = kwargs['fg']
        self.font = kwargs['font']
        self.fontsize = kwargs['fontsize']

    def render_font(self, text, filename, size):
        # Render the font using the specified font or a system font
        if not filename:
            f = pygame.font.SysFont('Arial', size)
        else:
            f = Font.load(self.font, size)
        font = f.render(text, True, self.text_color)
        rect = font.get_rect()
        return (font, rect)

    def render(self, screen):
        # Fill the background of the TextView
        self.image.fill(self.bg_color)

        # Calculate the visible part of the label inside the TextView bounds
        if self.label_rect.width > self.width or self.label_rect.height > self.height:
            # Clip text that goes outside the bounds
            visible_rect = self.label.get_rect()
            visible_rect.width = min(self.width, visible_rect.width)
            visible_rect.height = min(self.height, visible_rect.height)

            # Create a new surface for the clipped text
            clipped_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
            clipped_surface.fill(self.bg_color)
            
            # Blit the portion of the label that fits inside the TextView
            clipped_surface.blit(self.label, (0, 0), visible_rect)
            screen.blit(clipped_surface, self.rect.topleft)
        else:
            # If the text fits, blit it normally
            self.image.blit(self.label, (0, 0))
            screen.blit(self.image, self.rect.topleft)

    def update(self):
        # Center the label's rectangle within the TextView if needed
        self.label_rect.topleft = self.rect.topleft

    def setText(self, text):
        # Update the text and re-render the font
        self.label, self.label_rect = self.render_font(text, self.font, self.fontsize)
        self.label_rect.topleft = self.rect.topleft
