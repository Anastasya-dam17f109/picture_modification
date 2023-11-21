from PIL import Image,ImageOps,ImageStat,ImageDraw, ImageFilter
import numpy as np
import math

filelist =     [
"E:/_SAR_town/__SAR_HH.TIF_crop.JPG",
"E:/_SAR_town/new_mask_class_0.BMP",
"E:/_SAR_town/__SUMM_RGB.TIF-JSON.BMP_crop.JPG",
"E:/_SAR_town/new_mask_class_5.BMP",
"E:/_SAR_town/new_mask_class_3.BMP",
"E:/_SAR_town/new_mask_class_4.BMP",
]

class image_modifier:
    def __init__(self, ):
        self.filelist = []
    def set_filelist(self, filelist):
        self.filelist = filelist
    def crop_same_part(self, l1,l2,r1,r2):

        for resourse_filename in self.filelist:
            picture = Image.open(resourse_filename)
            img_accumulated = picture.crop((l1,l2,r1,r2))
            img_accumulated.save(resourse_filename + "_part.JPG")
            img_accumulated.close()
            picture.close()
    def make_one_color(self, filename):
        picture = Image.open(filename)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (  width_p, height_p), color=0)
        mass = np.array(picture)
        print(mass.shape, width_p, height_p)
        for i in range(height_p):
            for j in range(width_p):
                if mass[i,j,0] != 0:
                    img_accumulated.putpixel((j, i), (0, 0, 255))
        img_accumulated.save(filename + "_1c.JPG")
        img_accumulated.close()
        picture.close()

    def make_square(self, filename):
        picture = Image.open(filename)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (width_p, height_p), color=0)
        mass = np.array(picture, dtype="float32")
        print(mass.shape, width_p, height_p)
        for i in range(height_p):
            for j in range(width_p):
                #print(mass[i, j])
                mass[i, j] = np.array([mass[i, j, 0] - 50, mass[i, j, 0] - 50,
                                       mass[i, j, 0] - 50])
                #mass[i, j]= np.array([math.sqrt((mass[i, j,0]-120)**2),math.sqrt((mass[i, j,0]-120)**2),math.sqrt((mass[i, j,0]-120)**2)])
                #print(mass[i, j])
                img_accumulated.putpixel((j, i), (int(mass[i, j,0]), int(mass[i, j,0]), int(mass[i, j,0])))
        img_accumulated.save(filename + "_1square.JPG")
        img_accumulated.close()
        picture.close()

    def make_log(self, filename):
        picture = Image.open(filename)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (width_p, height_p), color=0)
        mass = np.array(picture, dtype="float32")
        print(mass.shape, width_p, height_p)
        for i in range(height_p):
            for j in range(width_p):
                mass[i, j] = np.array([math.log(mass[i, j,0]),  math.log(mass[i, j,0]), math.log(mass[i, j,0])],dtype="float32")* 13.15
                #print(mass[i, j])
                img_accumulated.putpixel((j, i), (int(mass[i, j, 0]), int(mass[i, j, 0]), int(mass[i, j, 0])))
        img_accumulated.save(filename + "_1log.JPG")
        img_accumulated.close()
        picture.close()


mod = image_modifier()
#mod.set_filelist(filelist)
#mod.crop_same_part(0,212,2197, 901)
#mod.make_one_color("E:/_SAR_town/__SUMM_RGB.TIF-JSON.BMP_crop.JPG_part.JPG")
mod.make_square("E:/_SAR_town/__SAR_HH.TIF_crop.JPG_part.JPG")
#mod.make_log("E:/_SAR_town/__SAR_HH.TIF_crop.JPG_part.JPG")