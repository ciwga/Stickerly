from bs4 import BeautifulSoup
import requests
import os

try:
    os.mkdir("Sticker.ly")
except FileExistsError:
    pass

id_stickers = input("Enter the sticker code: ")
site = "http://sticker.ly/s/" + id_stickers
try:
    img_links = []
    r = requests.get(site)
    soup = BeautifulSoup(r.content, "lxml")
    content_images = soup.find("ul", attrs={"id": "content_images"})\
        .find_all("li")
    for src in content_images:
        picture = src.find_all("picture")
        for img in picture:
            c_img = img.find("img").get("src")
            img_links.append(c_img)
except AttributeError:
    print("\nCheck your sticker code\nThis is invalid code!")


os.chdir("Sticker.ly")
number = 0
for link in img_links:
    r_link = requests.get(link, stream=True).raw.read()
    with open(str(number)+".png", "wb") as f:
        f.write(r_link)
        number = number + 1
