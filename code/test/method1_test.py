#### This is testing phase of method one now that the mathematically best threshold was found
#### The method utilizes ImageChops.difference, an image processing method to determine how similar two images are to each other
#### The smaller the number, the better ####
#### The best threshold determined was 0.145
import random
from PIL import Image, ImageChops, ImageStat
import glob

RESULTS = dict()
X = 6
Y = 8
HALF_FILES = 250
THRESHOLD = 0.11


def compare_images(imagef, images):
    """
    This method determineds the differences in the images and then
    returns it as a ratio for comparison
    """
    differences = ImageChops.difference(imagef, images)
    stat = ImageStat.Stat(differences)
    ratio = sum(stat.mean) / (len(stat.mean) * 255)
    return ratio


def caller():
    """
    This method completes the initialization of the images and the 
    testing against the threshold
    """
    ftrain = [] #initialize reference image test list
    strain = [] #initialize the subject image test list
    rejected = [] #initialize the reject list
    incorrect_accept = 0 
    correct_accept = 0
    for x in range (X,Y): 
        """
        populate the test list with all training documents
        """
        filepath = "../lab-4/data/NISTSpecialDatabase4GrayScaleImagesofFIGS/sd04/png_txt/figs_" + str(x) + "/*.png"
        images = glob.glob(filepath)
        for file in images:
            filename = file[-12:]
            if filename[0] == "f": #checking to see if a reference image
                image = Image.open(file)
                ftrain.append(image)
            elif filename[0] == "s": #checking to see if a subject image
                if len(strain) < HALF_FILES: #so there can be correct rejects and correct accepts, only half of the images will be in the database.
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

        while attempts < strain_length: #for every value left in strain
            s_image = strain[attempts] 
            comparison_value = compare_images(f_image,s_image) #compare the ftrain image with the strain image
            if comparison_value < THRESHOLD: # if similar enough, pop the strain value, close the images, and correct_accept += 1
                strain.pop(attempts)
                s_image.close()
                f_image.close()
                number_trained += 1
                attempts +=1
                break
            else: 
                attempts += 1
                if attempts >= strain_length: #no more simages to compare against, so no good enough  match was found
                    rejected.append(f_image)
                    number_trained += 1
                    break

        
    correct_reject = 0
    incorrect_reject = 0

    #Calculate the incorrect and correct rejects and their associates accepts. 
    for image in strain:
        image.close()
    for image in rejected:
        filenumber = int(image.filename[-11:-7])
        image.close()
        if filenumber > HALF_FILES:
            correct_reject += 1
        if filenumber <= HALF_FILES:
            incorrect_reject += 1
    incorrect_accept = HALF_FILES - correct_reject
    correct_accept = HALF_FILES - incorrect_reject
    ratio_of_ca = correct_accept / HALF_FILES
    ratio_of_ia = incorrect_accept / HALF_FILES
    ratio_of_cr = correct_reject / HALF_FILES
    ratio_of_ir = incorrect_reject / HALF_FILES
    print("Number of correct accepts: " + str(correct_accept) + "/750; ratio: " + str(ratio_of_ca))
    print("Number of incorrect accepts: " + str(incorrect_accept) + "/750; ratio: " + str(ratio_of_ia))
    print("Number of correct rejects: " + str(correct_reject) + "/750; ratio: " + str(ratio_of_cr))
    print("Number of incorrect rejects: " + str(incorrect_reject) + "/750; ratio: " + str(ratio_of_ir))
    print("Thus, the false reject rate is " + str(ratio_of_ir) + " and the false accept rate is " + str(ratio_of_ia))
    return ratio_of_ir, ratio_of_ia


def main():
    caller()


if __name__ == "__main__":
    main()
