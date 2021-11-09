import os
import requests
from bs4 import BeautifulSoup

def image_downloader(url,folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        print("Folder name might already exist")

    os.chdir(os.path.join(os.getcwd(), folder))

    request = requests.get(url)

    soup = BeautifulSoup(request.text, "html.parser")

    images = soup.find_all("img", width=True, height=True)

    item = 0

    for element in images:
        alt = element["alt"]
        if alt == "":
            alt = folder + str(item)
            item += 1
        if int(element["width"]) > 90 and int(element["height"]) > 90:
            link = element["src"]
            with open(alt.replace(" ","_").replace("/","") + '.jpg','wb') as file:
                image_request = requests.get(link)
                file.write(image_request.content)
                print("Writing: ", alt)
            break