#### This is for method 1 ####

import random
from PIL import Image, ImageChops, ImageStat
import glob

THRESHOLD = 0.1
RESULTS = dict()

def compare_images(imagef, images):
    differences = ImageChops.difference(imagef, images)
    stat = ImageStat.Stat(differences)
    ratio = sum(stat.mean) / (len(stat.mean) * 255)
    return ratio


def main():
    ftrain = [] #initialize train list
    strain = []
    for x in range (6): 
        """
        populate the train list with all training documents
        """
        filepath = "../lab-4/data/NISTSpecialDatabase4GrayScaleImagesofFIGS/sd04/png_txt/figs_" + str(x) + "/*.png"
        images = glob.glob(filepath)
        for file in images:
            filename = file[-12:]
            if filename[0] == "f":
                image = Image.open(file)
                ftrain.append(image)
            elif filename[0] == "s":
                if len(strain) < 1000:
                    image = Image.open(file)
                    strain.append(image)
    for x in range (6,8):
        """
        populate the test list with all training documents
        """
        filepath = "../lab-4/data/NISTSpecialDatabase4GrayScaleImagesofFIGS/sd04/png_txt/figs_" + str(x) + "/f*.png"
        images = glob.glob(filepath)
        for file in images:
            image = Image.open(file)
            ftrain.append(image)

    ## Begin processing the train images ##
    random.shuffle(strain)
    number_trained = 0
    ftrain_length = len(ftrain)
    while number_trained < ftrain_length:
        f_image = ftrain[number_trained]
        strain_length = len(strain)
        attempts = 0
        while attempts < strain_length:
            s_image = strain[attempts]
            comparison_value = compare_images(f_image,s_image)
            if comparison_value < THRESHOLD:
                strain.pop(attempts)
                number_trained += 1
                break
            else: 
                attempts += 1
                if attempts >= strain_length:
                    number_trained += 1
                    break

        
    correct_accept = 0
    correct_reject = 0
    incorrect_accept = 0
    incorrect_reject = 0

    for image in strain:
        filenumber = int(image.filename[-11:-4])
        if filenumber <= 1000:
            incorrect_reject += 1
        else: 
            correct_reject += 1
    correct_accept = 1000 - incorrect_reject
    incorrect_accept = 1000 - correct_reject
    ratio_of_ca = correct_accept / 1000
    ratio_of_ia = incorrect_accept / 1000
    ratio_of_cr = correct_reject / 1000
    ratio_of_ir = incorrect_reject / 1000
    print("Number of correct accepts: " + str(correct_accept) + "/1000; ratio: " + str(ratio_of_ca))
    print("Number of incorrect accepts: " + str(incorrect_accept) + "/1000; ratio: " + str(ratio_of_ia))
    print("Number of correct rejects: " + str(correct_reject) + "/1000; ratio: " + str(ratio_of_cr))
    print("Number of incorrect rejects: " + str(incorrect_reject) + "/1000; ratio: " + str(ratio_of_ir))
    print("Thus, the false reject rate is " + str(ratio_of_ir) + " and the false accept rate is " + str(ratio_of_ia))



if __name__ == "__main__":
    main()


#### All f images will be added to f_train
#### Only the first 1,000 s train images will be added to s_train.
#### This is to ensure validation is working properly by having some fingerprints that should authenticat successfully and some finger prints that should not authenticate successfully.