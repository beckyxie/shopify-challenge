# Author: Rebecca Xie

from PIL import Image
from collections import defaultdict
import sys
import os, os.path
import webcolors


def search_format(directory):
    """
    Searches for images given image extension (jpg, png, or jpeg) inputted by user.
    :param directory: name of directory containing the images
    :return: names of images that have the same image extension
    """
    img_ext = ['.jpg', '.png', '.jpeg']

    while True:
        user_input = input("Which type of image are you looking for (.jpg, .png, .jpeg)?" + '\n').lower()

        if user_input == 'stop':
            sys.exit()

        # input validation
        if user_input not in img_ext:
            print("Invalid input. Please try again.")
            continue

        # printing out image names that have the same image extensions
        try:
            for file in os.listdir(directory):
                file_ext = os.path.splitext(file)
                if user_input == file_ext[1].lower():
                    print(file_ext[0])
        except FileNotFoundError:
            print("Cannot find directory. Please try again.")
            print()
            break


def search_dominant_color(filename):
    """
    Searches for the dominant color of an image.
    :param filename: image path
    :return: dominant color of the image
    """
    # resizing the image for faster runtime
    width, height = 200, 200
    image = Image.open(filename)
    image = image.resize((width, height), resample=0)

    # getting list of colors (tuples) in image in the form of (count, pixel)
    colors = image.getcolors(width * height)

    # sorting pixels by the first element of the tuple (count)
    sort_colors = sorted(colors, key=lambda t: t[0])

    # getting color with the greatest count
    dom_color = sort_colors[0][1]

    return dom_color


def closest_color(rgb_tuple):
    """
    Searches for closest color given RBG tuple.
    Taken from https://stackoverflow.com/questions/9694165/convert-rgb-color
    -to-english-color-name-like-green-with-python
    :param rgb_tuple: tuple of red, green and blue pixels
    :return: color name closest to RGB tuple
    """
    min_colors = {}
    # looping through hex values and color names of color dictionary
    for hex, color in webcolors.CSS3_HEX_TO_NAMES.items():
        # converting hex to RGB tuple
        red, green, blue = webcolors.hex_to_rgb(hex)
        # using Euclidean distance to calculate closest color
        red_dist = (red - rgb_tuple[0]) ** 2
        green_dist = (green - rgb_tuple[1]) ** 2
        blue_dist = (blue - rgb_tuple[2]) ** 2
        min_colors[(red_dist + green_dist + blue_dist)] = color
    # color name that is closest to given RGB tuple
    return min_colors[min(min_colors.keys())]


def search_similar(directory):
    """
    This function searches for similar images based on the
    dominant color of the picture. It prints out images that
    have the same dominant colors.
    :param directory: name of directory containing the images
    :return: None
    """
    images = []
    img_formats = ['.jpg', '.png', '.jpeg']

    try:
        # appending all images from directory into images list
        for file in os.listdir(directory):
            for i in img_formats:
                if file.endswith(i) or file.endswith(i.upper()):
                    images.append(os.path.join(directory, file))
    except FileNotFoundError:
        print("Cannot find directory. Please try again.")
        print()

    # getting RGB tuple of each image
    rgb_tuples = []
    for image in images:
        rgb_tuples.append(search_dominant_color(image))

    # getting color name of each image
    img_colors = []
    for i in rgb_tuples:
        # tuples that have length greater than 3 are invalid, cannot be used
        if len(i) > 3:
            continue
        img_colors.append(closest_color(i))

    # getting occurrence of each dominant color
    occurrences = defaultdict(list)
    for i, color in enumerate(img_colors):
        occurrences[color].append(i)

    # printing out images that have the same dominant colors
    no_occurrences = 0
    for i in occurrences:
        if len(occurrences[i]) > 1:
            print("Dominant color of these images: ", i)
            for j in occurrences[i]:
                print(images[j].split('/')[1])
            print()
        no_occurrences += 1
        if no_occurrences == len(images):
            print("There are no images in directory, " + directory + ", that have the same dominant color.\n")


def main():
    """
    This function is the user interface of the program.
    Allows the user to choose one of the three options.
    :return: None
    """
    while True:
        option = input(
            "Hello! This program is designed for searching images. Enter 'stop' to exit the program.\n" +
            "Please enter one of the following options: \n" +
            "(1) search for images in a directory with the same image extensions\n" +
            "(2) search for the dominant color of an image\n" +
            "(3) search for images that have the same dominant colors\n")

        if option.lower() == 'stop':
            sys.exit()

        options = ['1', '2', '3']
        if option not in options:
            print("Invalid input. Please try again.")
            continue

        if option == '1':
            directory = input("Please enter the directory name: ")
            search_format(directory)
        elif option == '2':
            filename = input("Please enter the image pathname: ")
            rgb_tuple = search_dominant_color(filename)
            print("The dominant color of this image is: " + closest_color(rgb_tuple))
            print()
        elif option == '3':
            directory = input("Please enter the directory name: ")
            search_similar(directory)


main()

