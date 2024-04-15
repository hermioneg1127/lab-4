#!/bin/usr/python3
import os
from PIL import Image
import numpy as np

#used to convert the given image to a matrix
def convert_image_to_matrix(image_path):
    #opens the image
    img = Image.open(image_path)
    #converts to grayscale  (ensures the image is grayscale)
    img_gray = img.convert('L')
    #Converts the grayscale to a numpy array
    img_matrix = np.array(img_gray)
    return img_matrix

#saves the matrix to a file
def save_matrix_to_file(matrix, file_path):
    #saves the matrix file
    np.save(file_path, matrix)

def process_directory(input_directory, output_directory):
    #gets all the files in the directory
    files = os.listdir(input_directory)
    for file in files:
        #ensures the file is an image
        if file.lower().endswith(('.png')):
            image_matrix = convert_image_to_matrix(os.path.join(input_directory, file))
            save_matrix_to_file(image_matrix, os.path.join(output_directory, file + '.npy'))

#just change the number of hte figs you want to convert, I can go back leter and automate this
#should have all the images you want processed
input_directory="../data/NISTGrayScaleImages/sd04/png_txt/figs_0"
#where all the matrix files will be stored for later use
output_directory="../data/NISTGrayScaleImages/sd04/matrix/figs_0"


process_directory(input_directory, output_directory)
