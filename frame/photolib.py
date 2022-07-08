# -*- coding: utf-8 -*-

import logging
import random
from .photo import Photo
from .folder_import import FolderImport

class PhotoLib:
    def __init__(self):
        self.photos = [] # list of *photos to show*

    def Init(self, importer):
        self.photos = importer.Run()

    def Shuffle(self):
        logging.debug(f'Shuffling {len(self.photos)} photos')
        random.shuffle(self.photos)

    def GetPhoto(self, index):
        index = index % len(self.photos)
        photo = self.photos[index]
        #print("GetPhoto {0}, {1}".format(index, photo.fullpath))
        return photo

    def LoadPhoto(self, index, mode):
        photo = self.GetPhoto(index)
        photo.LoadImage(mode)
        return photo

    def UnloadPhoto(self, index):
        photo = self.GetPhoto(index)
        photo.UnloadImage()