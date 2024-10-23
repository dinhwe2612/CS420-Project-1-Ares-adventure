from .GameMode import GameMode
import pygame
from ui import Button


BUTTON_SETTINGS = {
    'hover'   : (155,155,155),
    'font'    : 'BD_Cartoon_Shout',
    'fg'      : (0,0,0),
    'bg'      : (255,255,255),
    'border'  : False,
    'fontsize': 25
}

class MenuGameMode(GameMode):
    def __init__(self, observer):
        super().__init__(observer)
        bfs_btn = Button(position=(400, 140), text='BFS', width=100, height=50, command=lambda: self.notifyLoadPlayGameMode('bfs'), **BUTTON_SETTINGS)
        self.addButton(bfs_btn)
        dfs_btn = Button(position=(400, 240), text='DFS', width=100, height=50, command=lambda: self.notifyLoadPlayGameMode('dfs'), **BUTTON_SETTINGS)
        self.addButton(dfs_btn)
        ucs_btn = Button(position=(400, 340), text='UCS', width=100, height=50, command=lambda: self.notifyLoadPlayGameMode('ucs'), **BUTTON_SETTINGS)
        self.addButton(ucs_btn)
        astar_btn = Button(position=(400, 440), text='A*', width=100, height=50, command=lambda: self.notifyLoadPlayGameMode('astar'), **BUTTON_SETTINGS)
        self.addButton(astar_btn)

    def render(self, surface):
        surface.fill((0, 0, 0))
        super().render(surface)
        