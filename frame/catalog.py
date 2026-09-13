import logging
logger = logging.getLogger()

import json
import os
import utils
import random
from .photo import Photo
from .config import Config
from .folder_import import FolderImport
from .constants import TRANSIENT_DIRECTORY

class Catalog:
    DatabaseDirectory = TRANSIENT_DIRECTORY

    def __init__(self, config):
        self.photos = []
        self.config = config
        self.database = os.path.join(
            Catalog.DatabaseDirectory,
            f'cat-{self.config.source_name}.json')
        self.load_database(self.config.force_init)

    def load_database(self, force_init):
        is_new = not os.path.exists(self.database)
        if force_init and not is_new:
            os.remove(self.database)
            is_new = True

        if not is_new:
            try:
                with open(self.database) as f:
                    data = json.load(f)
                self.photos = data['photos']
            except:
                assert False
        else:
            self.init_database()
            self.write_database()

    def write_database(self):
        os.makedirs(Catalog.DatabaseDirectory, exist_ok=True)
        with open(self.database, 'w') as f:
            json.dump({'photos': self.photos}, f, indent=4)

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
        self.config.save_state()
        return photo