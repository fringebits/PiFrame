
from pygame.constants import USEREVENT
from .photolib import PhotoLib

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT

class Frame:

    NextImageEvent = pygame.USEREVENT + 0
    WaitTime = 2500
    FPS = 60
    BackgroundColor = (0, 0, 0)
    IsAutomatic = True

    def __init__(self):
        self.index = 0
        self.lib = PhotoLib()

    def Init(self, importer):
        self.lib.Init(importer)
        self.lib.Shuffle()
    
    def InputHandler(self, events):
        """A function to handle keyboard/mouse/device input events. """
        for event in events:  # Hit the ESC key to quit the slideshow.
            if (event.type == self.NextImageEvent and self.IsAutomatic):
                self.NextImage(+1)
            if (event.type == KEYDOWN and event.key == K_SPACE):
                self.IsAutomatic = not self.IsAutomatic
            if (event.type == KEYDOWN and event.key == K_LEFT):
                self.IsAutomatic = False
                self.NextImage(-1)
            if (event.type == KEYDOWN and event.key == K_RIGHT):
                self.IsAutomatic = False
                self.NextImage(+1)
            if (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                self.IsRunning = False

    def NextImage(self, delta=1):
        self.index += delta
        photo = self.lib.GetPhoto(self.index)
        self.image = photo.LoadImage(self.mode)
        self.offset = photo.offset
        
    def Tick(self, dT):
        # rescale the image to fit the current display
        #image = pygame.transform.scale(image, max(modes))
        self.screen.fill(self.BackgroundColor)
        self.screen.blit(self.image, self.offset)
        pygame.display.flip()

        self.InputHandler(pygame.event.get())

        # except pygame.error as err:
        #     print("Failed to display %s: %s" % (photo.fullpath, err))

    def Run(self):

        pygame.init()

        # Test for image support
        if not pygame.image.get_extended():
            print("Your Pygame isn't built with extended image support.")
            print("It's likely this isn't going to work.")
            # sys.exit(1)

        modes = pygame.display.list_modes()
        self.mode = max(modes)
        pygame.display.set_mode(self.mode)

        self.screen = pygame.display.get_surface()
        pygame.display.set_caption("PiFrame")
        # pygame.display.toggle_fullscreen()

        pygame.time.set_timer(Frame.NextImageEvent, Frame.WaitTime)

        self.NextImage(0)
        self.IsRunning = True

        clock = pygame.time.Clock()

        while self.IsRunning:
            dT = clock.tick(self.FPS)
            self.Tick(dT)

        pygame.quit()

        