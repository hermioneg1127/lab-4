### This is the hybrid system that uses all three methods with their improved thresholds.
import random
from PIL import Image, ImageChops, ImageStat
import glob
import numpy
from skimage.metrics import structural_similarity
import skimage

RESULTS = dict()
X = 6
Y = 8
HALF_FILES = 1750
HALF_SIZE = 250
mse_threshold = 0.0272
compare_threshold = 0.1261
ssim_threshold = 0.2185


def compare_images(imagef, images):
    """
    This method determineds the differences in the images and then
    returns it as a ratio for comparison
    """
    differences = ImageChops.difference(imagef, images)
    stat = ImageStat.Stat(differences)
    ratio = sum(stat.mean) / (len(stat.mean) * 255)
    if ratio < compare_threshold:
        return 1
    return 0

def mse(fimage, simage):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
    err = numpy.sum((fimage.astype("float") - simage.astype("float")) ** 2)
    mean = err / float(fimage.shape[0] * simage.shape[1])
    if mean < mse_threshold:
        return 1
    return 0
    

def ssim(f_image, s_image):
    value = structural_similarity(f_image,s_image, data_range=1)
    if value > ssim_threshold:
        return 1
    return 0

def caller():
    """
    This method completes the initialization of the images and the 
    testing against the threshold
    """
    ftrain = [] #initialize reference image train list
    strain = [] #initialize the subject image train list
    rejected = [] #initialize the reject list
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
            if filename[0] == "f": #checking to see if a reference image
                image = Image.open(file)
                ftrain.append(image)
            elif filename[0] == "s": #checking to see if a subject image
                if len(strain) < HALF_SIZE: #so there can be correct rejects and correct accepts, only half of the images will be in the database.
                    image = Image.open(file)
                    strain.append(image)

    ## Begin processing the train images ##
    random.shuffle(strain) #shuffles to introduce randomness 
    number_trained = 0
    ftrain_length = len(ftrain)
    while number_trained < ftrain_length: #for every reference image
        f_image = ftrain[number_trained]
        strain_length = len(strain)
        attempts = 0
        f_image_conv = skimage.img_as_float(f_image)
        while attempts < strain_length: #for every value left in strain
            s_image = strain[attempts] 
            s_image_conv = skimage.img_as_float(s_image)
            method_1 = compare_images(f_image,s_image) #compare the ftrain image with the strain image
            method_2 = mse(f_image_conv, s_image_conv)
            method_3 = ssim(f_image_conv, s_image_conv)
            result = method_1 + method_2 + method_3
            if result >= 2: # if similar enough, pop the strain value, close the images, and correct_accept += 1
                f_image.close()
                number_trained += 1
                attempts +=1
                break
            else: 
                attempts += 1
                if attempts >= strain_length: #no more simages to compare against, so no good enough  match was found
                    filenumber = f_image.filename[-11:-7]
                    rejected.append(filenumber)
                    f_image.close()
                    number_trained += 1
                    break

        
    correct_reject = 0
    incorrect_reject = 0

    #Calculate the incorrect and correct rejects and their associates accepts. 
    for image in strain:
        image.close()
    for image in rejected:
        filenumber = int(image)
        if filenumber > HALF_FILES:
            correct_reject += 1
        if filenumber <= HALF_FILES:
            incorrect_reject += 1
    incorrect_accept = HALF_SIZE - correct_reject
    correct_accept = HALF_SIZE - incorrect_reject
    ratio_of_ca = correct_accept / HALF_SIZE
    ratio_of_ia = incorrect_accept / HALF_SIZE
    ratio_of_cr = correct_reject / HALF_SIZE
    ratio_of_ir = incorrect_reject / HALF_SIZE
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
