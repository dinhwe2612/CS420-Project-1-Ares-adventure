from .GameMode import GameMode
import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from PIL import Image

class MenuGameMode(GameMode):
    def __init__(self, observer, screenHeight, screenWidth):
        super().__init__(observer, screenHeight, screenWidth)
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.background_path = "./assets/background.jpg"  # Path to your static background image
        self.scale_factor = 1  # Scale factor if needed
        self.background_image = None
        self.load_background_image()

        # UI Elements
        self.start_button = UIButton(relative_rect=pygame.Rect(0, 140, 160, 100),
                                     text='Start', manager=self.ui_manager,
                                     anchors={'centerx': 'centerx'})
        self.exit_button = UIButton(relative_rect=pygame.Rect(0, 90, 160, 100),
                                    text='Exit', manager=self.ui_manager,
                                    anchors={'centerx': 'centerx', 'top_target': self.start_button})

    def load_background_image(self):
        # Load and scale the background image
        image = Image.open(self.background_path).convert("RGBA")  # Ensure it's in RGBA format
        
        # Scale the image if needed
        new_width = int(image.width * self.scale_factor)
        new_height = int(image.height * self.scale_factor)
        scaled_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert to pygame Surface
        mode = scaled_image.mode
        size = scaled_image.size
        data = scaled_image.tobytes()

        self.background_image = pygame.image.frombuffer(data, size, mode)  # Use frombuffer instead of fromstring


    def processInput(self, event):
        super().processInput(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.start_button:
                self.notifyLoadPlayGameMode()
            if event.ui_element == self.exit_button:
                self.observer.applicationExit()

    def update(self, delta_time):
        super().update(delta_time)

    def render(self, surface):
        # Display the background image
        surface.fill((0, 0, 0))  # Optional: Clear the screen with black
        background_surface = self.background_image

        # Center the background image on the screen
        x = (self.screenWidth - background_surface.get_width()) // 2
        y = (self.screenHeight - background_surface.get_height()) // 2
        surface.blit(background_surface, (x, y))
        
        super().render(surface)
