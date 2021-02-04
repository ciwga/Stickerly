# _*_ coding:utf-8 _*_
from bs4 import BeautifulSoup
import requests
import os
import time


class Stickerly():

    def __init__(self):
        self.StickersId = input("Enter the sticker id: ")
        self.website = "http://sticker.ly/s/" + self.StickersId
        self.imgLinks = []

    def SaveStickers(self, title, author):
        try:
            path = "stickerly/" + title
            os.makedirs(path)
            os.chdir(path)
        except NotADirectoryError:
            InvalidPath = "stickerly/Invalid Name"
            os.makedirs(InvalidPath)
            os.chdir(InvalidPath)
        except FileExistsError:
            pass

        with open("log.txt", "w+", encoding="utf-8") as log:
            log.write(f"Title: {title}\nAuthor: {author}\nCreated: {time.ctime()}\
            \nWebsite: {self.website}")

        number = 0
        for link in self.imgLinks:
            imgLink = requests.get(link, stream=True).raw.read()
            with open(str(number)+".webp", "wb") as image:
                image.write(imgLink)
                number = number + 1
        print("Done!")

    def StickerData(self):
        r = requests.get(self.website)
        soup = BeautifulSoup(r.content, "lxml")
        try:
            title = soup.find("div", attrs={"class": "sticker_name"})\
                .find("strong").text
            author = soup.find("span", attrs={"class": "sticker_author"})\
                .text.strip()
            content_images = soup.find("ul", attrs={"id": "content_images"})\
                .find_all("li")
        except AttributeError:
            print("\nCheck your sticker id.\nThat is an invalid id!")
        for media in content_images:
            picture = media.find_all("picture")
            for images in picture:
                src = images.find("img").get("src")
                self.imgLinks.append(src)
        self.SaveStickers(title, author)


sticker = Stickerly()
sticker.StickerData()
