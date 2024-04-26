import numpy 
import skimage
import glob
from PIL import Image
import random

THRESHOLD = 1100

def mse(fimage, simage):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	err = numpy.sum((fimage.astype("float") - simage.astype("float")) ** 2)
	mean = err / float(fimage.shape[0] * simage.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

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
        f_image_conv = skimage.img_as_float(f_image)
        attempts = 0
        while attempts < strain_length:
            s_image = strain[attempts]
            s_image_conv = skimage.img_as_float(s_image)
            comparison_value = mse(f_image_conv,s_image_conv)
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




    # for x in range (1500):
    #     compare_images(imagef, images)

    # return

if __name__ == "__main__":
    main()
