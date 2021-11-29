
import pygame
from exif import Image

class Photo:
    def __init__(self, fullpath):
        self.fullpath = fullpath
        self.image = None

    def Info(self):
        print("Photo: fullpath = " + self.fullpath)

    def LoadImage(self, mode):
        #if self.image is None:
        print("Loading image, {0}".format(self.fullpath))
        img = pygame.image.load(self.fullpath)
        img = img.convert()

        rot = self.GetOrientation()

        if rot == 2:
            print("RotateNoneFlipX")
        elif rot == 3:
            print("Rotate180FlipNone")
            img = pygame.transform.rotate(img, 180)
        elif rot == 4:
            print("Rotate180FlipX")
        elif rot == 5:
            print("Rotate90FlipX")
        elif rot == 6:
            print("Rotate90FlipNone")
            img = pygame.transform.rotate(img, -90)
        elif rot == 7:
            print("Rotate270FlipX")
        elif rot == 8:
            print("Rotate270FlipNone")
            img = pygame.transform.rotate(img, 270)
        
        # scale to FIT
        size = img.get_size()
        imgAspect = size[0] / size[1]
        modeAspect = mode[0] / mode[1]

        # choose some default
        scale = mode

        if imgAspect == modeAspect:
            scale = mode
        elif imgAspect < modeAspect:
            # wider than high
            s = mode[1] / size[1]
            scale = (s * size[0], mode[1])
        else:
            s = mode[0] / size[0]
            scale = (mode[0], s * size[1])

        self.image = pygame.transform.scale(img, scale)
        self.offset = ((mode[0] - scale[0]) / 2, (mode[1] - scale[1]) / 2)

        return self.image

    def GetOrientation(self):
        try:
            with open(self.fullpath, 'rb') as image_file:
                my_image = Image(image_file)

            if my_image.has_exif:
                return my_image.orientation

        except:
            return 0