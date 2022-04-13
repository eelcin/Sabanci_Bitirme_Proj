# importing os module 
import os
import os.path
from os import path

# Command to execute
# Using Windows OS command

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

    #search_what = search_what.replace(" ", "+")

    # Change the current working directory
    previous_dir = os.getcwd()
    os.chdir('{}/visual_data'.format(os.getcwd()))

    # Print the current working directory
    print("Visual data saved to path: {0}".format(os.getcwd()))

    #os.system('youtube-dl ytsearch{}:{}'.format(how_many, search_what))

    os.chdir(previous_dir)

    # Print the current working directory
    print("Current working directory: {0}".format(os.getcwd()))

def what_to_do(do_this):

    if do_this == "download":
        print("What to download from youtube?")
        search_what = input()

        print("How many to download?")
        how_many = input()

        download_visual_data(search_what, how_many)

    else:
        print("No such a command exist!")


if __name__ == "__main__":
    print ("Choose one of the input below give command to program:\n"
           "download")

    do_this = input()
    what_to_do(do_this)

else:
    print ("Failed to enter main.")