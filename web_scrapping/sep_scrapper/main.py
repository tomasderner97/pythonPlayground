# Stanford Encyclopedia of Philosophy scrapper

import requests
import bs4
import os
import re
import codecs


def find_note(sup_text, notes_soup):

    print(f"finding note {sup_text}")

    res = re.search(r"\[([0-9]+)\]", sup_text)
    num = res.group(1)

    try:
        note_p = notes_soup.find("a", {"name": num}).parent
    except AttributeError:
        note_p = notes_soup.find("a", string=f"{num}.").parent
    note_a = note_p.find("a")
    note_a.extract()
    note_p.name = "span"

    return note_p


input()
LINK = input("SEP page: ")

print("downloading link")
r = requests.get(LINK)

print("souping link")
soup = bs4.BeautifulSoup(r.content, "lxml")

title = soup.find("h1").text

print("searching aueditable")
aueditable_div = soup.find(id="aueditable")

print("searching stuff")
pubinfo_div = aueditable_div.find(id="pubinfo")
preamble_div = aueditable_div.find(id="preamble")
content_div = aueditable_div.find(id="toc")
main_text_div = aueditable_div.find(id="main-text")

try:
    preamble_div.find("div", class_="figureright").extract()
except AttributeError:
    pass

print("downloading notes")
notes_req = requests.get(os.path.join(LINK, "notes.html"))
print("souping notes")
notes_soup = bs4.BeautifulSoup(notes_req.content, "lxml")

for div in [preamble_div, content_div, main_text_div]:

    sups = div.find_all("sup")

    notes_sups = []
    for sup in sups:
        if sup.text[0] == "[":
            notes_sups.append(sup)

    for sup in notes_sups:
        sup.name = "span"
        sup_text = sup.text
        sup.string = ""
        sup.append(soup.new_string(" [Note: "))
        sup.append(find_note(sup_text, notes_soup))
        sup.append(soup.new_string("]"))

result = str(pubinfo_div) + str(preamble_div) + str(content_div) + str(main_text_div)

result = '''<html>
<head><style>
body {font-family:arial;text-align:justify;font-size: 13pt}
</style></head><body>''' + f'<h1 id="{title}">{title}</h1>' + result + '</body></html>'

with codecs.open(f"./downloads/{title}.html", "w", "utf-8-sig") as f:
    f.write(result)


command = r'cd downloads && wkhtmltopdf -s A7 -O Landscape '\
    "-B 0.1 -L 0 -R 0 -T 0.1 --dpi 96 "\
    f'"{title}.html" "{title}.pdf"'

os.system(command)
