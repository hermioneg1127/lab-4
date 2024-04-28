from skimage.metrics import structural_similarity
import glob
import random
import skimage
from PIL import Image

THRESHOLD = 0.225
HALF_SIZE = 250
HALF_FILES = 1750
THRESHOLD = .0273
X = 6
Y = 8

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
                if len(strain) < HALF_SIZE:
                    image = Image.open(file)
                    strain.append(image)

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
            comparison_value = comparison_value = structural_similarity(f_image_conv,s_image_conv,data_range=1)
            if comparison_value >= THRESHOLD:
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

    incorrect_reject = len(strain)
    for image in strain:
        image.close()
    for image in rejected:
        filenumber = int(image.filename[-11:-7])
        image.close()
        if filenumber > HALF_FILES:
            correct_reject += 1
        elif filenumber <= HALF_FILES:
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
    print("Thus, the false reject rate is " + str(ratio_of_ir) + " and the false accept rate is " + str(ratio_of_ia) + " when threshold is " + str(THRESHOLD))
    return ratio_of_ir, ratio_of_ia


def main():
    caller()


if __name__ == "__main__":
    main()


