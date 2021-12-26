
from pygame.constants import USEREVENT
from .photolib import PhotoLib

import logging
import sys
import time
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT, K_i, K_o, K_p

class Frame:

    NextImageEvent = pygame.USEREVENT + 0
    FlushImagesEvent = pygame.USEREVENT + 1
    WaitTime = 10000
    FlushTime = 20000
    WaitDelta = 1000
    FPS = 60
    BackgroundColor = (0, 0, 0) #(128, 128, 0)
    IsAutomatic = True

    def __init__(self):
        self.index = 0
        self.lib = PhotoLib()
        self.showInfo = False

    def Shutdown(self):
        pygame.quit()

    def Init(self, importer):
        self.lib.Init(importer)
        self.lib.Shuffle()
    
    def InputHandler(self, events):
        """A function to handle keyboard/mouse/device input events. """
        updateNextFrameEvent = False
        for event in events:  # Hit the ESC key to quit the slideshow.
            if (event.type == self.FlushImagesEvent):
                self.FlushImages()
            elif (event.type == self.NextImageEvent and self.IsAutomatic):
                self.NextImage(+1)
            elif (event.type == KEYDOWN and event.key == K_SPACE):
                self.IsAutomatic = not self.IsAutomatic
            elif (event.type == KEYDOWN and event.key == K_LEFT):
                self.IsAutomatic = False
                self.NextImage(-1)
            elif (event.type == KEYDOWN and event.key == K_RIGHT):
                self.IsAutomatic = False
                self.NextImage(+1)
            elif (event.type == KEYDOWN and event.key == K_p): # speed up the slide show
                self.WaitTime = max(1000, self.WaitTime - self.WaitDelta)
                updateNextFrameEvent = True
            elif (event.type == KEYDOWN and event.key == K_o): # slow down the slide show
                self.WaitTime += self.WaitDelta
                updateNextFrameEvent = True
            elif (event.type == QUIT or
                (event.type == KEYDOWN and event.key == K_ESCAPE)):
                self.IsRunning = False
            elif (event.type == KEYDOWN and event.key == K_i):
                self.showInfo = not self.showInfo
        if updateNextFrameEvent:
            pygame.time.set_timer(Frame.NextImageEvent, self.WaitTime)

    def NextImage(self, delta=1):
        self.index += delta
        logging.debug(f"NextImage: index={self.index}")
        self.photo = self.lib.GetPhoto(self.index)
        self.photo.LoadImage(self.mode)

    def FlushImages(self):
        loadedPhotos = self.lib.GetLoadedPhotos()
        loadedPhotos.discard(self.photo) # eliminate the current photo
        self.lib.UnloadPhotos(loadedPhotos)
        
    def Tick(self, dT):
        # rescale the image to fit the current display
        #image = pygame.transform.scale(image, max(modes))
        self.screen.fill(self.BackgroundColor)
        if self.photo is not None:
            image, offset = self.photo.GetImage(self.mode)
            self.screen.blit(image, offset)

        pygame.display.flip()

        self.InputHandler(pygame.event.get())

        # Test for image support except pygame.error as err: print("Failed to display %s: %s" % (photo.fullpath, err))

    def Run(self):
        pygame.init()

        # Test for image support
        if not pygame.image.get_extended():
            print("Your Pygame isn't built with extended image support.")
            print("It's likely this isn't going to work.")
            sys.exit(1)

        modes = pygame.display.list_modes()
        self.mode = max(modes)
        logging.debug(f"Setting mode = {self.mode}")
        pygame.display.set_mode(self.mode)

        self.screen = pygame.display.get_surface()
        # pygame.display.set_caption("PiFrame")
        # pygame.display.toggle_fullscreen()

        pygame.time.set_timer(Frame.NextImageEvent, Frame.WaitTime)
        pygame.time.set_timer(Frame.FlushImagesEvent, Frame.FlushTime)

        self.NextImage(0)
        self.IsRunning = True

        clock = pygame.time.Clock()

        try:
            while self.IsRunning:
                dT = clock.tick(self.FPS)
                self.Tick(dT)
                #time.sleep(0.100)
        except:
            e = sys.exc_info()[0]
            logging.debug(f"Unhandled exception: {e}")
            
        pygame.quit()