# -*- coding: utf-8 -*-

import random
from .photo import Photo
from .folder_import import FolderImport

class PhotoLib:

    ShuffleCount = 7
    
    def __init__(self):
        self.photos = []

    def Init(self, importer):
        self.photos = importer.Run()

    def Shuffle(self):
        count = len(self.photos)

        for n in range(self.ShuffleCount):
            for x in range(count):
                r = random.randint(0, count-1)
                self.photos[x], self.photos[r] = self.photos[r], self.photos[x]

    def GetPhoto(self, index):
        index = index % len(self.photos)
        photo = self.photos[index]
        print("GetPhoto {0}, {1}".format(index, photo.fullpath))
        return photo