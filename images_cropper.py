from PIL import Image,ImageOps,ImageStat,ImageDraw, ImageFilter
import numpy as np
import math

filelist =     [
"C:/Users/ADostovalova/Downloads/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG"
]

psp_list=[
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG4._PSP",
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG5._PSP",
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG._PSP",
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG1._PSP",
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG2._PSP",
"E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG3._PSP"
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

    def make_summ(self, f1, f2):
        picture = Image.open(f1)
        picture2 = Image.open(f2)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (width_p, height_p), color=0)
        mass = np.array(picture, dtype="float32")
        mass2 = np.array(picture2, dtype="float32")
        mass = mass + mass2
        print(mass.shape, width_p, height_p)
        for i in range(height_p):
            for j in range(width_p):

                img_accumulated.putpixel((j, i), (int(mass[i, j, 0]), int(mass[i, j, 1]), int(mass[i, j, 2])))
        img_accumulated.save(f1 + "_sum.JPG")
        img_accumulated.close()
        picture.close()
        picture2.close()

    def draw_psp_list(self, psp_list, dir,img_base):
        for i in range(len(psp_list)):
            t_color = ['blue', 'red', 'yellow', 'green', 'violet']
            temple_file = Image.open(img_base)
            colors = {}
            curColor = ""
            rect_flag = False

            img = Image.new('RGB', temple_file.size, color=0)
            draw = ImageDraw.Draw(img)
            fp = open(psp_list[i])
            print("all was opened")
            for k, txt in enumerate(fp):
                if k < 2:
                    continue
                zz, t = txt.split('=')
                if t.find('Pline') >= 0:
                    x2y = []
                    rect_flag = False
                    continue
                if t.find('Rectangle') >= 0:
                    x2y = []
                    rect_flag = True
                    continue
                if t.find('Pen') >= 0:
                    p = t.split(',')
                    curColor = p[2]
                    colors.update({p[2]: len(colors)})

                t = t.split(' ')
                if t[0] == '':
                    if rect_flag:
                        x2y.insert(1, (x2y[0][0], x2y[1][1]))
                        x2y.append((x2y[2][0], x2y[0][1]))
                        print(curColor)
                    draw.polygon(x2y, outline=t_color[0], fill=t_color[0])
                    continue
                x2y.append((int(t[0]), int(t[1])))
            print("masks were drawen")
            img.save(dir + "new_mask_class_" + str(i) + ".BMP")
            img.close()
            fp.close()

    def make_one_channel(self, filename):
        picture = Image.open(filename)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (width_p, height_p), color=0)
        mass = np.array(picture, dtype="float32")
        print(mass.shape, width_p, height_p)
        ch_num = 2
        for i in range(height_p):
            for j in range(width_p):

                # print(mass[i, j])
                img_accumulated.putpixel((j, i), (int(mass[i, j, ch_num]), int(mass[i, j, ch_num]), int(mass[i, j, ch_num])))
        img_accumulated.save(filename + "_" + str(ch_num) + "channel.JPG")
        img_accumulated.close()
        picture.close()

    def make_one_channel_as_summ(self, filename):
        picture = Image.open(filename)
        width_p, height_p = picture.size
        img_accumulated = Image.new('RGB', (width_p, height_p), color=0)
        mass = np.array(picture, dtype="float32")
        print(mass.shape, width_p, height_p)
        ch_num1 = 2
        ch_num2 = 0
        ch_num3 = 0
        for i in range(height_p):
            for j in range(width_p):
                color = int( 0.33*(mass[i, j, ch_num1] + mass[i, j, ch_num2]+mass[i, j, ch_num3]))
                img_accumulated.putpixel((j, i),
                                         (color, color, color))
        img_accumulated.save(filename + "_" + str(ch_num1) + "_" + str(ch_num2) +  "_" + str(ch_num3) +"channel.JPG")
        img_accumulated.close()
        picture.close()


mod = image_modifier()
mod.set_filelist(filelist)
#mod.crop_same_part(0,0,2866, 860)
#mod.make_one_color("E:/__SAR_ship2/P0119_2400_3200_6000_6800_instance_color_RGB.png")
#mod.make_square("E:/_SAR_town/__SAR_HH.TIF_crop.JPG_part.JPG")
#mod.make_log("E:/_SAR_town/__SAR_HH.TIF_crop.JPG_part.JPG")
#mod.make_summ(filelist[2], filelist[5])
mod.draw_psp_list(psp_list, "E:/_SAR_kalimantan/","E:/_SAR_kalimantan/q04indrex0401x2_t04_oceanmouth.jpeg_2_0channel.JPG_part.JPG")
#mod.make_one_channel("C:/Users/ADostovalova/Downloads/q04indrex0401x2_t04_oceanmouth.jpeg")
#mod.make_one_channel_as_summ("C:/Users/ADostovalova/Downloads/q04indrex0401x2_t04_oceanmouth.jpeg")