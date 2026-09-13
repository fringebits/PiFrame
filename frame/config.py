import logging
logger = logging.getLogger()

import os
import json
from .photo import Photo
from .constants import TRANSIENT_DIRECTORY

class Config:
    DefaultFilename = 'config.json'
    SecretsFilename = 'secrets.json'
    StateFilename = os.path.join(TRANSIENT_DIRECTORY, 'state.json')

    def __init__(self):
        self.sources = {}
        self.source_name = ''
        self.last_index = 0
        self.source = ''
        self.force_init = False
        self.wait_time = 10000
        self.slack_token = ''
        self.slack_channel = ''
        self.load_config()
        
    def load_config(self):
        try:
            with open(Config.DefaultFilename) as f:
                data = json.load(f)

            self.sources = data.get('sources', {})
            if not self.sources and data.get('source'):
                self.sources = {'default': data['source']}
            if not self.sources:
                self.sources = {'default': './content'}

            self.wait_time = data.get('wait_time', 10000)
            self.force_init = data.get('force_init', False)
            self.debug = data.get('debug', False)
            self.server = data.get('server', False)

        except FileNotFoundError:
            return

        try:
            with open(Config.SecretsFilename) as f:
                secrets = json.load(f)
            self.slack_token = secrets.get('slack_token', '')
            self.slack_channel = secrets.get('slack_channel', '')
        except FileNotFoundError:
            pass

        try:
            with open(Config.StateFilename) as f:
                state = json.load(f)
            self.states = state.get('sources', {})
            if not self.states and 'last_index' in state:
                self.states = {next(iter(self.sources)): {'last_index': state['last_index']}}
            selected_source = state.get('source_name', next(iter(self.sources)))
        except FileNotFoundError:
            self.states = {}
            if 'last_index' in data:
                self.states[next(iter(self.sources))] = {'last_index': data['last_index']}
            selected_source = next(iter(self.sources))

        if selected_source not in self.sources:
            selected_source = next(iter(self.sources))
        self.select_source(selected_source)

    def select_source(self, source_name):
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        self.source_name = source_name
        self.source = self.sources[source_name]
        self.last_index = getattr(self, 'states', {}).get(source_name, {}).get('last_index', 0)

    def save_state(self):
        states = getattr(self, 'states', {})
        states[self.source_name] = {'last_index': self.last_index}
        os.makedirs(TRANSIENT_DIRECTORY, exist_ok=True)
        with open(Config.StateFilename, 'w') as f:
            json.dump({'source_name': self.source_name, 'sources': states}, f, indent=4)