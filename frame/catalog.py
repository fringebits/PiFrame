import logging
logger = logging.getLogger()

import json
import os
import utils
import random
from .photo import Photo
from .config import Config
from .folder_import import FolderImport

class Catalog:
    PhotoExtensions = ['.jpg', '.png']
    Database = 'catalog.json'

    def __init__(self, config):
        self.photos = []
        self.config = config
        self.load_database(self.config.force_init)

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
        logger.debug(f"init_database")
        files = []
        importer = FolderImport()
        importer.AddPath(self.config.source, True)
        data = importer.Run()
        self.photos = [x.fullpath for x in data]
        random.shuffle(self.photos)

    def getNumPhotos(self):
        return len(self.photos)

    def LoadPhoto(self, index, mode):
        num = self.getNumPhotos()
        assert num > 0, "Catalog doesn't have any photos"
        index = index % num
        fullpath = self.photos[index]
        photo = Photo(fullpath)
        photo.LoadImage(mode)

        self.config.last_index = index
        self.config.save_config() # should create another runtime data file to track this
        return photo