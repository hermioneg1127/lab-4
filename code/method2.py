import numpy 
import skimage
import glob
from PIL import Image
import random

HALF_FILES = 750
X = 0
Y = 6

def mse(fimage, simage):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	err = numpy.sum((fimage.astype("float") - simage.astype("float")) ** 2)
	mean = err / float(fimage.shape[0] * simage.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err




def caller(threshold):
    ftrain = [] #initialize train list
    strain = []
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
    random.shuffle(ftrain)
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
            number_s = (s_image.filename[-11:-4])
            number_f = (f_image.filename[-11:-4])
            if comparison_value < threshold:
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
        filenumber = int(image.filename[-11:-7])
        if filenumber <= HALF_FILES:
            incorrect_reject += 1
        else: 
            correct_reject += 1
        image.close()
    correct_accept = HALF_FILES - incorrect_reject
    incorrect_accept = HALF_FILES - correct_reject
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
    thresh_l = 1000
    thresh_m = 1250
    thresh_r = 1500

    thresh = [thresh_l, thresh_m, thresh_r]
    l_frr = 0
    l_far = 0 
    m_frr = 0 
    m_far = 0
    r_frr = 0
    r_far = 0
    for i in range(depth):
        print("################ DEPTH " + str(i) + " ################")
        left_worse = True
        if i == 0:
            l_frr, l_far = caller(thresh_l)
            print("Threshold: " + str(thresh_l) + "; l_frr: " + str(l_frr) + "; l_far" + str(l_far))
            r_frr, r_far = caller(thresh_r)
            print("Threshold: " + str(thresh_r) + "; r_frr: " + str(r_frr) + "; r_far" + str(r_far))
            m_frr, m_far = caller(thresh_m)
            print("Threshold: " + str(thresh_m) + "; m_frr: " + str(m_frr) + "; m_far" + str(m_far))
        elif left_worse == False:
            r_frr, r_far = caller(thresh_r)
            print("Threshold: " + str(thresh_r) + "; r_frr: " + str(r_frr) + "; r_far" + str(r_far))
        elif left_worse == True:
            l_frr, l_far = caller(thresh_l)    
            print("Threshold: " + str(thresh_m) + "; l_frr: " + str(l_frr) + "; l_far" + str(l_far))       

        diff_r = abs(r_frr - r_far)
        diff_l = abs(l_frr - l_far)
        diff_m = abs(m_frr - m_far)
        if diff_r == 0:
            print("Best threshold: " + thresh_r)
            break
        elif diff_l == 0: 
            print("Best threshold: " + thresh_l)
            break
        elif diff_m == 0: 
            print("Best threshold: " + thresh_m)
            break
        if diff_r > diff_l:
            left_worse = False
        if left_worse:
            thresh_l = thresh_m
            l_frr = m_frr
            l_far = m_far
        else:
            thresh_r = thresh_m
            r_frr = m_frr
            r_far = m_far
        thresh_m = thresh_l + thresh_r / 2



    # for x in range (1500):
    #     compare_images(imagef, images)

    # return

def main():
    threshold_search(6)


if __name__ == "__main__":
    main()