# Image-Web-Scrapper
This is a microservice that extracts the first image from a website that is larger than 90 px x 90 px. 

This is a python file that contains a function by the name of image_downloader. It takes two paramters which are the url and a name.

This function will take the first image from the inputted url that is larger than 90 px and 90 px and has valid attributes for the height and width fields. It will then create a folder with the inputted name in the local directly of where it's being called from. This function will then download the image to that folder.

This is a microservice that is being used with another sliding puzzle game. 

How to use:

1)  Download all of the current files and put them in the same directory.  
2)  Download the packages bs4, watchdog in Python.
3)  Run the program. This program will run continuously. 
4)  Append to the current image.txt file any urls that contain pictures in a new line. 
5)  The program will download the first picture that is larger than 90 px x 90 px from that site. It will create a new folder in its existing directory called images. The picture will be downloaded there.
6) The program will write the file name in a new line on the same images.txt file. If an error has occured, an error message will be written instead. 
7) Repeat as needed. Close the program manually after completion.

For example, this program can be used with the url - https://naturedestinations.ca/canadas-natural-landscapes/. It also works with any Wikipedia page. 

This program will not work for websites where the images are in a .svg format. 
