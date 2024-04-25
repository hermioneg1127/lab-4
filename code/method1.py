#### This is for method 1 ####

from PIL import Image, ImageChops, ImageStat
import glob

def compare_images(imagef, images):
    return


def main():
    test = [] #initialize test list
    train = [] #initialize train list
    for x in range (6): 
        """
        populate the train list with all training documents
        """
        filepath = "../lab-4/data/NISTSpecialDatabase4GrayScaleImagesofFIGS/sd04/png_txt/figs_" + str(x) + "/*.png"
        images = glob.glob(filepath)
        for file in images:
            train.append(file)
    for x in range (6,8):
        """
        populate the test list with all training documents
        """
        filepath = "../lab-4/data/NISTSpecialDatabase4GrayScaleImagesofFIGS/sd04/png_txt/figs_" + str(x) + "/*.png"
        images = glob.glob(filepath)
        for file in images:
            test.append(file)
            
        


    # for x in range (1500):
    #     compare_images(imagef, images)

    # return

if __name__ == "__main__":
    main()