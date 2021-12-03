import os
import requests
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
from random import randrange


def create_folder_for_images(folder):
    """This function creates a folder to which the images will be downloaded to. If the folder already exists,
    it will just changes the current directory to it. Lastly, it will return the  directory that was assigned
    before any changes"""

    # Need to store directory's location for when it changes due to the creation of a new folder.
    current_dir = os.getcwd()
    target_dir = os.path.join(os.getcwd(), folder)
    # creates a new folder for the images
    try:
        os.mkdir(target_dir)
    except:
        pass
    os.chdir(target_dir)
    return current_dir


def image_name_transformer(image_name,folder):
    """This function takes the alternative name it receives and transforms it to a image_name without any extensions.
    If the alternative name doesn't exist or is none, it provides a random image name. At the end, it returns
    the image_name."""

    default_image_name = (randrange(10000))
    if image_name == "" or image_name is None:
        image_name = folder + str(default_image_name)
    # If the alternative name has a .jpg or .png ending (like Wikipedia), it is removed.
    if "png" in image_name or "jpg" in image_name:
        image_name = image_name[:-4]
    if "jpeg" in image_name:
        image_name = image_name[:-5]
    return image_name


def download_image_and_create_file_name(images, folder):
    """This function downloads the image in a .png format and creates the corresponding file name for it. If there
    isn't any valid image, a blank string will be returned."""

    # The below loop goes through the images on the url (img tag) by their order of appearance and
    # it will take the first image that is more than 90 x 90.

    for element in images:
        link = element["src"]
        if (int(element["width"]) > 90 and int(element["height"]) > 90 and (link[-3:] == "png"
           or link[-3:] == "jpg" or link[-3:] == "peg")):
            if link.startswith("//"):
                link = "http:" + link
            # It will take the alternative name of the image as a name for the file.
            image_name = element["alt"]
            image_name = image_name_transformer(image_name,folder)
            image_name = save_image_file_with_file_name(image_name,link)
            return image_name
    return ("")


def save_image_file_with_file_name(image_name, link):
    """This function saves the image in a .png format with the corresponding file name for it. Lastly, it returns
    the file name."""

    # Image is saved as a .png in specified folder.
    with open(image_name.replace(" ", "_").replace("/", "") + '.png', 'wb') as file:
        image_request = requests.get(link)
        file.write(image_request.content)
    image_name = image_name.replace(" ", "_").replace("/", "")
    file.close()
    return image_name


def image_downloader(url, folder):
    """This function downloads the image on the inputted url to a specified folder and returns the file's name or
    invalid if it was not possible. This function takes a url in a string format and a
    folder name as its parameters."""

    current_dir = create_folder_for_images(folder)
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    # This function will only takes images that have defined width and height attributes.
    images = soup.find_all("img", width=True, height=True)
    image_name = download_image_and_create_file_name(images, folder)
    # Changing pointer to stored directory.
    os.chdir(current_dir)
    if image_name == "":
        return ("Invalid")
    else:
        return image_name


def download_and_write_if_valid(url, current_dir):
    """This function checks if the images.txt file has received a valid url. If there is a valid URL, it
    downloads an image from that URL and writes the downloaded image's name on a new line in images.text. Any
    errors are also written to images.txt."""

    if "http" in url:
        try:
            name = image_downloader(url,"images")
        except:
            os.chdir(current_dir)
            name = "ERROR Please enter a valid site. This request was not successful"
        if name == "Invalid":
            string_to_print = "ERROR: Please enter a valid site. This request was not successful"
            name = string_to_print
        with open("./images.txt", "a") as file2:
            file2.write("\n" + name)
        file2.close()


def on_modified(event):
    """This function checks if there have been any valid modifications to images.txt. If there is a valid
    modification, it passes the URL to another function to download an image from it.."""
    current_dir = os.getcwd()
    line = ""
    with open(os.path.join(os.getcwd(), "images.txt"), "r") as file1:
        for line in file1:
            pass
        url = line
    file1.close()
    download_and_write_if_valid(url, current_dir)


# Creating variables to store parameters for PatternMatchingEventHandler and calling it.

if __name__ =="__main__":
    patterns = ["*images.txt"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns,ignore_patterns,ignore_directories,case_sensitive)


# Making sure that the on_modified function is called whenever there is a change to the image.txt file.

my_event_handler.on_modified = on_modified
path = "."
recursion = False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive = recursion)

# Below code is to run the function continuously until it is manually stopped.

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()