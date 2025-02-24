import logging
logger = logging.getLogger()

import pygame
import utils
import exif
import datetime
#from IPTCInfo3 import IPTCInfo
from iptcinfo3 import IPTCInfo
import json

# https://pypi.org/project/IPTCInfo3/  (iptcinfo)
# https://github.com/jamesacampbell/iptcinfo3/blob/master/iptcinfo3.py [iptc keys]

class Photo:
    def __init__(self, fullpath=None):
        self.fullpath = fullpath

        ## meta data
        self.keywords = []
        self.title = None
        self.timestamp = datetime.datetime(1900, 1, 1)
        self.orientation = None
        self.rotation = None

        ## image data
        self.image = None
        self.info = None
        self.offset = None

    def __str__(self):
        return self.fullpath

    @utils.timer
    def LoadImage(self, mode):
        #if self.image is None:
        logger.debug(f"Loading image, {self.fullpath}")

        img = pygame.image.load(self.fullpath)
        size = img.get_size()
        logger.debug(f"Loaded image {self.fullpath}, size={size}")

        self.LoadMetaData()

        self.LogInfo()

        rot = self.rotation
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

        if mode is not None:        
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

            logger.debug(f"ImageTransform:  size={size}, scale={scale}")

            self.image = pygame.transform.smoothscale(img, scale)
            self.offset = ((mode[0] - scale[0]) / 2, (mode[1] - scale[1]) / 2)
        else:
            self.image = img
            self.offset = (0, 0)

        return self.image, self.offset

    # Unload photo resources
    def UnloadImage(self):
        self.image = None
        self.offset = None

    def LogInfo(self):
        logger.debug(f"***PHOTO fullpath={self.fullpath}")
        logger.debug(f"\tIsLoaded = {self.IsLoaded()}")
        if self.IsLoaded():
            logger.debug(f"\t\tSize   = {self.image.get_size()}")
            logger.debug(f"\t\tOffset = {self.offset}")

    def GetImage(self, mode):
        if self.image is None:
            return self.LoadImage(mode)
        return self.image, self.offset

    def IsLoaded(self):
        return self.image is not None

    def LoadMetaData(self):
        exif_data = None
        iptc_data = None

        try:
            with open(self.fullpath, 'rb') as image_file:
                exif_data = exif.Image(image_file)                
        except:
             logger.warning(f'Failed to load exif from {self.fullpath}')
             return

        try:
            self.info = IPTCInfo(self.fullpath)

            ## capture time
            if exif_data is not None:
                for key in exif_data.get_all().keys():
                    logger.debug(f"\t\t{key} = {exif_data[key]}")    
                timestamp = exif_data.get('datetime_original')
                if timestamp is not None:
                    parts = timestamp.split(' ')
                    parts = parts[0].split(':')
                    self.timestamp = datetime.datetime(int(parts[0]), int(parts[1]), int(parts[2]))
                self.rotation = exif_data.get('orientation')

            if iptc_data is not None:
                for key in iptc_data._data:
                    logger.debug(f"\t\t{key} = {iptc_data._data[key]}")    
                self.keywords = iptc_data['keywords']

        except:
            logger.warning(f'Failed to load iptc info from {self.fullpath}')

    # def loadExif(self):
    #     try:
    #         with open(self.fullpath, 'rb') as image_file:
    #             self.exif = exif.Image(image_file)
    #     except:
    #         logger.warning(f'Failed to load exif info from {self.fullpath}')

    def GetExifAttr(self, attr):
        if self.HasExif():
            return self.exif.get(attr)
        return None

