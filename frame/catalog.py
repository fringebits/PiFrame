
import logging
logger = logging.getLogger()

import json
import os
import utils
import random
from .photo import Photo

class Catalog:
    PhotoExtensions = ['.jpg', '.png']
    Filename = 'catalog.json'

    def __init__(self, source):
        self.source = source
        self.photos = []
        if not self.load_catalog():
            self.update_catalog()

    def update_catalog(self):
        self.photos = self.source.Run()
        self.write_catalog()

    def load_catalog(self):
        try:
            with open(Catalog.Filename) as f:
                d = json.load(f)
                print(d)
            self.photos = [Photo.CreateFromJson(x) for x in d]
            return len(self.photos) > 0
        except FileNotFoundError:
            self.photos = []
            return False

    def write_catalog(self):
        data = []
        for rec in self.photos:
            data.append(rec.toJson())
        with open(Catalog.Filename, 'w') as f:
            f.write(data)        

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