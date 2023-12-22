from frame.folder_import import FolderImport
from frame.frame import Frame
from frame.catalog import Catalog
from frame.config import Config

import frame.server as server
import argparse
import os
import platform
from logging.handlers import RotatingFileHandler
import logging
logger = logging.getLogger()

logFile = 'piframe.log'

def init_logs(debug):
    handler = RotatingFileHandler(logFile, mode='a', backupCount=5)
    if os.path.isfile(logFile):
        handler.doRollover()
    logging.basicConfig(filename=logFile, level=logging.DEBUG)
    console = logging.StreamHandler()
    if debug:
        logLevel = logging.DEBUG
    else:
        logLevel = logging.INFO
    console.setLevel(logLevel)
    logger.addHandler(console)

def main():
    logger.debug("PiFrame main")
    logger.info(f'python-version = {platform.python_version()}')

    # parser = argparse.ArgumentParser()
    # parser.add_argument("--debug", help="Debug mode, forces use of windows", action="store_true")
    # parser.add_argument("--noserver", help="Disable use of webserver", action="store_true")
    # args = parser.parse_args()

    config = Config()

    init_logs(config.debug)

    # if args.debug:
    #     importer.AddPath("//merlin/photo/BestOf2018", True)
    # else:
    #     importer.AddPath("./content", True)
    #     importer.AddPath("//merlin/photo/PiFrame", True)

    frame = None
    
    try:
        catalog = Catalog(config)

        frame = Frame(config, catalog)

        if config.server:
            # start the bottle-webserver
            server.Run(config, frame)
        
        frame.Run()

    finally:
        if frame is not None:
            frame.Shutdown()
            frame = None

if __name__ == "__main__":
    main()
