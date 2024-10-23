from .Layer import Layer
import pygame
import json

class PlayerLayer(Layer):
    def __init__(self, size, filename, state):
        self.__walk_frames, self.__stand_still_frame, self.__animation_per_frame, self.__num_walk_frames = self.load_sprite_data(filename, size)
        self.__state = state
        self.__curFrame = self.__stand_still_frame
        self.__walkFrameIndex = -1
        self.__counter = -1
        self.__size = size

    def render(self, surface):
        player = self.__state.getPlayer()
        if (player.isWalking()):
            self.updateWalkFrame()
        elif (player.isPushing()):
            self.updatePushFrame()
        else:
            self.stop()
        position = player.getPosition()
        position = (position.x - self.__size.x / 2, position.y - self.__size.y / 2)
        # transform the current frame to the left if isFlip is True
        curFrame = self.__curFrame
        if player.isFlip():
            curFrame = pygame.transform.flip(curFrame, True, False)
        surface.blit(curFrame, position)
    
    def updateWalkFrame(self):
        self.__counter = (self.__counter + 1) % self.__animation_per_frame
        if (self.__counter == 0):
            self.__walkFrameIndex = (self.__walkFrameIndex + 1) % self.__num_walk_frames
        self.__curFrame = self.__walk_frames[self.__walkFrameIndex]

    def updatePushFrame(self):
        pass

    def stop(self):
        self.__curFrame = self.__stand_still_frame
        self.__walkFrameIndex = -1
        self.__counter = -1


    def load_sprite_data(self, filename, size):
        """
        Loads sprite data from the given JSON file, including both walk and standstill sprites.
        Returns the frames for walking, standstill frame, and relevant metadata.
        """
        with open(filename, 'r') as f:
            data = json.load(f)

        # Load walking sprite sheet
        walk_sprite_sheet = pygame.image.load(f"assets/{data['walk']['sprite_sheet']}").convert_alpha()

        # Extract walking frames
        walk_frames = []
        for i in range(data['walk']['num_frames']):
            frame = walk_sprite_sheet.subsurface(pygame.Rect(
                i * data['walk']['frame_width'], 0, data['walk']['frame_width'], data['walk']['frame_height']
            ))
            walk_frames.append(frame)

        # Load standstill sprite sheet
        stand_still_sprite_sheet = pygame.image.load(f"assets/{data['stand_still']['sprite_sheet']}").convert_alpha()
        
        # Extract the standstill frame
        stand_still_frame = stand_still_sprite_sheet.subsurface(pygame.Rect(
            0, 0, data['stand_still']['frame_width'], data['stand_still']['frame_height']
        ))

        # Scale the frames to the desired size
        walk_frames = [pygame.transform.scale(frame, size) for frame in walk_frames]
        stand_still_frame = pygame.transform.scale(stand_still_frame, size)

        # Return both frames and necessary metadata
        return (
            walk_frames,
            stand_still_frame,
            data['walk']['animation_per_frame'],
            data['walk']['num_frames']
        )