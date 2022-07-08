
from frame.folder_import import FolderImport
from frame.frame import Frame
from frame.server import FrameServer

import argparse

import os
import logging
from logging.handlers import RotatingFileHandler

logFile = 'piframe.log'
logLevel = logging.DEBUG
isDebug = True

handler = RotatingFileHandler(logFile, mode='a', backupCount=5)
if os.path.isfile(logFile):
    handler.doRollover()
logging.basicConfig(filename=logFile, level=logging.DEBUG)

def main():
    logging.debug("PiFrame main")

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Debug mode, forces use of windows", action="store_true")
    args = parser.parse_args()

    importer = FolderImport()
    if isDebug:
        importer.AddPath("//merlin/photo/BestOf2018", True)
    else:
        importer.AddPath("/home/pi/photo/PiFrame", True)
        importer.AddPath("//merlin/photo/PiFrame", True)
    
    try:
        server = FrameServer()
        server.start()

        frame = Frame()
        frame.Init(importer)
        frame.Run(args.debug)

    finally:
        frame.Shutdown()

if __name__ == "__main__":
    main()