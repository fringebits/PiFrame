
from frame.folder_import import FolderImport
from frame.frame import Frame

def main():

    importer = FolderImport()
    importer.AddPath("/home/pi/photo", True)
    # importer.AddPath("K:\\Cloud\\Dropbox (Personal)\\Camera Uploads", True)
    # importer.AddPath("K:\\Cloud\Dropbox (Personal)\\External\\Camera Uploads", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2021", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2020", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2019", True)
    # importer.AddPath("K:\\Cloud\\GoogleDrive\\Content\\Photos\\2018", True)

    frame = Frame()
    frame.Init(importer)
    frame.Run()

if __name__ == "__main__":
    main()