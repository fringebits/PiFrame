from frame.folder_import import FolderImport
from frame.frame import Frame
from frame.catalog import Catalog
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Debug mode, forces use of windows", action="store_true")
    parser.add_argument("--noserver", help="Disable use of webserver", action="store_true")
    parser.add_argument("--source", help="Path to images to load.", default="./content")
    parser.add_argument("--refresh", help="Reset and ignore existing catalog.", action="store_true")
    args = parser.parse_args()

    init_logs(args.debug)

    importer = FolderImport()
    logger.debug(f'Image Sorce = {args.source}')
    importer.AddPath(args.source, True)
    # if args.debug:
    #     importer.AddPath("//merlin/photo/BestOf2018", True)
    # else:
    #     importer.AddPath("./content", True)
    #     importer.AddPath("//merlin/photo/PiFrame", True)

    frame = None
    
    try:
        catalog = Catalog(importer, args.refresh)

        frame = Frame(catalog)

        if not args.noserver:
            # start the bottle-webserver
            server.Run(frame, args.debug)
        
        frame.Run(args.debug)

    finally:
        if frame is not None:
            frame.Shutdown()
            frame = None

if __name__ == "__main__":
    main()
