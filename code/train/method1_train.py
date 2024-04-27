#### This is training phse of method one to ensure the mathematically best threshold was found. 
#### The method utilizes ImageChops.difference, an image processing method to determine how similar two images are to each other
#### The smaller the number, the better ####
#### The best threshold determined was 0.145
import random
from PIL import Image, ImageChops, ImageStat
import glob

RESULTS = dict()
X = 0
Y = 6
HALF_FILES = 750


def compare_images(imagef, images):
    """
    This method determineds the differences in the images and then
    returns it as a ratio for comparison
    """
    differences = ImageChops.difference(imagef, images)
    stat = ImageStat.Stat(differences)
    ratio = sum(stat.mean) / (len(stat.mean) * 255)
    return ratio


def caller(threshold):
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
            if comparison_value < threshold: # if similar enough, pop the strain value, close the images, and correct_accept += 1
                f_image.close()
                number_trained += 1
                attempts +=1
                break
            else: 
                if attempts >= strain_length: #no more simages to compare against, so no good enough  match was found
                    filenumber = f_image.filename[-11:-7]
                    rejected.append(filenumber)
                    f_image.close()
                    number_trained += 1
                    break
                attempts += 1

        
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


def threshold_search(depth):
    """
    THis function was used in an attempt to find the mathematically best threshold
    However, it would freeze on the second or third instance, so the binary search
    I was attempt to accomplish was instead done by hand (and a calculator). 
    """
    thresh_l = 0.145
    thresh_m = 0.175
    thresh_r = 0.2

    # thresh = [thresh_l, thresh_m, thresh_r]
    # l_frr = 0
    # l_far = 0 
    # m_frr = 0 
    # m_far = 0
    # r_frr = 0
    # r_far = 0
    # for i in range(depth):
    print("################ DEPTH " + str(0) + " ################")
    left_worse = True
    # if i == 0:
    l_frr, l_far = caller(thresh_l)
    print("Threshold: " + str(thresh_l) + "; l_frr: " + str(l_frr) + "; l_far" + str(l_far))
        #     r_frr, r_far = caller(thresh_r)
        #     print("Threshold: " + str(thresh_r) + "; r_frr: " + str(r_frr) + "; r_far" + str(r_far))
        #     m_frr, m_far = caller(thresh_m)
        #     print("Threshold: " + str(thresh_m) + "; m_frr: " + str(m_frr) + "; m_far" + str(m_far))
        # elif left_worse == False:
        #     r_frr, r_far = caller(thresh_r)
        #     print("Threshold: " + str(thresh_r) + "; r_frr: " + str(r_frr) + "; r_far" + str(r_far))
        # elif left_worse == True:
        #     l_frr, l_far = caller(thresh_l)    
        #     print("Threshold: " + str(thresh_m) + "; l_frr: " + str(l_frr) + "; l_far" + str(l_far))       

        # diff_r = abs(r_frr - r_far)
        # diff_l = abs(l_frr - l_far)
        # diff_m = abs(m_frr - m_far)
        # if diff_r == 0:
        #     print("Best threshold: " + thresh_r)
        #     break
        # elif diff_l == 0: 
        #     print("Best threshold: " + thresh_l)
        #     break
        # elif diff_m == 0: 
        #     print("Best threshold: " + thresh_m)
        #     break
        # if diff_r > diff_l:
        #     left_worse = False
        # # check middle and then get rid of the worse 
        # #    l/r side, replacing that value with the current middle
        # #    and calculating a new middle value halfway between l and r
        # # thresh_l = thresh_m if left_worse else thresh_r = thresh_m # i will make this ternary work if it kills me
        # if left_worse:
        #     thresh_l = thresh_m
        #     l_frr = m_frr
        #     l_far = m_far
        # else:
        #     thresh_r = thresh_m
        #     r_frr = m_frr
        #     r_far = m_far
        # thresh_m = thresh_l + thresh_r / 2


def main():
    threshold_search(6)


if __name__ == "__main__":
    main()
