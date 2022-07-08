
from pygame.constants import USEREVENT
from .photolib import PhotoLib
from .photo import Photo

from datetime import date, datetime, timedelta
import logging
import sys
import time
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT, K_i, K_o, K_p, K_d

class Frame:

    NextImageEvent = pygame.USEREVENT + 0
    WaitTime = 10000
    WaitDelta = 1000
    FPS = 30
    BackgroundColor = (0, 0, 0) #(128, 128, 0)
    IsAutomatic = True
    FontName = 'Comic Sans MS'
    FontSize = 30
    OutputStep = 35
    DefaultCursor = (15, 15)
    KeywordFilter = {b'GUTMANN', b'people', b'instagram'}

    def __init__(self):
        self.index = 0
        self.lib = PhotoLib()
        self.photo = None
        self.showInfo = False
        self.showDebug = False
        self.isWindowed = False
        self.mode = None
        self.runtime = 0
        self.pos = Frame.DefaultCursor

    def Shutdown(self):
        pygame.quit()

    def Init(self, importer):
        self.lib.Init(importer)
        self.lib.Shuffle()
    
    def InputHandler(self, events):
        """A function to handle keyboard/mouse/device input events. """
        updateNextFrameEvent = False
        for event in events:  # Hit the ESC key to quit the slideshow.
            if (event.type == self.NextImageEvent and self.IsAutomatic):
                self.NextImage(+1)
            elif (event.type == KEYDOWN):
                if event.key == K_SPACE:
                    self.IsAutomatic = not self.IsAutomatic
                elif event.key == K_LEFT:
                    self.IsAutomatic = False
                    self.NextImage(-1)
                elif event.key == K_RIGHT:
                    self.IsAutomatic = False
                    self.NextImage(+1)
                elif event.key == K_p: # speed up the slide show
                    self.WaitTime = max(1000, self.WaitTime - self.WaitDelta)
                    updateNextFrameEvent = True
                elif event.key == K_o: # slow down the slide show
                    self.WaitTime += self.WaitDelta
                    updateNextFrameEvent = True
                elif event.key == K_ESCAPE:
                    self.IsRunning = False
                elif event.key == K_i:
                    self.showInfo = not self.showInfo
                elif event.key == K_d:
                    self.showDebug = not self.showDebug
            elif (event.type == QUIT):
                self.IsRunning = False

        if updateNextFrameEvent:
            pygame.time.set_timer(Frame.NextImageEvent, self.WaitTime)

    def NextImage(self, delta=1):
        logging.debug(f"NextImage: index={self.index}, delta={delta}")

        self.lib.UnloadPhoto(self.index)
        self.index += delta
        self.photo = self.lib.LoadPhoto(self.index, self.mode)
        self.lib.LoadPhoto(self.index + 1, self.mode)
        self.runtime = 0

        # if self.photo is not None:
        #     self.photo.UnloadImage()
        # self.photo = self.lib.GetPhoto(self.index)
        # self.photo.LoadImage(self.mode)
        # self.lib.LoadPhoto(self.index+1)

    def Tick(self, dT):
        self.pos = Frame.DefaultCursor

        self.runtime += dT
        self.screen.fill(self.BackgroundColor)
        if self.photo is not None:
            image, offset = self.photo.GetImage(self.mode)
            self.screen.blit(image, offset)

            if self.showDebug:
                elapsed = (self.runtime / 1000.0)
                self.OutputText(f'{self.index:-5} {elapsed:.1f}', (255, 0, 0))
                self.OutputNewline()

            if self.showInfo:
                # year, month, day
                timestamp = self.photo.GetCaptureDate()
                self.OutputText(f'{timestamp.year}', (255, 0, 0))
                self.OutputText(f'{timestamp:%B}', (255, 0, 0))
                # delta = datetime.now() - timestamp
                # total_years = delta.total_seconds() / (60 * 60 * 24 * 365)
                # if total_years > 2:
                #     self.OutputText(f'{total_years}yrs ago', (255, 0, 0))
                self.OutputNewline()
                keywords = [k for k in self.photo.GetKeywords() if k not in Frame.KeywordFilter]
                for k in keywords:
                    self.OutputText(k, (255, 0, 0))

        pygame.display.flip()

        self.InputHandler(pygame.event.get())

        # Test for image support except pygame.error as err: print("Failed to display %s: %s" % (photo.fullpath, err))

    def Run(self, isDebug):
        self.NextImage(0)

        if isDebug:
            self.isWindowed = True
            self.showDebug = True
            self.showInfo = True

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

        # Test for image support
        if not pygame.image.get_extended():
            print("Your Pygame isn't built with extended image support.")
            print("It's likely this isn't going to work.")
            sys.exit(1)

        pygame.display.set_caption("PiFrame")
        if self.isWindowed:
            self.mode = (1920, 1024)
        else:
            modes = pygame.display.list_modes()
            self.mode = max(modes)
            logging.debug(f"Setting mode = {self.mode}")

        self.screen = pygame.display.set_mode(self.mode)

        pygame.time.set_timer(Frame.NextImageEvent, Frame.WaitTime)

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

    def OutputText(self, text, color):
        self.DrawText(text, color, self.pos)
        self.OutputNewline()

    def OutputNewline(self):
        self.pos = (self.pos[0], self.pos[1] + self.OutputStep)

    def DrawText(self, text, color, pos):
        surface = self.font.render(text, False, color)
        self.screen.blit(surface, pos)