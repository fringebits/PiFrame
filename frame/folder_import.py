
import os
from .photo import Photo

class Folder:
    PhotoExtensions = ['.jpg', '.png']

    def __init__(self, basepath, recurse):
        self.basepath = basepath
        self.recurse = recurse
        self.Info()

    def Info(self):
        print("Folder: path={0}, recurse={1}".format(self.basepath, self.recurse))

    def Scan(self):
        files = self.ScanInternal(self.basepath, self.recurse)
        print("Imported {0} files from path={1}, recurse={2}".format(len(files), self.basepath, self.recurse))
        return files

    def ScanInternal(self, filepath, recurse):
        dirfiles = os.listdir(filepath)
        fullpaths = map(lambda name: os.path.join(filepath, name), dirfiles)
        dirs = []
        files = []
        for file in fullpaths:
            if os.path.isdir(file): dirs.append(file)
            if os.path.isfile(file):
                (name, ext) = os.path.splitext(file)
                if (ext in self.PhotoExtensions):
                    files.append(Photo(file))

        if recurse == True:
            for path in dirs:
                files = files + self.ScanInternal(path, recurse)
            
        return files
                    

class FolderImport:
    def __init__(self):
        self.folders = []

    def AddPath(self, path, recurse):
        self.folders.append(Folder(path, recurse))

    def Run(self):
        files = []

        for folder in self.folders:
            files = files + folder.Scan()

        print("Imported {0} files".format(len(files)))
        return files