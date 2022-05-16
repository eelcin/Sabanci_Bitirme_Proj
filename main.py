# importing os module 
import os
import os.path
from os import path
import cv2 as cv
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
import numpy as np
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76


# Load the classifier and create a cascade object for face detection
face_cascade = cv.CascadeClassifier('{}/opencv/data/haarcascades/haarcascade_frontalface_alt.xml'.format(os.getcwd()))

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# function to plot n images using subplots
def plot_image(images, captions=None, cmap=None):
    f, axes = plt.subplots(1, len(images), sharey=True)
    f.set_figwidth(15)
    for ax, image, caption in zip(axes, images, captions):
        ax.imshow(image, cmap)
        ax.set_title(caption)


def download_visual_data(search_what, how_many):
    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))

    is_exist = path.exists("visual_data")

    if is_exist:
        print("file exist")

    else:
        os.system('mkdir visual_data')

        is_exist = path.exists("visual_data")

        if is_exist:
            print("File created successfully.")

        else:
            print("File creation failed!")

    search_what = search_what.replace(" ", "+")

    # Change the current working directory
    previous_dir = os.getcwd()
    os.chdir('{}/visual_data'.format(os.getcwd()))

    # Print the current working directory
    print("Visual data saved to path: {0}".format(os.getcwd()))

    os.system('youtube-dl ytsearch{}:{}'.format(how_many, search_what))

    os.chdir(previous_dir)

    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))


def what_to_do(do_this):

    #download
    if do_this == "1":
        print("What to download from youtube?")
        search_what = input()

        print("How many to download?")
        how_many = input()

        download_visual_data(search_what, how_many)

    #process_video
    elif do_this == "2":
        files = os.listdir('{}/visual_data'.format(os.getcwd()))

        print("How many video should be processed?(current max= {})".format(len(files)))
        how_many = input()
        how_many = int(how_many)

        print("Processing the video...")
        if(how_many == 0):
            print("No process done, program exits...")
            return 0

        elif((how_many) <= len(files)):
            for index in range((how_many-1)):
                print(index)
                video_processing(files[index])

        else:
            print("No such a command exist!")

    else:
        print("No such a command exist!")


def process_image(image_name):
    SHOW_DEBUG_STEPS = True

    # Read image from your local file system
    #original_image = cv.imread('{}/visual_data/{}.jpg'.format(os.getcwd(), image_name))
    original_image = image_name

    #print("original_image",original_image)

    # Convert color image to grayscale for Viola-Jones
    grayscale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)

    get_colors(original_image, 8)

    detected_faces = face_cascade.detectMultiScale(grayscale_image)

    #print(detected_faces)

    if (SHOW_DEBUG_STEPS):

        for (column, row, width, height) in detected_faces:
            cv.rectangle(
                original_image,
                (column, row),
                (column + width, row + height),
                (0, 255, 0),
                2
            )

        cv.imshow('Image', original_image)
        cv.waitKey(1)
        #cv.destroyAllWindows()

    if len(detected_faces):
        return 1

    else:
        return 0


def video_processing(video_name):
    SHOW_DEBUG_STEPS = False

    # Reading video
    cap = cv.VideoCapture('{}/visual_data/{}'.format(os.getcwd(), video_name))

    # if video is not present, show error
    if not (cap.isOpened()):
        print("Error reading file")

    """start_frame_number = 0
    cap.set(cv.CAP_PROP_POS_FRAMES, start_frame_number)"""

    count = 0
    can_continue = True
    total_frame = 0
    start_frame_number = 0

    while(can_continue):
        cap.set(cv.CAP_PROP_POS_FRAMES, start_frame_number)
        success, fFrame = cap.read()
        total_frame += 1
        start_frame_number += 10

        if success:
            result = process_image(fFrame)
            count += result

            if (SHOW_DEBUG_STEPS):
                print("result:", result)
                print("count:", count)

        else:
            print("total_frame:", total_frame)
            print("count:", count)
            can_continue = False

def get_colors(image, number_of_colors):
    SHOW_DEBUG_STEPS = True

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    modified_image = cv.resize(image, (25, 16), interpolation = cv.INTER_AREA)

    if(SHOW_DEBUG_STEPS):
        plt.imshow(modified_image)
        plt.waitforbuttonpress(1)

    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)



    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    #rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (SHOW_DEBUG_STEPS):
        plt.figure(figsize=(8, 6))
        plt.pie(counts.values(), labels=hex_colors, colors=hex_colors)
        plt.waitforbuttonpress(1)
        print("Dominant Colors of the frame: ", hex_colors)

    #return hex_colors

if __name__ == "__main__":
    print("Choose one of the numbers as input to do the following commands:\n"
          "1-download\n"
          "2-process_video")

    do_this = input()
    print("command: ",do_this)
    what_to_do(do_this)

else:
    print("Failed to enter main.")
