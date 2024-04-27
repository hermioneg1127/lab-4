#### This is for method 1 ####

import random
from PIL import Image, ImageChops, ImageStat
import glob
import numpy
import skimage

RESULTS = dict()
X = 6
Y = 8
HALF_FILES = 250
THRESHOLD = ""


def mse(fimage, simage):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	err = numpy.sum((fimage.astype("float") - simage.astype("float")) ** 2)
	mean = err / float(fimage.shape[0] * simage.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err


def caller():
    ftrain = [] #initialize train list
    strain = []
    rejected = []
    incorrect_accept = 0
    correct_accept = 0
    for x in range (X,Y): 
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
                if len(strain) < HALF_FILES:
                    image = Image.open(file)
                    strain.append(image)

    ## Begin processing the train images ##
    random.shuffle(strain)
    number_trained = 0
    ftrain_length = len(ftrain)
    while number_trained < ftrain_length:
        f_image = ftrain[number_trained]
        strain_length = len(strain)
        attempts = 0
        f_image_conv = skimage.img_as_float(f_image)
        while attempts < strain_length:
            s_image = strain[attempts]
            s_image_conv = skimage.img_as_float(s_image)
            comparison_value = mse(f_image_conv,s_image_conv)
            if comparison_value < THRESHOLD:
                # strain.pop(attempts)
                #s_image.close()
                f_image.close()
                number_trained += 1
                attempts +=1
                break
            else: 
                attempts += 1
                if attempts >= strain_length:
                    rejected.append(f_image)
                    number_trained += 1
                    break

        
    correct_reject = 0
    incorrect_reject = 0

    for image in strain:
        image.close()
    for image in rejected:
        filenumber = int(image.filename[-11:-7])
        image.close()
        if filenumber > HALF_FILES:
            correct_reject += 1
        elif filenumber <= HALF_FILES:
            incorrect_reject += 1
    incorrect_accept = HALF_FILES - correct_reject
    correct_accept = HALF_FILES - incorrect_reject
    ratio_of_ca = correct_accept / HALF_FILES
    ratio_of_ia = incorrect_accept / HALF_FILES
    ratio_of_cr = correct_reject / HALF_FILES
    ratio_of_ir = incorrect_reject / HALF_FILES
    print("Number of correct accepts: " + str(correct_accept) + "/250; ratio: " + str(ratio_of_ca))
    print("Number of incorrect accepts: " + str(incorrect_accept) + "/250; ratio: " + str(ratio_of_ia))
    print("Number of correct rejects: " + str(correct_reject) + "/250; ratio: " + str(ratio_of_cr))
    print("Number of incorrect rejects: " + str(incorrect_reject) + "/250; ratio: " + str(ratio_of_ir))
    print("Thus, the false reject rate is " + str(ratio_of_ir) + " and the false accept rate is " + str(ratio_of_ia))
    return ratio_of_ir, ratio_of_ia

def main():
    caller()


if __name__ == "__main__":
    main()


#### All f images will be added to f_train
#### Only the first 1,000 s train images will be added to s_train.
#### This is to ensure validation is working properly by having some fingerprints that should authenticat successfully and some finger prints that should not authenticate successfully.