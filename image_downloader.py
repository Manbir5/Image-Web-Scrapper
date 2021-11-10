import os
import requests
from bs4 import BeautifulSoup
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
from random import randrange


def image_downloader(url,folder):

    current_dir = os.getcwd()

    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass

    os.chdir(os.path.join(os.getcwd(), folder))

    request = requests.get(url)

    soup = BeautifulSoup(request.text, "html.parser")

    images = soup.find_all("img", width=True, height=True)

    item = (randrange(10000))

    for element in images:
        if int(element["width"]) > 90 and int(element["height"]) > 90:
            link = element["src"]
            alt = element["alt"]
            if alt == "" or alt is None:
                alt = folder + str(item)
            with open(alt.replace(" ", "_").replace("/", "") + '.jpg', 'wb') as file:
                image_request = requests.get(link)
                file.write(image_request.content)
                print("Writing: ", alt)
                file.close()
            os.chdir(current_dir)
            return alt
    invalid = "Invalid"
    return invalid

if __name__ =="__main__":
    patterns = ["*images.txt"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns,ignore_patterns,ignore_directories,case_sensitive)

def on_modified(event):
    with open(os.path.join(os.getcwd(), "images.txt"), "r") as file2:
        for line in file2:
            pass
        url = line
    file2.close()
    if "http" in url:
        name = image_downloader(url,"images")
        with open("./images.txt", "a") as file3:
            file3.write("\n" + name)
        file3.close()


my_event_handler.on_modified = on_modified

path = "."
recursion = False
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive = recursion)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()