import logging
logger = logging.getLogger()

import json
from .photo import Photo

class Config:
    DefaultFilename = 'config.json'

    def __init__(self):
        self.last_index = 0
        self.source = ''
        self.force_init = False
        self.wait_time = 10000
        self.load_config()
        
    def load_config(self):
        try:
            with open(Config.DefaultFilename) as f:
                data = json.load(f)

            self.last_index = data.get('last_index', 0)
            self.source = data.get('source', './content')
            self.wait_time = data.get('wait_time', 10000)
            self.force_init = data.get('force_init', False)
            self.debug = data.get('debug', False)
            self.server = data.get('server', False)

        except FileNotFoundError:
            return
        
    def save_config(self):
        with open(Config.DefaultFilename, 'w') as f:
            json_object = json.dumps(self, default=lambda o: o.__dict__, indent=4)
            f.write(json_object)