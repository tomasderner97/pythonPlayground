import requests
from bs4 import BeautifulSoup
import os
import sys

try:
    url = sys.argv[1]
except IndexError:
    url = input("Gimme ficwad link: ")

r = requests.get(url)
page = BeautifulSoup(r.content, "lxml")

author = page.find("span", {"class": "author"}).find("a").text
story_name = ""

chapters_select = page.find("select", {"name": "goto"})

chapter_list = []

if chapters_select:
    story_name = page.find("div", {"id": "story"}).find("h2").find_all("a")[-1].text

    for option in chapters_select.find_all("option"):
        chapter_list.append(option["value"])
    chapter_list.pop(0)
else:
    story_name = page.find("div", {"class": "storylist"}).find("h4").text

    chapter_list.append(url[url.find("/story"):])

chapter_texts = []

for chapter_url in chapter_list:
    full_url = f"https://ficwad.com{chapter_url}"
    print(f"requesting {full_url}")

    r = requests.get(full_url)
    page = BeautifulSoup(r.content, "lxml")

    ch_name = page.find("div", {"class": "storylist"}).find("h4").text
    ch_content = str(page.find("div", {"id": "storytext"}))
    ch_content = f'<h1 class="chapter">{ch_name}</h1>{ch_content}'
    print(f"scrapping {ch_name}")

    chapter_texts.append(ch_content)

file_name = f"{author} - {story_name}.html"
file_path = os.path.join(os.path.expanduser("~"), file_name)
with open(file_path, "w", encoding="utf-8") as f:
    for text in chapter_texts:
        f.write(text)
        f.write("\n")
    print("done")
