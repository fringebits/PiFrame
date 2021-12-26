
from frame.folder_import import FolderImport
from frame.frame import Frame

import os
import logging
from logging.handlers import RotatingFileHandler

logFile = 'piframe.log'
logLevel = logging.DEBUG

handler = RotatingFileHandler(logFile, mode='w', backupCount=5)
if os.path.isfile(logFile):
    handler.doRollover()
logging.basicConfig(filename=logFile, level=logging.DEBUG)

def main():
    logging.debug("PiFrame main")
    importer = FolderImport()
    importer.AddPath("/home/pi/photo/PiFrame", True)
    importer.AddPath("//merlin/photo/PiFrame", True)

    # importer.AddPath("K:\\Cloud\\Dropbox (Personal)\\Camera Uploads", True)
    # importer.AddPath("K:\\Cloud\Dropbox (Personal)\\External\\Camera Uploads", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2021", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2020", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2019", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2018", True)

    try:
        frame = Frame()
        frame.Init(importer)
        frame.Run()

    finally:
        frame.Shutdown()

if __name__ == "__main__":
    main()