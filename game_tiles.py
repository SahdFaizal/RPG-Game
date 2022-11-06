from PIL import Image
import glob
image_list = []
i = 0
bush_index = 0
background_index = 0
for filename in glob.glob('tiles/*.png'): #assuming gif
    im= filename
    #print(im)
    #print(i)
    image_list.append(im)
    i += 1
