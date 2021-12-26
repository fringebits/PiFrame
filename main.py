
from frame.folder_import import FolderImport
from frame.frame import Frame

import os
import logging
from logging.handlers import RotatingFileHandler

logFile = 'piframe.log'
logLevel = logging.DEBUG

handler = RotatingFileHandler(logFile, mode='a', backupCount=5)
if os.path.isfile(logFile):
    handler.doRollover()
logging.basicConfig(filename=logFile, level=logging.DEBUG)

def main():
    logging.debug("PiFrame main")
    importer = FolderImport()
    importer.AddPath("/home/pi/photo/PiFrame", True)
    importer.AddPath("//merlin/photo/PiFrame", True)

    try:
        frame = Frame()
        frame.Init(importer)
        frame.Run()

    finally:
        frame.Shutdown()

if __name__ == "__main__":
    main()