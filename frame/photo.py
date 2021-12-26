
import logging
import pygame
import utils
import exif

class Photo:
    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.image = None
        self.offset = None
        self.exif = None

    @utils.timer
    def LoadImage(self, mode):
        #if self.image is None:
        logging.debug(f"Loading image, {self.fullpath}")

        img = pygame.image.load(self.fullpath)
        size = img.get_size()
        logging.debug(f"Loaded image {self.fullpath}, size={size}")

        self.LoadExif()

        self.LogInfo()

        rot = self.GetExifAttr('orientation')
        if rot is None:
            ""
        if rot == 2:
            print("RotateNoneFlipX")
        elif rot == 3:
            print("Rotate180FlipNone")
            img = pygame.transform.rotate(img, 180)
        elif rot == 4:
            print("Rotate180FlipX")
        elif rot == 5:
            print("Rotate90FlipX")
        elif rot == 6:
            print("Rotate90FlipNone")
            img = pygame.transform.rotate(img, -90)
        elif rot == 7:
            print("Rotate270FlipX")
        elif rot == 8:
            print("Rotate270FlipNone")
            img = pygame.transform.rotate(img, 270)
        
        # scale to FIT
        size = img.get_size()
        imgAspect = size[0] / size[1]
        modeAspect = mode[0] / mode[1]

        # choose some default
        scale = mode

        if imgAspect == modeAspect:
            scale = mode
        elif imgAspect < modeAspect:
            # wider than high
            s = mode[1] / size[1]
            scale = (int(s * size[0]), mode[1])
        else:
            s = mode[0] / size[0]
            scale = (mode[0], int(s * size[1]))

        logging.debug(f"ImageTransform:  size={size}, scale={scale}")

        self.image = pygame.transform.smoothscale(img, scale)
        self.offset = ((mode[0] - scale[0]) / 2, (mode[1] - scale[1]) / 2)

        return self.image, self.offset

    # Unload photo resources
    def UnloadImage(self):
        self.image = None
        self.offset = None
        self.exif = None

    def LogInfo(self):
        logging.debug(f"***PHOTO fullpath={self.fullpath}")
        logging.debug(f"\tIsLoaded = {self.IsLoaded()}")
        if self.IsLoaded():
            logging.debug(f"\t\tSize   = {self.image.get_size()}")
            logging.debug(f"\t\tOffset = {self.offset}")
        logging.debug(f"\tHasExif  = {self.HasExif()}")
        if self.HasExif():
            keywords = self.exif.get('xp_keywords')
            logging.debug(f"\t\tKeywords = {self.offset}")
            data = self.exif.get_all()
            for key in data.keys():
                logging.debug(f"\t\t{key} = {data[key]}")    

    def GetImage(self, mode):
        if self.image is None:
            return self.LoadImage(mode)
        return self.image, self.offset

    def HasExif(self):
        return self.exif is not None

    def IsLoaded(self):
        return self.image is not None

    def LoadExif(self):
        try:
            with open(self.fullpath, 'rb') as image_file:
                self.exif = exif.Image(image_file)
        except:
            logging.warning(f'Failed to load exif info from {self.fullpath}')

    def LoadExif(self):
        try:
            with open(self.fullpath, 'rb') as image_file:
                self.exif = exif.Image(image_file)
        except:
            logging.warning(f'Failed to load exif info from {self.fullpath}')

    def GetExifAttr(self, attr):
        if self.HasExif():
            return self.exif.get(attr)