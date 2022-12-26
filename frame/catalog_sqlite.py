
import logging
logger = logging.getLogger()

import sqlite3
import json
import os
import utils
import random
from .photo import Photo

class CatalogSqlite:
    PhotoExtensions = ['.jpg', '.png']
    Filename = 'catalog.json'
    Database = 'catalog.db'

    def __init__(self, source):
        self.source = source
        self.photos = []
        self.load_database(False)

    def load_config(self):
        try:
            with open(Catalog.Filename) as f:
                data = json.load(f)
            self.config = data
            return True
        except FileNotFoundError:
            return False
        # except:
        #     # This is something other than missing a file! (probably bad data)
        #     return False

    def write_config(self):
        with open(Catalog.Filename, 'w') as f:
            json_object = json.dumps(self, default=lambda o: o.__dict__, indent=4)
            f.write(json_object)

    def load_database(self, force_init):
        is_new = not os.path.exists(Catalog.Database)
        if force_init and not is_new:
            os.remove(Catalog.Database)
            is_new = True

        self.database = sqlite3.connect(Catalog.Database)
        if is_new:
            self.init_database()
        else:
            cur = self.database.cursor()
            cur.execute("SELECT rowid FROM photos")
            self.photos = cur.fetchall()

    def init_database(self):
        self.database.execute("CREATE TABLE photos(fullpath, title, timestamp)")
        data = self.source.Run()
        cur = self.database.cursor()
        for photo in data:
            photo.LoadMetaData()
            cur.execute(f"INSERT INTO photos VALUES ('{photo.fullpath}', '{photo.title}', '{photo.timestamp}')")
            self.photos.append(cur.lastrowid)

    def getNumPhotos(self):
        return len(self.photos)

    # def getPhoto(self, index):
    #     index = index % len(self.photos)
    #     photo = self.photos[index]
    #     #print("GetPhoto {0}, {1}".format(index, photo.fullpath))
    #     return photo

    def LoadPhoto(self, index, mode):
        rowid = self.photos[index % len(self.photos)]
        fullpath = self.database.execute("SELECT fullpath FROM photos WHERE rowid='{rowid}'").fetchone()

        if fullpath is None:
            return None
        
        photo = Photo(fullpath)
        photo.LoadImage()

        return photo

    def UnloadPhoto(self, index):
        photo = self.GetPhoto(index)
        photo.UnloadImage()