
import logging
logger = logging.getLogger()

import json
import os
import utils
import random
from .photo import Photo

class Config:
    def __init__(self):
        self.last_index = 0

class Catalog:
    PhotoExtensions = ['.jpg', '.png']
    Config = 'config.json'
    Database = 'catalog.json'

    def __init__(self, source, refresh):
        self.source = source
        self.photos = []
        self.config = Config()
        self.load_database(refresh)

    def load_config(self):
        try:
            with open(Catalog.Config) as f:
                data = json.load(f)
            self.config.last_index = data['last_index']
        except FileNotFoundError:
            return

    def write_config(self):
        with open(Catalog.Config, 'w') as f:
            json_object = json.dumps(self.config, default=lambda o: o.__dict__, indent=4)
            f.write(json_object)

    def load_database(self, force_init):
        is_new = not os.path.exists(Catalog.Database)
        if force_init and not is_new:
            os.remove(Catalog.Database)
            is_new = True

        if not is_new:
            try:
                with open(Catalog.Database) as f:
                    data = json.load(f)
                self.photos = data['photos']
            except:
                assert False
        else:
            self.init_database()
            self.write_database()

    def write_database(self):
        with open(Catalog.Database, 'w') as f:
            json_object = json.dumps(self, default=lambda o: o.__dict__, indent=4)
            f.write(json_object)

    def init_database(self):
        data = self.source.Run()
        self.photos = [x.fullpath for x in data]
        random.shuffle(self.photos)

    def update_database(self):
        logger.info('update_database')
        files = self.source.Run()
        photos = [x.fullpath for x in files]
        new_photos = [x for x in photos if x not in self.photos]
        del_photos = [x for x in self.photos if x not in self.photos]
        for item in new_photos:
            # insert this item in a random position between self.config.last_index and end of the list
            index = random.randint(self.config.last_index, len(self.photos))
            self.photos.insert(index, item)
            logger.info(f'Insert [{item}] at index={index}')
        for item in del_photos:
            self.photos.remove(item)
            logger.info(f'Removing [{item}]')
        self.write_database()

    def numPhotos(self):
        return len(self.photos)

    def LoadPhoto(self, index, mode):
        num = self.numPhotos()
        assert num > 0, "Catalog doesn't have any photos"
        index = index % num
        fullpath = self.photos[index]
        photo = Photo(fullpath)
        photo.LoadImage(mode)

        self.config.last_index = index
        self.write_config()
        return photo