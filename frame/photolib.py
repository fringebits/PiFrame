# -*- coding: utf-8 -*-

import random
from .photo import Photo
from .folder_import import FolderImport

class PhotoLib:
    def __init__(self):
        self.photos = []

    def Init(self, importer):
        self.photos = importer.Run()

    def Shuffle(self):
        random.shuffle(self.photos)

    def GetPhoto(self, index):
        index = index % len(self.photos)
        photo = self.photos[index]
        print("GetPhoto {0}, {1}".format(index, photo.fullpath))
        return photo